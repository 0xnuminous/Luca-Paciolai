# SPEC Change Log

This document records variances between `SPEC.md` and the current codebase as of this commit.

## Implemented Portions

- Basic CLI with `add` and `select_model` commands is present.
- Transactions are persisted to SQLite through SQLModel.
- LLM parsing stub exists (`luca_paciolai.llm.parse_transaction`).
- Venice model selection helpers (`model_selection.py`) allow choosing a reasoning-capable model.
- `parse_transaction` now receives the list of existing accounts, providing
  the LLM with account context.
- The ledger creates missing accounts on demand using `ensure_accounts`.

## Missing or Incomplete Features

The following areas of `SPEC.md` are not fully implemented:

- **Balance Enforcement**: Transactions are not checked to ensure debits equal credits.
- **Tax Lot Tracking**: `TaxLot` model is defined but acquisition/sale logic and prompts are absent.
- **Multi-Currency and Reporting**: Support for exchange rates and financial reports is not implemented.

These gaps should be addressed before the software fully conforms to the functional specification.
