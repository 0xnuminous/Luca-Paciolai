import json
from types import SimpleNamespace

from typer.testing import CliRunner
import typer

from luca_paciolai import cli
from luca_paciolai.models import Transaction


def test_add_command_persists_transaction(monkeypatch):
    runner = CliRunner()

    parsed = {
        "date": "2023-01-01",
        "description": "Coffee",
        "debit": "Expenses:Coffee",
        "credit": "Assets:Cash",
        "amount": 5.0,
        "currency": "USD",
    }

    captured = {}

    monkeypatch.setattr(cli, "create_session", lambda: SimpleNamespace())
    monkeypatch.setattr(cli, "get_account_names", lambda session: [])
    monkeypatch.setattr(cli, "ensure_accounts", lambda session, names: None)

    def fake_add_transaction(session, tx):
        captured["tx"] = tx

    def fake_parse_transaction(text, accounts):
        captured["text"] = text
        return parsed

    monkeypatch.setattr(cli, "add_transaction", fake_add_transaction)
    monkeypatch.setattr(cli, "parse_transaction", fake_parse_transaction)
    monkeypatch.setattr(cli, "load_selected_model", lambda: "model")

    result = runner.invoke(cli.app, ["add", "I bought coffee for $5"])
    assert result.exit_code == 0
    assert json.loads(result.stdout) == parsed
    assert captured["text"] == "I bought coffee for $5"
    assert isinstance(captured["tx"], Transaction)
    assert captured["tx"].amount == 5.0


def test_select_model_valid_and_invalid(monkeypatch):
    runner = CliRunner()

    models = [
        {"id": "a", "model_spec": {"name": "A"}},
        {"id": "b", "model_spec": {"name": "B"}},
    ]

    monkeypatch.setattr(cli, "fetch_venice_models", lambda: models)

    saved = {}

    def fake_save(model_id: str) -> None:
        saved["model"] = model_id

    monkeypatch.setattr(cli, "save_selected_model", fake_save)

    # Valid selection
    monkeypatch.setattr(typer, "prompt", lambda *a, **kw: 2)
    result = runner.invoke(cli.app, ["select-model"])
    assert result.exit_code == 0
    assert saved["model"] == "b"

    # Invalid selection
    monkeypatch.setattr(typer, "prompt", lambda *a, **kw: 3)
    result = runner.invoke(cli.app, ["select-model"])
    assert result.exit_code != 0
    assert "Invalid selection." in result.stdout
