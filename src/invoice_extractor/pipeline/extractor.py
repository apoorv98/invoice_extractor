#!/usr/bin/env python3

from utils.pdf import pdf_to_images
from preprocessing.image import preprocess_image

from parsing.header import extract_invoice_number, extract_invoice_date
from parsing.totals import extract_gstin, extract_total_value
from parsing.address import extract_addresses
from parsing.items import parse_invoice_items


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


class InvoiceExtractor:
    def __init__(self, ocr_engine):
        self.ocr = ocr_engine

    def extract(self, pdf_path: str):
        images = pdf_to_images(pdf_path)
        results = []

        for page_num, img in enumerate(images, start=1):
            processed = preprocess_image(img)
            ocr_result = self.ocr.extract(processed)
            lines = build_lines_from_doc_ocr(ocr_result)

            results.append({
                "page": page_num,
                "invoice_number": extract_invoice_number(lines),
                "invoice_date": extract_invoice_date(lines),
                "gstin": extract_gstin(lines),
                "total_value": extract_total_value(lines),
                "address": extract_addresses(lines),
                "items": parse_invoice_items(lines),
            })

        return results
