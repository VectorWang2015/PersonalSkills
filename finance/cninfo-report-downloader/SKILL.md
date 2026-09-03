---
name: cninfo-report-downloader
description: Use when the user wants to download A-share annual reports, quarterly reports, interim reports, latest financial reports, or 巨潮资讯 disclosures by stock code. Triggers include "下载年报", "拉一下季报", "最新财报", "巨潮", and A 股代码 such as 600219. Do not use for analyzing already-downloaded reports without a download request.
metadata:
  status: active
  release-record: references/release-evaluation.md
---

# 巨潮财报下载器

## Overview

输入 A 股股票代码，从巨潮资讯下载最新年度报告完整版和最近一期非年报定期报告，并保存到项目标准目录 `raw/reports/<报告期>/`。

## When To Use

Use when the user asks to:

- 下载某个 A 股代码的最新年报、季报、半年报或财报。
- 从巨潮资讯拉取公告 PDF。
- 为后续财报分析准备原始报告文件。

Do not use when the user only wants interpretation of an existing local report; call the relevant analysis skill instead.

## Command

From the `financial_skills` workspace root when using this repository layout:

```bash
python3 skills/finance/cninfo-report-downloader/scripts/download_cninfo_reports.py 600219
```

If the skill is installed directly under opencode's project skill directory, use the installed path instead:

```bash
python3 .opencode/skills/cninfo-report-downloader/scripts/download_cninfo_reports.py 600219
```

Run the command from the project root where `raw/reports/` should be created. The default output root is relative to the current working directory.

Runtime requirements:

- Required: Python 3.9+ with standard library network access.
- TXT conversion uses `pdfplumber` when installed, otherwise falls back to the
  system `pdftotext` command from Poppler.
- If neither converter is available, pass `--no-txt` to download PDF only.

Install either TXT conversion dependency when needed:

```bash
python3 -m pip install pdfplumber
# or install Poppler with the operating system package manager
```

Options:

```bash
--output-root raw/reports   # default
--no-txt                   # download PDF only
--overwrite                # replace existing files
--dry-run                  # query and show selected reports without downloading
--report-type TYPE         # both, annual, latest-periodic, q1, interim, or q3
--max-pages N              # announcement pagination safety limit; default 20
```

## Behavior

The script downloads two reports by default:

- 最新年度报告完整版，不使用摘要、简报、英文版或更正摘要替代。
- 最近一期非年报定期报告，一季报、半年报、三季报三者中取最新。

Use `--report-type` when the user requests only one category. In `both` mode, if only one category exists, keep the available result and print a warning instead of discarding the successful selection.

The announcement query follows all reported result pages up to `--max-pages`, deduplicates announcements, and retries transient network/HTTP 429/5xx failures. Increase the limit explicitly if the API reports more pages than the safety cap.

“最新年度报告”按报告期年份判断，不按公告发布时间判断。若过去年报的更正后版本晚于最新年报发布，仍应选择报告期最新的年报；只有在同一报告期内，才优先选择更正后/修订版。

Output files:

```text
raw/reports/2025/南山铝业-2025年报.pdf
raw/reports/2025/南山铝业-2025年报.txt
raw/reports/2026Q1/南山铝业-2026Q1.pdf
raw/reports/2026Q1/南山铝业-2026Q1.txt
```

Downloaded content must start with a valid PDF signature before it replaces the target path. HTML error/rate-limit pages are rejected, and both PDF and TXT writes use a temporary file plus atomic rename. If TXT conversion fails because no converter is available or a PDF is malformed, keep the validated PDF and any existing TXT, then report the conversion error.

## After Download

After a successful download, continue into parsing and analysis only when the request includes that work; otherwise briefly suggest the next command.

Recommended next step for PDFs:

```bash
python .opencode/skills/financial-pdf-parser/scripts/parse_financial_pdf.py raw/reports/<报告期>/<公司>-<报告期>.pdf --out reports/parsed/<公司>-<报告期>
```

After parsing succeeds, pass the parsed directory to the relevant analysis entry point:

- 普通非金融公司：`financial-statement-analysis`
- 消费公司：`consumer-analysis`
- 银行：`bank-comprehensive-analysis`
- 保险：`insurance-comprehensive-analysis`
- 林奇视角：`peter-lynch-investment`

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Downloading 年报摘要 as 年报 | Require title contains `年度报告` and excludes `摘要` |
| Treating 半年度报告 as 年报 | Parse `半年度报告` before generic `年度报告` |
| Downloading older-year correction as latest annual report | Sort annual reports by report year first, announcement time only within the same year |
| Inferring market from `orgId` | Infer market from stock code prefix |
| Saving an HTML error page as `.pdf` | Verify the `%PDF-` signature before the atomic write |
| Reading only the first announcement page | Follow `totalpages`/`hasMore` with a bounded safety limit |
| Skipping TXT status | Report TXT conversion success, skip, or failure explicitly |

发布状态及其边界见 [release-evaluation.md](references/release-evaluation.md)。
