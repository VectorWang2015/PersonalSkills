#!/usr/bin/env python3
"""Calculate borrower-side installment loan annualized cost from cash flows.

Sign convention: money received by the borrower is positive; money paid by the
borrower is negative. Cash flows on the same date are aggregated before solving.
The primary dated result uses an actual/365 XIRR-style effective annual rate.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Callable, Iterable


class CalculationError(ValueError):
    """Raised when the input cannot support a unique, reliable calculation."""


def _finite_number(value: object, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CalculationError(f"{field} must be a number")
    number = float(value)
    if not math.isfinite(number):
        raise CalculationError(f"{field} must be finite")
    return number


def _solve_root(function: Callable[[float], float]) -> float:
    low = -0.999999999
    high = 1.0
    f_low = function(low)
    f_high = function(high)
    if abs(f_low) < 1e-14:
        return low
    if abs(f_high) < 1e-14:
        return high
    while f_low * f_high > 0 and high < 1_000_000:
        high = high * 2 + 1
        f_high = function(high)
    if f_low * f_high > 0:
        raise CalculationError("unable to bracket a unique rate")
    for _ in range(250):
        midpoint = (low + high) / 2
        f_mid = function(midpoint)
        if abs(f_mid) < 1e-13:
            return midpoint
        if f_low * f_mid <= 0:
            high = midpoint
            f_high = f_mid
        else:
            low = midpoint
            f_low = f_mid
    return (low + high) / 2


def _require_conventional_borrower_cashflows(amounts: Iterable[float]) -> list[float]:
    values = [value for value in amounts if abs(value) > 1e-12]
    if len(values) < 2 or values[0] <= 0 or not any(value < 0 for value in values[1:]):
        raise CalculationError(
            "cash flows must begin with a positive net disbursement and include later payments"
        )
    signs = [1 if value > 0 else -1 for value in values]
    changes = sum(left != right for left, right in zip(signs, signs[1:]))
    if changes != 1:
        raise CalculationError(
            "non-conventional cash flows can have multiple or no IRR roots; provide a specialist model"
        )
    return values


def periodic_irr(cashflows: Iterable[float]) -> float:
    values = _require_conventional_borrower_cashflows(cashflows)

    def npv(rate: float) -> float:
        return sum(value / ((1 + rate) ** period) for period, value in enumerate(values))

    return _solve_root(npv)


def xirr(cashflows: Iterable[tuple[date, float]], day_count_basis: float = 365.0) -> float:
    if day_count_basis <= 0:
        raise CalculationError("day_count_basis must be positive")
    aggregated: dict[date, float] = defaultdict(float)
    for flow_date, amount in cashflows:
        aggregated[flow_date] += amount
    ordered = sorted(aggregated.items())
    values = _require_conventional_borrower_cashflows(amount for _, amount in ordered)
    ordered = [(flow_date, amount) for flow_date, amount in ordered if abs(amount) > 1e-12]
    start = ordered[0][0]

    def npv(rate: float) -> float:
        total = 0.0
        for flow_date, amount in ordered:
            years = (flow_date - start).days / day_count_basis
            total += amount / ((1 + rate) ** years)
        return total

    result = _solve_root(npv)
    if len(values) != len(ordered):
        raise AssertionError("internal cash-flow normalization mismatch")
    return result


def book_simple_average_balance_rate(periods: int, fee_rate_per_period: float) -> float:
    if isinstance(periods, bool) or not isinstance(periods, int) or periods <= 0:
        raise CalculationError("book_approximation.periods must be a positive integer")
    fee_rate = _finite_number(
        fee_rate_per_period, "book_approximation.fee_rate_per_period"
    )
    if fee_rate < 0:
        raise CalculationError("book fee rate cannot be negative")
    return 24 * periods * fee_rate / (periods + 1)


def _validate_regular_dates(dates: list[date], periods_per_year: int) -> None:
    if len(dates) < 2:
        raise CalculationError("regular cash flows need at least two distinct dates")
    expected_days = 365.0 / periods_per_year
    tolerance_days = max(2.0, min(10.0, expected_days * 0.15))
    intervals = [(right - left).days for left, right in zip(dates, dates[1:])]
    if any(interval <= 0 for interval in intervals):
        raise CalculationError("regular cash-flow dates must be strictly increasing")
    if any(abs(interval - expected_days) > tolerance_days for interval in intervals):
        raise CalculationError(
            "cash-flow dates are not regular enough for periodic IRR; use the XIRR result"
        )


def calculate(payload: dict[str, object]) -> dict[str, object]:
    if payload.get("perspective") != "borrower":
        raise CalculationError("perspective must be 'borrower'")
    if payload.get("all_direct_loan_costs_included") is not True:
        raise CalculationError(
            "all_direct_loan_costs_included must be true before presenting an all-in annualized rate"
        )
    raw_flows = payload.get("cashflows")
    if not isinstance(raw_flows, list) or len(raw_flows) < 2:
        raise CalculationError("cashflows must contain at least two dated entries")

    dated_flows: list[tuple[date, float]] = []
    for index, item in enumerate(raw_flows):
        if not isinstance(item, dict):
            raise CalculationError(f"cashflows[{index}] must be an object")
        raw_date = item.get("date")
        if not isinstance(raw_date, str):
            raise CalculationError(f"cashflows[{index}].date must be YYYY-MM-DD")
        try:
            flow_date = date.fromisoformat(raw_date)
        except ValueError as exc:
            raise CalculationError(f"cashflows[{index}].date must be YYYY-MM-DD") from exc
        amount = _finite_number(item.get("amount"), f"cashflows[{index}].amount")
        dated_flows.append((flow_date, amount))

    basis = _finite_number(payload.get("day_count_basis", 365.0), "day_count_basis")
    xirr_rate = xirr(dated_flows, basis)
    result: dict[str, object] = {
        "status": "calculated",
        "perspective": "borrower",
        "sign_convention": "positive=borrower receipt; negative=borrower payment",
        "day_count_basis": basis,
        "xirr_effective_annual_rate": xirr_rate,
        "xirr_effective_annual_percent": xirr_rate * 100,
        "warnings": [
            "The result is conditional on the assertion that every directly related loan cost is included."
        ],
    }

    regular = payload.get("regular_periodic") is True
    periods_per_year_raw = payload.get("periods_per_year")
    if regular:
        if isinstance(periods_per_year_raw, bool) or not isinstance(periods_per_year_raw, int):
            raise CalculationError("periods_per_year must be a positive integer for regular cash flows")
        periods_per_year = periods_per_year_raw
        if periods_per_year <= 0:
            raise CalculationError("periods_per_year must be positive")
        aggregated: dict[date, float] = defaultdict(float)
        for flow_date, amount in dated_flows:
            aggregated[flow_date] += amount
        ordered_periodic = [
            (flow_date, amount)
            for flow_date, amount in sorted(aggregated.items())
            if abs(amount) > 1e-12
        ]
        _validate_regular_dates([flow_date for flow_date, _ in ordered_periodic], periods_per_year)
        amounts = [amount for _, amount in ordered_periodic]
        periodic_rate = periodic_irr(amounts)
        result.update(
            {
                "periodic_irr": periodic_rate,
                "periods_per_year": periods_per_year,
                "periodic_irr_nominal_annual_rate": periodic_rate * periods_per_year,
                "periodic_irr_nominal_annual_percent": periodic_rate * periods_per_year * 100,
                "periodic_irr_effective_annual_rate": (1 + periodic_rate) ** periods_per_year - 1,
                "periodic_irr_effective_annual_percent": (
                    (1 + periodic_rate) ** periods_per_year - 1
                )
                * 100,
            }
        )

    approximation = payload.get("book_approximation")
    if approximation is not None:
        if not isinstance(approximation, dict):
            raise CalculationError("book_approximation must be an object")
        periods = approximation.get("periods")
        fee_rate = approximation.get("fee_rate_per_period")
        simple_rate = book_simple_average_balance_rate(periods, fee_rate)  # type: ignore[arg-type]
        result.update(
            {
                "book_simple_average_balance_annual_rate": simple_rate,
                "book_simple_average_balance_annual_percent": simple_rate * 100,
                "book_approximation_assumptions": [
                    "monthly periods",
                    "equal principal repayment",
                    "the same fee rate is charged each period on original principal",
                    "no upfront or additional loan-related fees",
                    "the result is a simple annualized approximation, not the primary IRR/XIRR result",
                ],
            }
        )
    return result


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Calculate borrower-side installment annualized cost from dated cash flows."
    )
    parser.add_argument(
        "--input",
        default="-",
        help="JSON input path, or '-' for stdin (default)",
    )
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON output")
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        if args.input == "-":
            payload = json.load(sys.stdin)
        else:
            payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise CalculationError("top-level input must be a JSON object")
        output = calculate(payload)
    except (CalculationError, json.JSONDecodeError, OSError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(output, ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
