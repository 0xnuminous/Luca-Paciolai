#!/usr/bin/env bash
set -euo pipefail

# Install uv if missing
if ! command -v uv >/dev/null 2>&1; then
  echo "Installing uv package manager..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

# Initialize project if needed
if [ ! -f pyproject.toml ]; then
  echo "Initializing pyproject via uv..."
  uv init .
fi

# Sync dependencies
uv sync

# Run tests when available
if [ -d tests ]; then
  echo "Running tests..."
  uv run -- pytest -q
else
  echo "No tests directory found. Skipping tests."
fi
