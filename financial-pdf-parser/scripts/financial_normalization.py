from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from typing import Any


NULL_TOKENS = {"", "-", "--", "—", "不适用", "无", "nan", "None", "null"}
UNIT_PATTERNS = ["万元", "亿元", "元/股", "元／股", "元", "%", "股", "人"]


def normalize_number(value: Any) -> Any:
    if value is None:
        return None
    text = str(value).strip().replace("，", ",")
    text = re.sub(r"\s+", "", text)
    if text in NULL_TOKENS:
        return None
    text = text.replace("（", "(").replace("）", ")")
    negative = False
    if text.startswith("(") and text.endswith(")"):
        negative = True
        text = text[1:-1]
    if text.startswith("-") or text.startswith("－"):
        negative = True
        text = text[1:]
    is_percent = text.endswith("%") or text.endswith("％")
    if is_percent:
        text = text[:-1]
    text = text.replace(",", "")
    if not re.fullmatch(r"\d+(\.\d+)?", text):
        return value
    try:
        number = Decimal(text)
    except InvalidOperation:
        return value
    if negative:
        number = -number
    if is_percent:
        return f"{number}%"
    return float(number) if "." in text else int(number)


def repair_wrapped_amount(text: str) -> str:
    return re.sub(r"(?<=\d)[\n\s]+(?=\d{3}(?:,|\.|$))", "", text)


def detect_unit(text: str) -> str | None:
    compact = re.sub(r"\s+", "", text)
    for unit in UNIT_PATTERNS:
        if unit in compact:
            return unit.replace("／", "/")
    return None


def reconstruct_headers(rows: list[list[Any]]) -> list[str]:
    if not rows:
        return []
    first = [str(c or "").strip() for c in rows[0]]
    if len(rows) < 2:
        return first
    second = [str(c or "").strip() for c in rows[1]]
    if not any(h in {"调整前", "调整后"} for h in second):
        return first
    headers: list[str] = []
    last_parent = ""
    for parent, child in zip(first, second):
        if parent:
            last_parent = parent
        if child in {"调整前", "调整后"} and last_parent:
            headers.append(f"{last_parent}{child}")
        else:
            headers.append(parent or child)
    return headers


def markdown_table(rows: list[list[Any]]) -> str:
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    padded = [[str(c or "") for c in r] + [""] * (width - len(r)) for r in rows]
    header = padded[0]
    out = ["| " + " | ".join(header) + " |", "| " + " | ".join(["---"] * width) + " |"]
    for row in padded[1:]:
        out.append("| " + " | ".join(row) + " |")
    return "\n".join(out)
