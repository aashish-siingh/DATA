import tempfile
import unittest
from pathlib import Path

from location_score import (
    DEFAULT_WEIGHTS, Location, load_locations, score_locations, validate_weights
)


class LocationScoreTests(unittest.TestCase):
    def test_weight_validation(self):
        validate_weights(DEFAULT_WEIGHTS)
        with self.assertRaises(ValueError):
            validate_weights({**DEFAULT_WEIGHTS, "rent": 0.5})

    def test_lower_costs_are_rewarded(self):
        a = Location("Low cost", 100, 100, 100, 1, 100)
        b = Location("High cost", 100, 100, 100, 10, 1000)
        ranked = score_locations([b, a])
        self.assertEqual(ranked[0]["name"], "Low cost")

    def test_equal_metrics_do_not_divide_by_zero(self):
        a = Location("A", 100, 100, 100, 1, 100)
        self.assertAlmostEqual(score_locations([a])[0]["score"], 50.0)

    def test_invalid_csv_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.csv"
            path.write_text("name,population,income,foot_traffic,competition,rent\nA,-1,20,30,1,50\n")
            with self.assertRaises(ValueError):
                load_locations(path)


if __name__ == "__main__":
    unittest.main()
