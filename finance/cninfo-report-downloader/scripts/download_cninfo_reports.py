#!/usr/bin/env python3
"""Download latest A-share periodic reports from cninfo.com.cn."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional, Tuple


STOCK_LIST_URL = "https://www.cninfo.com.cn/new/data/szse_stock.json"
ANNOUNCEMENT_QUERY_URL = "https://www.cninfo.com.cn/new/hisAnnouncement/query"
STATIC_PDF_BASE_URL = "https://static.cninfo.com.cn/"
PERIODIC_CATEGORY = "category_ndbg_szsh;category_yjdbg_szsh;category_sjdbg_szsh;category_bndbg_szsh;"
DEFAULT_PAGE_SIZE = 50
DEFAULT_MAX_PAGES = 20
REPORT_TYPE_CHOICES = ("both", "annual", "latest-periodic", "q1", "interim", "q3")


class StockInfo(NamedTuple):
    code: str
    name: str
    org_id: str
    column: str
    plate: str


class DownloadedReport(NamedTuple):
    title: str
    announcement_time: Any
    url: str
    pdf_path: Optional[Path]
    txt_path: Optional[Path]
    status: str
    txt_status: str


def open_with_retry(request: urllib.request.Request, timeout: int, attempts: int = 3) -> Any:
    if attempts < 1:
        raise ValueError("attempts must be at least 1")
    last_error: Optional[Exception] = None
    for attempt in range(attempts):
        try:
            return urllib.request.urlopen(request, timeout=timeout)
        except urllib.error.HTTPError as exc:
            if exc.code not in {429, 500, 502, 503, 504}:
                raise
            last_error = exc
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
        if attempt + 1 < attempts:
            time.sleep(0.5 * (2**attempt))
    raise RuntimeError(f"网络请求失败，已重试 {attempts} 次: {last_error}") from last_error


def request_json(url: str, data: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
        "Referer": "https://www.cninfo.com.cn/new/disclosure/stock",
        "Origin": "https://www.cninfo.com.cn",
    }
    body = urllib.parse.urlencode(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers)
    with open_with_retry(req, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError(f"接口返回的不是 JSON 对象: {url}")
    return payload


def market_for_code(stock_code: str) -> Tuple[str, str]:
    if not re.fullmatch(r"\d{6}", stock_code):
        raise ValueError(f"仅支持 6 位 A 股股票代码: {stock_code}")
    if stock_code[0] in {"6", "9"}:
        return "sse", "sse"
    if stock_code[0] in {"0", "2", "3"}:
        return "szse", "szse"
    if stock_code[0] in {"4", "8"}:
        return "bj", "bj"
    raise ValueError(f"无法识别 A 股市场前缀: {stock_code}")


def resolve_stock_info(stock_code: str) -> StockInfo:
    column, plate = market_for_code(stock_code)
    payload = request_json(STOCK_LIST_URL)
    for item in payload.get("stockList", []):
        if item.get("code") == stock_code:
            return StockInfo(
                code=stock_code,
                name=str(item.get("zwjc") or stock_code),
                org_id=str(item.get("orgId") or ""),
                column=column,
                plate=plate,
            )
    raise ValueError(f"未在巨潮股票表找到该代码: {stock_code}")


def query_announcements(
    stock: StockInfo,
    *,
    page_size: int = DEFAULT_PAGE_SIZE,
    max_pages: int = DEFAULT_MAX_PAGES,
) -> List[Dict[str, Any]]:
    if page_size < 1 or max_pages < 1:
        raise ValueError("page_size and max_pages must be positive")
    announcements: List[Dict[str, Any]] = []
    seen: set[Any] = set()
    for page_num in range(1, max_pages + 1):
        data = {
            "stock": f"{stock.code},{stock.org_id}",
            "tabName": "fulltext",
            "pageSize": str(page_size),
            "pageNum": str(page_num),
            "column": stock.column,
            "category": PERIODIC_CATEGORY,
            "plate": stock.plate,
            "seDate": "",
            "searchkey": "",
            "secid": "",
            "sortName": "",
            "sortType": "",
            "isHLtitle": "true",
        }
        payload = request_json(ANNOUNCEMENT_QUERY_URL, data)
        page_items = payload.get("announcements") or []
        for item in page_items:
            key = item.get("announcementId") or item.get("adjunctUrl") or (
                item.get("announcementTitle"),
                item.get("announcementTime"),
            )
            if key not in seen:
                seen.add(key)
                announcements.append(item)

        total_pages_value = payload.get("totalpages") or 0
        try:
            total_pages = int(total_pages_value)
        except (TypeError, ValueError):
            total_pages = 0
        has_more = payload.get("hasMore") is True or str(payload.get("hasMore")).lower() == "true"
        if not page_items or (total_pages and page_num >= total_pages) or (not total_pages and not has_more):
            break
    else:
        raise RuntimeError(f"公告分页超过安全上限 {max_pages}，请增大 --max-pages 后重试")

    if not announcements:
        raise RuntimeError(f"未查询到定期报告公告: {stock.code} {stock.name}")
    return announcements


def clean_title(title: str) -> str:
    title = re.sub(r"<[^>]+>", "", title or "")
    return title.replace(" ", "").replace("_", "")


def announcement_time(item: Dict[str, Any]) -> int:
    value = item.get("announcementTime") or item.get("announcementTimeStr") or 0
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def report_year(title: str) -> int:
    match = re.search(r"(20\d{2})年?", clean_title(title))
    if not match:
        return 0
    return int(match.group(1))


def is_correction_title(title: str) -> bool:
    title = clean_title(title)
    return any(word in title for word in ("更正", "修订", "修正"))


def annual_report_sort_key(item: Dict[str, Any]) -> Tuple[int, bool, int]:
    title = str(item.get("announcementTitle") or "")
    return report_year(title), is_correction_title(title), announcement_time(item)


def select_newest(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not items:
        raise ValueError("没有找到符合条件的公告")
    return max(items, key=announcement_time)


def select_annual_report(announcements: List[Dict[str, Any]]) -> Dict[str, Any]:
    excluded = ("半年度报告", "摘要", "简报", "英文", "取消", "更正摘要")
    matches = []
    for item in announcements:
        title = clean_title(str(item.get("announcementTitle") or ""))
        if "年度报告" in title and not any(word in title for word in excluded):
            matches.append(item)
    if not matches:
        raise ValueError("没有找到符合条件的公告")
    return max(matches, key=annual_report_sort_key)


def select_latest_periodic_report(announcements: List[Dict[str, Any]]) -> Dict[str, Any]:
    included = ("一季度报告", "第一季度报告", "半年度报告", "三季度报告", "第三季度报告")
    excluded = ("摘要", "英文", "取消", "更正公告", "修订说明")
    matches = []
    for item in announcements:
        title = clean_title(str(item.get("announcementTitle") or ""))
        if any(word in title for word in included) and not any(word in title for word in excluded):
            matches.append(item)
    return select_newest(matches)


def select_periodic_report(announcements: List[Dict[str, Any]], report_type: str) -> Dict[str, Any]:
    included_by_type = {
        "q1": ("一季度报告", "第一季度报告"),
        "interim": ("半年度报告",),
        "q3": ("三季度报告", "第三季度报告"),
    }
    if report_type not in included_by_type:
        raise ValueError(f"不支持的定期报告类型: {report_type}")
    excluded = ("摘要", "英文", "取消", "更正公告", "修订说明")
    matches = []
    for item in announcements:
        title = clean_title(str(item.get("announcementTitle") or ""))
        if any(word in title for word in included_by_type[report_type]) and not any(
            word in title for word in excluded
        ):
            matches.append(item)
    return select_newest(matches)


def select_requested_reports(
    announcements: List[Dict[str, Any]], report_type: str
) -> Tuple[List[Dict[str, Any]], List[str]]:
    if report_type not in REPORT_TYPE_CHOICES:
        raise ValueError(f"不支持的报告类型: {report_type}")
    requested = ("annual", "latest-periodic") if report_type == "both" else (report_type,)
    selected: List[Dict[str, Any]] = []
    missing: List[str] = []
    for current_type in requested:
        try:
            if current_type == "annual":
                item = select_annual_report(announcements)
            elif current_type == "latest-periodic":
                item = select_latest_periodic_report(announcements)
            else:
                item = select_periodic_report(announcements, current_type)
            selected.append(item)
        except ValueError:
            missing.append(current_type)
    if not selected:
        raise ValueError(f"没有找到请求的报告类型: {', '.join(requested)}")
    if report_type != "both" and missing:
        raise ValueError(f"没有找到请求的报告类型: {report_type}")
    return selected, missing


def parse_report_period(title: str) -> Tuple[str, str]:
    title = clean_title(title)
    year_match = re.search(r"(20\d{2})年?", title)
    if not year_match:
        raise ValueError(f"无法从标题解析年份: {title}")
    year = year_match.group(1)
    if "第一季度报告" in title or "一季度报告" in title:
        return f"{year}Q1", f"{year}Q1"
    if "半年度报告" in title:
        return f"{year}H1", f"{year}H1"
    if "第三季度报告" in title or "三季度报告" in title:
        return f"{year}Q3", f"{year}Q3"
    if "年度报告" in title:
        return f"{year}年报", year
    raise ValueError(f"无法从标题解析报告期: {title}")


def safe_filename_part(value: str) -> str:
    return re.sub(r"[\\/:*?\"<>|\s]+", "", value)


def target_paths(output_root: Path, company_name: str, report_period: str, period_dir: str) -> Tuple[Path, Path]:
    safe_name = safe_filename_part(company_name)
    pdf_path = output_root / period_dir / f"{safe_name}-{report_period}.pdf"
    txt_path = output_root / period_dir / f"{safe_name}-{report_period}.txt"
    return pdf_path, txt_path


def download_file(url: str, target: Path, overwrite: bool) -> str:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and not overwrite:
        return "skipped_existing"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with open_with_retry(req, timeout=60) as response:
        payload = response.read()
        content_type = str(response.headers.get("Content-Type", "")).lower()
    if not payload.startswith(b"%PDF-"):
        raise RuntimeError(
            f"下载内容不是有效 PDF: content-type={content_type or 'unknown'}, url={url}"
        )
    temporary_path: Optional[Path] = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=f".{target.name}.",
            suffix=".part",
            dir=target.parent,
            delete=False,
        ) as temporary:
            temporary.write(payload)
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary_path = Path(temporary.name)
        temporary_path.replace(target)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()
    return "downloaded"


def extract_pdf_text(pdf_path: Path) -> str:
    try:
        import pdfplumber
    except ImportError:
        pdftotext = shutil.which("pdftotext")
        if pdftotext is None:
            raise RuntimeError(
                "TXT 转换需要 Python 包 pdfplumber 或系统命令 pdftotext (Poppler)"
            )
        completed = subprocess.run(
            [pdftotext, "-layout", str(pdf_path), "-"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return completed.stdout
    else:
        with pdfplumber.open(str(pdf_path)) as pdf:
            pages = []
            for page in pdf.pages:
                pages.append(page.extract_text() or "")
        return "\n\n".join(pages)


def write_text_atomic(target: Path, text: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Optional[Path] = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            prefix=f".{target.name}.",
            suffix=".part",
            dir=target.parent,
            delete=False,
        ) as temporary:
            temporary.write(text)
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary_path = Path(temporary.name)
        temporary_path.replace(target)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def convert_pdf_to_txt(pdf_path: Path, txt_path: Path, overwrite: bool) -> str:
    if txt_path.exists() and not overwrite:
        return "skipped_existing"
    try:
        text = extract_pdf_text(pdf_path)
        write_text_atomic(txt_path, text)
        return "converted"
    except Exception as exc:  # noqa: BLE001 - CLI should report conversion errors without deleting PDF.
        return f"failed: {exc}"


def pdf_url_for(item: Dict[str, Any]) -> str:
    adjunct_url = str(item.get("adjunctUrl") or "")
    if not adjunct_url:
        raise ValueError(f"公告缺少 adjunctUrl: {item.get('announcementTitle')}")
    return urllib.parse.urljoin(STATIC_PDF_BASE_URL, adjunct_url)


def handle_report(
    stock: StockInfo,
    item: Dict[str, Any],
    output_root: Path,
    convert_txt: bool,
    overwrite: bool,
    dry_run: bool,
) -> DownloadedReport:
    title = clean_title(str(item.get("announcementTitle") or ""))
    report_period, period_dir = parse_report_period(title)
    pdf_path, txt_path = target_paths(output_root, stock.name, report_period, period_dir)
    url = pdf_url_for(item)
    if dry_run:
        return DownloadedReport(title, item.get("announcementTime"), url, pdf_path, txt_path if convert_txt else None, "dry_run", "dry_run")
    pdf_status = download_file(url, pdf_path, overwrite)
    txt_status = "disabled"
    if convert_txt:
        txt_status = convert_pdf_to_txt(pdf_path, txt_path, overwrite)
    return DownloadedReport(title, item.get("announcementTime"), url, pdf_path, txt_path if convert_txt else None, pdf_status, txt_status)


def print_summary(stock: StockInfo, reports: List[DownloadedReport]) -> None:
    print(f"公司: {stock.name} ({stock.code})")
    print(f"orgId: {stock.org_id}; column={stock.column}; plate={stock.plate}")
    for report in reports:
        print("-")
        print(f"标题: {report.title}")
        print(f"公告时间: {report.announcement_time}")
        print(f"PDF URL: {report.url}")
        print(f"PDF: {report.pdf_path} [{report.status}]")
        if report.txt_path is not None:
            print(f"TXT: {report.txt_path} [{report.txt_status}]")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Download latest A-share reports from cninfo.com.cn")
    parser.add_argument("stock_code", help="6 位 A 股股票代码，例如 600219")
    parser.add_argument("--output-root", default="raw/reports", help="输出根目录，默认 raw/reports")
    parser.add_argument("--no-txt", action="store_true", help="只下载 PDF，不转换 TXT")
    parser.add_argument("--overwrite", action="store_true", help="覆盖已有 PDF/TXT")
    parser.add_argument("--dry-run", action="store_true", help="只查询和筛选公告，不下载文件")
    parser.add_argument(
        "--report-type",
        choices=REPORT_TYPE_CHOICES,
        default="both",
        help="报告类型，默认 both（年报 + 最近一期非年报）",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=DEFAULT_MAX_PAGES,
        help=f"公告查询最大页数，默认 {DEFAULT_MAX_PAGES}",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    convert_txt = not args.no_txt
    try:
        stock = resolve_stock_info(args.stock_code)
        announcements = query_announcements(stock, max_pages=args.max_pages)
        selected, missing = select_requested_reports(announcements, args.report_type)
        reports = [
            handle_report(stock, item, Path(args.output_root), convert_txt, args.overwrite, args.dry_run)
            for item in selected
        ]
        print_summary(stock, reports)
        if missing:
            print(f"警告: 未找到以下报告类型，已保留其他成功结果: {', '.join(missing)}", file=sys.stderr)
        return 0
    except Exception as exc:  # noqa: BLE001 - CLI reports actionable errors.
        print(f"错误: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
