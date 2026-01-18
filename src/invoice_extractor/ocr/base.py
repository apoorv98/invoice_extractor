#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Dict, Any


class OCREngine(ABC):
    @abstractmethod
    def extract(self, image) -> Dict[str, Any]:
        """
        Accepts a preprocessed image.
        Returns normalized OCR output (engine-specific details hidden).
        """
        raise NotImplementedError
