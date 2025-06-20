Refer to `agentinstructs/` for detailed usage instructions and the complete functional specification (`SPEC.md`).

## Environment Setup
Codex automatically executes `agentinstructs/setup.md` when the Docker container starts. This script installs `uv`, syncs dependencies, and runs lint and test commands. You generally do not need to manually reinstall tooling.

## Quality Checks
Run these commands before committing changes:

```bash
uv run python -m pytest -q
uv run ruff check luca_paciolai
uv run mypy luca_paciolai  # optional; may fail due to missing stubs
```
