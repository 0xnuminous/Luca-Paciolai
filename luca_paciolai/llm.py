"""Parse transactions via the Venice.ai API."""
from __future__ import annotations

import json
import os
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


VENICE_BASE_URL = os.getenv("VENICE_BASE_URL", "https://api.venice.ai/api/v1")
"""Base URL for the Venice.ai API."""

VENICE_MODELS = {
    "qwen3-4b": "Venice Small",
    "mistral-31-24b": "Venice Medium",
    "qwen3-235b": "Venice Large",
    "llama-3.2-3b": "Llama 3.2 3B",
    "llama-3.3-70b": "Llama 3.3 70B",
}
"""Allowed model identifiers mapped to human-friendly names."""


def _call_venice(text: str, accounts: list[str], api_key: str) -> Dict:
    """Call the Venice ``/chat/completions`` endpoint and return parsed JSON."""

    client = openai.OpenAI(api_key=api_key, base_url=VENICE_BASE_URL)

    system = (
        "You are a bookkeeping assistant. Parse the user transaction into the "
        "following JSON schema: " + json.dumps(SCHEMA)
    )
    if accounts:
        system += " Available accounts: " + ", ".join(accounts) + "."

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": text},
    ]

    model = os.getenv("VENICE_MODEL", "qwen3-4b")
    if model not in VENICE_MODELS:
        raise RuntimeError(f"Unsupported VENICE_MODEL: {model}")

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content
    return json.loads(content)


def parse_transaction(text: str, accounts: list[str]) -> Dict:
    """Parse ``text`` using the Venice API.

    ``VENICE_API_KEY`` must be defined in the environment.
    """

    api_key = os.getenv("VENICE_API_KEY")
    if not api_key:
        raise RuntimeError("VENICE_API_KEY is not set")

    return _call_venice(text, accounts, api_key)
