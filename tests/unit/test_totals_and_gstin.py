#!/usr/bin/env python3

import json
from invoice_extractor.parsing.totals import (
    extract_gstin,
    extract_total_value,
)

FIXTURES = "tests/fixtures/sample_lines.json"


def load_lines(key):
    with open(FIXTURES) as f:
        return json.load(f)[key]


def test_extract_gstin():
    lines = load_lines("basic_invoice")
    assert extract_gstin(lines) == "27ABCDE1234F1Z5"


def test_extract_total_invoice_value_next_line():
    lines = load_lines("basic_invoice")
    assert extract_total_value(lines) == "125000.00"
