from __future__ import annotations

import argparse
import csv
import json
import time
import traceback
from pathlib import Path
from typing import Any

from financial_normalization import markdown_table


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(path: Path, rows: list[list[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def run_pymupdf(pdf_path: Path, out: Path) -> list[dict[str, Any]]:
    import pymupdf

    page_reports = []
    doc = pymupdf.open(pdf_path)
    all_text = []
    for page in doc:
        start = time.perf_counter()
        page_no = page.number + 1
        text = page.get_text("text")
        tables_out = []
        try:
            tables = page.find_tables().tables
            for idx, table in enumerate(tables, 1):
                rows = table.extract()
                table_id = f"page_{page_no:03d}_table_{idx:02d}"
                write_csv(out / "tables" / f"{table_id}.csv", rows)
                write_text(out / "tables" / f"{table_id}.md", markdown_table(rows))
                write_json(out / "tables" / f"{table_id}.json", {"page": page_no, "bbox": list(table.bbox), "rows": rows})
                tables_out.append({"id": table_id, "rows": len(rows), "cols": max((len(r) for r in rows), default=0), "bbox": list(table.bbox)})
        except Exception as exc:
            tables_out.append({"error": repr(exc)})
        (out / "debug").mkdir(parents=True, exist_ok=True)
        pix = page.get_pixmap(dpi=110)
        pix.save(out / "debug" / f"page_{page_no:03d}.png")
        elapsed = time.perf_counter() - start
        all_text.append(f"\n\n<!-- page {page_no} -->\n\n{text}")
        write_json(out / "pages" / f"page_{page_no:03d}.json", {"page": page_no, "text": text, "tables": tables_out})
        page_reports.append({"page": page_no, "seconds": elapsed, "tables": len(tables_out)})
    write_text(out / "document.txt", "".join(all_text))
    write_json(out / "timing.json", page_reports)
    return page_reports


def run_pymupdf4llm(pdf_path: Path, out: Path) -> dict[str, Any]:
    import pymupdf4llm

    start = time.perf_counter()
    md = pymupdf4llm.to_markdown(str(pdf_path))
    write_text(out / "document.md", md)
    report = {"seconds": time.perf_counter() - start, "markdown_chars": len(md)}
    write_json(out / "timing.json", report)
    return report


def run_pdfplumber(pdf_path: Path, out: Path) -> list[dict[str, Any]]:
    import pdfplumber

    reports = []
    all_text = []
    settings_list = [
        {"vertical_strategy": "lines", "horizontal_strategy": "lines"},
        {"vertical_strategy": "text", "horizontal_strategy": "text", "min_words_vertical": 2, "min_words_horizontal": 1},
    ]
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            start = time.perf_counter()
            text = page.extract_text(layout=True) or ""
            page_tables = []
            for sidx, settings in enumerate(settings_list, 1):
                try:
                    tables = page.extract_tables(table_settings=settings)
                    for tidx, rows in enumerate(tables, 1):
                        table_id = f"page_{page.page_number:03d}_s{sidx}_table_{tidx:02d}"
                        write_csv(out / "tables" / f"{table_id}.csv", rows)
                        write_text(out / "tables" / f"{table_id}.md", markdown_table(rows))
                        write_json(out / "tables" / f"{table_id}.json", {"page": page.page_number, "settings": settings, "rows": rows})
                        page_tables.append({"id": table_id, "settings": settings, "rows": len(rows), "cols": max((len(r) for r in rows), default=0)})
                    img = page.to_image(resolution=110).debug_tablefinder(table_settings=settings)
                    img.save(out / "debug" / f"page_{page.page_number:03d}_s{sidx}.png")
                except Exception as exc:
                    page_tables.append({"settings": settings, "error": repr(exc)})
            elapsed = time.perf_counter() - start
            all_text.append(f"\n\n<!-- page {page.page_number} -->\n\n{text}")
            write_json(out / "pages" / f"page_{page.page_number:03d}.json", {"page": page.page_number, "text": text, "tables": page_tables})
            reports.append({"page": page.page_number, "seconds": elapsed, "tables": len(page_tables)})
    write_text(out / "document.txt", "".join(all_text))
    write_json(out / "timing.json", reports)
    return reports


def run_camelot(pdf_path: Path, out: Path, pages: str) -> dict[str, Any]:
    import camelot

    reports = {}
    for flavor in ["lattice", "stream"]:
        start = time.perf_counter()
        flavor_reports = []
        try:
            tables = camelot.read_pdf(str(pdf_path), pages=pages, flavor=flavor)
            for idx, table in enumerate(tables, 1):
                page = table.parsing_report.get("page")
                table_id = f"{flavor}_page_{int(page):03d}_table_{idx:02d}" if page else f"{flavor}_table_{idx:02d}"
                rows = table.df.values.tolist()
                write_csv(out / "tables" / f"{table_id}.csv", rows)
                write_text(out / "tables" / f"{table_id}.md", markdown_table(rows))
                write_json(out / "tables" / f"{table_id}.json", {"parser": f"camelot_{flavor}", "report": table.parsing_report, "rows": rows})
                flavor_reports.append({"id": table_id, "shape": list(table.shape), "report": table.parsing_report})
        except Exception as exc:
            flavor_reports.append({"error": repr(exc), "traceback": traceback.format_exc()})
        reports[flavor] = {"seconds": time.perf_counter() - start, "tables": flavor_reports}
    write_json(out / "timing.json", reports)
    return reports


def run_docling(pdf_path: Path, out: Path) -> dict[str, Any]:
    from docling.document_converter import DocumentConverter

    start = time.perf_counter()
    converter = DocumentConverter()
    result = converter.convert(str(pdf_path))
    doc = result.document
    md = doc.export_to_markdown()
    write_text(out / "document.md", md)
    try:
        data = doc.export_to_dict()
    except Exception:
        data = json.loads(doc.model_dump_json())
    write_json(out / "document.json", data)
    report = {"seconds": time.perf_counter() - start, "markdown_chars": len(md)}
    write_json(out / "timing.json", report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf")
    parser.add_argument("--out", default="outputs/pdf_parser_benchmark")
    parser.add_argument("--pages", default="all")
    parser.add_argument("--tools", default="pymupdf,pymupdf4llm,pdfplumber,camelot,docling")
    args = parser.parse_args()
    pdf_path = Path(args.pdf)
    base = Path(args.out)
    for tool in args.tools.split(","):
        tool = tool.strip()
        out = base / tool
        out.mkdir(parents=True, exist_ok=True)
        log_path = base / "logs" / f"{tool}.json"
        try:
            if tool == "pymupdf":
                result = run_pymupdf(pdf_path, out)
            elif tool == "pymupdf4llm":
                result = run_pymupdf4llm(pdf_path, out)
            elif tool == "pdfplumber":
                result = run_pdfplumber(pdf_path, out)
            elif tool == "camelot":
                result = run_camelot(pdf_path, out, args.pages)
            elif tool == "docling":
                result = run_docling(pdf_path, out)
            else:
                continue
            write_json(log_path, {"tool": tool, "status": "ok", "result": result})
        except Exception as exc:
            write_json(log_path, {"tool": tool, "status": "error", "error": repr(exc), "traceback": traceback.format_exc()})


if __name__ == "__main__":
    main()
