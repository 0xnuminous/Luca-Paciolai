from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import requests

from .config import MODEL_CONFIG_PATH

__all__ = [
    "fetch_venice_models",
    "save_selected_model",
    "load_selected_model",
    "CONFIG_PATH",
]

CONFIG_PATH = MODEL_CONFIG_PATH


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


def save_selected_model(model_id: str, path: Path | None = None) -> None:
    """Persist the chosen model ID."""
    cfg_path = CONFIG_PATH if path is None else path
    cfg_path.write_text(json.dumps({"model": model_id}))


def load_selected_model(path: Path | None = None) -> str | None:
    """Return the currently selected model ID if stored."""
    cfg_path = CONFIG_PATH if path is None else path
    if cfg_path.exists():
        return json.loads(cfg_path.read_text()).get("model")
    return None
