# uv - The Modern Python Package and Project Manager

This guide provides comprehensive instructions for AI coding agents on using **uv**, an extremely fast Python package and project manager written in Rust. This documentation is based on official Context7 sources and is designed to help agents understand and implement proper uv workflows.

## Overview

**uv** is a drop-in replacement for `pip`, `pip-tools`, `pipx`, `poetry`, and `virtualenv` that provides:
- **10-100x faster** package installation than pip
- **Universal lockfiles** for reproducible environments
- **Project management** with dependency resolution
- **Python version management** with automatic installation
- **Tool execution** in isolated environments

## Installation

Install uv using the official standalone installer:

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Core Concepts

### 1. Project Management Workflow

uv follows a modern Python project workflow similar to poetry or rye:

```bash
# Initialize a new project
uv init example
cd example

# Add dependencies
uv add requests pytest

# Run commands in project environment
uv run python main.py
uv run pytest

# Create lockfile
uv lock

# Sync dependencies
uv sync
```

### 2. Virtual Environment Management

uv automatically manages virtual environments:

```bash
# Create virtual environment
uv venv

# uv automatically activates environments for commands
uv run python script.py  # Runs in project environment

# Manual activation (if needed)
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### 3. Dependency Management

#### Adding Dependencies

```bash
# Add runtime dependencies
uv add requests httpx

# Add development dependencies
uv add --dev pytest ruff black

# Add with version constraints
uv add "django>=4.0,<5.0"

# Add from Git repository
uv add "git+https://github.com/user/repo.git"

# Add local editable package
uv add --editable ./local/package
```

#### Removing Dependencies

```bash
# Remove a dependency
uv remove requests

# Remove development dependency
uv remove --dev pytest
```

#### Upgrading Dependencies

```bash
# Upgrade specific package
uv lock --upgrade-package requests

# Upgrade all packages
uv lock --upgrade
```

### 4. Project Types

#### Application Project (Default)

```bash
# Initialize application project
uv init my-app
cd my-app
uv run main.py
```

#### Library Project

```bash
# Initialize library project with src layout
uv init --lib my-library
cd my-library
uv build  # Create distribution packages
```

#### Minimal Project

```bash
# Initialize with minimal configuration
uv init --bare my-minimal
```

## Essential Commands

### Project Commands

```bash
# Initialize new project
uv init [project-name]
uv init --lib [library-name]    # Library with src layout
uv init --bare [minimal-name]   # Minimal configuration

# Add/remove dependencies
uv add <package>
uv add --dev <package>          # Development dependency
uv remove <package>

# Sync environment with dependencies
uv sync                         # Sync all dependencies
uv sync --dev                   # Include development dependencies
uv sync --locked                # Use exact lockfile versions

# Create/update lockfile
uv lock
uv lock --check                 # Check if lockfile is up-to-date

# Run commands in project environment
uv run <command>
uv run python script.py
uv run pytest
uv run --with httpx script.py   # Add temporary dependency
```

### Tool Management with uvx

Use `uvx` (alias for `uv tool run`) to run tools in isolated environments:

```bash
# Run tools without installation
uvx ruff check .
uvx black src/
uvx pytest
uvx mypy src/

# Run specific version
uvx ruff@0.3.0 check .
uvx ruff@latest check .

# Run tool from different package
uvx --from httpie http
```

### Python Version Management

```bash
# Install Python versions
uv python install 3.11 3.12
uv python install              # Install latest version

# Pin Python version for project
uv python pin 3.11

# List available/installed versions
uv python list
uv python list --managed-python
```

### Environment Management

```bash
# Create virtual environment
uv venv
uv venv --python 3.11          # Specific Python version

# Activate environment manually (optional)
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows
```

### Build and Publish

```bash
# Build distribution packages
uv build                       # Creates .whl and .tar.gz
uv build --wheel               # Only wheel
uv build --sdist               # Only source distribution

# Publish to package index
uv publish                     # Publish to PyPI
uv publish --repository testpypi  # Test PyPI
```

## Configuration

### pyproject.toml Structure

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "A sample project"
dependencies = [
    "requests>=2.28.0",
    "click>=8.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
    "black>=23.0.0",
]

[project.scripts]
my-cli = "my_project.cli:main"

[tool.uv]
managed = true                 # Enable uv project management
dev-dependencies = [
    "pytest",
    "ruff",
    "black",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### uv Tool Configuration

```toml
[tool.uv]
# Project management
managed = true

# Python version constraints
requires-python = ">=3.11"

# Dependency sources
[tool.uv.sources]
my-package = { path = "../my-package", editable = true }
other-package = { git = "https://github.com/user/repo.git" }

# Development dependencies
dev-dependencies = [
    "pytest>=7.0.0",
    "mypy>=1.0.0",
]
```

## Advanced Usage

### Script Dependencies

Create Python scripts with inline dependency metadata:

```python
# /// script
# dependencies = [
#   "httpx",
#   "rich",
# ]
# ///

import httpx
from rich import print

response = httpx.get("https://api.github.com")
print(response.json())
```

Run with:
```bash
uv run script.py
```

### Workspace Management

For multi-package projects:

```toml
# pyproject.toml (root)
[tool.uv.workspace]
members = ["packages/*"]

[project]
name = "my-workspace"
version = "0.1.0"
```

### Docker Integration

```dockerfile
FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src/ ./src/

# Install dependencies
RUN uv sync --locked --no-editable

# Run application
CMD ["/app/.venv/bin/python", "-m", "src.main"]
```

### GitHub Actions Integration

```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v5
        
      - name: Install dependencies
        run: uv sync --locked --all-extras --dev
        
      - name: Run tests
        run: uv run pytest
        
      - name: Run linting
        run: uv run ruff check .
```

## Best Practices for AI Agents

### 1. Project Initialization

Always start new projects with uv:

```bash
# For applications/scripts
uv init my-app

# For libraries
uv init --lib my-library

# For minimal setup
uv init --bare my-project
```

### 2. Dependency Management

- Use `uv add` instead of manually editing pyproject.toml
- Separate development dependencies with `--dev` flag
- Lock dependencies with `uv lock` for reproducibility
- Use version constraints for stability

```bash
# Good practices
uv add "requests>=2.28,<3"     # Version range
uv add --dev pytest            # Development dependency
uv lock                        # Lock for reproducibility
```

### 3. Running Code

Always use `uv run` for consistency:

```bash
# Instead of: python script.py
uv run python script.py

# Instead of: pytest
uv run pytest

# For tools, use uvx
uvx ruff check .
uvx black src/
```

### 4. Environment Synchronization

Keep environments in sync:

```bash
# After cloning repository
uv sync --locked

# After adding dependencies
uv sync

# For development
uv sync --dev
```

### 5. Tool Usage

Use uvx for ephemeral tool execution:

```bash
# Linting and formatting
uvx ruff check .
uvx ruff format .
uvx black src/

# Type checking
uvx mypy src/

# Security scanning
uvx bandit -r src/
```

## Migration from Other Tools

### From pip + requirements.txt

```bash
# Add dependencies from requirements.txt
uv add -r requirements.txt -c constraints.txt

# Remove old files (optional)
rm requirements.txt constraints.txt
```

### From poetry

```bash
# Convert poetry project
uv init --no-package  # If not a package
uv add $(poetry show --no-dev | cut -d' ' -f1)
uv add --dev $(poetry show --dev | cut -d' ' -f1)
```

### From pipenv

```bash
# Convert Pipfile dependencies
uv add -r Pipfile
# Manual conversion may be needed for complex Pipfiles
```

## Common Patterns

### Development Workflow

```bash
# 1. Clone and setup
git clone <repository>
cd <repository>
uv sync --dev

# 2. Make changes
# ... edit code ...

# 3. Test and lint
uv run pytest
uvx ruff check .
uvx black src/

# 4. Add new dependency
uv add new-package

# 5. Update lockfile
uv lock

# 6. Commit changes
git add .
git commit -m "feat: add new feature"
```

### CI/CD Pipeline

```bash
# Install dependencies
uv sync --locked --dev

# Run quality checks
uvx ruff check .
uvx black --check src/
uv run mypy src/

# Run tests
uv run pytest --cov=src

# Build package
uv build

# Publish (if on main branch)
uv publish
```

## Troubleshooting

### Common Issues

1. **Virtual environment not found**
   ```bash
   uv sync  # Create and sync environment
   ```

2. **Dependency conflicts**
   ```bash
   uv lock --upgrade  # Resolve with latest versions
   ```

3. **Python version not available**
   ```bash
   uv python install 3.11  # Install missing Python
   ```

4. **Lockfile out of sync**
   ```bash
   uv lock  # Regenerate lockfile
   uv sync --locked  # Sync with lockfile
   ```

### Debug Commands

```bash
# Verbose output
uv --verbose sync

# Check project status
uv lock --check

# List environments
uv venv list

# Show dependency tree
uv tree
```

## Performance Benefits

uv provides significant performance improvements:

- **Installation**: 10-100x faster than pip
- **Resolution**: Advanced dependency resolver
- **Caching**: Aggressive caching of downloads and builds
- **Parallel**: Parallel downloads and installs
- **Incremental**: Only processes changes
```
