import re
import pprint
import json
import numpy as np
import cv2
from pdf2image import convert_from_path
from paddleocr import PaddleOCR
from PIL import Image

# -----------------------------
# CONFIG
# -----------------------------
PDF_PATH = "RSG TELECOM.pdf"
DPI = 300
MIN_CONFIDENCE = 0.6

# -----------------------------
# INITIALIZE OCR
# -----------------------------
ocr = PaddleOCR(
    use_angle_cls=True,   # handles rotated scans
    lang="en"
)

# -----------------------------
# PDF → IMAGES
# -----------------------------
def pdf_to_images(pdf_path, DPI):
    images = convert_from_path(pdf_path, dpi=DPI, poppler_path=r'C:\Users\Developer\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin')
    return images

# -----------------------------
# IMAGE PREPROCESSING
# -----------------------------
def preprocess_image(pil_image):
    img = np.array(pil_image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

# -----------------------------
# NORMALIZE BBOX
# -----------------------------
def normalize_bbox(bbox):
    """
    Returns (x_min, y_min) or (None, None) if invalid
    """
    try:
        # Case 1: [[x,y], [x,y], [x,y], [x,y]]
        if (
            isinstance(bbox, list)
            and len(bbox) == 4
            and all(isinstance(p, (list, tuple)) and len(p) == 2 for p in bbox)
        ):
            xs = [p[0] for p in bbox]
            ys = [p[1] for p in bbox]
            return min(xs), min(ys)

        # Case 2: [x1, y1, x2, y2]
        if (
            isinstance(bbox, list)
            and len(bbox) == 4
            and all(isinstance(v, (int, float)) for v in bbox)
        ):
            return min(bbox[0], bbox[2]), min(bbox[1], bbox[3])

    except Exception:
        pass

    return None, None



# -----------------------------
# OCR
# -----------------------------
def run_ocr(image):
    result = ocr.predict(image)
    result = _unwrap_ocr_result(result)

    return result

def _unwrap_ocr_result(result):
    if isinstance(result, list) and result and isinstance(result[0], dict):
        return result[0]
    return result


# Extract lines
def build_lines_from_doc_ocr(result):
    lines = []
    texts = result.get("rec_texts", [])
    scores = result.get("rec_scores", [])

    for i, text in enumerate(texts):
        if not text or not text.strip():
            continue

        conf = scores[i] if i < len(scores) else 1.0

        lines.append({
            "text": text.strip(),
            "confidence": float(conf),
            "x": None,
            "y": None
        })

    return lines

# --------------------------------
# EXTRACTION of important values
# --------------------------------
def extract_invoice_number(lines):
    for line in lines:
        if "invoice no" in line['text'].lower():
            return line['text'].split("Invoice No")[-1].strip()

            
def extract_invoice_date(lines):
    for line in lines:
        if "invoice date" in line['text'].lower():
            return line['text'].split("Invoice Date")[-1].strip()
        # fallback for dates like 13-Aug-2025
        match = re.search(r"\d{1,2}-[A-Za-z]{3}-\d{4}", line['text'])
        if match:
            return match.group(0)
    return None

def extract_gstin(lines):
    for line in lines:
        match = re.search(r"\d{2}[A-Z]{5}\d{4}[A-Z]\dZ[A-Z0-9]", line['text'])
        if match:
            return match.group(0)
    return None

def extract_total_value(lines):
    for i, line in enumerate(lines):
        if "total invoice value" in line['text'].lower():
            # Usually next line has the amount
            if i + 1 < len(lines):
                return lines[i + 1]['text'].strip()
    return None

def extract_addresses(lines):
    """
    Heuristic: find lines containing keywords like 'street', 'road', 'shop', etc.
    Usually top 50% lines contain addresses.
    """
    keywords = ["street", "st.", "road", "rd.", "chowk", "office", "nagar", "lane", "shop", "society"]
    address_lines = []
    for line in lines[:50]:
        if any(k in line['text'].lower() for k in keywords):
            address_lines.append(line['text'])
    return " ".join(address_lines)


# -----------------------------
# LINE ITEM EXTRACTION
# -----------------------------
def parse_invoice_items(lines):
    items = []
    current_block = []

    # Step 1: group by SKU
    for line in lines:
        text = line['text'].strip()
        # valid SKU: 6-8 digit number
        if re.match(r'^\d{6,8}$', text):
            if current_block:
                items.append(current_block)
            current_block = [text]
        else:
            if current_block:
                current_block.append(text)
    if current_block:
        items.append(current_block)

    # Step 2: parse each block
    structured_items = []
    for block in items:
        sku = block[0]
        description = None
        tax = None
        quantity = None
        rate = None
        final_amount = None
        imeis = []

        for val in block[1:]:
            val = val.strip()
            # IMEI (12-20 digits)
            if re.match(r'^\d{12,20},?$', val):
                imeis.append(val)
            # Tax %
            elif re.match(r'^\d{1,2}(\.\d+)?%$', val) and tax is None:
                tax = val
            # Quantity: integer ≤ 1000
            elif re.match(r'^\d+(\.\d+)?$', val):
                num_val = float(val)
                if quantity is None and num_val.is_integer() and num_val <= 1000:
                    quantity = str(int(num_val))
                # Rate: first numeric > 1000
                elif rate is None and num_val > 1000:
                    rate = val
                # Final amount: last numeric
                else:
                    final_amount = val
            # Description: first non-numeric, non-tax, non-IMEI string
            elif description is None:
                description = val

        structured_items.append({
            "hsn_cd": sku,
            "description": description,
            "quantity": quantity,
            "rate": rate,
            "tax": tax,
            "final_amount": final_amount,
            "imeis": imeis
        })

    return structured_items






# -----------------------------
# MAIN
# -----------------------------
def extract_invoice(pdf_path):
    images = pdf_to_images(pdf_path, DPI)
    all_results = []

    for page_num, img in enumerate(images, start=1):
        processed = preprocess_image(img)
        result = run_ocr(processed)
        lines = build_lines_from_doc_ocr(result)
        pprint.pprint(lines)

        invoice_number = extract_invoice_number(lines)
        invoice_date = extract_invoice_date(lines)
        gstin = extract_gstin(lines)
        total_value = extract_total_value(lines)

        address = extract_addresses(lines)
        items = parse_invoice_items(lines)

        result = {
            "page": page_num,
            "invoice_number": invoice_number,
            "invoice_date": invoice_date,
            "gstin": gstin,
            "total_value": total_value,
            "address": address,
            "items": items,
        }

        all_results.append(result)

    return all_results

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    data = extract_invoice(PDF_PATH)
    print(json.dumps(data, indent=2))