# AGENTS.md — Instructions for Codex Agents

> **Scope**  All files in this repository are covered by these rules. Nested `AGENTS.md` files may refine or override guidance for their sub‑trees.

---

## 1  Project Overview

**The Accountant** is a plain‑text double‑entry accounting tool that:

1. Accepts natural‑language transaction descriptions.
2. Uses an LLM (Venice AI on cloud or Apple on‑device Foundation Models) to draft hledger journal lines **with in‑line tax‑lot tags**.
3. Requires explicit user confirmation before persisting changes.

Key directories:

```
/              ← project root, Git repo
├─ src/        ← Python source (PEP 621 layout)
│  └─ accountant/   ← CLI + core logic
├─ tests/      ← pytest test‑suite
└─ journal.journal  ← single hledger journal file
```

---

## 2  Language & Tooling Conventions

| Topic                                | Guideline                                                                                                                                         |                                                                                                                                                                                                              |                                                |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------- |
| **Python**                           | Target **Python 3.12** with full type‑hints.                                                                                                      |                                                                                                                                                                                                              |                                                |
| **Dependency & environment manager** | Use **`uv` (Astral)** — it replaces pip/venv.<br>Install once:<br>\`curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh`.<br>Initialize project: `uv init .`(creates *pyproject.toml*, **.venv**, *uv.lock*).<br>Add deps:`uv add requests rich`.<br>Upgrade deps: `uv lock --upgrade-package requests`.<br>Sync env: `uv sync\`. |                                                |
| **Running scripts**                  | In‑project: `uv run main.py`.<br>Stand‑alone: `uv run --no-project example.py`.<br>Ad‑hoc deps: `uv run --with rich example.py`.                  |                                                                                                                                                                                                              |                                                |
| **Running tools / commands**         | Via project env: `uv run -- pytest -q` or `uv run -- ruff .`.<br>Shortcut form: `uv --tool pytest -q`.                                            |                                                                                                                                                                                                              |                                                |
| **Formatting**                       | Run **Black** (`black -l 120`) and **Ruff**.                                                                                                      |                                                                                                                                                                                                              |                                                |
| **Testing**                          | `uv run -- pytest -q` and optionally `pytest‑cov`. Tests must pass.                                                                               |                                                                                                                                                                                                              |                                                |
| **Static analysis**                  | `uv run -- mypy --strict .` must succeed.                                                                                                         |                                                                                                                                                                                                              |                                                |
| **Commits**                          | *Do not create new branches.* After code edits:<br>\`pre-commit run --all-files && git add -u && git commit -m "\<feat                            | fix                                                                                                                                                                                                          | docs>: …"`<br>`git status\` **must be clean**. |
| **Docs**                             | Update AGENTS.md or docstrings when behavior changes.                                                                                             |                                                                                                                                                                                                              |                                                |

---

## 3  Journal & Tax‑Lot Specification  Journal & Tax‑Lot Specification

* Use standard **hledger** syntax.
* Track lots **inside the same file** using posting‑level tags:

  ```ledger
  2024-01-15 * "Buy BTC"
      Assets:Crypto:BTC   0.5 BTC {30_000 USD}  ; lot_id:BTC-2024-01-15-1 acquired:2024-01-15 method:Specific
      Assets:Cash        -15_000 USD
  ```
* When selling, repeat the same `lot_id:` tag on the posting that reduces quantity.
* The CLI’s lot engine scans the journal to derive remaining quantities; **no external lot files**.

---

## 4  LLM Interaction Contract

1. **Choose provider** by calling `accountant.llm.get_default_provider()` which resolves:

   * `AppleOnDeviceProvider` if available.
   * Else one of the three Venice AI models:

     * `qwen-2.5-qwq-32b` (“Venice Reasoning”)
     * `mistral-31-24b` (“Venice Medium”)
     * `qwen3-4b` (“Venice Small”)
2. Draft a transaction **only after** all required details are known. If data is missing, emit a `ClarificationRequest` object and **return**—the CLI will ask the user.
3. After the user confirms, format the posting exactly, append to `journal.journal`, and ensure the file ends with a trailing newline.

---

## 5  Testing & Validation Rules

* Every commit **must** leave:

  * `pytest` green
  * `ruff --fix --exit-zero` clean
  * `mypy --strict` clean
  * `hledger check journal.journal` with **no warnings or errors**
* If any check fails, *fix and recommit* before exiting.

---

## 6  Pull‑Request / Patch Message Template

If a PR message is required, use:

```
### Summary
<one‑sentence change summary>

### Details
* Why: <reason>
* What: <key bullet points>
* Tests: <pytest‑id / manual>

### Checklist
- [ ] Code formatted (Black, Ruff)
- [ ] Tests pass
- [ ] Docs updated
```

---

## 7  Forbidden Actions

* Never amend or squash existing commits.
* Never push unformatted code.
* Never write to any file outside the repo root.
* Never add secrets or API keys to the journal or source.

---

Happy Accounting! 🧮
