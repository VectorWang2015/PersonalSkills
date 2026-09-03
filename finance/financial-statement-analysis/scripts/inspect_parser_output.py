#!/usr/bin/env python3
"""Read-only inventory for a financial-pdf-parser style output directory."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def status(path: Path, root: Path) -> dict[str, object]:
    return {
        "path": path.relative_to(root).as_posix(),
        "exists": path.exists(),
        "is_file": path.is_file(),
        "bytes": path.stat().st_size if path.is_file() else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect parser output without modifying it.")
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    root = args.directory.expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"error: not a directory: {root}")

    expected = [
        root / "analysis_context.md",
        root / "validation" / "validation_report.md",
        root / "chunks.jsonl",
        root / "document.md",
    ]
    merged = sorted((root / "tables_merged").glob("*.json")) if (root / "tables_merged").is_dir() else []
    page_tables = sorted((root / "tables").glob("*.json")) if (root / "tables").is_dir() else []

    invalid_json: list[str] = []
    for path in merged:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            invalid_json.append(path.relative_to(root).as_posix())

    result = {
        "root_name": root.name,
        "expected_files": [status(path, root) for path in expected],
        "merged_table_count": len(merged),
        "merged_tables": [path.relative_to(root).as_posix() for path in merged],
        "page_table_count": len(page_tables),
        "invalid_merged_json": invalid_json,
        "calculation_ready": bool(merged) and not invalid_json,
        "notes": [
            "A present validation report must still be read for semantic failures and warnings.",
            "Calculation-ready means JSON is parseable, not that table identity, units or values are correct.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["calculation_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
