#!/usr/bin/env python3

import json
from invoice_extractor.parsing.items import parse_invoice_items

FIXTURES = "tests/fixtures/sample_lines.json"


def load_lines(key):
    with open(FIXTURES) as f:
        return json.load(f)[key]


def test_parse_single_invoice_item_block():
    lines = load_lines("line_items")
    items = parse_invoice_items(lines)

    assert len(items) == 1

    item = items[0]
    assert item["hsn_cd"] == "851712"
    assert item["description"] == "Mobile Handset Model X"
    assert item["quantity"] == "2"
    assert item["rate"] == "45000"
    assert item["tax"] == "18%"
    assert item["final_amount"] == "90000"
    assert item["imeis"] == ["356789012345678"]
