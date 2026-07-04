#!/usr/bin/env python3
"""Download latest A-share periodic reports from cninfo.com.cn."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional, Tuple


STOCK_LIST_URL = "https://www.cninfo.com.cn/new/data/szse_stock.json"
ANNOUNCEMENT_QUERY_URL = "https://www.cninfo.com.cn/new/hisAnnouncement/query"
STATIC_PDF_BASE_URL = "https://static.cninfo.com.cn/"
PERIODIC_CATEGORY = "category_ndbg_szsh;category_yjdbg_szsh;category_sjdbg_szsh;category_bndbg_szsh;"


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


def request_json(url: str, data: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
        "Referer": "https://www.cninfo.com.cn/new/disclosure/stock",
        "Origin": "https://www.cninfo.com.cn",
    }
    body = urllib.parse.urlencode(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


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


def query_announcements(stock: StockInfo) -> List[Dict[str, Any]]:
    data = {
        "stock": f"{stock.code},{stock.org_id}",
        "tabName": "fulltext",
        "pageSize": "50",
        "pageNum": "1",
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
    announcements = payload.get("announcements") or []
    if not announcements:
        raise RuntimeError(f"未查询到定期报告公告，请求参数: {data}")
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


def select_newest(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not items:
        raise ValueError("没有找到符合条件的公告")
    return max(items, key=announcement_time)


def select_annual_report(announcements: List[Dict[str, Any]]) -> Dict[str, Any]:
    excluded = ("摘要", "简报", "英文", "取消", "更正摘要")
    matches = []
    for item in announcements:
        title = clean_title(str(item.get("announcementTitle") or ""))
        if "年度报告" in title and not any(word in title for word in excluded):
            matches.append(item)
    return select_newest(matches)


def select_latest_periodic_report(announcements: List[Dict[str, Any]]) -> Dict[str, Any]:
    included = ("一季度报告", "第一季度报告", "半年度报告", "三季度报告", "第三季度报告")
    excluded = ("摘要", "英文", "更正", "取消")
    matches = []
    for item in announcements:
        title = clean_title(str(item.get("announcementTitle") or ""))
        if any(word in title for word in included) and not any(word in title for word in excluded):
            matches.append(item)
    return select_newest(matches)


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
    with urllib.request.urlopen(req, timeout=60) as response:
        target.write_bytes(response.read())
    return "downloaded"


def convert_pdf_to_txt(pdf_path: Path, txt_path: Path, overwrite: bool) -> str:
    if txt_path.exists() and not overwrite:
        return "skipped_existing"
    try:
        import pdfplumber
    except ImportError as exc:
        return f"failed: missing pdfplumber ({exc})"
    try:
        with pdfplumber.open(str(pdf_path)) as pdf:
            pages = []
            for page in pdf.pages:
                pages.append(page.extract_text() or "")
        txt_path.write_text("\n\n".join(pages), encoding="utf-8")
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
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    convert_txt = not args.no_txt
    try:
        stock = resolve_stock_info(args.stock_code)
        announcements = query_announcements(stock)
        selected = [select_annual_report(announcements), select_latest_periodic_report(announcements)]
        reports = [
            handle_report(stock, item, Path(args.output_root), convert_txt, args.overwrite, args.dry_run)
            for item in selected
        ]
        print_summary(stock, reports)
        return 0
    except Exception as exc:  # noqa: BLE001 - CLI reports actionable errors.
        print(f"错误: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
