#!/usr/bin/env python3

import logging
from typing import List, Dict, Any

from utils.pdf import load_pdf_as_images
from preprocessing.image import preprocess_for_ocr

from parsing.lines import normalize_ocr_result
from parsing.header import extract_invoice_number, extract_invoice_date
from parsing.totals import extract_gstin, extract_total_value
from parsing.address import extract_addresses
from parsing.items import parse_invoice_items


logger = logging.getLogger(__name__)

InvoicePageResult = Dict[str, Any]


class InvoiceExtractor:
    """
    Public API for invoice data extraction.

    Responsibilities:
    - Orchestrate PDF loading, OCR, preprocessing
    - Invoke parsing domain logic
    - Assemble structured invoice output

    Does NOT:
    - Implement OCR logic
    - Implement parsing heuristics
    """
    def __init__(self, ocr_engine):
        self.ocr = ocr_engine

    def extract(self, pdf_path: str) -> List[InvoicePageResult]:
        logger.info("Starting invoice extraction", extra={"pdf_path": pdf_path})

        try:
            images = load_pdf_as_images(pdf_path)
        except Exception as exc:
            logger.exception("Failed to load PDF", extra={"pdf_path": pdf_path})
            raise

        results: List[InvoicePageResult] = []

        for page_num, img in enumerate(images, start=1):
            try:
                logger.debug("Processing page", extra={"page": page_num})

                processed_image = preprocess_for_ocr(img)
                ocr_result = self.ocr.extract(processed_image)
                lines = normalize_ocr_result(ocr_result)

                results.append({
                    "page": page_num,
                    "invoice_number": extract_invoice_number(lines),
                    "invoice_date": extract_invoice_date(lines),
                    "gstin": extract_gstin(lines),
                    "total_value": extract_total_value(lines),
                    "address": extract_addresses(lines),
                    "items": parse_invoice_items(lines),
                })

            except Exception as exc:
                logger.exception(
                    "Failed to process page",
                    extra={"page": page_num, "error": str(exc)},
                )

                # Graceful degradation: preserve page boundary
                results.append({
                    "page": page_num,
                    "error": "page_processing_failed",
                })

        logger.info(
            "Invoice extraction completed",
            extra={"pages_processed": len(results)},
        )

        return results
