#!/usr/bin/env python3
"""Mechanical semantic guards for the released v3 contract."""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


required = {
    "SKILL.md": ["无法拆分", "研究状态门", "负基期", "恢复研究", "既非稳态FCF，也非数学上下界", "设计与有效产能"],
    "references/capabilities/three-statement-linkage.md": ["无法拆分", "保守现金余量代理", "不是数学下界", "设计产能", "有效产能", "利用率", "良率", "闲置/停建", "单位成本", "转固后的折旧和减值", "资本承诺"],
    "references/capabilities/leverage-stress.md": ["资本承诺", "担保", "表外", "受限", "专项募集", "少数股东", "最低运营现金", "租赁", "未来12个月", "利息保障倍数", "现金口径辅助指标", "已承诺", "续作", "再融资"],
    "references/capabilities/anomaly-triage.md": ["低毛利贸易", "经营性应付", "应付票据", "持续现金创造", "账龄迁移", "逾期", "保理", "追索", "期后回款", "设计/有效产能", "恢复条件"],
    "references/capabilities/basis-and-comparison.md": ["基期为负", "亏损收窄"],
    "references/capabilities/cash-earnings-quality.md": ["账龄迁移", "逾期余额", "保理", "追索权", "期后回款"],
    "references/formulas.md": ["EBIT / 利息费用", "现金利息覆盖辅助指标", "扣资本开支前现金参考量", "扣全部现金购建支出后的保守现金余量代理", "不得称为下界", "本期仍为负且没有跨零"]
}

errors: list[str] = []
check_count = 0
for path, tokens in required.items():
    content = read(path)
    for token in tokens:
        check_count += 1
        if token not in content:
            errors.append(f"{path}: missing {token}")

for path in ["SKILL.md", "references/capabilities/three-statement-linkage.md", "references/formulas.md"]:
    content = read(path)
    for phrase in ["保守代理/下界", "下界/保守代理", "cash surplus proxy or lower bound", "upper/lower bounds"]:
        check_count += 1
        if phrase in content:
            errors.append(f"{path}: forbidden phrase {phrase}")

tests = json.loads(read("test-prompts.json"))
test_ids = {item["id"] for item in tests["test_cases"]}
for test_id in {"proxy-not-lower-bound", "capacity-utilization", "earmarked-cash", "receivables-aging"}:
    check_count += 1
    if test_id not in test_ids:
        errors.append(f"test-prompts.json: missing {test_id}")

bundle = json.loads(read("references/capability-bundle.json"))
check_count += 1
if len(bundle["capabilities"]) != 7:
    errors.append("capability-bundle.json: expected 7 capabilities")
check_count += 1
if any(item["status"] != "draft" for item in bundle["capabilities"]):
    errors.append("capability-bundle.json: all capabilities must remain draft")
bundle_text = json.dumps(bundle, ensure_ascii=False)
for token in ("candidate 98.0", "old skill 97.0", "no skill 96.5"):
    check_count += 1
    if token not in bundle_text:
        errors.append(f"capability-bundle.json: released v3 aggregate token missing: {token}")
check_count += 1
if "behavioral-evaluation" not in bundle["quality"]["passed_gates"] or any(
    item["severity"] == "blocking" for item in bundle["quality"]["open_issues"]
):
    errors.append("capability-bundle.json: package-level behavioral release gate is not closed")

result = {"check_count": check_count, "failed_count": len(errors), "errors": errors}
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(0 if not errors else 1)
