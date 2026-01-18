#!/usr/bin/env python3

from typing import Dict, Any
import pytesseract
from PIL import Image

from invoice_extractor.ocr.base import OCREngine


class TesseractOCREngine(OCREngine):
    """
    Tesseract OCR engine adapter.

    Produces output normalized to match PaddleOCR-style keys
    so downstream parsing remains unchanged.
    """

    def extract(self, image) -> Dict[str, Any]:
        # pytesseract prefers PIL images
        if not isinstance(image, Image.Image):
            image = Image.fromarray(image)

        data = pytesseract.image_to_data(
            image,
            output_type=pytesseract.Output.DICT
        )

        texts = []
        scores = []

        for text, conf in zip(data["text"], data["conf"]):
            if text and text.strip():
                texts.append(text.strip())

                # pytesseract uses -1 for unknown confidence
                try:
                    conf_val = float(conf)
                    scores.append(conf_val / 100 if conf_val >= 0 else 0.0)
                except Exception:
                    scores.append(0.0)

        return {
            "rec_texts": texts,
            "rec_scores": scores,
        }
