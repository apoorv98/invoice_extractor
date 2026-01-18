#!/usr/bin/env python3

import re

def extract_gstin(lines):
    for line in lines:
        match = re.search(r"\d{2}[A-Z]{5}\d{4}[A-Z]\dZ[A-Z0-9]", line["text"])
        if match:
            return match.group(0)
    return None


def extract_total_value(lines):
    for i, line in enumerate(lines):
        if "total invoice value" in line["text"].lower():
            if i + 1 < len(lines):
                return lines[i + 1]["text"].strip()
    return None
