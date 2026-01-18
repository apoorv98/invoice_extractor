#!/usr/bin/env python3

from paddleocr import PaddleOCR

_ocr = PaddleOCR(use_angle_cls=True, lang="en")


def run_ocr(image):
    result = _ocr.predict(image)
    return _unwrap(result)


def _unwrap(result):
    if isinstance(result, list) and result and isinstance(result[0], dict):
        return result[0]
    return result
