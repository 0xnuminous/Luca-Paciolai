import typer

from luca_paciolai.ledger import create_session, get_account_names, ensure_accounts


def test_create_session_initializes_roots(tmp_path):
    db_url = f"sqlite:///{tmp_path/'ledger.db'}"
    session = create_session(db_url)
    names = get_account_names(session)
    assert set(names) >= {"Assets", "Liabilities", "Equity", "Income", "Expenses"}


def test_ensure_accounts_creates_on_confirm(tmp_path, monkeypatch):
    db_url = f"sqlite:///{tmp_path/'ledger.db'}"
    session = create_session(db_url)
    monkeypatch.setattr(typer, "confirm", lambda *args, **kwargs: True)
    ensure_accounts(session, ["Assets:Cash"])
    assert "Assets:Cash" in get_account_names(session)
