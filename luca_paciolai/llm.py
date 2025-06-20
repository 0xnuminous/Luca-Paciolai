"""LLM integration for natural language transaction parsing."""
from __future__ import annotations

import json
from typing import Dict

import openai


SCHEMA = {
    "date": "YYYY-MM-DD",
    "description": "string",
    "debit": "Expenses:Coffee",
    "credit": "Assets:Cash",
    "amount": 0.0,
    "currency": "USD",
    "instrument": None,
    "quantity": None,
    "price": None,
    "lot_id": None,
}


def parse_transaction(text: str, accounts: list[str]) -> Dict:
    """Call the LLM to parse a natural language statement."""
    prompt = f"Accounts: {', '.join(accounts)}\nTransaction: {text}"
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    content = response.choices[0].message.content
    return json.loads(content)
