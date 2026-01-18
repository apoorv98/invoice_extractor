#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

from invoice_extractor.config.logging import setup_logging
from invoice_extractor.pipeline.extractor import InvoiceExtractor

from invoice_extractor.ocr.paddle import PaddleOCREngine
from invoice_extractor.ocr.tesseract import TesseractOCREngine


# --- OCR engine registry (extensible) ---
OCR_ENGINES = {
    "paddle": PaddleOCREngine,
    "tesseract": TesseractOCREngine,
}


def resolve_pdfs(path: Path) -> list[Path]:
    if path.is_file():
        if path.suffix.lower() != ".pdf":
            raise ValueError(f"Not a PDF file: {path}")
        return [path]

    if path.is_dir():
        pdfs = sorted(path.glob("*.pdf"))
        if not pdfs:
            raise ValueError(f"No PDF files found in directory: {path}")
        return pdfs

    raise ValueError(f"Invalid path: {path}")


def main():
    parser = argparse.ArgumentParser(
        description="Invoice extraction CLI"
    )

    parser.add_argument(
        "input",
        help="Path to a PDF file or a directory containing PDFs"
    )

    parser.add_argument(
        "--ocr",
        choices=OCR_ENGINES.keys(),
        default="paddle",
        help="OCR engine to use (default: paddle)"
    )

    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory to save output JSON files"
    )

    args = parser.parse_args()

    setup_logging()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = resolve_pdfs(input_path)

    ocr_engine_cls = OCR_ENGINES[args.ocr]
    extractor = InvoiceExtractor(
        ocr_engine=ocr_engine_cls()
    )

    for pdf_path in pdf_files:
        result = extractor.extract(str(pdf_path))

        output_name = (
            f"output_{pdf_path.stem}_{args.ocr}.json"
        )
        output_path = output_dir / output_name

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
