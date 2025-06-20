from types import SimpleNamespace

import openai

from luca_paciolai.llm import parse_transaction


def test_parse_transaction_amount(monkeypatch) -> None:
    class FakeClient:
        def __init__(self) -> None:
            self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.create))

        def create(self, *args, **kwargs):
            resp = SimpleNamespace()
            msg = SimpleNamespace(content='{"amount": 10.0}')
            resp.choices = [SimpleNamespace(message=msg)]
            return resp

    monkeypatch.setattr(openai, "OpenAI", lambda: FakeClient())
    result = parse_transaction("I bought 2 coffees for 10 dollars", [])
    assert result["amount"] == 10.0
