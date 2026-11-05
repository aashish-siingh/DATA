# SQLite Expense Tracker

A lightweight command-line expense tracker demonstrating a persistent relational database, parameterized SQL, input validation, financial aggregation, and tests.

## Quick start

Python 3.10+; no installations needed.

```bash
cd projects/sqlite-expense-tracker
python expense_tracker.py add 2026-11-01 Food 12.50 --note "Lunch"
python expense_tracker.py add 2026-11-02 Transit 4.00
python expense_tracker.py report 2026-11
python -m unittest discover -p "test_*.py"
```

Use `--db another-file.db` before the command to choose a database location. The app creates `expenses.db` locally and does not upload your data.

## Engineering choices

- Integer cents instead of floating-point monetary storage
- SQLite schema with a database-level positive-amount constraint
- Prepared/parameterized statements (no string interpolation in SQL)
- Group-by monthly reporting
- Unit tests using an in-memory database

## Extensions

CSV export, editable records, recurring expenses, REST API, and CI checks.

**Scope:** Educational command-line demo, not a personal-finance service.
