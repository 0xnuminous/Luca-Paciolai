Refer to `agentinstructs/` for detailed usage instructions and the complete functional specification (`SPEC.md`).
Outstanding implementation tasks are tracked in `agentinstructs/TODO.md`.
Additional Venice integration tips are documented in `agentinstructions/venice_best_practices.md`.

## Engineering Guide
For an overview of the repository structure and module responsibilities, see
`agentinstructs/engineering.md`.

## Environment Setup
Codex automatically executes `agentinstructs/setup.md` when the Docker container starts. This script installs `uv`, syncs dependencies, and runs lint and test commands. You generally do not need to manually reinstall tooling.

## Quality Checks
Run these commands before committing changes:

```bash
uv run python -m pytest -q
uvx ruff check luca_paciolai
uv run mypy luca_paciolai  # optional; may fail due to missing stubs
```
### Constraints

Guidelines

    Keep code intuitive and user‑friendly.
    Ensure new code merges cleanly and runs as expected.
    Document usage clearly for end users.

    Language: Python 3.12
    Prioritise correctness over premature optimisation.
    Every new feature must include its own tests.
    Be creative and novel using first-principles thinking and coding.
    Keep it simple.

### Ruff Errors
`ruff` enforces our Python style. If `uvx ruff check luca_paciolai` reports
issues, fix them **before committing**. You can auto-apply many fixes with:

```bash
uvx ruff check --fix luca_paciolai
```
Manual edits may still be required for complex violations.
