"""Utility for interacting with Venice's OpenAI-compatible API."""

from __future__ import annotations

import os
from typing import Dict, List

from openai import OpenAI, OpenAIError

BASE_URL = "https://api.venice.ai/api/v1"


def create_client(api_key: str | None = None) -> OpenAI:
    """Return an OpenAI client configured for Venice."""
    key = api_key or os.getenv("VENICE_API_KEY")
    if not key:
        raise ValueError("A Venice API key is required")
    return OpenAI(api_key=key, base_url=BASE_URL)


def chat_completion(
    client: OpenAI,
    messages: List[Dict[str, str]],
    *,
    model: str = "default",
    include_venice_system_prompt: bool = True,
) -> str:
    """Request a chat completion from Venice with basic error handling."""
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            venice_parameters={"include_venice_system_prompt": include_venice_system_prompt},
        )
    except OpenAIError as exc:  # pragma: no cover - network failure
        raise RuntimeError(f"Venice API error: {exc}") from exc
    return resp.choices[0].message.content  # type: ignore[return-value]
