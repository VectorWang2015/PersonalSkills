from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_skill_tree.py"


class ValidateSkillTreeTests(unittest.TestCase):
    def run_script(self, root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(root), *arguments],
            text=True,
            capture_output=True,
            check=False,
        )

    def write(self, path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    def test_valid_tree_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = root / "portfolio-review"
            self.write(
                skill / "SKILL.md",
                """
                ---
                name: portfolio-review
                description: |
                  Review a portfolio when the user wants a structured risk check.
                metadata:
                  owner: research
                ---

                # Portfolio review

                Read the [method notes](references/method.md), then use
                `atomic/risk-check/SKILL.md`.
                """,
            )
            self.write(skill / "references" / "method.md", "# Method\n")
            self.write(
                skill / "atomic" / "risk-check" / "SKILL.md",
                """
                ---
                name: risk-check
                description: Check portfolio risks when concentration may be excessive.
                allowed-tools: Read
                ---

                # Risk check
                """,
            )
            test_file = skill / "atomic" / "risk-check" / "test-prompts.json"
            test_file.write_text(json.dumps({"test_cases": []}), encoding="utf-8")

            result = self.run_script(root)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("OK: validated 2 SKILL.md file(s)", result.stdout)
            self.assertIn("1 JSON file(s)", result.stdout)

    def test_template_placeholders_are_allowed_and_json_is_checked(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write(
                root / "SKILL.md",
                """
                ---
                name: example-skill
                description: A complete example.
                ---

                # Example
                """,
            )
            self.write(
                root / "templates" / "SKILL.md.template",
                """
                ---
                name: {{skill-slug}}
                description: {{description}}
                ---

                # {{title}}
                TODO: fill this during generation.
                """,
            )
            self.write(
                root / "templates" / "test-prompts.json.template",
                '{"skill": "{{skill-slug}}", "tests": []}\n',
            )

            result = self.run_script(root)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn("[PLACEHOLDER]", result.stdout)
            self.assertIn("1 JSON file(s)", result.stdout)

    def test_template_conflicts_and_invalid_json_still_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write(
                root / "SKILL.md",
                """
                ---
                name: example-skill
                description: A complete example.
                ---

                # Example
                """,
            )
            self.write(
                root / "templates" / "notes.md.template",
                """
                <<<<<<< HEAD
                {{first-version}}
                =======
                {{second-version}}
                >>>>>>> branch
                """,
            )
            self.write(
                root / "templates" / "test-prompts.json.template",
                '{"skill": {{skill-slug}}}\n',
            )

            result = self.run_script(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("[MERGE_CONFLICT]", result.stdout)
            self.assertIn("[INVALID_JSON]", result.stdout)
            self.assertNotIn("[PLACEHOLDER]", result.stdout)

    def test_reports_all_supported_validation_failures(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = root / "broken"
            self.write(
                skill / "SKILL.md",
                """
                ---
                name: Bad_Name
                description: Broken example.
                source_book: Example
                ---

                # {{TITLE}}

                [Missing notes](references/missing.md)
                Use `atomic/no-such-skill/SKILL.md`.

                <<<<<<< HEAD
                first version
                =======
                second version
                >>>>>>> branch
                """,
            )
            self.write(skill / "test-prompts.json", "{not valid json")
            self.write(
                skill / "notes.md",
                """
                # Notes

                TODO: replace this section.
                [Also missing](references/also-missing.md)
                """,
            )

            result = self.run_script(root)

            self.assertEqual(result.returncode, 1)
            for code in (
                "UNKNOWN_FRONTMATTER_KEY",
                "INVALID_NAME",
                "PLACEHOLDER",
                "MERGE_CONFLICT",
                "BROKEN_MARKDOWN_LINK",
                "BROKEN_ATOMIC_REFERENCE",
                "INVALID_JSON",
            ):
                self.assertIn(f"[{code}]", result.stdout)
            self.assertIn("FAILED:", result.stdout)
            self.assertIn("notes.md", result.stdout)

    def test_compatibility_is_not_allowed_by_default_but_can_be_opted_in(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write(
                root / "SKILL.md",
                """
                ---
                name: example-skill
                description: A complete example.
                compatibility: Requires a PDF reader.
                ---

                # Example
                """,
            )

            failed = self.run_script(root)
            passed = self.run_script(root, "--allow-key", "compatibility")

            self.assertEqual(failed.returncode, 1)
            self.assertIn("[UNKNOWN_FRONTMATTER_KEY]", failed.stdout)
            self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)

    def test_missing_root_uses_invocation_error_exit_status(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            missing = Path(temporary) / "missing"

            result = self.run_script(missing)

            self.assertEqual(result.returncode, 2)
            self.assertIn("does not exist", result.stderr)


if __name__ == "__main__":
    unittest.main()
