#!/usr/bin/env python3

import json
from invoice_extractor.parsing.header import (
    extract_invoice_number,
    extract_invoice_date,
)

FIXTURES = "tests/fixtures/sample_lines.json"


def load_lines(key):
    with open(FIXTURES) as f:
        return json.load(f)[key]


def test_extract_invoice_number_simple():
    lines = load_lines("basic_invoice")
    assert extract_invoice_number(lines) == "INV-10293"


def test_extract_invoice_date_labeled():
    lines = load_lines("basic_invoice")
    assert extract_invoice_date(lines) == "13-Aug-2025"


def test_extract_invoice_date_fallback_regex():
    lines = [{"text": "Date: 01-Jan-2024"}]
    assert extract_invoice_date(lines) == "01-Jan-2024"
