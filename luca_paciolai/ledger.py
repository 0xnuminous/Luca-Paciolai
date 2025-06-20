"""Core ledger operations."""

from __future__ import annotations

from sqlmodel import SQLModel, Session, create_engine

from .models import Transaction


def init_db(db_url: str) -> Session:
    """Initializes the SQLite database and returns a session."""
    engine = create_engine(db_url, echo=False)
    SQLModel.metadata.create_all(engine)
    return Session(engine)


def add_transaction(session: Session, tx: Transaction) -> None:
    """Persist a transaction to the ledger."""
    session.add(tx)  # type: ignore[arg-type]
    session.commit()

