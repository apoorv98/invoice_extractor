#!/usr/bin/env python3

from pdf2image import convert_from_path
from invoice_extractor.config.settings import PDFSettings, OCRSettings


def load_pdf_as_images(pdf_path: str):
    pdf_cfg = PDFSettings()
    ocr_cfg = OCRSettings()

    return convert_from_path(
        pdf_path,
        dpi=ocr_cfg.dpi,
        poppler_path=pdf_cfg.poppler_path
    )
