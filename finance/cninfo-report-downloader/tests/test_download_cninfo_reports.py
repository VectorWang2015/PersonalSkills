import importlib.util
import sys
import unittest
from pathlib import Path


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
        announcements = [
            {"announcementTitle": "奕东电子科技股份有限公司2024年年度报告（更正后）", "announcementTime": 1782471000000},
            {"announcementTitle": "2025年年度报告", "announcementTime": 1777392000000},
            {"announcementTitle": "2025年年度报告摘要", "announcementTime": 1777392000000},
        ]

        selected = module.select_annual_report(announcements)

        self.assertEqual(selected["announcementTitle"], "2025年年度报告")

    def test_annual_report_prefers_same_year_correction_over_original(self):
        module = load_module()
        announcements = [
            {"announcementTitle": "2025年年度报告", "announcementTime": 1777392000000},
            {"announcementTitle": "2025年年度报告（更正后）", "announcementTime": 1782471000000},
        ]

        selected = module.select_annual_report(announcements)

        self.assertEqual(selected["announcementTitle"], "2025年年度报告（更正后）")

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
