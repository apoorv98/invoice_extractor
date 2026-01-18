#!/usr/bin/env python3

import re

def parse_invoice_items(lines):
    items = []
    current_block = []

    # Step 1: group by SKU
    for line in lines:
        text = line['text'].strip()
        # valid SKU: 6-8 digit number
        if re.match(r'^\d{6,8}$', text):
            if current_block:
                items.append(current_block)
            current_block = [text]
        else:
            if current_block:
                current_block.append(text)
    if current_block:
        items.append(current_block)

    # Step 2: parse each block
    structured_items = []
    for block in items:
        sku = block[0]
        description = None
        tax = None
        quantity = None
        rate = None
        final_amount = None
        imeis = []

        for val in block[1:]:
            val = val.strip()
            # IMEI (12-20 digits)
            if re.match(r'^\d{12,20},?$', val):
                imeis.append(val)
            # Tax %
            elif re.match(r'^\d{1,2}(\.\d+)?%$', val) and tax is None:
                tax = val
            # Quantity: integer ≤ 1000
            elif re.match(r'^\d+(\.\d+)?$', val):
                num_val = float(val)
                if quantity is None and num_val.is_integer() and num_val <= 1000:
                    quantity = str(int(num_val))
                # Rate: first numeric > 1000
                elif rate is None and num_val > 1000:
                    rate = val
                # Final amount: last numeric
                else:
                    final_amount = val
            # Description: first non-numeric, non-tax, non-IMEI string
            elif description is None:
                description = val

        structured_items.append({
            "hsn_cd": sku,
            "description": description,
            "quantity": quantity,
            "rate": rate,
            "tax": tax,
            "final_amount": final_amount,
            "imeis": imeis
        })

    return structured_items
