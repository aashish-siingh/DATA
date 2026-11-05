"""Local SQLite expense tracker CLI; Python standard library only."""
from __future__ import annotations

import argparse
import sqlite3
from datetime import date
from pathlib import Path


def connect(db_path: str | Path) -> sqlite3.Connection:
    connection = sqlite3.connect(str(db_path))
    connection.row_factory = sqlite3.Row
    connection.execute(
        """CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            spent_on TEXT NOT NULL,
            category TEXT NOT NULL,
            amount_cents INTEGER NOT NULL CHECK(amount_cents > 0),
            note TEXT NOT NULL DEFAULT ''
        )"""
    )
    connection.commit()
    return connection


def add_expense(connection: sqlite3.Connection, spent_on: str, category: str,
                amount: str, note: str = "") -> int:
    from decimal import Decimal, InvalidOperation
    try:
        date.fromisoformat(spent_on)
        dollars = Decimal(amount)
        cents = dollars * 100
        if not dollars.is_finite() or dollars <= 0 or cents != cents.to_integral_value():
            raise ValueError("Amount must be positive with at most two decimals")
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("Use YYYY-MM-DD and a positive dollar amount (up to two decimals)") from exc
    if not category.strip():
        raise ValueError("Category cannot be empty")
    cursor = connection.execute(
        "INSERT INTO expenses (spent_on,category,amount_cents,note) VALUES (?,?,?,?)",
        (spent_on, category.strip(), int(cents), note.strip()),
    )
    connection.commit()
    return int(cursor.lastrowid)


def monthly_report(connection: sqlite3.Connection, month: str) -> list[tuple[str, int]]:
    if len(month) != 7 or month[4] != "-":
        raise ValueError("Month must be YYYY-MM")
    try:
        date.fromisoformat(month + "-01")
    except ValueError as exc:
        raise ValueError("Month must be YYYY-MM") from exc
    return [
        (row["category"], row["total"])
        for row in connection.execute(
            """SELECT category, SUM(amount_cents) AS total
               FROM expenses WHERE substr(spent_on,1,7) = ?
               GROUP BY category ORDER BY total DESC, category""",
            (month,),
        )
    ]


def money(cents: int) -> str:
    return f"${cents / 100:,.2f}"


def main() -> None:
    parser = argparse.ArgumentParser(description="SQLite expense tracker")
    parser.add_argument("--db", default="expenses.db", help="SQLite file path")
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="Add an expense")
    add.add_argument("date", help="YYYY-MM-DD")
    add.add_argument("category")
    add.add_argument("amount", help="Dollars, e.g. 12.45")
    add.add_argument("--note", default="")
    report = commands.add_parser("report", help="Summarize a month")
    report.add_argument("month", help="YYYY-MM")
    args = parser.parse_args()
    with connect(args.db) as connection:
        try:
            if args.command == "add":
                item_id = add_expense(connection, args.date, args.category, args.amount, args.note)
                print(f"Saved expense #{item_id}")
            elif args.command == "report":
                rows = monthly_report(connection, args.month)
                for category, cents in rows:
                    print(f"{category}: {money(cents)}")
                print(f"TOTAL: {money(sum(cents for _, cents in rows))}")
        except ValueError as exc:
            parser.error(str(exc))


if __name__ == "__main__":
    main()
