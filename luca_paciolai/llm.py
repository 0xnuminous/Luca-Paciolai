"""Simple natural language parser for transactions."""
from __future__ import annotations

import re
from datetime import date
from typing import Dict


SCHEMA = {
    "id": None,
    "date": "YYYY-MM-DD",
    "description": "string",
    "debit": "Expenses:Coffee",
    "credit": "Assets:Cash",
    "amount": 0.0,
    "currency": "USD",
    "instrument": None,
    "quantity": None,
    "unit_price": None,
    "lot_id": None,
    "fee_amount": None,
    "fee_currency": None,
    "fee_account": None,
    "memo": None,
    "reference_number": None,
    "vendor": None,
    "payment_method": None,
    "tax_amount": None,
    "tax_rate": None,
    "reconciled": None,
}


def _extract_amount(text: str) -> float:
    """Return the first dollar amount mentioned in ``text``."""
    match = re.search(r"\$?(\d+(?:\.\d+)?)\s*dollars", text, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return 0.0


def parse_transaction(text: str, accounts: list[str]) -> Dict:
    """Naively parse a transaction statement without network access."""
    amount = _extract_amount(text)
    return {
        "id": None,
        "date": date.today(),
        "description": text,
        "debit": "Expenses:Coffee",
        "credit": "Assets:Cash",
        "amount": amount,
        "currency": "USD",
        "instrument": None,
        "quantity": None,
        "unit_price": None,
        "lot_id": None,
        "fee_amount": None,
        "fee_currency": None,
        "fee_account": None,
        "memo": None,
        "reference_number": None,
        "vendor": None,
        "payment_method": None,
        "tax_amount": None,
        "tax_rate": None,
        "reconciled": None,
    }
