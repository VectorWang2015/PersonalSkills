"""只验证技能包结构与场景格式，不评价写作质量。"""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def test_frontmatter(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        header = text.split("---", 2)[1]
        fields = dict(re.findall(r"^([a-z-]+): (.+)$", header, re.M))
        self.assertEqual(set(fields), {"name", "description"})
        self.assertEqual(fields["name"], ROOT.name)
        self.assertLessEqual(len(fields["description"]), 1024)
        self.assertIn("中文", fields["description"])

    def test_package_links(self):
        for relative in ("SKILL.md", "README.md", "references/examples.md"):
            path = ROOT / relative
            text = path.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
                if re.match(r"[a-z]+://", target):
                    continue
                target = target.split("#", 1)[0]
                if not target:
                    continue
                resolved = (path.parent / target).resolve()
                self.assertTrue(resolved.is_relative_to(ROOT), target)
                self.assertTrue(resolved.is_file(), target)

    def test_regression_case_shape(self):
        data = json.loads((ROOT / "evals/cases.json").read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], 1)
        self.assertIsInstance(data["behavioral_evaluation_executed"], bool)
        cases = data["cases"]
        self.assertGreaterEqual(len(cases), 8)
        ids = [case["id"] for case in cases]
        self.assertEqual(len(ids), len(set(ids)))
        for case in cases:
            for field in ("id", "request", "input", "checks"):
                self.assertTrue(case[field], (case["id"], field))
            self.assertIsInstance(case["checks"], list)
            self.assertGreaterEqual(len(case["checks"]), 2)

    def test_reader_context_regression_cases_present(self):
        """检查场景清单不丢失；不对生成文本做词频或语言评分。"""
        data = json.loads((ROOT / "evals/cases.json").read_text(encoding="utf-8"))
        ids = {case["id"] for case in data["cases"]}
        required = {
            "abstract-body-independent-organization",
            "first-use-model-reference-context",
            "section-entry-before-formulas",
            "main-results-coverage",
            "positive-model-definition",
        }
        self.assertTrue(required.issubset(ids), required - ids)

    def test_direct_statement_regression_cases_present(self):
        """仅保护场景覆盖；句式与证据保留仍由行为试读评价。"""
        data = json.loads((ROOT / "evals/cases.json").read_text(encoding="utf-8"))
        ids = {case["id"] for case in data["cases"]}
        required = {
            "direct-statements-with-evidence-scope",
            "formal-declarative-with-genre-contrast",
            "handoff-material-to-reader-prose",
            "necessary-negative-and-safety-restraint",
        }
        self.assertTrue(required.issubset(ids), required - ids)

    def test_no_local_project_paths(self):
        for relative in ("SKILL.md", "README.md", "references/examples.md", "evals/cases.json"):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertNotRegex(
                text,
                r"(?:/(?:home|Users)/[^/\s]+/|[A-Za-z]:\\Users\\[^\\\s]+\\)",
                relative,
            )


if __name__ == "__main__":
    unittest.main()
