# SPEC.md – Functional Specification

> **System**: Command-Line Double-Entry Accounting System with LLM Integration

This document defines the core requirements and behaviors for a plain-English transaction parsing CLI app that records double-entry journal entries and tracks tax lots for investments.

---

## \ud83d\udccc 1. Summary

This system enables users to record journal entries using natural language such as:

* "I bought coffee today at Starbucks for $6."
* "I sold 0.5 BTC today for $1000."

It interprets the statement via LLM and converts it into a structured, double-entry accounting record. It supports tax lot tracking for all investment transactions.

---

## \ud83e\udd96 2. Features

### 2.1 Natural Language Input via LLM

* Parses free-form transaction text.
* When sending a natural language statement to the LLM, the system must also include a current list of account names (both root and sub-accounts) as context. This helps guide the LLM toward matching or suggesting accurate account names.
* Extracts: `date`, `amount`, `currency`, `instrument` (if any), `quantity`, `description`, debit/credit account suggestions.
* LLM output must follow a defined JSON schema.

### 2.2 Dynamic Chart of Accounts

* Root-level accounts (`Assets`, `Liabilities`, `Equity`, `Income`, `Expenses`) exist by default.
* Sub-accounts are created **on-demand** only when referenced by a transaction.
* If a parsed account does not exist, user is prompted to confirm its creation.

### 2.3 Double-Entry Ledger Engine

* Enforces that every transaction has equal debit and credit values.
* Stores `Transaction` objects with metadata.
* Persists entries in a local **SQLite** database using a schema-compatible ORM (e.g. SQLModel).

### 2.4 Tax Lot Tracking

* All investment acquisitions (e.g., crypto, stocks, metals) must create a `TaxLot`.
* Sales require existing lots to calculate cost basis and gain/loss.
* If no lot exists, user is prompted to create one manually.
* Supports FIFO, LIFO, and specific-id methods (user-selectable).

### 2.5 CLI Interface

* `ledger add "<text>"`: parse and confirm entry.
* Interactively confirm new accounts and tax lots.
* Show parsed entry before saving.

### 2.6 Multi-Currency Support

* Records original currency, quantity, and exchange rate.
* Can report in a user-defined base currency.

### 2.7 Reports

* Balance Sheet
* Income Statement
* Tax-Lot Registry
* Realized & Unrealized Gains
* Investment Return (XIRR, TWRR)

---

## \ud83d\udcaa 3. JSON Schema (LLM Output)

```json
{
  "date": "YYYY-MM-DD",
  "description": "string",
  "debit": "Expenses:Coffee",
  "credit": "Assets:Cash",
  "amount": 6.00,
  "currency": "USD",
  "instrument": null,
  "quantity": null,
  "price": null,
  "lot_id": null
}
```

Fields:

* `instrument`, `quantity`, `price`: only required for investment transactions.
* `lot_id`: must be generated or matched when an investment is recorded.

---

## \u2699\ufe0f 4. Internal Object Models (Pythonic)

### Transaction

```python
@dataclass
class Transaction:
    date: date
    description: str
    debit: str
    credit: str
    amount: float
    currency: str
    instrument: Optional[str] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    lot_id: Optional[str] = None
```

### TaxLot

```python
@dataclass
class TaxLot:
    lot_id: str
    instrument: str
    quantity: float
    cost_basis_per_unit: float
    acquisition_date: date
```

---

## \ud83d\udd04 5. Workflow Summary

1. User enters natural language statement via CLI.
2. System calls LLM with that text.
3. LLM returns structured JSON.
4. CLI checks accounts: prompts user if missing.
5. CLI checks tax lot (if applicable): prompts if missing.
6. On confirmation, entry is saved to ledger (SQLite).
7. System updates accounts, lots, balances.

---

## \ud83d\udd12 6. Assumptions & Constraints

* All investment entries must have corresponding tax lot.
* Every transaction must be balanced (debits = credits).
* LLM output must be parseable by pydantic or schema validator.
* All new accounts and lots require user confirmation.
* **SQLite is the required persistence layer.**

---

## \ud83d\udcda 7. References

* `agentinstructs/uv.md` for CLI usage & local tooling.
* `AGENTS.md` for agent workflow and developer guide.

---

**End of Specification.**
