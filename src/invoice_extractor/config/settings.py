#!/usr/bin/env python3

# src/invoice_extractor/config/settings.py
from dataclasses import dataclass
import os


@dataclass(frozen=True)
class OCRSettings:
    dpi: int = int(os.getenv("OCR_DPI", 300))
    min_confidence: float = float(os.getenv("OCR_MIN_CONF", 0.6))


@dataclass(frozen=True)
class PDFSettings:
    poppler_path: str | None = os.getenv("POPPLER_PATH")
