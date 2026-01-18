#!/usr/bin/env python3

def normalize_ocr_result(result: dict) -> list[dict]:
    """
    Converts OCR engine output into normalized line dictionaries.
    """
    lines = []
    texts = result.get("rec_texts", [])
    scores = result.get("rec_scores", [])

    for i, text in enumerate(texts):
        if not text or not text.strip():
            continue

        confidence = scores[i] if i < len(scores) else 1.0

        lines.append({
            "text": text.strip(),
            "confidence": float(confidence),
            "x": None,
            "y": None,
        })

    return lines
