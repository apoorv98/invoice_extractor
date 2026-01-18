#!/usr/bin/env python3

import re

def extract_invoice_number(lines):
    for line in lines:
        if "invoice no" in line['text'].lower():
            return line['text'].split("Invoice No")[-1].strip()

def extract_invoice_date(lines):
    for line in lines:
        if "invoice date" in line['text'].lower():
            return line['text'].split("Invoice Date")[-1].strip()
        # fallback for dates like 13-Aug-2025
        match = re.search(r"\d{1,2}-[A-Za-z]{3}-\d{4}", line['text'])
        if match:
            return match.group(0)
    return None
