#!/usr/bin/env bash
# Codex setup script
# This file is executed automatically when Codex spins up the docker
# container for this project. It installs the **uv** package manager,
# synchronizes dependencies and runs basic quality checks.
set -euo pipefail

# Optional: debug trace output
[ "${DEBUG:-0}" = "1" ] && set -x

echo "🔧 Bootstrapping Double-Entry Accounting Environment..."

# Install uv if not found
if ! command -v uv &> /dev/null; then
  echo "🚀 Installing uv package manager..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
  # Persist PATH
  if ! grep -q 'uv' "$HOME/.bashrc"; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
  fi
fi

# Show versions
echo "📦 Python: $(python --version)"
echo "📦 UV:     $(uv --version)"

# Initialize project if needed
if [ ! -f pyproject.toml ]; then
  echo "🧱 Initializing pyproject with uv..."
  uv init
fi

# Sync dependencies
echo "🔄 Syncing dependencies with development extras..."
uv sync --dev

# Dev tooling runs via uvx; no installation needed

# Pre-commit hook setup (if available)
if [ -f .pre-commit-config.yaml ]; then
  echo "⚙️  Installing pre-commit hooks..."
  uvx pre-commit install
fi

# Run static checks
echo "🧪 Running static checks..."
uvx ruff check luca_paciolai || true
uv run mypy luca_paciolai || true

# Run tests if available
if [ -d tests ]; then
  echo "🧪 Running tests..."
  uv run --with pytest-cov python -m pytest -q \
    --cov=luca_paciolai --cov-report=term-missing
else
  echo "⚠️  No tests directory found. Skipping tests."
fi

echo "✅ Setup complete."
