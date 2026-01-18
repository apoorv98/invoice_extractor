# Invoice Extraction System

## Overview

This project extracts structured invoice data from PDF files using pluggable OCR engines and pure parsing logic. It is designed for production use: testable, extensible, and safe to operate in batch environments.

Key goals:

* OCR engine agnostic (PaddleOCR, Tesseract, future engines)
* Deterministic, testable parsing logic
* Clean separation between IO, OCR, and domain logic
* Safe batch processing with logging and graceful failures

---

## How to Run (Linux + uv)

### System Dependencies

```bash
sudo pacman -S poppler tesseract tesseract-data-eng
```

### Python Environment

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```


### Setup instructions

``` bash
uv pip install opencv-python pdf2image paddleocr pytesseract
uv pip install --pre paddlepaddle-gpu -i https://www.paddlepaddle.org.cn/packages/nightly/cu129/
```

Or use requirements.txt

``` bash
uv pip install requirements.txt
```

### Run via CLI

Single PDF:

```bash
python scripts/invoice_extract_cli.py invoice.pdf
```

Directory of PDFs:

```bash
python scripts/invoice_extract_cli.py ./invoices/
```

Switch OCR engine:

```bash
python scripts/invoice_extract_cli.py invoice.pdf --ocr tesseract
```

Outputs are written as:

```
output_<pdf-name>_<ocr-engine>.json
```

---


## Design Principles (for New Contributors)

* Separate domain logic from infrastructure
* Prefer interfaces over concrete implementations
* Assume OCR engines will change
* Write tests before refactoring
* Keep public APIs boring and stable


