"""Offline regression tests for skill discovery and local-link management."""

import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "skillctl"
MODULE = runpy.run_path(str(SCRIPT), run_name="skillctl_tests")


class SkillctlTests(unittest.TestCase):
    """Exercise the executable against an isolated catalog and Git project."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="skillctl-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.catalog = self.root / "catalog"
        self.project = self.root / "project"
        self.catalog.mkdir()
        self.project.mkdir()
        subprocess.run(["git", "init", "-q", str(self.project)], check=True)
        excludes = self.root / "empty-excludes"
        excludes.touch()
        self.git("config", "core.excludesFile", str(excludes))
        self.target = self.project / ".opencode" / "skills"
        self.skill(self.catalog / "workflows" / "review", "review", True, ["resolver"])
        self.skill(self.catalog / "shared" / "resolver", "resolver", requires=["vocabulary"])
        self.skill(self.catalog / "shared" / "vocabulary", "vocabulary", description="Context. " * 20)

    def git(self, *arguments):
        """Run Git in the disposable project.

        :param arguments: Git arguments.
        :return: Captured process result.
        """
        return subprocess.run(["git", "-C", str(self.project), *arguments],
                              text=True, capture_output=True, check=True)

    def skill(self, directory, name, manual=False, requires=(), description="Useful workflow."):
        """Write a fixture skill.

        :param directory: Fixture directory.
        :param name: Skill name.
        :param manual: Whether invocation is manual.
        :param requires: Dependency names.
        :param description: Full description.
        :return: Fixture entrypoint path.
        """
        directory.mkdir(parents=True, exist_ok=True)
        lines = ["---", f"name: {name}", f"description: {json.dumps(description, ensure_ascii=False)}"]
        if manual:
            lines.append("disable-model-invocation: true")
        if requires:
            lines.extend(["metadata:", "  requires:", *(f"    - {item}" for item in requires)])
        path = directory / "SKILL.md"
        path.write_text("\n".join([*lines, "---", "", "Workflow.", ""]), encoding="utf-8")
        return path

    def command(self, *arguments, code=0):
        """Run the CLI with isolated paths and assert its exit status.

        :param arguments: Subcommand and options.
        :param code: Expected exit status.
        :return: Captured process result.
        """
        result = subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "--catalog", str(self.catalog),
             "--project", str(self.project), *arguments],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result

    def parse(self, header):
        """Parse fixture frontmatter.

        :param header: Frontmatter source, including delimiters.
        :return: Parsed metadata.
        """
        path = self.root / "SKILL.md"
        path.write_text(header, encoding="utf-8")
        return MODULE["read_frontmatter"](path)

    def ignore_links(self):
        """Ignore the disposable project's skill installation directory."""
        (self.project / ".gitignore").write_text(".opencode/skills/\n", encoding="utf-8")

    def test_double_quoted_description(self):
        description = 'Say "hello": # literally.'
        data = self.parse(f"---\nname: sample\ndescription: {json.dumps(description)}\n---\n")
        self.assertEqual(data["description"], description)

    def test_single_quoted_description(self):
        data = self.parse("---\nname: sample\ndescription: 'It''s concise: 清楚。' # note\n---\n")
        self.assertEqual(data["description"], "It's concise: 清楚。")

    def test_requires_and_existing_scalar_metadata(self):
        data = self.parse('---\nname: sample\ndescription: Clear text\nversion: 1.0.0\n'
                          'metadata:\n  status: active\n  requires:\n    - first\n    - "second"\n---\n')
        self.assertEqual(data["requires"], ["first", "second"])
        self.assertFalse(data["manual"])

    def test_folded_description_used_by_catalog(self):
        data = self.parse("---\nname: sample\ndescription: >-\n  First line\n  second line.\n---\n")
        self.assertEqual(data["description"], "First line second line.")
        data = self.parse("---\nname: sample\ndescription: >-\n  First paragraph.\n\n  Second paragraph.\n---\n")
        self.assertEqual(data["description"], "First paragraph.\nSecond paragraph.")

    def test_missing_required_fields(self):
        for header in ("name: sample", "description: Something", "name: sample\ndescription:"):
            with self.subTest(header=header):
                with self.assertRaises(MODULE["SkillError"]) as caught:
                    self.parse(f"---\n{header}\n---\n")
                self.assertIn(str(self.root / "SKILL.md"), str(caught.exception))

    def test_invalid_headers_are_errors_with_paths(self):
        headers = [
            "name: sample\ndescription: Missing delimiters",
            "---\nname: sample\ndescription: Missing close",
            "---\nname: sample\nname: duplicate\ndescription: Text\n---",
            '---\nname: sample\ndescription: "Unclosed\n---',
            "---\nname: sample\ndescription: Text\ndisable-model-invocation: maybe\n---",
            '---\nname: sample\ndescription: Text\ndisable-model-invocation: "true"\n---',
            "---\nname: sample\ndescription: Text\nmetadata:\n  requires: [other]\n---",
            "---\nname: sample\ndescription: Text\nmetadata:\n  requires:\n   - other\n---",
            "---\nname: sample\ndescription: Text\nmetadata:\n\trequires:\n---",
            "---\nname: sample\ndescription: Text\nunknown:\n  nested: text\n---",
            "---\nname: ../escape\ndescription: Text\n---",
        ]
        for header in headers:
            with self.subTest(header=header):
                with self.assertRaises(MODULE["SkillError"]) as caught:
                    self.parse(header)
                self.assertIn(str(self.root / "SKILL.md"), str(caught.exception))

    def test_list_does_not_silently_skip_bad_frontmatter(self):
        path = self.catalog / "shared" / "resolver" / "SKILL.md"
        path.write_text("broken", encoding="utf-8")
        result = self.command("list", "--manual", code=1)
        self.assertIn(str(path), result.stderr)

    def test_list_manual_filter(self):
        rows = json.loads(self.command("list", "--manual", "--json").stdout)
        self.assertEqual([row["name"] for row in rows], ["review"])
        self.assertEqual(rows[0]["category"], "workflows")
        self.assertEqual(rows[0]["requires"], ["resolver"])
        self.assertEqual(rows[0]["invocation"], "manual")

    def test_list_installed_filter(self):
        self.command("install", "vocabulary")
        rows = json.loads(self.command("list", "--installed", "--json").stdout)
        self.assertEqual([row["name"] for row in rows], ["vocabulary"])
        self.assertTrue(rows[0]["installed"])

    def test_list_external_directory_and_link(self):
        self.skill(self.target / "local", "local", True)
        outside = self.root / "outside"
        self.skill(outside, "outside", True)
        (self.target / "outside").symlink_to(outside, target_is_directory=True)
        rows = json.loads(self.command("list", "--manual", "--installed", "--json").stdout)
        self.assertEqual({row["name"] for row in rows}, {"local", "outside"})
        self.assertTrue(all(row["external"] and row["category"] == "external" for row in rows))
        text = self.command("list", "--installed").stdout
        self.assertIn("external", text)

    def test_list_description_truncation(self):
        rows = json.loads(self.command("list", "--json").stdout)
        row = next(item for item in rows if item["name"] == "vocabulary")
        self.assertEqual(len(row["description"]), 100)

    def test_install_relative_links_and_recursive_dependencies(self):
        result = self.command("install", "review")
        self.assertLess(result.stdout.index("LINK vocabulary:"), result.stdout.index("LINK resolver:"))
        self.assertLess(result.stdout.index("LINK resolver:"), result.stdout.index("LINK review:"))
        for name, category in (("review", "workflows"), ("resolver", "shared"), ("vocabulary", "shared")):
            link = self.target / name
            self.assertTrue(link.is_symlink())
            self.assertFalse(Path(os.readlink(link)).is_absolute())
            self.assertEqual(link.resolve(), self.catalog / category / name)
        self.assertIn("new session", result.stdout)

    def test_install_idempotence(self):
        self.command("install", "review")
        before = {path.name: path.lstat().st_ino for path in self.target.iterdir()}
        result = self.command("install", "review")
        self.assertEqual(result.stdout.count("SKIP "), 3)
        self.assertEqual(before, {path.name: path.lstat().st_ino for path in self.target.iterdir()})

    def test_install_preflights_directory_conflict(self):
        (self.target / "review").mkdir(parents=True)
        result = self.command("install", "review", code=1)
        self.assertIn("conflict", result.stderr)
        self.assertFalse((self.target / "resolver").exists())

    def test_install_refuses_wrong_link(self):
        self.target.mkdir(parents=True)
        other = self.root / "different"
        other.mkdir()
        (self.target / "review").symlink_to(other, target_is_directory=True)
        result = self.command("install", "review", code=1)
        self.assertIn("conflict", result.stderr)
        self.assertEqual((self.target / "review").resolve(), other)

    def test_install_dry_run_writes_nothing(self):
        result = self.command("install", "review", "--dry-run")
        self.assertEqual(result.stdout.count("WOULD LINK "), 3)
        self.assertFalse((self.project / ".opencode").exists())

    def test_install_unknown_dependency_preflights(self):
        self.skill(self.catalog / "workflows" / "review", "review", True, ["absent"])
        self.command("install", "review", code=1)
        self.assertFalse(self.target.exists())

    def test_dependency_cycle_preflights(self):
        self.skill(self.catalog / "shared" / "vocabulary", "vocabulary", requires=["review"])
        self.assertIn("cycle", self.command("install", "review", code=1).stderr)
        self.assertFalse(self.target.exists())

    def test_git_tracking_warning_and_doctor_nonzero(self):
        result = self.command("install", "review")
        self.assertIn("WARNING:", result.stderr)
        self.assertIn("/.opencode/skills/", result.stderr)
        self.assertFalse((self.project / ".gitignore").exists())
        data = json.loads(self.command("doctor", "--json", code=1).stdout)
        self.assertFalse(data["ok"])
        self.assertTrue(data["warnings"])

    def test_ignored_links_do_not_warn(self):
        self.ignore_links()
        result = self.command("install", "review")
        self.assertNotIn("WARNING:", result.stderr)
        self.assertIn("doctor: OK", self.command("doctor").stdout)

    def test_already_tracked_link_still_warns_after_ignore(self):
        self.command("install", "vocabulary")
        self.git("add", ".opencode/skills/vocabulary")
        self.ignore_links()
        result = self.command("install", "vocabulary")
        self.assertIn("already tracked", result.stderr)
        self.assertIn("do not untrack", result.stderr)

    def test_non_git_project_skips_tracking_check(self):
        project = self.root / "non-git-project"
        project.mkdir()
        result = self.command("install", "review", "--project", str(project))
        self.assertNotIn("WARNING:", result.stderr)
        self.command("doctor", "--project", str(project))

    def test_target_override_and_common_options_after_subcommand(self):
        self.command("install", "review", "--target", "custom/skills")
        self.assertTrue((self.project / "custom" / "skills" / "review").is_symlink())
        self.assertFalse(self.target.exists())
        rows = json.loads(self.command("list", "--installed", "--json", "--target", "custom/skills").stdout)
        self.assertEqual(len(rows), 3)

    def test_symlinked_target_uses_physical_relative_paths_and_checks_ancestor(self):
        outside = self.root / "shared-target"
        outside.mkdir()
        self.target.parent.mkdir(parents=True)
        self.target.symlink_to(outside, target_is_directory=True)
        result = self.command("install", "review")
        self.assertEqual((self.target / "review").resolve(), self.catalog / "workflows" / "review")
        self.assertFalse(Path(os.readlink(self.target / "review")).is_absolute())
        self.assertIn(f"{self.target}: not ignored", result.stderr)
        self.assertIn("Suggested ignore rule: /.opencode/skills;", result.stderr)
        (self.project / ".gitignore").write_text(".opencode/skills\n", encoding="utf-8")
        self.command("doctor")

    def test_remove_dependency_protection_and_force(self):
        self.command("install", "review")
        result = self.command("remove", "resolver", code=1)
        self.assertIn("review requires resolver", result.stderr)
        self.assertTrue((self.target / "resolver").is_symlink())
        self.command("remove", "resolver", "--force")
        self.assertFalse((self.target / "resolver").exists())
        self.assertTrue((self.target / "review").is_symlink())

    def test_remove_dependents_together(self):
        self.command("install", "review")
        self.command("remove", "review", "resolver", "vocabulary")
        self.assertEqual(list(self.target.iterdir()), [])

    def test_remove_dry_run(self):
        self.command("install", "review")
        result = self.command("remove", "review", "--dry-run")
        self.assertIn("WOULD REMOVE", result.stdout)
        self.assertTrue((self.target / "review").is_symlink())

    def test_remove_refuses_ordinary_directory(self):
        self.skill(self.target / "review", "review", True)
        self.command("remove", "review", "--force", code=1)
        self.assertTrue((self.target / "review" / "SKILL.md").is_file())

    def test_remove_refuses_external_link_and_traversal(self):
        outside = self.root / "outside"
        self.skill(outside, "outside")
        self.target.mkdir(parents=True)
        (self.target / "outside").symlink_to(outside, target_is_directory=True)
        self.command("remove", "outside", "--force", code=1)
        self.command("remove", "../outside", "--force", code=1)
        self.assertTrue((self.target / "outside").is_symlink())

    def test_doctor_broken_link(self):
        self.target.mkdir(parents=True)
        (self.target / "broken").symlink_to(self.root / "missing")
        data = json.loads(self.command("doctor", "--json", code=1).stdout)
        self.assertTrue(any("broken link" in item for item in data["errors"]))

    def test_doctor_missing_dependency(self):
        self.command("install", "review")
        (self.target / "resolver").unlink()
        data = json.loads(self.command("doctor", "--json", code=1).stdout)
        self.assertTrue(any("missing dependency resolver" in item for item in data["errors"]))

    def test_doctor_duplicate_names(self):
        self.skill(self.target / "one", "duplicate")
        self.skill(self.target / "two", "duplicate")
        data = json.loads(self.command("doctor", "--json", code=1).stdout)
        self.assertTrue(any("duplicate installed name" in item for item in data["errors"]))

    def test_doctor_malformed_installed_header(self):
        path = self.skill(self.target / "bad", "bad")
        path.write_text("not frontmatter", encoding="utf-8")
        data = json.loads(self.command("doctor", "--json", code=1).stdout)
        self.assertTrue(any(str(path) in item for item in data["errors"]))

    def test_doctor_malformed_catalog_header(self):
        path = self.catalog / "shared" / "resolver" / "SKILL.md"
        path.write_text("invalid", encoding="utf-8")
        data = json.loads(self.command("doctor", "--json", code=1).stdout)
        self.assertTrue(any(str(path) in item for item in data["errors"]))

    def test_doctor_counts_full_auto_descriptions(self):
        self.ignore_links()
        self.command("install", "review")
        data = json.loads(self.command("doctor", "--json").stdout)
        self.assertEqual(data["auto_description_characters"], len("Useful workflow.") + len("Context. " * 20))
        self.assertEqual(data["installed_count"], 3)

    def test_catalog_excludes_submodules_and_git_internals(self):
        hidden = self.skill(self.catalog / "nested" / "vendor" / "deeper", "hidden")
        hidden.write_text("invalid", encoding="utf-8")
        (self.catalog / ".gitmodules").write_text(
            '[submodule "vendor"]\n  path = nested/vendor\n  url = unused\n', encoding="utf-8",
        )
        self.skill(self.catalog / ".git" / "hidden", "internal")
        self.skill(self.catalog / "a" / "b" / "c" / "deep", "deep")
        rows = json.loads(self.command("list", "--json").stdout)
        self.assertEqual({row["name"] for row in rows}, {"review", "resolver", "vocabulary", "deep"})
        self.assertEqual(next(row for row in rows if row["name"] == "deep")["category"], "a/b/c")

    def test_catalog_duplicate_names_are_errors(self):
        self.skill(self.catalog / "another" / "review", "review")
        self.assertIn("duplicate catalog name", self.command("list", code=1).stderr)

    def test_default_catalog_follows_script_realpath(self):
        destination = self.catalog / "meta" / "router" / "scripts" / "skillctl"
        destination.parent.mkdir(parents=True)
        shutil.copy2(SCRIPT, destination)
        subprocess.run(["git", "init", "-q", str(self.catalog)], check=True)
        link = self.root / "linked-tool"
        link.symlink_to(destination)
        result = subprocess.run(
            [sys.executable, "-B", str(link), "--project", str(self.project), "list", "--json"],
            cwd=self.project, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)), 3)

    def test_help_and_executable_bit(self):
        self.assertTrue(os.access(SCRIPT, os.X_OK))
        result = self.command("--help")
        for text in ("--catalog", "--project", "--target", "--manual", "--installed",
                     "--json", "--dry-run", "--force", "first 100", "external", ".gitignore"):
            self.assertIn(text, result.stdout)


if __name__ == "__main__":
    unittest.main()
