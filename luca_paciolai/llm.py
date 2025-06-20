"""Simple natural language parser for transactions."""
from __future__ import annotations

import re
from datetime import date
from typing import Dict, Sequence, Any

__all__ = ["parse_transaction", "extract_amount", "SCHEMA"]


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


_AMOUNT_RE = re.compile(r"\$?(\d+(?:\.\d+)?)\s*dollars", re.IGNORECASE)


def extract_amount(text: str) -> float:
    """Return the first dollar amount mentioned in ``text``."""
    match = _AMOUNT_RE.search(text)
    if match:
        return float(match.group(1))
    return 0.0


def parse_transaction(text: str, accounts: Sequence[str]) -> Dict[str, Any]:
    """Naively parse a transaction statement without network access."""
    amount = extract_amount(text)
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
