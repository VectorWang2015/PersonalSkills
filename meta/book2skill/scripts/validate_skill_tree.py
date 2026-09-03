#!/usr/bin/env python3
"""Validate a directory tree containing Codex/Agent skills."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
from urllib.parse import unquote, urlsplit


DEFAULT_FRONTMATTER_KEYS = frozenset(
    {"name", "description", "license", "metadata", "allowed-tools"}
)
REQUIRED_FRONTMATTER_KEYS = frozenset({"name", "description"})
KEBAB_CASE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TOP_LEVEL_KEY = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s*(.*))?$")
MARKDOWN_LINK = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
ATOMIC_REFERENCE = re.compile(
    r"(?<![A-Za-z0-9_./-])((?:(?:\.\./)+|\./)?atomic/"
    r"[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*/SKILL\.md)"
)
CONFLICT_MARKER = re.compile(r"^(?:<{7}(?: .*)?|={7}|>{7}(?: .*)?)$")
PLACEHOLDER_PATTERNS = (
    ("template expression", re.compile(r"\{\{[^{}\n]+\}\}")),
    (
        "unfinished marker",
        re.compile(
            r"(?im)(?:\[(?:TODO|TBD|FIXME)\]|\b(?:TODO|TBD|FIXME)\s*:|"
            r"\b(?:REPLACE_ME|CHANGEME)\b)"
        ),
    ),
    (
        "placeholder token",
        re.compile(r"(?i)(?:<|\[)\s*(?:placeholder|insert[^>\]\n]*here)\s*(?:>|\])"),
    ),
)
SKIP_DIRECTORIES = frozenset({".git", ".hg", ".svn", ".venv", "node_modules", "__pycache__"})


@dataclass(frozen=True)
class Issue:
    path: Path
    line: int
    code: str
    message: str


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _display_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _iter_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root]

    files: list[Path] = []
    for current, directories, filenames in os.walk(root):
        directories[:] = sorted(
            name
            for name in directories
            if name not in SKIP_DIRECTORIES and not (Path(current) / name).is_symlink()
        )
        files.extend(Path(current) / name for name in sorted(filenames))
    return files


def _read_text(path: Path) -> tuple[str | None, Issue | None]:
    try:
        return path.read_text(encoding="utf-8-sig"), None
    except (OSError, UnicodeError) as exc:
        return None, Issue(path, 1, "READ_ERROR", str(exc))


def _unquote_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return re.split(r"\s+#", value, maxsplit=1)[0].strip()


def _validate_frontmatter(path: Path, text: str, allowed_keys: frozenset[str]) -> list[Issue]:
    issues: list[Issue] = []
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return [Issue(path, 1, "MISSING_FRONTMATTER", "SKILL.md must start with '---'")]

    closing_index = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.rstrip() == "---"),
        None,
    )
    if closing_index is None:
        return [Issue(path, 1, "UNCLOSED_FRONTMATTER", "frontmatter has no closing '---'")]

    values: dict[str, tuple[str, int]] = {}
    for index, line in enumerate(lines[1:closing_index], start=2):
        if not line.strip() or line.lstrip().startswith("#") or line[:1].isspace():
            continue
        match = TOP_LEVEL_KEY.match(line)
        if not match:
            issues.append(
                Issue(path, index, "MALFORMED_FRONTMATTER", "expected a top-level 'key: value'")
            )
            continue
        key, value = match.group(1), match.group(2) or ""
        if key in values:
            issues.append(Issue(path, index, "DUPLICATE_FRONTMATTER_KEY", f"duplicate key: {key}"))
        else:
            values[key] = (value, index)
        if key not in allowed_keys:
            issues.append(
                Issue(path, index, "UNKNOWN_FRONTMATTER_KEY", f"top-level key is not allowed: {key}")
            )

    for key in sorted(REQUIRED_FRONTMATTER_KEYS - values.keys()):
        issues.append(Issue(path, 1, "MISSING_FRONTMATTER_KEY", f"required key is missing: {key}"))

    if "name" in values:
        raw_name, line = values["name"]
        name = _unquote_scalar(raw_name)
        if not name or len(name) > 64 or not KEBAB_CASE.fullmatch(name):
            issues.append(
                Issue(
                    path,
                    line,
                    "INVALID_NAME",
                    "name must be 1-64 characters of lowercase kebab-case",
                )
            )
    return issues


def _validate_placeholders(path: Path, text: str) -> list[Issue]:
    issues: list[Issue] = []
    for label, pattern in PLACEHOLDER_PATTERNS:
        for match in pattern.finditer(text):
            issues.append(
                Issue(
                    path,
                    _line_number(text, match.start()),
                    "PLACEHOLDER",
                    f"unresolved {label}: {match.group(0)!r}",
                )
            )
    return issues


def _validate_conflicts(path: Path, text: str) -> list[Issue]:
    lines = text.splitlines()
    markers = [(index, line) for index, line in enumerate(lines, start=1) if CONFLICT_MARKER.match(line)]
    if not any(line.startswith("<<<<<<<") or line.startswith(">>>>>>>") for _, line in markers):
        return []
    return [
        Issue(path, line_number, "MERGE_CONFLICT", f"unresolved merge marker: {line}")
        for line_number, line in markers
    ]


def _markdown_target(raw_target: str) -> str | None:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        target = target.split(maxsplit=1)[0]
    target = unquote(target.strip())
    if not target or target.startswith(("#", "/")):
        return None

    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return None
    relative = parsed.path
    if not relative or any(token in relative for token in ("{{", "}}", "<", ">", "*")):
        return None
    return relative


def _validate_markdown_links(path: Path, text: str) -> list[Issue]:
    issues: list[Issue] = []
    for match in MARKDOWN_LINK.finditer(text):
        target = _markdown_target(match.group(1))
        if target is None:
            continue
        if not (path.parent / target).exists():
            issues.append(
                Issue(
                    path,
                    _line_number(text, match.start(1)),
                    "BROKEN_MARKDOWN_LINK",
                    f"relative link does not exist: {target}",
                )
            )
    return issues


def _atomic_reference_exists(document: Path, root: Path, reference: str) -> bool:
    if reference.startswith(("./", "../")):
        return (document.parent / reference).exists()

    base = document.parent
    while True:
        if (base / reference).exists():
            return True
        if base == root or root not in base.parents:
            return False
        base = base.parent


def _validate_atomic_references(path: Path, text: str, root: Path) -> list[Issue]:
    issues: list[Issue] = []
    for match in ATOMIC_REFERENCE.finditer(text):
        reference = match.group(1)
        if not _atomic_reference_exists(path, root, reference):
            issues.append(
                Issue(
                    path,
                    _line_number(text, match.start(1)),
                    "BROKEN_ATOMIC_REFERENCE",
                    f"atomic skill reference does not exist: {reference}",
                )
            )
    return issues


def _is_test_json(path: Path, root: Path) -> bool:
    if path.suffix.lower() != ".json":
        return False
    relative_parts = path.relative_to(root).parts if root in path.parents else path.parts
    return (
        path.name == "test-prompts.json"
        or path.stem.lower().startswith("test")
        or "tests" in relative_parts
    )


def _is_in_templates(path: Path, root: Path) -> bool:
    base = root.parent if root.is_file() else root
    try:
        relative_parts = path.relative_to(base).parts
    except ValueError:
        relative_parts = path.parts
    return base.name == "templates" or "templates" in relative_parts


def _is_json_template(path: Path, root: Path) -> bool:
    return _is_in_templates(path, root) and path.name.endswith(".json.template")


def _validate_json(path: Path, text: str) -> list[Issue]:
    try:
        json.loads(text)
    except json.JSONDecodeError as exc:
        return [Issue(path, exc.lineno, "INVALID_JSON", exc.msg)]
    return []


def validate_tree(root: Path, allowed_keys: frozenset[str]) -> tuple[list[Issue], int, int]:
    files = _iter_files(root)
    skill_files = [
        path for path in files if path.name == "SKILL.md" and not _is_in_templates(path, root)
    ]
    markdown_files = [
        path for path in files if path.suffix.lower() == ".md" and not _is_in_templates(path, root)
    ]
    json_files = [
        path for path in files if _is_test_json(path, root) or _is_json_template(path, root)
    ]
    issues: list[Issue] = []
    text_cache: dict[Path, str] = {}

    if not skill_files:
        issues.append(Issue(root, 1, "NO_SKILLS", "no SKILL.md files were found"))

    relevant_text_files = {
        path
        for path in files
        if path.suffix.lower() in {".md", ".json"}
        or path.name == "SKILL.md"
        or _is_json_template(path, root)
        or (_is_in_templates(path, root) and path.suffix.lower() == ".template")
    }
    for path in sorted(relevant_text_files):
        text, read_issue = _read_text(path)
        if read_issue is not None:
            issues.append(read_issue)
        elif text is not None:
            text_cache[path] = text
            issues.extend(_validate_conflicts(path, text))

    for path in skill_files:
        text = text_cache.get(path)
        if text is None:
            continue
        issues.extend(_validate_frontmatter(path, text, allowed_keys))

    for path in markdown_files:
        text = text_cache.get(path)
        if text is None:
            continue
        issues.extend(_validate_placeholders(path, text))
        issues.extend(_validate_markdown_links(path, text))
        issues.extend(_validate_atomic_references(path, text, root))

    for path in json_files:
        text = text_cache.get(path)
        if text is not None:
            issues.extend(_validate_json(path, text))

    issues.sort(key=lambda issue: (str(issue.path), issue.line, issue.code, issue.message))
    return issues, len(skill_files), len(json_files)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Recursively validate SKILL.md frontmatter, placeholders, conflict markers, "
            "test/template JSON, and local Markdown/atomic references."
        ),
        epilog="Exit status: 0 valid, 1 validation issues found, 2 invocation or I/O error.",
    )
    parser.add_argument("root", type=Path, help="skill directory tree, or one SKILL.md file")
    parser.add_argument(
        "--allow-key",
        action="append",
        default=[],
        metavar="KEY",
        help="permit an additional top-level frontmatter key (repeatable)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    root = args.root.expanduser().resolve()
    if not root.exists():
        print(f"error: validation root does not exist: {root}", file=sys.stderr)
        return 2
    if root.is_file() and root.name != "SKILL.md":
        print("error: a file validation root must be named SKILL.md", file=sys.stderr)
        return 2

    tree_root = root.parent if root.is_file() else root
    allowed_keys = frozenset(DEFAULT_FRONTMATTER_KEYS | set(args.allow_key))
    try:
        issues, skill_count, json_count = validate_tree(root, allowed_keys)
    except OSError as exc:
        print(f"error: unable to traverse validation root: {exc}", file=sys.stderr)
        return 2

    if issues:
        print(f"FAILED: {len(issues)} validation issue(s) found under {tree_root}")
        for issue in issues:
            location = _display_path(issue.path, tree_root)
            print(f"ERROR [{issue.code}] {location}:{issue.line}: {issue.message}")
        return 1

    print(
        f"OK: validated {skill_count} SKILL.md file(s) and "
        f"{json_count} JSON file(s) under {tree_root}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
