#!/usr/bin/env python3

import json
from invoice_extractor.parsing.address import (extract_addresses)

FIXTURES = "tests/fixtures/sample_lines.json"

def load_lines(key):
    with open(FIXTURES) as f:
        return json.load(f)[key]

def test_extract_addresses_heuristic():
    lines = load_lines("address_block")
    address = extract_addresses(lines)
    assert "MG Road" in address
