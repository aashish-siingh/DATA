"""Explainable, dependency-free location scoring demo.

Input is illustrative data, not real market measurements.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

CRITERIA = ("population", "income", "foot_traffic", "competition", "rent")
DEFAULT_WEIGHTS = {
    "population": 0.25,
    "income": 0.20,
    "foot_traffic": 0.25,
    "competition": 0.15,
    "rent": 0.15,
}
LOWER_IS_BETTER = {"competition", "rent"}


@dataclass(frozen=True)
class Location:
    name: str
    population: float
    income: float
    foot_traffic: float
    competition: float
    rent: float


def validate_weights(weights: dict[str, float]) -> None:
    if set(weights) != set(CRITERIA):
        raise ValueError(f"Weights must contain exactly: {', '.join(CRITERIA)}")
    if any(not 0 <= weight <= 1 for weight in weights.values()):
        raise ValueError("Each weight must be between 0 and 1")
    if abs(sum(weights.values()) - 1.0) > 1e-9:
        raise ValueError("Weights must add up to 1.0")


def load_locations(path: str | Path) -> list[Location]:
    with open(path, encoding="utf-8", newline="") as file:
        records = list(csv.DictReader(file))
    if not records:
        raise ValueError("CSV has no location records")
    locations = []
    for row in records:
        try:
            values = {key: float(row[key]) for key in CRITERIA}
            name = row["name"].strip()
            if not name or any(value < 0 for value in values.values()):
                raise ValueError("Name required; metrics must be nonnegative")
            locations.append(Location(name=name, **values))
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Invalid CSV record: {row}") from exc
    if len({loc.name for loc in locations}) != len(locations):
        raise ValueError("Location names must be unique")
    return locations


def score_locations(
    locations: list[Location], weights: dict[str, float] | None = None
) -> list[dict]:
    """Min-max normalize each metric, invert costs, and sum weighted scores."""
    if not locations:
        raise ValueError("At least one location is required")
    weights = DEFAULT_WEIGHTS.copy() if weights is None else weights.copy()
    validate_weights(weights)
    bounds = {
        key: (min(getattr(loc, key) for loc in locations),
              max(getattr(loc, key) for loc in locations))
        for key in CRITERIA
    }
    results = []
    for loc in locations:
        contributions = {}
        for key in CRITERIA:
            low, high = bounds[key]
            normalized = 0.5 if high == low else (getattr(loc, key) - low) / (high - low)
            if key in LOWER_IS_BETTER:
                normalized = 1 - normalized
            contributions[key] = round(normalized * weights[key] * 100, 4)
        results.append({
            "name": loc.name,
            "score": round(sum(contributions.values()), 2),
            "contributions": contributions,
        })
    return sorted(results, key=lambda item: (-item["score"], item["name"]))


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Rank illustrative site alternatives")
    parser.add_argument("csv_file", nargs="?", default=str(Path(__file__).with_name("sample_locations.csv")))
    args = parser.parse_args()
    for rank, result in enumerate(score_locations(load_locations(args.csv_file)), start=1):
        factors = ", ".join(f"{key}={value:.1f}" for key, value in result["contributions"].items())
        print(f"{rank}. {result['name']}: {result['score']:.2f}/100 | {factors}")


if __name__ == "__main__":
    main()
