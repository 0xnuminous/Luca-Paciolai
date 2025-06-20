import typer
from datetime import date
from sqlmodel import select
import pytest

from luca_paciolai.ledger import (
    create_session,
    get_account_names,
    ensure_accounts,
    add_transaction,
)
from luca_paciolai.models import Transaction


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


def test_add_transaction_commits(tmp_path):
    db_url = f"sqlite:///{tmp_path/'ledger.db'}"
    session = create_session(db_url)
    tx = Transaction(
        date=date.today(),
        description="Test",
        debit="Expenses:Misc",
        credit="Assets:Cash",
        amount=1.0,
        currency="USD",
    )
    add_transaction(session, tx)
    stored = session.exec(select(Transaction)).first()
    assert stored is not None
    assert stored.amount == 1.0


def test_ensure_accounts_aborts_on_decline(tmp_path, monkeypatch):
    db_url = f"sqlite:///{tmp_path/'ledger.db'}"
    session = create_session(db_url)
    monkeypatch.setattr(typer, "confirm", lambda *args, **kwargs: False)
    with pytest.raises(typer.Abort):
        ensure_accounts(session, ["Assets:Bank"])
