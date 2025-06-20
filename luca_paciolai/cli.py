"""Command line interface."""
from __future__ import annotations

import json

__all__ = ["app", "main", "add", "select_model"]

import typer

from .ledger import create_session, add_transaction, list_accounts
from .llm import parse_transaction
from .models import Transaction
from .model_selection import (
    fetch_venice_models,
    load_selected_model,
    save_selected_model,
)

app = typer.Typer()


@app.command()
def add(text: str) -> None:
    """Parse natural language transaction and save to the ledger."""
    session = create_session()
    accounts = list_accounts(session)
    _model = load_selected_model()
    # TODO: pass `_model` to the LLM API when implemented
    result = parse_transaction(text, accounts)
    tx = Transaction(**result)
    add_transaction(session, tx)
    typer.echo(json.dumps(result, indent=2, default=str))


@app.command()
def select_model() -> None:
    """Choose and persist a Venice model for LLM parsing."""
    models = fetch_venice_models()
    if not models:
        typer.echo("No compatible models found.")
        raise typer.Exit(code=1)
    for idx, model in enumerate(models, start=1):
        name = model["model_spec"]["name"]
        typer.echo(f"{idx}. {name} ({model['id']})")
    choice = typer.prompt("Enter model number", type=int)
    if choice < 1 or choice > len(models):
        typer.echo("Invalid selection.")
        raise typer.Exit(code=1)
    selected = models[choice - 1]["id"]
    save_selected_model(selected)
    typer.echo(f"Selected model: {selected}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
