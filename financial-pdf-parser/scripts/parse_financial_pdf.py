from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

import pymupdf

from financial_normalization import detect_unit, markdown_table, normalize_number, repair_wrapped_amount, reconstruct_headers
from financial_validation import detect_quarter_anomaly, validate_balance_sheet, validate_pct_change


KEYWORDS = ["营业收入", "归母净利润", "扣非净利润", "经营现金流", "ROE", "每股收益", "资产负债表", "利润表", "现金流量表"]
TITLE_PATTERNS = ["主要会计数据和财务指标", "分季度主要财务指标", "非经常性损益项目及金额", "非经常性损益项目和金额", "合并资产负债表", "母公司资产负债表", "合并利润表", "母公司利润表", "合并现金流量表", "母公司现金流量表"]
STATEMENT_TITLES = {"合并资产负债表", "母公司资产负债表", "合并利润表", "母公司利润表", "合并现金流量表", "母公司现金流量表"}
CONTINUATION_TITLES = STATEMENT_TITLES | {"非经常性损益项目及金额", "非经常性损益项目和金额"}


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_csv(path: Path, rows: list[list[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        csv.writer(f).writerows(rows)


def report_period_from_source(source_name: str) -> str:
    if re.search(r"Q[1-4]|一季报|三季报|季度报告", source_name, re.IGNORECASE):
        return "quarterly"
    if re.search(r"半年报|中报|半年度", source_name):
        return "interim"
    return "annual"


def min_core_checks_for_report(period: str) -> int:
    if period == "quarterly":
        return 1
    if period == "interim":
        return 2
    return 4


def clean_cell(value: Any) -> Any:
    if value is None:
        return None
    text = repair_wrapped_amount(str(value)).replace("\n", " ").strip()
    return normalize_number(text)


def page_section(text: str) -> str | None:
    match = re.search(r"第[一二三四五六七八九十]+节[^\n]{0,40}|[一二三四五六七八九十]+、[^\n]{2,40}", text)
    return match.group(0) if match else None


def normalize_table_section(title: str | None, section: str | None) -> str | None:
    if title in STATEMENT_TITLES:
        return "二、财务报表"
    return section


def title_near_page(text: str) -> str | None:
    for pattern in TITLE_PATTERNS:
        if pattern in text:
            return pattern
    return None


def page_text_lines(page: Any) -> list[dict[str, Any]]:
    lines: list[dict[str, Any]] = []
    for block in page.get_text("dict").get("blocks", []):
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            text = "".join(span.get("text", "") for span in line.get("spans", [])).strip()
            if text:
                lines.append({"text": text, "bbox": list(line.get("bbox", [0, 0, 0, 0]))})
    return lines


def assign_title_by_bbox(table_bbox: list[float], text_lines: list[dict[str, Any]]) -> str | None:
    x0, y0, x1, _ = table_bbox
    candidates: list[tuple[float, str]] = []
    for line in text_lines:
        text = line["text"].replace(" ", "")
        lx0, ly0, lx1, ly1 = line["bbox"]
        if ly1 > y0 or ly1 < y0 - 180:
            continue
        if lx1 < x0 - 80 or lx0 > x1 + 80:
            continue
        for title in TITLE_PATTERNS:
            if title.replace(" ", "") in text:
                candidates.append((y0 - ly1, title))
    if candidates:
        return sorted(candidates, key=lambda item: item[0])[0][1]
    return None


def infer_table_unit(table_bbox: list[float], text_lines: list[dict[str, Any]], rows: list[list[Any]] | None = None) -> str | None:
    x0, y0, x1, _ = table_bbox
    row_text = json.dumps(rows or [], ensure_ascii=False)
    if any(word in row_text for word in ["资产", "负债", "收入", "现金", "利润", "成本", "费用", "利息"]):
        return "元"
    nearby = []
    for line in text_lines:
        lx0, ly0, lx1, ly1 = line["bbox"]
        if ly1 <= y0 and ly1 >= y0 - 160 and not (lx1 < x0 - 80 or lx0 > x1 + 80):
            nearby.append(line["text"])
    unit = detect_unit("\n".join(nearby))
    if unit:
        return unit
    return detect_unit(row_text)


def confidence_proxy(rows: list[list[Any]], columns: list[str], bbox: list[float]) -> float:
    if not rows or not columns or not bbox:
        return 0.0
    score = 0.45
    row_lengths = [len(row) for row in rows if row]
    if row_lengths:
        expected = max(set(row_lengths), key=row_lengths.count)
        consistent = sum(1 for length in row_lengths if length == expected) / len(row_lengths)
        score += 0.25 * consistent
    numeric_cells = sum(1 for row in rows for cell in row if isinstance(cell, (int, float)))
    total_cells = sum(len(row) for row in rows) or 1
    if numeric_cells:
        score += 0.2 * min(numeric_cells / total_cells * 2, 1)
    x0, y0, x1, y1 = bbox
    if x1 > x0 and y1 > y0:
        score += 0.1
    return round(min(score, 1.0), 2)


def table_has_continuation_header(table: dict[str, Any]) -> bool:
    first_col = str((table.get("columns") or [""])[0]).replace(" ", "")
    return "非经常性损益项目" in first_col


def is_continued_table(previous: dict[str, Any], current: dict[str, Any]) -> bool:
    if current.get("page_start") != previous.get("page_end", previous.get("page_start")) + 1:
        return False
    previous_title = previous.get("title")
    if previous_title not in CONTINUATION_TITLES and not table_has_continuation_header(previous):
        return False
    if current.get("title") and current.get("title") != previous_title:
        return False
    if previous.get("unit") and current.get("unit") and previous.get("unit") != current.get("unit"):
        return False
    prev_cols = previous.get("columns") or []
    curr_cols = current.get("columns") or []
    if len(prev_cols) != len(curr_cols):
        return False
    return bool(current.get("rows")) and current["rows"][0] != prev_cols


def merge_continued_tables(tables: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    for table in tables:
        current = dict(table)
        current["rows"] = [list(r) for r in table.get("rows", [])]
        current["quality_flags"] = list(table.get("quality_flags") or [])
        if merged and is_continued_table(merged[-1], current):
            target = merged[-1]
            target["rows"].extend(current["rows"])
            target["page_end"] = current.get("page_end", current.get("page_start"))
            for flag in ["cross_page_merged", "continued_table_header_inherited"]:
                if flag not in target["quality_flags"]:
                    target["quality_flags"].append(flag)
            target.setdefault("merged_from", []).append(current["table_id"])
        else:
            merged.append(current)
    return merged


def normalized_row_label(row: list[Any]) -> str | None:
    for cell in row:
        if isinstance(cell, str) and cell.strip():
            return re.sub(r"[（(](元|万元|亿元|%|％|元/股|元／股)[）)]$", "", cell.replace(" ", ""))
    return None


def row_has_numeric_value(row: list[Any]) -> bool:
    return any(isinstance(cell, (int, float)) for cell in row)


def is_section_header_label(label: str) -> bool:
    return label.endswith("：") or label.endswith(":")


def validation_rows(table: dict[str, Any]) -> list[list[Any]]:
    rows = [list(row) for row in table.get("rows", [])]
    normalized: list[list[Any]] = []
    idx = 0
    while idx < len(rows):
        row = rows[idx]
        combined = list(row)
        if row_has_numeric_value(row):
            lookahead = idx + 1
            while lookahead < len(rows) and not row_has_numeric_value(rows[lookahead]):
                continuation = normalized_row_label(rows[lookahead])
                if not continuation:
                    break
                if is_section_header_label(continuation):
                    break
                label_idx = next((i for i, cell in enumerate(combined) if isinstance(cell, str) and cell.strip()), None)
                if label_idx is None:
                    break
                combined[label_idx] = f"{combined[label_idx]}{continuation}"
                lookahead += 1
            normalized.append(combined)
            idx = lookahead
        else:
            normalized.append(row)
            idx += 1
    return normalized


def row_by_label(tables: list[dict[str, Any]], label: str) -> list[Any] | None:
    normalized_label = label.replace(" ", "")
    exact_match = None
    prefix_match = None
    substring_match = None
    for table in tables:
        for row in validation_rows(table):
            if not row:
                continue
            row_label = normalized_row_label(row)
            if not row_label:
                continue
            if row_label == normalized_label:
                return row
            if row_label.startswith(normalized_label):
                prefix_match = prefix_match or row
                continue
            if row_label.endswith(normalized_label) and "归属于母公司" not in row_label:
                exact_match = exact_match or row
            elif normalized_label in row_label:
                substring_match = substring_match or row
    return prefix_match or exact_match or substring_match


def rows_by_labels(tables: list[dict[str, Any]], labels: list[str]) -> list[list[Any]]:
    rows: list[list[Any]] = []
    for label in labels:
        normalized_label = label.replace(" ", "")
        for table in tables:
            for row in validation_rows(table):
                if not row:
                    continue
                row_label = normalized_row_label(row)
                if not row_label:
                    continue
                if row_label == normalized_label or row_label.startswith(normalized_label) or (row_label.endswith(normalized_label) and "归属于母公司" not in row_label):
                    rows.append(row)
    return rows


def numeric_cells(row: list[Any] | None) -> list[float]:
    if not row:
        return []
    return [float(v) for v in row[1:] if isinstance(v, (int, float))]


def pct_change_cells(row: list[Any] | None) -> list[Any]:
    if not row:
        return []
    return [v for v in row[1:] if isinstance(v, (int, float)) or (isinstance(v, str) and ("%" in v or "％" in v))]


def tables_with_title(tables: list[dict[str, Any]], title: str) -> list[dict[str, Any]]:
    return [table for table in tables if table.get("title") == title]


def first_row_by_labels(tables: list[dict[str, Any]], labels: list[str]) -> list[Any] | None:
    for label in labels:
        row = row_by_label(tables, label)
        if row:
            return row
    return None


def first_pct_row_by_labels(tables: list[dict[str, Any]], labels: list[str]) -> list[Any] | None:
    for label in labels:
        for row in rows_by_labels(tables, [label]):
            if len(pct_change_cells(row)) >= 3:
                return row
    return None


class ValidationIndex:
    def __init__(self, tables: list[dict[str, Any]]):
        self.tables = tables

    def run_core_checks(self) -> list[dict[str, Any]]:
        checks: list[dict[str, Any]] = []
        annual_metric_tables = tables_with_title(self.tables, "主要会计数据和财务指标") or self.tables
        quarter_tables = tables_with_title(self.tables, "分季度主要财务指标") or [table for table in self.tables if "季度" in (table.get("section") or "") or "季度" in json.dumps(table.get("columns", []), ensure_ascii=False)]
        revenue = row_by_label(annual_metric_tables, "营业收入")
        pct_row = first_pct_row_by_labels(annual_metric_tables, [
            "营业收入",
            "归属于上市公司股东的净利润",
            "归属于母公司股东的净利润",
            "归属于母公司所有者的净利润",
            "归属于本行股东的净利润",
            "净利润",
            "资产总计",
            "资产总额",
        ])
        if pct_row and len(pct_change_cells(pct_row)) >= 3:
            values = pct_change_cells(pct_row)
            checks.append(validate_pct_change(values[0], values[1], values[2], tolerance=0.1))

        annual_profit = first_row_by_labels(annual_metric_tables, ["归属于上市公司股东的净利润", "归属于上市公司股东 的净利润", "归属于母公司股东的净利润", "归属于母公司所有者的净利润"])
        for label, annual_row in [("营业收入", revenue), ("归母净利润", annual_profit)]:
            if not annual_row:
                continue
            annual_values = numeric_cells(annual_row)
            for table in quarter_tables:
                qrow = row_by_label([table], "营业收入" if label == "营业收入" else "归属于上市公司股东的净利润")
                qvalues = numeric_cells(qrow)
                if len(qvalues) == 4 and annual_values:
                    diff = sum(qvalues) - annual_values[0]
                    checks.append({"check": "quarter_sum", "label": label, "status": "pass" if abs(diff) <= 1 else "fail", "diff": diff})

        asset_candidates = [numeric_cells(row) for row in rows_by_labels(self.tables, ["资产总计", "资产总额"])]
        liability_candidates = [numeric_cells(row) for row in rows_by_labels(self.tables, ["负债合计", "负债总额"])]
        equity_candidates = [numeric_cells(row) for row in rows_by_labels(self.tables, ["所有者权益（或股东权益）合计", "所有者权益合计", "股东权益合计"])]
        balance_checks = [
            validate_balance_sheet(a[0], l[0], e[0])
            for a in asset_candidates if a
            for l in liability_candidates if l
            for e in equity_candidates if e
        ]
        if balance_checks:
            checks.append(sorted(balance_checks, key=lambda check: abs(check["diff"]))[0])

        cash_checks = []
        for table in self.tables:
            cash_increase = numeric_cells(first_row_by_labels([table], ["现金及现金等价物净增加额", "现金及现金等价物净减少额", "现金及现金等价物净(减少)/增加额"]))
            cash_start = numeric_cells(row_by_label([table], "期初现金及现金等价物余额"))
            cash_end = numeric_cells(row_by_label([table], "期末现金及现金等价物余额"))
            if cash_increase and cash_start and cash_end:
                diff = cash_increase[0] + cash_start[0] - cash_end[0]
                cash_checks.append({"check": "cash_ending_tie_out", "status": "pass" if abs(diff) <= 1 else "fail", "diff": diff})
        if cash_checks:
            checks.append(sorted(cash_checks, key=lambda check: abs(check["diff"]))[0])
        return checks


def extract_with_pymupdf(pdf_path: Path, out_dir: Path) -> dict[str, Any]:
    doc = pymupdf.open(pdf_path)
    tables_meta = []
    chunks = []
    document_md_parts = []
    for page in doc:
        page_no = page.number + 1
        text = page.get_text("text")
        text_lines = page_text_lines(page)
        section = page_section(text)
        page_title = title_near_page(text)
        page_unit = detect_unit(text)
        document_md_parts.append(f"\n\n<!-- page {page_no} -->\n\n{text}")
        chunks.append({"chunk_id": f"text_{page_no:04d}", "type": "text", "source_file": pdf_path.name, "section": section, "page_start": page_no, "page_end": page_no, "content": text, "linked_tables": []})
        page_tables = []
        try:
            tables = page.find_tables().tables
        except Exception:
            tables = []
        for idx, table in enumerate(tables, 1):
            raw_rows = table.extract()
            rows = [[clean_cell(cell) for cell in row] for row in raw_rows]
            columns = reconstruct_headers(raw_rows[:2]) or [f"col_{i+1}" for i in range(max((len(r) for r in rows), default=0))]
            table_id = f"table_{len(tables_meta)+1:04d}"
            bbox = list(table.bbox)
            table_title = assign_title_by_bbox(bbox, text_lines)
            table_unit = infer_table_unit(bbox, text_lines, rows)
            quality_flags = ["numeric_values_normalized"] if rows != raw_rows else []
            if table_title is None and page_title is not None:
                quality_flags.append("title_missing_needs_context")
            if table_unit is None and page_unit is not None:
                quality_flags.append("unit_missing_needs_context")
            table_json = {
                "table_id": table_id,
                "source_file": pdf_path.name,
                "page_start": page_no,
                "page_end": page_no,
                "title": table_title,
                "section": normalize_table_section(table_title, section),
                "unit": table_unit,
                "parser": "pymupdf_find_tables",
                "confidence": confidence_proxy(rows, columns, bbox),
                "columns": columns,
                "rows": rows,
                "notes": [],
                "bbox": bbox,
                "quality_flags": quality_flags,
            }
            write_csv(out_dir / "tables" / f"{table_id}.csv", rows)
            write_text(out_dir / "tables" / f"{table_id}.md", markdown_table(rows))
            write_json(out_dir / "tables" / f"{table_id}.json", table_json)
            tables_meta.append(table_json)
            page_tables.append(table_id)
            chunks.append({"chunk_id": table_id, "type": "table", "source_file": pdf_path.name, "section": section, "page_start": page_no, "page_end": page_no, "title": table_title, "content_markdown": markdown_table(rows), "content_json_path": f"tables/{table_id}.json", "keywords": [k for k in KEYWORDS if k in text]})
        write_json(out_dir / "pages" / f"page_{page_no:03d}.json", {"page": page_no, "section": section, "title": page_title, "unit": page_unit, "text": text, "tables": page_tables})
    merged_tables = merge_continued_tables(tables_meta)
    for idx, table in enumerate(merged_tables, 1):
        merged_id = f"merged_table_{idx:04d}"
        table = dict(table)
        table["table_id"] = merged_id
        write_csv(out_dir / "tables_merged" / f"{merged_id}.csv", table["rows"])
        write_text(out_dir / "tables_merged" / f"{merged_id}.md", markdown_table(table["rows"]))
        write_json(out_dir / "tables_merged" / f"{merged_id}.json", table)
    write_text(out_dir / "document.md", "".join(document_md_parts))
    write_json(out_dir / "document.json", {"source_file": pdf_path.name, "page_count": doc.page_count, "tables": [t["table_id"] for t in tables_meta], "merged_tables": [f"merged_table_{i+1:04d}" for i in range(len(merged_tables))]})
    with (out_dir / "chunks.jsonl").open("w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
    return {"tables": tables_meta, "merged_tables": merged_tables, "chunks": chunks}


def validate_outputs(parsed: dict[str, Any], out_dir: Path, source_name: str | None = None) -> list[dict[str, Any]]:
    checks = ValidationIndex(parsed.get("merged_tables") or parsed["tables"]).run_core_checks()
    period = report_period_from_source(source_name or str(parsed.get("source_file") or ""))
    min_checks = min_core_checks_for_report(period)
    if len(checks) < min_checks:
        checks.append({"check": "validation_coverage", "status": "warn", "reason": "fewer_than_required_core_checks", "period": period, "required": min_checks, "count": len(checks)})
    write_json(out_dir / "validation" / "validation_report.json", checks)
    lines = ["# Validation Report", ""]
    for check in checks:
        lines.append(f"- {check['check']}: {check['status']} `{json.dumps(check, ensure_ascii=False)}`")
    write_text(out_dir / "validation" / "validation_report.md", "\n".join(lines))
    return checks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf")
    parser.add_argument("--out", default="outputs/annual_report_parsed")
    args = parser.parse_args()
    out_dir = Path(args.out)
    parsed = extract_with_pymupdf(Path(args.pdf), out_dir)
    checks = validate_outputs(parsed, out_dir, Path(args.pdf).name)
    failed = sum(1 for c in checks if c.get("status") == "fail")
    warned = sum(1 for c in checks if c.get("status") == "warn")
    write_text(out_dir / "parse_report.md", f"# Parse Report\n\n- parser: hybrid v3 (PyMuPDF extraction with bbox title/unit, conservative continuation merges, confidence proxy, validation gate; Camelot/pdfplumber benchmark remains available via extract_tables.py)\n- raw tables: {len(parsed['tables'])}\n- merged tables: {len(parsed['merged_tables'])}\n- chunks: {len(parsed['chunks'])}\n- validation checks: {len(checks)}\n- validation failed: {failed}\n- validation warnings: {warned}\n")


if __name__ == "__main__":
    main()
