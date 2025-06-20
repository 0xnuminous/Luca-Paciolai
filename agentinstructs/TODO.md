# TODO.md – Implementation Roadmap

The following tasks outline how to complete the missing features documented in `specchange.md` so the application conforms to `SPEC.md`.

1. **Account Context**
   - Implement a function to list all account names from the database.
   - Pass this list to `llm.parse_transaction` when parsing a transaction.

2. **Dynamic Chart of Accounts**
   - Define an `Account` model and CRUD helpers.
   - When a parsed account doesn't exist, prompt the user to confirm creation and save it.

3. **Balance Enforcement**
   - Add validation ensuring every transaction's debit amount equals its credit amount before saving.

4. **Tax Lot Tracking**
   - Create helpers to add lots on acquisitions and select lots on sales.
   - Store cost basis and adjust quantities as lots are consumed.

5. **Multi-Currency Support**
   - Record exchange rates and original currencies in the `Transaction` model.
   - Provide a utility to convert amounts to a base currency for reports.

6. **Reporting Commands**
   - Implement CLI commands for Balance Sheet, Income Statement, Tax-Lot Registry, and Gains reports.

7. **Tests and Linting**
   - Add comprehensive unit tests for the new modules and update `ruff` and `mypy` configurations as needed.

These steps should be tackled incrementally, committing code after each major component is functional and covered by tests.
