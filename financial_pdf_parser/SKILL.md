---
name: financial-pdf-parser
description: Use when parsing Chinese A-share annual, interim, or quarterly report PDFs into structured text, tables, chunks, and validation artifacts before LLM or agent financial analysis.
---

# Financial PDF Parser

## Goal

Build a traceable PDF preprocessing pipeline for financial reports: page text, table structure, units, section context, normalized numbers, validation checks, and RAG/Agent-ready chunks. Plain-text-only extraction is a failed parse for financial reports.

## When To Use

- User provides A股/港股/上市公司 PDF annual reports, quarterly reports, prospectuses, or financial statement PDFs.
- The downstream task is LLM/Agent analysis and needs reliable tables, page references, units, and validation.
- Existing `pdftotext`/`pdf2text` output has broken headers, split numbers, lost units, or cross-page table issues.

## When Not To Use

- User asks only to summarize a short text already extracted from a report.
- The document is not a financial report and table fidelity is not important.
- The PDF is scanned/image-only and no OCR/VLM dependency is available; first request OCR setup or use a fallback.

## Environment

Use Python 3.11+ in an activated environment. In this repository, prefer the project conda environment:

```bash
conda activate trading_agents
```

On a fresh host, create an equivalent environment first if it does not exist:

```bash
conda create -n trading_agents python=3.11
conda activate trading_agents
```

Install core dependencies:

```bash
python -m pip install pymupdf pymupdf4llm pdfplumber camelot-py opencv-python
```

Install Docling only when full document structure/OCR-heavy layout parsing is acceptable:

```bash
python -m pip install docling
```

System packages only if optional backends are needed:

```bash
sudo apt install ghostscript poppler-utils tesseract-ocr tesseract-ocr-chi-sim
```

## Recommended Workflow

1. Create an output folder with `document.md`, `document.json`, `chunks.jsonl`, `tables/`, `pages/`, `images/`, `validation/`, and `parse_report.md`.
2. Financial statement pages are table-first: extract tables and provenance before summarizing page text.
3. Use bbox-proximate text, not whole-page keywords, to assign table title and unit. A table title must come from the nearest title above the table bbox; page-bottom titles belong to the next table.
4. Use PyMuPDF for page count, text, coordinates, rendering, and fast table detection.
5. Use Camelot `lattice` for ruled tables; use Camelot `stream` or pdfplumber when tables are borderless or weakly ruled.
6. Use Docling or PyMuPDF4LLM for integrated Markdown and section reading order, not as the sole source of financial numbers.
7. Normalize numbers and reconstruct headers before handing tables to an LLM.
8. Merge cross-page financial statements and disclosure tables such as `非经常性损益项目及金额` into `tables_merged/` and mark `cross_page_merged` plus `continued_table_header_inherited`.
9. Run financial validations and mark low-confidence tables with `quality_flags`; when a parser has no native confidence, record a conservative structure-based confidence proxy rather than `null`.
10. Do not pass key financial figures downstream until `validation_report.md` exists and every failed check is either fixed or explicitly flagged.

## Table Handling

For ordinary text pages, store page text and create text chunks with `page_start`, `page_end`, and `section`.

For ruled tables, prefer Camelot `lattice` or PyMuPDF `page.find_tables()`; keep `bbox`, parser name, page number, and parsing confidence. If PyMuPDF has no native confidence, derive a simple proxy from row consistency, numeric density, and valid bbox.

For borderless tables, try Camelot `stream`, then pdfplumber with `vertical_strategy="text"` and `horizontal_strategy="text"`.

For complex pdfplumber pages, tune `explicit_vertical_lines`, `explicit_horizontal_lines`, and save `debug_tablefinder` images.

For cross-page tables, merge when titles/headers/units match and adjacent pages continue row labels. Continuation pages must inherit the first page title and header; add `cross_page_merged` to `quality_flags`. Keep raw page tables in `tables/`, but downstream agents should prefer `tables_merged/` when present.

For scanned PDFs, use OCR only as fallback. Never let OCR/VLM invent financial values; keep low confidence and require validation.

## Cleaning And Validation

Always apply:

- Numeric repair: split amounts, thousand commas, Chinese/English parentheses, negative signs, percentages, blanks, `--`, `不适用`.
- Unit detection: 元, 万元, 亿元, 元/股, %, 人数, 股数.
- Header reconstruction: multi-level years, 调整前/调整后, 本年比上年增减, quarterly columns.
- Checks: YoY recomputation, quarterly sums when four-quarter data exists, `资产 = 负债 + 所有者权益/股东权益`, cash-flow ending balance tie-out, recurring/non-recurring profit relation, anomaly detection.
- Quality gate: `parse_report.md` must report raw table count, merged table count, validation check count, failed checks, warnings, and fallback/tool evidence. Annual reports require at least four core checks; interim reports require at least two; quarterly reports require at least one applicable core check.

## Output Contract

Required output structure:

```text
annual_report_parsed/
  document.md
  document.json
  chunks.jsonl
  tables/table_0001.csv
  tables/table_0001.json
  tables/table_0001.md
  tables_merged/merged_table_0001.json
  pages/page_001.json
  validation/validation_report.json
  validation/validation_report.md
  parse_report.md
```

Table JSON must include `table_id`, `source_file`, `page_start`, `page_end`, `title`, `section`, `unit`, `parser`, `confidence`, `columns`, `rows`, `notes`, `bbox`, and `quality_flags`.

Merged table JSON must keep the same fields and may add `merged_from`. It must preserve `page_start/page_end` across the merged range.

Chunk JSONL must separate text chunks and table chunks. Every chunk must include `chunk_id`, `type`, `source_file`, `section`, `page_start`, `page_end`, and retrieval keywords when available. Table chunks must link to `tables/table_xxxx.json`.

## Command Examples

Benchmark tools on key pages:

```bash
python .opencode/skills/financial-pdf-parser/scripts/extract_tables.py path/to/annual_report.pdf --tools pymupdf,pymupdf4llm,pdfplumber,camelot,docling
```

Build unified output:

```bash
python .opencode/skills/financial-pdf-parser/scripts/parse_financial_pdf.py path/to/annual_report.pdf --out reports/parsed/company-2025
```

## Fallback Strategy

- If table count is zero on a financial-statement page, retry with Camelot `stream` and pdfplumber text strategy.
- If numbers contain embedded spaces or line breaks, run numeric repair before validation.
- If title or unit comes only from a page-level guess, mark `title_missing_needs_context` or `unit_missing_needs_context`; do not silently attach a title from a page-bottom next-section heading.
- If financial statement tables span pages, use merged tables for validation and downstream analysis.
- If validation fails, do not ask the LLM to guess; save the table with `validation_failed` and inspect debug images.
- If Docling is slow or too heavy, use it only for Markdown/section context and keep PyMuPDF/Camelot/pdfplumber as numeric sources.
