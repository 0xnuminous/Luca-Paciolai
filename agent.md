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

* **Python** — target Python 3.12 with full type hints.
* **Dependency manager** — use [`uv`](https://astral.sh) exclusively.
  * Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  * Initialize project: `uv init .` (creates `pyproject.toml`, `.venv`, `uv.lock`)
  * Add deps: `uv add <package>`
  * Upgrade deps: `uv lock --upgrade-package <package>`
  * Sync env: `uv sync`
  * **Never** call `uv pip`.
* **Running scripts** — `uv run main.py`.
  * Stand‑alone: `uv run --no-project script.py`
  * Extra deps: `uv run --with rich script.py`
* **Running tools** — `uv run -- pytest -q` or `uv run -- ruff .`.
  * When using the **context7** environment you may run tools via `uvx`, e.g. `uvx ruff .`.
* **Formatting** — use Black (`black -l 120`) and Ruff.
* **Testing** — `uv run -- pytest -q`.
* **Static analysis** — `uv run -- mypy --strict .`.
* **Commits** — do not create new branches. After edits run `pre-commit run --all-files && git add -u && git commit -m "<feat|fix|docs>: …"` and ensure `git status` is clean.
* **Docs** — update `AGENTS.md` or docstrings when behavior changes.

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

---

## Build Specification

Here’s the tighter, fully-merged prompt describing the desired system.

### Prompt for the Coding Agent

You are building a **command-line double-entry accounting system** that parses **plain-English transactions** via an LLM and writes balanced journal entries to a ledger.

### 1️⃣ Natural-Language Parsing (LLM)
* Accept inputs such as "I bought coffee today at Starbucks for $6." or "I sold bitcoin today for 100." and return structured JSON:

```json
{
  "date": "2025-06-19",
  "description": "Coffee at Starbucks",
  "debit": "Expenses:Coffee",
  "credit": "Assets:Cash",
  "amount": 6.00,
  "currency": "USD",
  "instrument": null,
  "quantity": null,
  "price": null
}
```

### 2️⃣ Chart of Accounts Logic
| Step | Rule |
| --- | --- |
| **Boot** | Pre-seed only the five roots: `Assets, Liabilities, Equity, Income, Expenses`. |
| **Discovery** | If the LLM-parsed debit or credit sub-account does not yet exist, prompt: `Account 'Expenses:Coffee' does not exist. Create? [Y/n]` |
| **Action** | `Y/Enter` → create sub-account & continue. `n` → allow user to type another account or abort. |
| **Persistence** | Once created, sub-accounts live in the persistent store (SQLite/JSON/Beancount). |

### 3️⃣ Investment & Tax-Lot Logic
1. **Lot Requirement** — every investment transaction must reference a tax lot `{lot_id}`.
2. **Existing-Lot Check** — when an instrument is present, locate an open lot using the user’s default lot-selection method. If none found, prompt:
   `No tax lot on record for BTC purchased on 2025-06-19 @ $1800/BTC (quantity 0.5). ➜ Create new tax lot? [Y/n]`
3. **Lot Creation Workflow** — on `Y/Enter` assign a unique `lot_id` and store `{instrument, acquisition_date, quantity, cost_basis_per_unit, total_cost}`. On `n` allow manual `lot_id` selection or cancel.
4. **Sale / Closing Lots** — when selling, identify lot(s) to close, compute realized gain/loss, and record remaining quantities for partial closures.

### 4️⃣ Double-Entry Ledger Engine
* Post journal entries only after both account and lot confirmations succeed.
* Validate that total debits equal total credits for each transaction.

### 5️⃣ Multi-Currency & Commodity Handling
* Store the original currency and quantity; translate to a base currency for reports using stored or user-provided FX rates.

### 6️⃣ CLI Interaction Flow (Illustrative)
```
$ bookkeep add "Bought 0.5 BTC for $18,000"
> Parsed:
  Debit Assets:Crypto:BTC (Qty 0.5)           $18,000
  Credit Assets:Cash                          $18,000
  Date: 2025-06-19

Account 'Assets:Crypto:BTC' does not exist. Create? [Y/n] Y
No tax lot on record for BTC acquired 2025-06-19 (0.5 @ $18,000). Create tax lot? [Y/n] Y
Lot ID BTC-20250619-001 created.
Transaction saved.
```

### 7️⃣ Reports & Extras (Optional)
* Balance Sheet, Income Statement, Tax-Lot Register, Realized & Unrealized Gains, XIRR, TWRR.
* CSV/API importers, encrypted storage, vendor auto-categorization, CLI auto-complete.

### Deliverables
* CLI app
* LLM prompt schema & caching layer
* Persistent ledger & tax-lot store
* Unit tests for: parsing, account creation workflow, lot creation & gain/loss math, double-entry balancing
