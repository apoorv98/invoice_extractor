#!/usr/bin/env python3

import numpy as np
import cv2


def preprocess_for_ocr(pil_image):
    """
    Converts PIL image into OCR-ready RGB ndarray.
    """
    img = np.array(pil_image)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
