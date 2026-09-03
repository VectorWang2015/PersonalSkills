from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_source_manifest.py"


class BuildSourceManifestTests(unittest.TestCase):
    def run_script(self, *arguments: object, cwd: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *(str(argument) for argument in arguments)],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_builds_manifest_for_multiple_sources_without_changing_them(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = root / "chapter.txt"
            second = root / "appendix.PDF"
            first_bytes = "第一章\n".encode()
            second_bytes = b"%PDF-test\x00"
            first.write_bytes(first_bytes)
            second.write_bytes(second_bytes)
            unrelated = root / "keep.me"
            unrelated.write_text("unchanged", encoding="utf-8")
            output = root / "manifest.json"

            result = self.run_script(
                first,
                second,
                "--base-dir",
                root,
                "--title",
                "示例书",
                "--author",
                "示例作者",
                "--version",
                "第三版",
                "--output",
                output,
                cwd=root,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertEqual(first.read_bytes(), first_bytes)
            self.assertEqual(second.read_bytes(), second_bytes)
            self.assertEqual(unrelated.read_text(encoding="utf-8"), "unchanged")

            manifest = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(manifest["schema_version"], 1)
            self.assertEqual(manifest["title"], "示例书")
            self.assertEqual(manifest["author"], "示例作者")
            self.assertEqual(manifest["version"], "第三版")
            self.assertIs(manifest["local_paths_redacted"], False)
            self.assertEqual(manifest["base_directory"], str(root.resolve()))
            self.assertEqual(manifest["source_count"], 2)
            self.assertEqual(
                manifest["sources"],
                [
                    {
                        "absolute_path": str(first.resolve()),
                        "relative_path": "chapter.txt",
                        "sha256": hashlib.sha256(first_bytes).hexdigest(),
                        "bytes": len(first_bytes),
                        "format": "txt",
                    },
                    {
                        "absolute_path": str(second.resolve()),
                        "relative_path": "appendix.PDF",
                        "sha256": hashlib.sha256(second_bytes).hexdigest(),
                        "bytes": len(second_bytes),
                        "format": "pdf",
                    },
                ],
            )

    def test_prints_to_stdout_when_output_is_not_given(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            source.write_bytes(b"data")

            result = self.run_script(source, "--base-dir", root, cwd=root)

            self.assertEqual(result.returncode, 0, result.stderr)
            manifest = json.loads(result.stdout)
            self.assertEqual(manifest["sources"][0]["format"], "unknown")
            self.assertEqual(set(root.iterdir()), {source})

    def test_portable_manifest_redacts_all_local_absolute_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "private" / "book.txt"
            source.parent.mkdir()
            source.write_text("portable source", encoding="utf-8")

            result = self.run_script(
                source,
                "--base-dir",
                root,
                "--title",
                "Portable example",
                "--portable",
                cwd=root,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn(str(root.resolve()), result.stdout)
            manifest = json.loads(result.stdout)
            self.assertIs(manifest["local_paths_redacted"], True)
            self.assertIsNone(manifest["base_directory"])
            self.assertIsNone(manifest["sources"][0]["absolute_path"])
            self.assertEqual(manifest["sources"][0]["relative_path"], "private/book.txt")
            self.assertEqual(
                manifest["sources"][0]["sha256"],
                hashlib.sha256(b"portable source").hexdigest(),
            )
            self.assertEqual(manifest["sources"][0]["bytes"], len(b"portable source"))
            self.assertEqual(manifest["sources"][0]["format"], "txt")

    def test_missing_source_fails_without_creating_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "manifest.json"

            result = self.run_script(
                root / "missing.epub", "--output", output, cwd=root
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("does not exist", result.stderr)
            self.assertFalse(output.exists())

    def test_refuses_to_use_a_source_as_the_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "book.txt"
            original = b"do not overwrite"
            source.write_bytes(original)

            result = self.run_script(source, "--output", source, cwd=root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("must not be one of the source files", result.stderr)
            self.assertEqual(source.read_bytes(), original)

    def test_existing_output_requires_force(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "book.txt"
            source.write_text("source", encoding="utf-8")
            output = root / "manifest.json"
            output.write_text("keep this", encoding="utf-8")

            refused = self.run_script(source, "--output", output, cwd=root)

            self.assertEqual(refused.returncode, 1)
            self.assertIn("already exists", refused.stderr)
            self.assertIn("--force", refused.stderr)
            self.assertEqual(output.read_text(encoding="utf-8"), "keep this")

            replaced = self.run_script(
                source, "--output", output, "--force", cwd=root
            )

            self.assertEqual(replaced.returncode, 0, replaced.stderr)
            manifest = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(manifest["sources"][0]["absolute_path"], str(source.resolve()))


if __name__ == "__main__":
    unittest.main()
