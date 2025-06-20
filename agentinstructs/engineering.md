# Engineering Overview

This document describes the architecture of **Luca Paciolai**, a command-line double-entry accounting tool that integrates a language model for natural language parsing.

## Repository Layout

```
.
├── AGENTS.md                – Guidelines for AI contributors
├── README.md                – Basic usage instructions
├── agentinstructs/          – Setup scripts and the functional specification
│   ├── SPEC.md
│   ├── setup.md
│   └── uv.md
├── luca_paciolai/           – Source package
│   ├── __init__.py
│   ├── cli.py               – Typer CLI entry points
│   ├── ledger.py            – SQLite persistence helpers
│   ├── llm.py               – Natural language parser
│   ├── model_selection.py   – Venice model selection helpers
│   └── models.py            – SQLModel data models
├── main.py                  – Thin wrapper that invokes the CLI
├── pyproject.toml           – Project metadata and dependencies
├── tests/                   – Pytest unit tests
│   ├── test_llm.py
│   ├── test_model_selection.py
│   └── test_models.py
└── uv.lock                  – Reproducible dependency lockfile
```

## Key Components

### CLI
`luca_paciolai/cli.py` defines commands using [Typer](https://typer.tiangolo.com/). The `add` command parses a natural-language transaction, converts it to a `Transaction` object and stores it in the ledger. The `select_model` command retrieves compatible Venice models from the API and saves the user's choice.

### Ledger
`luca_paciolai/ledger.py` handles database initialization and transaction persistence with SQLModel, using SQLite as the storage backend.

### Models
`luca_paciolai/models.py` defines the `Transaction` and `TaxLot` data models. These map to SQLite tables via SQLModel and enforce the fields expected by the functional specification.

### Natural Language Parsing
`luca_paciolai/llm.py` contains a simple regex-based parser used in tests. It extracts a dollar amount from text and returns a dictionary following the JSON schema described in `SPEC.md`. In a full implementation, this would call a remote LLM service.

### Model Selection
`luca_paciolai/model_selection.py` fetches Venice model metadata via HTTP, filters for reasoning-capable models, and stores the selected model ID in `model.json`.

### Entry Point
`main.py` is a minimal launcher that invokes the CLI when the package is executed directly.

### Tests
Unit tests under `tests/` verify the transaction parser, model selection helpers, and data models. Run `uv run python -m pytest -q` to execute them.

## Development Workflow

1. Install dependencies with `uv sync --dev` (handled automatically by `agentinstructs/setup.md`).
2. Run static checks:
   ```bash
   uvx ruff check luca_paciolai
   uv run mypy luca_paciolai  # optional
   ```
3. Execute the test suite:
   ```bash
   uv run python -m pytest -q
   ```

See `AGENTS.md` for contributor guidelines and `SPEC.md` for the functional specification.
