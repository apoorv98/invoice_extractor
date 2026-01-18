#!/usr/bin/env python3

import json

from invoice_extractor.config.logging import setup_logging
from invoice_extractor.ocr.paddle import PaddleOCREngine
from invoice_extractor.ocr.tesseract import TesseractOCREngine
from invoice_extractor.pipeline.extractor import InvoiceExtractor


def main():
    setup_logging()

    # extractor = InvoiceExtractor(
    #     ocr_engine=PaddleOCREngine()
    # )
    
    extractor = InvoiceExtractor(
        ocr_engine=TesseractOCREngine()
    )

    pdf_path = "OTHER TELECOM.pdf"  # adjust as needed
    result = extractor.extract(pdf_path)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
