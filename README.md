# Luca Paciolai

A command-line double-entry accounting system powered by an LLM. The tool parses natural-language transactions, confirms accounts and tax lots, and stores entries in SQLite.

## Usage

```bash
export VENICE_API_KEY=<your-key>
# optional: choose a Venice model
export VENICE_MODEL=qwen3-4b
uv run main.py "I bought coffee today for $6"
```

Supported models:

```
qwen3-4b (Venice Small)
mistral-31-24b (Venice Medium)
qwen3-235b (Venice Large)
llama-3.2-3b (Llama 3.2 3B)
llama-3.3-70b (Llama 3.3 70B)
```

Run the test suite with:

```bash
uv run python -m pytest -q
```

