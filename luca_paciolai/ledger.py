"""Core ledger operations."""

from __future__ import annotations

from typing import List, Sequence

import typer
from sqlmodel import SQLModel, Session, create_engine, select

from .config import LEDGER_PATH

from .models import Transaction, Account

__all__ = [
    "create_session",
    "init_db",
    "add_transaction",
    "get_account_names",
    "ensure_accounts",
]


def create_session(db_url: str | None = None) -> Session:
    """Return a database session, creating tables on first use."""
    url = f"sqlite:///{LEDGER_PATH}" if db_url is None else db_url
    engine = create_engine(url, echo=False)
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    _ensure_root_accounts(session)
    return session


# Backwards compatibility
init_db = create_session


def add_transaction(session: Session, tx: Transaction) -> None:
    """Persist a transaction to the ledger."""
    session.add(tx)  # type: ignore[arg-type]
    session.commit()


ROOT_ACCOUNTS = ["Assets", "Liabilities", "Equity", "Income", "Expenses"]


def _ensure_root_accounts(session: Session) -> None:
    for name in ROOT_ACCOUNTS:
        if not session.exec(select(Account).where(Account.name == name)).first():
            session.add(Account(name=name))
    session.commit()


def get_account_names(session: Session) -> List[str]:
    return [a.name for a in session.exec(select(Account)).all()]


def ensure_accounts(session: Session, names: Sequence[str]) -> None:
    created = False
    for name in names:
        if not session.exec(select(Account).where(Account.name == name)).first():
            if typer.confirm(f"Create account '{name}'?", default=True):
                session.add(Account(name=name))
                created = True
            else:
                raise typer.Abort()
    if created:
        session.commit()

