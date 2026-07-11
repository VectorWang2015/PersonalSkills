import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from financial_validation import validate_balance_sheet, validate_pct_change
from parse_financial_pdf import ValidationIndex


def test_financial_validation():
    assert validate_balance_sheet(100, 40, 60)["status"] == "pass"


def test_validation_handles_pct_change_with_trailing_label_text():
    check = validate_pct_change(100.0, 86.5, "15.61营业收入", tolerance=0.1)

    assert check["status"] == "pass"


def test_validation_prefers_annual_table_when_labels_have_unit_suffix():
    tables = [
        {"title": "主要会计数据和财务指标", "rows": [["营业收入（元）", 2600859747.67, 2135559372.81, "21.79%"], ["归属于上市公司股东 的净利润（元）", 599631709.82, 356803430.03, "68.06%"]]},
        {"title": "分季度主要财务指标", "rows": [["营业收入", 550336243.99, 660103477.51, 665815103.16, 724604923.01], ["归属于上市公司股东 的净利润", 103101566.47, 141157195.93, 180387474.59, 174985472.83]]},
    ]
    checks = ValidationIndex(tables).run_core_checks()
    assert all(check["status"] == "pass" for check in checks)


def test_validation_handles_leading_blank_columns_and_wrapped_labels():
    tables = [
        {"title": "主要会计数据和财务指标", "rows": [[None, "营业收入（元）", None, 2952270108.43, None, 3135825731.09, None, "-5.85%"], [None, "归属于上市公司股东的", None, 165420013.21, None, 503823356.22, None, "-67.17%"], [None, "净利润（元）", None, None, None, None, None, None]]},
        {"title": "分季度主要财务指标", "rows": [[None, "营业收入", None, 622899262.79, None, 698193984.04, None, 715357228.19, None, 915819633.41], [None, "归属于上市公司股东的净利润", None, -13168062.05, None, 19323128.21, None, 25631803.47, None, 133633143.58]]},
    ]
    checks = ValidationIndex(tables).run_core_checks()
    assert all(check["status"] == "pass" for check in checks)


def test_validation_does_not_treat_balance_sheet_section_headers_as_label_continuations():
    tables = [{"title": "合并资产负债表", "rows": [[None, "资产总计", None, 100.0], [None, "流动负债：", None, None], [None, "流动负债合计", None, 30.0], [None, "非流动负债合计", None, 10.0], [None, "负债合计", None, 40.0], [None, "所有者权益：", None, None], [None, "所有者权益合计", None, 60.0]]}]
    checks = ValidationIndex(tables).run_core_checks()
    assert [c for c in checks if c["check"] == "assets_equal_liabilities_plus_equity"][0]["status"] == "pass"


def test_validation_supports_quarterly_bank_and_insurer_patterns():
    tables = [
        {"title": "主要会计数据和财务指标", "rows": [["营业收入", 178846, None, 8.44], ["资产总计", 39594197, 38358076, 3.22]]},
        {"rows": [["资产总额", 100.0], ["负债总额", 40.0], ["股东权益合计", 60.0]]},
    ]
    checks = ValidationIndex(tables).run_core_checks()
    assert [c for c in checks if c["check"] == "pct_change"][0]["status"] == "pass"
    assert [c for c in checks if c["check"] == "assets_equal_liabilities_plus_equity"][0]["status"] == "pass"


def test_validation_cash_tie_out_stays_within_same_cash_flow_table():
    tables = [
        {"title": "合并现金流量表", "rows": [["五、现金及现金等价物净(减少)/增加额", -51977], ["加：期初现金及现金等价物余额", 650224], ["六、期末现金及现金等价物余额", 598247]]},
        {"title": "母公司现金流量表", "rows": [["五、现金及现金等价物净减少额", -3724], ["加：期初现金及现金等价物余额", 9127], ["六、期末现金及现金等价物余额", 5403]]},
    ]
    cash = [c for c in ValidationIndex(tables).run_core_checks() if c["check"] == "cash_ending_tie_out"][0]
    assert cash["status"] == "pass"
