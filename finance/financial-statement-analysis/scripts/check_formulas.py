#!/usr/bin/env python3
"""Deterministic formula and edge-case assertions for the skill references."""

from decimal import Decimal, getcontext
import json

getcontext().prec = 28
D = Decimal
TOL = D("0.000000000001")


def mean(opening: str | Decimal, closing: str | Decimal) -> Decimal:
    return (D(opening) + D(closing)) / D(2)


def ratio(numerator: str | Decimal, denominator: str | Decimal, *, positive=False, epsilon=D("0.000001")):
    n, d = D(numerator), D(denominator)
    if abs(d) <= epsilon or (positive and d <= 0):
        return None
    return n / d


def ordinary_growth(current: str | Decimal, base: str | Decimal, epsilon=D("0.000001")):
    """Return None when the base cannot support ordinary growth interpretation."""
    current_value, base_value = D(current), D(base)
    if base_value <= epsilon:
        return None
    return (current_value - base_value) / base_value


checks: list[dict[str, object]] = []


def assert_equal(check_id: str, observed, expected) -> None:
    passed = observed is None and expected is None
    if observed is not None and expected is not None:
        passed = abs(D(observed) - D(expected)) <= TOL
    checks.append({"check_id": check_id, "passed": passed, "observed": None if observed is None else str(observed), "expected": None if expected is None else str(expected)})


assets, liabilities, equity = D("100"), D("70"), D("30")
assert_equal("balance-sheet-identity", assets - liabilities - equity, D("0"))

avg_assets, avg_equity = mean("180", "220"), mean("80", "120")
profit, revenue = D("20"), D("200")
roe = ratio(profit, avg_equity, positive=True)
net_margin = ratio(profit, revenue)
asset_turnover = ratio(revenue, avg_assets, positive=True)
equity_multiplier = ratio(avg_assets, avg_equity, positive=True)
assert_equal("average-assets", avg_assets, D("200"))
assert_equal("average-equity", avg_equity, D("100"))
assert_equal("roe", roe, D("0.2"))
assert_equal("dupont-closure", net_margin * asset_turnover * equity_multiplier, roe)

assert_equal("gross-margin", ratio(D("200") - D("120"), "200"), D("0.4"))
assert_equal("cash-collection-not-ocf", ratio("220", "200"), D("1.1"))
assert_equal("profit-cash", ratio("24", "20"), D("1.2"))
assert_equal("profit-cash-zero", ratio("24", "0"), None)
assert_equal("profit-cash-negative-is-nm", ratio("24", "-2", positive=True), None)
assert_equal("profit-cash-near-zero", ratio("24", "0.0000001"), None)
assert_equal("recurring-profit", ratio("18", "20"), D("0.9"))

avg_inventory = mean("30", "50")
opening_receivables = D("10") + D("5") + D("5")
closing_receivables = D("20") + D("5") + D("5")
avg_receivables = mean(opening_receivables, closing_receivables)
inventory_turnover = ratio("120", avg_inventory, positive=True)
receivables_turnover = ratio("200", avg_receivables, positive=True)
assert_equal("inventory-turnover", inventory_turnover, D("3"))
assert_equal("receivables-complete-scope", receivables_turnover, D("8"))
assert_equal("turnover-days", ratio("365", receivables_turnover, positive=True), D("45.625"))

interest_debt = D("40") + D("30") + D("20") + D("10")
available_cash = D("120") - D("90")
assert_equal("interest-debt-ratio", ratio(interest_debt, "500", positive=True), D("0.2"))
assert_equal("cash-cover-net-restrictions", ratio(available_cash, interest_debt, positive=True), D("0.3"))
assert_equal("zero-interest-debt", ratio("30", "0", positive=True), None)
assert_equal("negative-equity", ratio("20", "-10", positive=True), None)

operating_cash, total_cash_capex = D("120"), D("100")
assert_equal("before-capex-cash-reference", operating_cash, D("120"))
assert_equal("after-all-capex-conservative-proxy", operating_cash - total_cash_capex, D("20"))
assert_equal("ebit-interest-cover", ratio("30", "10", positive=True), D("3"))
assert_equal("cash-interest-cover-auxiliary", ratio("40", "8", positive=True), D("5"))
assert_equal("negative-base-growth-is-nm", ordinary_growth("-50", "-100"), None)

result = {"check_count": len(checks), "passed_count": sum(1 for c in checks if c["passed"]), "failed_count": sum(1 for c in checks if not c["passed"]), "checks": checks}
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(0 if result["failed_count"] == 0 else 1)
