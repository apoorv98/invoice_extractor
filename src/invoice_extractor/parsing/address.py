#!/usr/bin/env python3

import re

def extract_addresses(lines):
    keywords = [
        "street", "st.", "road", "rd.", "chowk",
        "office", "nagar", "lane", "shop", "society"
    ]

    address_lines = []
    for line in lines[:50]:
        if any(k in line["text"].lower() for k in keywords):
            address_lines.append(line["text"])

    return " ".join(address_lines)
