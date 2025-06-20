from typing import Any, Dict

from luca_paciolai import venice_client


def test_create_client_uses_base_url(monkeypatch):
    captured: Dict[str, Any] = {}

    class Dummy:
        def __init__(self, api_key: str, base_url: str):
            captured["api_key"] = api_key
            captured["base_url"] = base_url

    monkeypatch.setattr(venice_client, "OpenAI", Dummy)
    venice_client.create_client("key")
    assert captured["api_key"] == "key"
    assert captured["base_url"] == venice_client.BASE_URL


def test_chat_completion_passes_system_prompt(monkeypatch):
    class Chat:
        def __init__(self):
            self.kwargs: Dict[str, Any] = {}

        class Completions:
            def __init__(self, parent: "Chat"):
                self.parent = parent

            def create(self, **kwargs: Any) -> Any:  # type: ignore[override]
                self.parent.kwargs = kwargs
                return type("Resp", (), {"choices": [type("M", (), {"message": type("Msg", (), {"content": "ok"})()})()]})()

        @property
        def completions(self) -> "Chat.Completions":
            return Chat.Completions(self)

    class Dummy:
        def __init__(self):
            self.chat = Chat()

    client = Dummy()
    venice_client.chat_completion(
        client,
        [{"role": "user", "content": "hi"}],
        include_venice_system_prompt=False,
    )
    assert client.chat.kwargs["venice_parameters"] == {"include_venice_system_prompt": False}

