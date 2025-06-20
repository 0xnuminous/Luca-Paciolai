"""Command line interface."""
from __future__ import annotations

import json
from pathlib import Path

import typer

from .ledger import init_db, add_transaction
from .llm import parse_transaction
from .models import Transaction

app = typer.Typer()
DB_PATH = Path("ledger.db")


@app.command()
def add(text: str) -> None:
    """Parse natural language transaction and save to the ledger."""
    session = init_db(f"sqlite:///{DB_PATH}")
    # TODO: load existing accounts
    result = parse_transaction(text, [])
    tx = Transaction(**result)
    add_transaction(session, tx)
    typer.echo(json.dumps(result, indent=2))


def main() -> None:
    app()


if __name__ == "__main__":
    main()
