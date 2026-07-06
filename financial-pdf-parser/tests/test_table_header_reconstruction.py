import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from financial_normalization import reconstruct_headers


def test_table_header_reconstruction():
    rows = [["项目", "2024年", ""], ["", "调整前", "调整后"]]
    assert reconstruct_headers(rows) == ["项目", "2024年调整前", "2024年调整后"]
