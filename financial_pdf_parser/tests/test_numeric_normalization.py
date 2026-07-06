import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from financial_normalization import normalize_number, repair_wrapped_amount


def test_numeric_normalization():
    assert normalize_number(repair_wrapped_amount("3,197,324,28\n8.02")) == 3197324288.02
