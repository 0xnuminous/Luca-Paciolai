from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import requests

CONFIG_PATH = Path("model.json")


def fetch_venice_models() -> List[Dict[str, Any]]:
    """Return Venice models that support reasoning."""
    url = "https://api.venice.ai/api/v1/models?type=text"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json().get("data", [])
    return [
        m
        for m in data
        if m.get("model_spec", {})
        .get("capabilities", {})
        .get("supportsReasoning")
    ]


def save_selected_model(model_id: str) -> None:
    """Persist the chosen model ID."""
    CONFIG_PATH.write_text(json.dumps({"model": model_id}))


def load_selected_model() -> str | None:
    """Return the currently selected model ID if stored."""
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text()).get("model")
    return None
