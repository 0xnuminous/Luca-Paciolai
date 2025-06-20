import json
from types import SimpleNamespace

from typer.testing import CliRunner

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

    def fake_add_transaction(session, tx):
        captured["tx"] = tx

    def fake_parse_transaction(text, accounts):
        captured["text"] = text
        captured["accounts"] = accounts
        return parsed

    monkeypatch.setattr(cli, "add_transaction", fake_add_transaction)
    monkeypatch.setattr(cli, "parse_transaction", fake_parse_transaction)
    monkeypatch.setattr(cli, "load_selected_model", lambda: "model")
    monkeypatch.setattr(cli, "list_accounts", lambda session: ["Assets:Cash"]) 

    result = runner.invoke(cli.app, ["add", "I bought coffee for $5"])
    assert result.exit_code == 0
    assert json.loads(result.stdout) == parsed
    assert captured["text"] == "I bought coffee for $5"
    assert captured["accounts"] == ["Assets:Cash"]
    assert isinstance(captured["tx"], Transaction)
    assert captured["tx"].amount == 5.0
