# Location Score Engine

A small, explainable Python decision-support prototype that ranks candidate business locations using a **weighted, normalized score**. This is an independent programming exercise inspired by business-location analysis, **not** a validated commercial recommendation system.

## Run

Requires Python 3.10+; no third-party packages.

```bash
cd projects/location-score-engine
python location_score.py
python -m unittest discover -p "test_*.py"
```

To score your own data: `python location_score.py your_locations.csv`.

## How the algorithm works

1. Read and validate CSV records.
2. Normalize each numeric feature using min-max scaling across the comparison set.
3. Invert rent and competitor-count metrics because lower values are preferred.
4. Multiply each normalized feature by a weight, then sum to a score out of 100.
5. Print a ranked list and a criterion-by-criterion explanation.

Weights: population 25%, income 20%, foot traffic 25%, competition 15%, rent 15%.

## Important limitations

All sample records are **synthetic**. The measures are not independently validated, normalization is relative to the compared locations, and rank is sensitive to choice of candidates and weights. A real implementation would require trusted geographic data, a defined catchment radius, missing-data handling, sensitivity analysis, and out-of-sample validation.

## Skills demonstrated

Python, dataclasses, CSV input, validation, algorithm design, unit testing, explainability.
