#!/usr/bin/env python3

import re
from typing import Optional


def extract_invoice_number(lines: list[dict]) -> Optional[str]:
    for line in lines:
        if "invoice no" in line["text"].lower():
            return line["text"].split("Invoice No")[-1].strip()
    return None


def extract_invoice_date(lines: list[dict]) -> Optional[str]:
    for line in lines:
        if "invoice date" in line["text"].lower():
            return line["text"].split("Invoice Date")[-1].strip()

        match = re.search(r"\d{1,2}-[A-Za-z]{3}-\d{4}", line["text"])
        if match:
            return match.group(0)

    return None
