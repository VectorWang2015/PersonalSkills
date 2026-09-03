import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from financial_normalization import detect_unit, normalize_number, repair_wrapped_amount


def test_numeric_normalization():
    assert normalize_number(repair_wrapped_amount("3,197,324,28\n8.02")) == 3197324288.02


def test_detect_unit_supports_common_scaled_report_units():
    assert detect_unit("金额单位：人民币百万元") == "百万元"
    assert detect_unit("单位：千元") == "千元"
