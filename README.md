# Python & Data Projects

A collection of runnable programming exercises exploring backend logic, relational databases, testing, and data-driven decisions. Each project has its own setup instructions and tests.

| Project | What it demonstrates |
| --- | --- |
| [Location Score Engine](projects/location-score-engine/) | Weighted scoring, CSV validation, feature normalization, interpretable ranking, unit tests |
| [SQLite Expense Tracker](projects/sqlite-expense-tracker/) | Relational data modeling, parameterized SQL, money-safe integer storage, CLI design, unit tests |

## Try the projects

Both examples use Python 3.10+ and **only the standard library**.

```bash
cd projects/location-score-engine
python location_score.py
python -m unittest discover -p 'test_*.py'

cd ../sqlite-expense-tracker
python expense_tracker.py --help
python -m unittest discover -p 'test_*.py'
```

These are educational sample projects and are distinct from my ongoing Business Location Analyzer research application.

See my [portfolio](https://github.com/aashish-siingh/myportfolio) for other projects.
