import importlib.util
import unittest
from datetime import date
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "installment_cost.py"
SPEC = importlib.util.spec_from_file_location("installment_cost", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class InstallmentCostTests(unittest.TestCase):
    def test_book_example_periodic_irr_and_simple_approximation(self):
        rate = MODULE.periodic_irr([12000.0] + [-1079.2] * 12)
        self.assertAlmostEqual(rate, 0.0119255130618, places=11)
        self.assertAlmostEqual((1 + rate) ** 12 - 1, 0.1528758657823, places=11)
        self.assertAlmostEqual(
            MODULE.book_simple_average_balance_rate(12, 0.0066),
            0.1462153846154,
            places=11,
        )

    def test_pbc_fee_example_matches_effective_irr(self):
        rate = MODULE.periodic_irr([99000.0] + [-8833.3] * 12)
        self.assertAlmostEqual((1 + rate) ** 12 - 1, 0.1358255763, places=9)

    def test_xirr_one_year(self):
        rate = MODULE.xirr(
            [(date(2026, 1, 1), 1000.0), (date(2027, 1, 1), -1100.0)]
        )
        self.assertAlmostEqual(rate, 0.10, places=10)

    def test_requires_all_costs_assertion(self):
        with self.assertRaises(MODULE.CalculationError):
            MODULE.calculate(
                {
                    "perspective": "borrower",
                    "all_direct_loan_costs_included": False,
                    "cashflows": [
                        {"date": "2026-01-01", "amount": 1000},
                        {"date": "2027-01-01", "amount": -1100},
                    ],
                }
            )

    def test_rejects_multiple_sign_changes(self):
        with self.assertRaises(MODULE.CalculationError):
            MODULE.periodic_irr([1000.0, -1200.0, 300.0])

    def test_regular_flag_rejects_irregular_dates(self):
        with self.assertRaises(MODULE.CalculationError):
            MODULE.calculate(
                {
                    "perspective": "borrower",
                    "all_direct_loan_costs_included": True,
                    "regular_periodic": True,
                    "periods_per_year": 12,
                    "cashflows": [
                        {"date": "2026-01-01", "amount": 1000},
                        {"date": "2026-02-01", "amount": -500},
                        {"date": "2026-05-01", "amount": -600},
                    ],
                }
            )

    def test_same_day_fee_is_netted_for_xirr(self):
        rate = MODULE.xirr(
            [
                (date(2026, 1, 1), 100000.0),
                (date(2026, 1, 1), -1000.0),
                (date(2027, 1, 1), -108900.0),
            ]
        )
        self.assertAlmostEqual(rate, 0.10, places=10)


if __name__ == "__main__":
    unittest.main()
