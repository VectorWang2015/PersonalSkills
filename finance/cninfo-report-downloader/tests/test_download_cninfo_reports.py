import importlib.util
import sys
import tempfile
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "download_cninfo_reports.py"


def load_module():
    if not SCRIPT_PATH.exists():
        raise AssertionError(f"script not found: {SCRIPT_PATH}")
    spec = importlib.util.spec_from_file_location("download_cninfo_reports", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class CninfoDownloaderTests(unittest.TestCase):
    def test_transient_network_error_is_retried(self):
        module = load_module()
        response = object()
        request = urllib.request.Request("https://example.invalid")

        with mock.patch.object(
            module.urllib.request,
            "urlopen",
            side_effect=[urllib.error.URLError("temporary"), response],
        ) as urlopen, mock.patch.object(module.time, "sleep") as sleep:
            result = module.open_with_retry(request, timeout=1, attempts=2)

        self.assertIs(result, response)
        self.assertEqual(urlopen.call_count, 2)
        sleep.assert_called_once_with(0.5)

    def test_market_for_code_maps_a_share_prefixes(self):
        module = load_module()

        self.assertEqual(module.market_for_code("600219"), ("sse", "sse"))
        self.assertEqual(module.market_for_code("002901"), ("szse", "szse"))
        self.assertEqual(module.market_for_code("301078"), ("szse", "szse"))
        self.assertEqual(module.market_for_code("430418"), ("bj", "bj"))

        with self.assertRaises(ValueError):
            module.market_for_code("123456")

    def test_filter_selects_full_annual_report_not_summary(self):
        module = load_module()
        announcements = [
            {"announcementTitle": "2025年年度报告摘要", "announcementTime": 1777000000000},
            {"announcementTitle": "2025年年度报告", "announcementTime": 1777000000000},
            {"announcementTitle": "2025年年度报告（英文版）", "announcementTime": 1777000000000},
        ]

        selected = module.select_annual_report(announcements)

        self.assertEqual(selected["announcementTitle"], "2025年年度报告")

    def test_annual_report_prefers_latest_report_year_over_older_correction(self):
        module = load_module()
        # These are synthetic report years.  The invariant must survive calendar
        # rollovers: a late correction to an older report must never displace the
        # newest report period.
        for latest_year in (2025, 2026, 2031):
            with self.subTest(latest_year=latest_year):
                older_year = latest_year - 1
                announcements = [
                    {
                        "announcementTitle": f"示例公司{older_year}年年度报告（更正后）",
                        "announcementTime": 9_999,
                    },
                    {
                        "announcementTitle": f"{latest_year}年年度报告",
                        "announcementTime": 1_000,
                    },
                    {
                        "announcementTitle": f"{latest_year}年年度报告摘要",
                        "announcementTime": 1_000,
                    },
                ]

                selected = module.select_annual_report(announcements)

                self.assertEqual(selected["announcementTitle"], f"{latest_year}年年度报告")

    def test_annual_report_prefers_same_year_correction_over_original(self):
        module = load_module()
        announcements = [
            {"announcementTitle": "2025年年度报告", "announcementTime": 1777392000000},
            {"announcementTitle": "2025年年度报告（更正后）", "announcementTime": 1782471000000},
        ]

        selected = module.select_annual_report(announcements)

        self.assertEqual(selected["announcementTitle"], "2025年年度报告（更正后）")

    def test_annual_report_excludes_newer_half_year_report(self):
        module = load_module()
        announcements = [
            {"announcementTitle": "2025年年度报告", "announcementTime": 1777392000000},
            {"announcementTitle": "2026年年度报告", "announcementTime": 1808928000000},
            {"announcementTitle": "2026年半年度报告（更正后）", "announcementTime": 1814000000000},
        ]

        selected = module.select_annual_report(announcements)

        self.assertEqual(selected["announcementTitle"], "2026年年度报告")

    def test_filter_selects_latest_non_annual_periodic_report(self):
        module = load_module()
        announcements = [
            {"announcementTitle": "2026年半年度报告", "announcementTime": 1785000000000},
            {"announcementTitle": "2026年第三季度报告", "announcementTime": 1793000000000},
            {"announcementTitle": "2026年第三季度报告摘要", "announcementTime": 1793000000001},
            {"announcementTitle": "2025年年度报告", "announcementTime": 1777000000000},
        ]

        selected = module.select_latest_periodic_report(announcements)

        self.assertEqual(selected["announcementTitle"], "2026年第三季度报告")

    def test_periodic_report_allows_full_corrected_report(self):
        module = load_module()
        announcements = [
            {"announcementTitle": "2026年第一季度报告", "announcementTime": 1777000000000},
            {"announcementTitle": "2026年第一季度报告（更正后）", "announcementTime": 1778000000000},
            {"announcementTitle": "2026年第一季度报告更正公告", "announcementTime": 1779000000000},
        ]

        selected = module.select_periodic_report(announcements, "q1")

        self.assertEqual(selected["announcementTitle"], "2026年第一季度报告（更正后）")

    def test_report_type_can_select_interim_only(self):
        module = load_module()
        announcements = [
            {"announcementTitle": "2025年年度报告", "announcementTime": 1},
            {"announcementTitle": "2026年半年度报告", "announcementTime": 2},
            {"announcementTitle": "2026年第三季度报告", "announcementTime": 3},
        ]

        selected, missing = module.select_requested_reports(announcements, "interim")

        self.assertEqual([item["announcementTitle"] for item in selected], ["2026年半年度报告"])
        self.assertEqual(missing, [])

    def test_both_mode_keeps_available_report_and_reports_missing_type(self):
        module = load_module()
        announcements = [{"announcementTitle": "2025年年度报告", "announcementTime": 1}]

        selected, missing = module.select_requested_reports(announcements, "both")

        self.assertEqual([item["announcementTitle"] for item in selected], ["2025年年度报告"])
        self.assertEqual(missing, ["latest-periodic"])

    def test_query_announcements_follows_pagination_and_deduplicates(self):
        module = load_module()
        stock = module.StockInfo("600219", "南山铝业", "gssh0600219", "sse", "sse")
        first = {"announcementId": "a1", "announcementTitle": "2025年年度报告"}
        second = {"announcementId": "a2", "announcementTitle": "2026年第一季度报告"}
        payloads = [
            {"announcements": [first], "totalpages": 2, "hasMore": True},
            {"announcements": [first, second], "totalpages": 2, "hasMore": False},
        ]

        with mock.patch.object(module, "request_json", side_effect=payloads) as request:
            announcements = module.query_announcements(stock, page_size=1, max_pages=3)

        self.assertEqual(announcements, [first, second])
        self.assertEqual([call.args[1]["pageNum"] for call in request.call_args_list], ["1", "2"])

    def test_download_rejects_non_pdf_without_creating_target(self):
        module = load_module()

        class FakeResponse:
            headers = {"Content-Type": "text/html"}

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return None

            def read(self):
                return b"<html>rate limited</html>"

        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "report.pdf"
            with mock.patch.object(module, "open_with_retry", return_value=FakeResponse()):
                with self.assertRaisesRegex(RuntimeError, "不是有效 PDF"):
                    module.download_file("https://example.invalid/report.pdf", target, overwrite=False)

            self.assertFalse(target.exists())

    def test_invalid_overwrite_keeps_existing_valid_pdf(self):
        module = load_module()

        class FakeResponse:
            headers = {"Content-Type": "text/html"}

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return None

            def read(self):
                return b"<html>temporary error</html>"

        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "report.pdf"
            target.write_bytes(b"%PDF-1.7\nexisting")

            with mock.patch.object(module, "open_with_retry", return_value=FakeResponse()):
                with self.assertRaisesRegex(RuntimeError, "不是有效 PDF"):
                    module.download_file("https://example.invalid/report.pdf", target, overwrite=True)

            self.assertEqual(target.read_bytes(), b"%PDF-1.7\nexisting")

    def test_download_validates_then_atomically_writes_pdf(self):
        module = load_module()

        class FakeResponse:
            headers = {"Content-Type": "application/pdf"}

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return None

            def read(self):
                return b"%PDF-1.7\nexample"

        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "report.pdf"
            with mock.patch.object(module, "open_with_retry", return_value=FakeResponse()):
                status = module.download_file("https://example.invalid/report.pdf", target, overwrite=False)

            self.assertEqual(status, "downloaded")
            self.assertEqual(target.read_bytes(), b"%PDF-1.7\nexample")
            self.assertFalse(list(target.parent.glob("*.part")))

    def test_text_conversion_falls_back_to_pdftotext(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as temporary:
            pdf_path = Path(temporary) / "report.pdf"
            txt_path = Path(temporary) / "report.txt"
            pdf_path.write_bytes(b"%PDF-1.7\nexample")
            completed = mock.Mock(stdout="第一页\n第二页\n")

            with mock.patch.dict(sys.modules, {"pdfplumber": None}), mock.patch.object(
                module.shutil, "which", return_value="/usr/bin/pdftotext"
            ), mock.patch.object(module.subprocess, "run", return_value=completed) as run:
                status = module.convert_pdf_to_txt(pdf_path, txt_path, overwrite=False)

            self.assertEqual(status, "converted")
            self.assertEqual(txt_path.read_text(encoding="utf-8"), "第一页\n第二页\n")
            run.assert_called_once_with(
                ["/usr/bin/pdftotext", "-layout", str(pdf_path), "-"],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertFalse(list(txt_path.parent.glob("*.part")))

    def test_failed_text_overwrite_preserves_existing_file(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as temporary:
            pdf_path = Path(temporary) / "report.pdf"
            txt_path = Path(temporary) / "report.txt"
            pdf_path.write_bytes(b"%PDF-1.7\nexample")
            txt_path.write_text("existing", encoding="utf-8")

            with mock.patch.object(module, "extract_pdf_text", side_effect=RuntimeError("broken PDF")):
                status = module.convert_pdf_to_txt(pdf_path, txt_path, overwrite=True)

            self.assertEqual(status, "failed: broken PDF")
            self.assertEqual(txt_path.read_text(encoding="utf-8"), "existing")
            self.assertFalse(list(txt_path.parent.glob("*.part")))

    def test_report_period_parses_common_titles(self):
        module = load_module()

        self.assertEqual(module.parse_report_period("2025年年度报告"), ("2025年报", "2025"))
        self.assertEqual(module.parse_report_period("2026年第一季度报告"), ("2026Q1", "2026Q1"))
        self.assertEqual(module.parse_report_period("2026年半年度报告"), ("2026H1", "2026H1"))
        self.assertEqual(module.parse_report_period("2026年第三季度报告"), ("2026Q3", "2026Q3"))

    def test_target_paths_use_safe_company_name_and_period_dir(self):
        module = load_module()

        pdf_path, txt_path = module.target_paths(Path("raw/reports"), "南山/铝业", "2025年报", "2025")

        self.assertEqual(pdf_path, Path("raw/reports/2025/南山铝业-2025年报.pdf"))
        self.assertEqual(txt_path, Path("raw/reports/2025/南山铝业-2025年报.txt"))


if __name__ == "__main__":
    unittest.main()
