#!/usr/bin/env python3

from paddleocr import PaddleOCR
from ocr.base import OCREngine


class PaddleOCREngine(OCREngine):
    def __init__(self):
        self._ocr = PaddleOCR(use_angle_cls=True, lang="en")

    def extract(self, image):
        result = self._ocr.predict(image)

        # Normalize Paddle's inconsistent return shapes
        if isinstance(result, list) and result and isinstance(result[0], dict):
            return result[0]
        return result
