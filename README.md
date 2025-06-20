# Luca Paciolai

A command-line double-entry accounting system powered by an LLM. The tool parses natural-language transactions, confirms accounts and tax lots, and stores entries in SQLite.

## Usage

```bash
uv run main.py add "I bought coffee today for $6"
```

The ledger database path is configurable via ``luca_paciolai.config.LEDGER_PATH``.

Select a Venice model for LLM parsing:

```bash
uv run main.py select-model
```

Run the test suite with:

```bash
uv run python -m pytest -q
```

