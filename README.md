# Luca Paciolai

A command-line double-entry accounting system powered by an LLM. The tool parses natural-language transactions, confirms accounts and tax lots, and stores entries in SQLite.

## Installation

Install the project dependencies into a local `.venv` directory using `uv`:

```bash
uv sync --dev
```

This command creates the environment and installs runtime and development
packages specified in `pyproject.toml`. All subsequent commands, including
`uv run main.py add ...`, require this initial sync so that `uv` can locate the
dependencies.

## Usage

```bash
uv run main.py add "I bought coffee today for $6"
```

You can also launch a small ASCII notepad interface:

```bash
uv run main.py notepad
```

Set the `OPENAI_API_KEY` environment variable before running commands. The
parser sends statements to OpenAI's API.

The ledger database path is configurable via ``luca_paciolai.config.LEDGER_PATH``.

Select a Venice model for LLM parsing:

```bash
uv run main.py select-model
```

Run the test suite with coverage:

```bash
uv run pytest --cov=luca_paciolai
```

### Using the Venice API

`luca_paciolai.venice_client` provides a helper for interacting with Venice's
OpenAI-compatible API:

```python
from luca_paciolai.venice_client import create_client, chat_completion

client = create_client("your-api-key")
response = chat_completion(
    client,
    [{"role": "user", "content": "Why is the sky blue?"}],
    include_venice_system_prompt=False,
)
print(response)
```

