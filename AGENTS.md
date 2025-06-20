1️⃣ Natural-Language Parsing (LLM)

    Input examples

        "I bought coffee today at Starbucks for $6."

        "I sold bitcoin today for 100."

    Return structured JSON

{
  "date": "2025-06-19",
  "description": "Coffee at Starbucks",
  "debit": "Expenses:Coffee",
  "credit": "Assets:Cash",
  "amount": 6.00,
  "currency": "USD",
  "instrument": null,          // e.g. "BTC" or "AAPL" when present
  "quantity": null,            // number of units for an instrument
  "price": null                // unit price when instrument present
}

2️⃣ Chart of Accounts Logic
StepRule
BootPre-seed only the five roots: Assets, Liabilities, Equity, Income, Expenses.
DiscoveryIf the LLM-parsed debit or credit sub-account does not yet exist, prompt:
Account 'Expenses:Coffee' does not exist. Create? [Y/n]
ActionY/Enter → create sub-account & continue. n → let user type another account or abort.
PersistenceOnce created, sub-accounts live in the persistent store (SQLite/JSON/Beancount).
3️⃣ Investment & Tax-Lot Logic

    Lot Requirement

        Every investment transaction (crypto, stocks, metals, etc.) must reference a tax lot {lot_id}.

    Existing-Lot Check

        When the parsed transaction references an instrument (instrument key not null), look up an open lot that matches the user’s default lot-selection method (FIFO/LIFO/specific-id).

        If no suitable lot exists → prompt:

        No tax lot on record for BTC purchased on 2025-06-19 @ $1800/BTC (quantity 0.5).
        ➜ Create new tax lot? [Y/n]

    Lot Creation Workflow

        On Y/Enter:

            Assign a unique lot_id.

            Store {instrument, acquisition_date, quantity, cost_basis_per_unit, total_cost}.

        On n: allow user to specify an existing lot_id manually or cancel.

    Sale / Closing Lots

        When selling, system must:

            Identify lot(s) to close.

            Calculate realized gain/loss (credit or debit Income:CapitalGains / Expenses:CapitalLosses).

            Record remaining quantity for partial lot closures.

4️⃣ Double-Entry Ledger Engine

    Post journal entries only after both account and lot confirmations succeed.

    Validate ∑ debits = ∑ credits per transaction.

5️⃣ Multi-Currency & Commodity Handling

    Store original currency & quantity; translate to base currency for reports via stored or user-provided FX rates.

6️⃣ CLI Interaction Flow (Illustrative)

$ ledger add "Bought 0.5 BTC for $18,000"
> Parsed:
  Debit Assets:Crypto:BTC (Qty 0.5)           $18,000
  Credit Assets:Cash                          $18,000
  Date: 2025-06-19

Account 'Assets:Crypto:BTC' does not exist. Create? [Y/n] Y
No tax lot on record for BTC acquired 2025-06-19 (0.5 @ $18,000). Create tax lot? [Y/n] Y
Lot ID BTC-20250619-001 created.
Transaction saved.

7️⃣ Reports & Extras (Optional)

    Balance Sheet, Income Statement, Tax-Lot Register, Realized & Unrealized Gains, XIRR, TWRR.

    CSV/API importers, encrypted storage, vendor auto-categorization, CLI auto-complete.

Deliverables

    CLI app

    LLM prompt schema & caching layer

    Persistent ledger & tax-lot store

    Unit tests for: parsing, account creation workflow, lot creation & gain/loss math, double-entry balancing
