#!/usr/bin/env python3

import numpy as np
import cv2

def preprocess_image(pil_image):
    img = np.array(pil_image)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
