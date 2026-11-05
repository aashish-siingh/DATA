import sqlite3
import unittest

from expense_tracker import add_expense, connect, monthly_report


class ExpenseTrackerTests(unittest.TestCase):
    def setUp(self):
        self.db = connect(":memory:")

    def tearDown(self):
        self.db.close()

    def test_monthly_grouping(self):
        add_expense(self.db, "2026-11-01", "Food", "10.20")
        add_expense(self.db, "2026-11-02", "Food", "2.30")
        add_expense(self.db, "2026-10-31", "Food", "99.00")
        self.assertEqual(monthly_report(self.db, "2026-11"), [("Food", 1250)])

    def test_invalid_amount(self):
        for amount in ("-1", "0", "1.234", "abc"):
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    add_expense(self.db, "2026-11-01", "Food", amount)

    def test_sql_injection_is_data(self):
        add_expense(self.db, "2026-11-01", "'); DROP TABLE expenses;--", "4.00")
        self.assertEqual(len(monthly_report(self.db, "2026-11")), 1)


if __name__ == "__main__":
    unittest.main()
