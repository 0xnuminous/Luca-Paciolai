from luca_paciolai.llm import parse_transaction


def test_parse_transaction_requires_key() -> None:
    """Calling ``parse_transaction`` without an API key should fail."""

    import pytest

    with pytest.raises(RuntimeError):
        parse_transaction("I bought coffee for 10 dollars", [])


def test_parse_transaction_venice(monkeypatch) -> None:
    """Ensure API code path is exercised when VENICE_API_KEY is set."""

    import json
    from types import SimpleNamespace
    import openai

    expected = {
        "date": "2024-01-01",
        "description": "Coffee",
        "debit": "Expenses:Coffee",
        "credit": "Assets:Cash",
        "amount": 10.0,
        "currency": "USD",
        "instrument": None,
        "quantity": None,
        "price": None,
        "lot_id": None,
    }

    class FakeCompletions:
        def create(self, **kwargs):
            return SimpleNamespace(
                choices=[
                    SimpleNamespace(
                        message=SimpleNamespace(content=json.dumps(expected))
                    )
                ]
            )

    class FakeClient:
        def __init__(self, *args, **kwargs):
            self.chat = SimpleNamespace(completions=FakeCompletions())

    monkeypatch.setattr(openai, "OpenAI", FakeClient)
    monkeypatch.setenv("VENICE_API_KEY", "test-key")
    result = parse_transaction("I bought coffee for 10 dollars", [])
    assert result == expected


def test_invalid_model(monkeypatch) -> None:
    """An unsupported VENICE_MODEL should raise an error."""

    monkeypatch.setenv("VENICE_API_KEY", "key")
    monkeypatch.setenv("VENICE_MODEL", "bad-model")

    import pytest

    with pytest.raises(RuntimeError):
        parse_transaction("hello", [])
