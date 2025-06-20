from pathlib import Path
from typing import Any, Dict

import requests

from luca_paciolai import model_selection


def test_fetch_venice_models_filters(monkeypatch):
    sample: Dict[str, Any] = {
        "data": [
            {
                "id": "a",
                "model_spec": {"capabilities": {"supportsReasoning": True}},
            },
            {
                "id": "b",
                "model_spec": {"capabilities": {"supportsReasoning": False}},
            },
        ]
    }

    class Resp:
        def raise_for_status(self) -> None:
            pass

        def json(self) -> Dict[str, Any]:
            return sample

    def fake_get(url: str, timeout: int = 10) -> Resp:  # type: ignore[override]
        return Resp()

    monkeypatch.setattr(requests, "get", fake_get)
    models = model_selection.fetch_venice_models()
    assert [m["id"] for m in models] == ["a"]


def test_save_and_load_selected_model(tmp_path: Path, monkeypatch):
    path = tmp_path / "model.json"
    monkeypatch.setattr(model_selection, "CONFIG_PATH", path)
    model_selection.save_selected_model("foo")
    assert model_selection.load_selected_model() == "foo"
