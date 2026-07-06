from __future__ import annotations

from typing import Any


def pct_change(current: float, previous: float) -> float | None:
    if previous == 0:
        return None
    return (current - previous) / abs(previous) * 100


def validate_pct_change(current: float, previous: float, reported: str | float, tolerance: float = 0.05) -> dict[str, Any]:
    calculated = pct_change(current, previous)
    if calculated is None:
        return {"check": "pct_change", "status": "skip", "reason": "previous_zero"}
    if isinstance(reported, str):
        reported_value = float(reported.replace("%", "").replace("％", ""))
    else:
        reported_value = float(reported)
    ok = abs(calculated - reported_value) <= tolerance
    return {"check": "pct_change", "status": "pass" if ok else "fail", "calculated": calculated, "reported": reported_value}


def validate_balance_sheet(assets: float, liabilities: float, equity: float, tolerance: float = 1.0) -> dict[str, Any]:
    diff = assets - liabilities - equity
    return {"check": "assets_equal_liabilities_plus_equity", "status": "pass" if abs(diff) <= tolerance else "fail", "diff": diff}


def detect_quarter_anomaly(values: list[float], threshold_ratio: float = 0.5) -> dict[str, Any]:
    if len(values) != 4:
        return {"check": "quarter_anomaly", "status": "skip", "reason": "need_four_quarters"}
    total_abs = sum(abs(v) for v in values) or 1.0
    flags = [i + 1 for i, v in enumerate(values) if abs(v) / total_abs > threshold_ratio]
    return {"check": "quarter_anomaly", "status": "warn" if flags else "pass", "quarters": flags}
