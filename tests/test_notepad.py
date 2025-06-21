from luca_paciolai import cli


def test_notepad_calls_add(monkeypatch):
    captured = {}

    def fake_add(text: str) -> None:
        captured['text'] = text

    class FakeSession:
        def __init__(self, *args, **kwargs) -> None:
            pass

        def prompt(self) -> str:  # type: ignore[override]
            return "test tx"

    monkeypatch.setattr(cli, "add", fake_add)
    monkeypatch.setattr("prompt_toolkit.PromptSession", lambda *a, **k: FakeSession())
    monkeypatch.setattr("prompt_toolkit.shortcuts.print_formatted_text", lambda *a, **k: None)
    cli.notepad()
    assert captured['text'] == "test tx"
