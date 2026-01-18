## Architecture

### High-Level Flow

```
PDF -> Images -> Preprocessing -> OCR -> Normalized Lines -> Parsing -> JSON
```

### Layer Responsibilities

**Infrastructure (unstable, replaceable)**

* PDF loading (`utils/pdf.py`)
* Image preprocessing (`preprocessing/image.py`)
* OCR engines (`ocr/`)

**Domain Logic (stable, testable)**

* Line normalization (`parsing/lines.py`)
* Header parsing (`parsing/header.py`)
* Totals & GSTIN (`parsing/totals.py`)
* Address parsing (`parsing/address.py`)
* Line items (`parsing/items.py`)

**Orchestration**

* Extraction pipeline (`pipeline/extractor.py`)

---

## OCR Engines

### PaddleOCR

* Default engine
* Better structure and accuracy
* Heavier dependency footprint

Usage:

```python
from ocr.paddle import PaddleOCREngine
```

### Tesseract (pytesseract)

* Lightweight
* Faster
* Noisier output

Usage:

```python
from ocr.tesseract import TesseractOCREngine
```

### Adding a New OCR Engine

1. Create a new class in `src/ocr/`
2. Implement the `OCREngine` interface
3. Normalize output to:

```python
{
  "rec_texts": list[str],
  "rec_scores": list[float]
}
```

4. Register it in the CLI registry

No parsing or pipeline changes required.

---

## Testing Strategy

* Unit tests cover **parsing logic only**
* OCR and PDF handling are excluded from unit tests
* Real PDFs are validated via CLI scripts

Why:

* OCR is non-deterministic
* Parsing logic is deterministic
* Tests lock down behavior before refactors

---

## Logging & Error Handling

* Structured logging via `logging` module
* Page-level failures do not abort jobs
* PDF load failures fail fast

Enable debug logging:

```bash
LOG_LEVEL=DEBUG python scripts/invoice_extract_cli.py invoice.pdf
```

---

## Development Workflow

* `main` branch is protected
* Feature branches only
* Tests required before merge
* Refactors happen **after** tests

Guiding rule:

> Make behavior explicit before improving it

---
