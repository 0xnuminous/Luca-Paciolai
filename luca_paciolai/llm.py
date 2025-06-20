"""OpenAI-powered transaction parser."""
from __future__ import annotations

import json
from typing import Any, Dict, Sequence

import openai

__all__ = ["parse_transaction", "SCHEMA"]

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


def parse_transaction(text: str, accounts: Sequence[str]) -> Dict[str, Any]:
    """Parse a transaction statement using the OpenAI API."""
    client = openai.OpenAI()
    prompt = (
        "Convert the following statement into JSON following this schema:"
        f" {json.dumps(SCHEMA)}\nAccounts: {', '.join(accounts)}\n{text}"
    )
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    content = resp.choices[0].message.content
    return json.loads(content)
