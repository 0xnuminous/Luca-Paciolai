"""Core ledger operations."""

from __future__ import annotations

from sqlmodel import SQLModel, Session, create_engine, select

from .config import LEDGER_PATH

from .models import Transaction

__all__ = ["create_session", "init_db", "add_transaction", "list_accounts"]


def create_session(db_url: str | None = None) -> Session:
    """Return a database session, creating tables on first use."""
    url = f"sqlite:///{LEDGER_PATH}" if db_url is None else db_url
    engine = create_engine(url, echo=False)
    SQLModel.metadata.create_all(engine)
    return Session(engine)


# Backwards compatibility
init_db = create_session


def add_transaction(session: Session, tx: Transaction) -> None:
    """Persist a transaction to the ledger."""
    session.add(tx)  # type: ignore[arg-type]
    session.commit()


def list_accounts(session: Session) -> list[str]:
    """Return unique account names present in the ledger."""
    debit_accounts = session.exec(select(Transaction.debit)).all()
    credit_accounts = session.exec(select(Transaction.credit)).all()
    accounts = set(debit_accounts + credit_accounts)
    return sorted(a for a in accounts if a)

