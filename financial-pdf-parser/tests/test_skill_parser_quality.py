import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from parse_financial_pdf import assign_merged_table_ids, assign_title_by_bbox, build_analysis_context, confidence_proxy, infer_table_unit, merge_continued_tables, normalize_table_section


def test_title_uses_table_bbox_proximity():
    lines = [
        {"text": "母公司利润表", "bbox": [55, 40, 200, 55]},
        {"text": "合并现金流量表", "bbox": [55, 740, 200, 755]},
    ]
    assert assign_title_by_bbox([55, 70, 540, 700], lines) == "母公司利润表"


def test_unit_uses_nearby_table_context():
    lines = [{"text": "单位：元", "bbox": [55, 60, 120, 75]}, {"text": "实收资本（或股本）", "bbox": [55, 500, 200, 515]}]
    assert infer_table_unit([55, 80, 540, 700], lines, rows=[["实收资本（或股本）", 1]]) == "元"


def test_profit_statement_continuation_unit_is_money_not_per_share():
    lines = [{"text": "（一）基本每股收益(元/股)", "bbox": [55, 40, 200, 55]}]
    rows = [["其中：利息费用", None, 643464.68, 121883.83]]
    assert infer_table_unit([55, 70, 540, 700], lines, rows=rows) == "元"


def test_cross_page_statement_merge():
    tables = [
        {"table_id": "t1", "title": "合并资产负债表", "page_start": 1, "page_end": 1, "columns": ["项目", "附注", "2025", "2024"], "rows": [["项目", "附注", "2025", "2024"], ["货币资金", None, 1, 2]], "quality_flags": []},
        {"table_id": "t2", "title": None, "page_start": 2, "page_end": 2, "columns": ["存货", "七", "3", "4"], "rows": [["存货", "七", 3, 4]], "quality_flags": []},
    ]
    merged = merge_continued_tables(tables)
    assert len(merged) == 1
    assert "cross_page_merged" in merged[0]["quality_flags"]


def test_cross_page_non_recurring_items_merge():
    tables = [
        {"table_id": "t1", "title": "非经常性损益项目及金额", "page_start": 1, "page_end": 1, "unit": "元", "columns": ["非经常性损益项目", "2025", "2024"], "rows": [["非经常性损益项目", "2025", "2024"], ["政府补助", 10, 8]], "quality_flags": []},
        {"table_id": "t2", "title": None, "page_start": 2, "page_end": 2, "unit": "元", "columns": ["除上述各项之外", "1", "2"], "rows": [["除上述各项之外", 1, 2], ["合计", 11, 10]], "quality_flags": []},
    ]
    merged = merge_continued_tables(tables)
    assert len(merged) == 1
    assert merged[0]["columns"] == ["非经常性损益项目", "2025", "2024"]
    assert merged[0]["rows"][-1][0] == "合计"


def test_statement_section_and_confidence_are_normalized():
    assert normalize_table_section("合并现金流量表", "五、其他综合收益的税后净额") == "二、财务报表"
    assert confidence_proxy([["项目", "2025"], ["营业收入", 100.0]], ["项目", "2025"], [1, 2, 3, 4]) > 0


def test_analysis_context_points_downstream_skills_to_merged_validated_tables():
    parsed = {
        "source_file": "测试公司-2025年报.pdf",
        "tables": [{"table_id": "table_0001"}],
        "merged_tables": [
            {"table_id": "merged_table_0001", "title": "合并资产负债表", "page_start": 10, "page_end": 12, "quality_flags": ["cross_page_merged"]},
            {"table_id": "merged_table_0002", "title": "合并利润表", "page_start": 13, "page_end": 14, "quality_flags": []},
        ],
        "chunks": [{"chunk_id": "text_0001"}],
    }
    checks = [{"check": "pct_change", "status": "pass"}, {"check": "cash_ending_tie_out", "status": "pass"}]
    context = build_analysis_context(parsed, checks)
    assert "validation failed: 0" in context
    assert "Use `tables_merged/` first" in context
    assert "tables_merged/merged_table_0001.json" in context
    assert "合并资产负债表" in context


def test_assign_merged_table_ids_matches_written_file_names():
    tables = [{"table_id": "table_0007", "title": "合并资产负债表", "rows": []}]
    assigned = assign_merged_table_ids(tables)
    assert assigned[0]["table_id"] == "merged_table_0001"
    assert tables[0]["table_id"] == "table_0007"
