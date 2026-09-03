#!/usr/bin/env python3
"""Create a reproducible JSON manifest for one or more source files."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Sequence


SCHEMA_VERSION = 1
READ_CHUNK_SIZE = 1024 * 1024


class ManifestError(Exception):
    """Raised when a manifest cannot be built safely."""


def _hash_file(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    byte_count = 0
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(READ_CHUNK_SIZE), b""):
            digest.update(chunk)
            byte_count += len(chunk)
    return digest.hexdigest(), byte_count


def _source_format(path: Path) -> str:
    suffix = path.suffix.lower().lstrip(".")
    return suffix or "unknown"


def build_manifest(
    sources: Sequence[Path],
    *,
    base_dir: Path,
    title: str | None = None,
    author: str | None = None,
    version: str | None = None,
    portable: bool = False,
) -> dict[str, object]:
    """Return manifest data without modifying any source file."""

    resolved_base = base_dir.expanduser().resolve()
    if not resolved_base.is_dir():
        raise ManifestError(f"base directory does not exist or is not a directory: {base_dir}")

    entries: list[dict[str, object]] = []
    seen: set[Path] = set()
    for source_arg in sources:
        source = source_arg.expanduser().resolve()
        if source in seen:
            raise ManifestError(f"source was provided more than once: {source_arg}")
        seen.add(source)

        if not source.is_file():
            raise ManifestError(f"source does not exist or is not a regular file: {source_arg}")

        sha256, byte_count = _hash_file(source)
        relative = Path(os.path.relpath(source, resolved_base)).as_posix()
        entries.append(
            {
                "absolute_path": None if portable else str(source),
                "relative_path": relative,
                "sha256": sha256,
                "bytes": byte_count,
                "format": _source_format(source),
            }
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "title": title,
        "author": author,
        "version": version,
        "local_paths_redacted": portable,
        "base_directory": None if portable else str(resolved_base),
        "source_count": len(entries),
        "sources": entries,
    }


def _render_manifest(manifest: dict[str, object]) -> str:
    return json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"


def _write_output(
    rendered: str,
    output_arg: str,
    source_paths: Sequence[Path],
    *,
    force: bool,
) -> None:
    if output_arg == "-":
        sys.stdout.write(rendered)
        return

    output = Path(output_arg).expanduser().resolve()
    resolved_sources = {path.expanduser().resolve() for path in source_paths}
    if output in resolved_sources:
        raise ManifestError("output path must not be one of the source files")
    if not output.parent.is_dir():
        raise ManifestError(f"output parent directory does not exist: {output.parent}")
    if output.exists() and not force:
        raise ManifestError(f"output already exists (pass --force to replace it): {output}")

    # The explicitly named output is the only path this program writes.
    output.write_text(rendered, encoding="utf-8")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build a JSON manifest containing paths, SHA-256 digests, byte sizes, "
            "formats, and optional source metadata."
        ),
        epilog=(
            "The command never modifies source files. It writes only the path passed "
            "to --output; without --output it prints JSON to stdout."
        ),
    )
    parser.add_argument("sources", nargs="+", type=Path, help="source file(s) to hash")
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path.cwd(),
        help="base for relative_path values (default: current directory)",
    )
    parser.add_argument("--title", help="title recorded in the manifest")
    parser.add_argument("--author", help="author recorded in the manifest")
    parser.add_argument("--version", help="edition, release, or source version")
    parser.add_argument(
        "--portable",
        action="store_true",
        help="redact local absolute paths while retaining relative paths and integrity data",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="-",
        metavar="PATH",
        help="write JSON to PATH instead of stdout; refuses an existing PATH by default",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace an existing --output file (source files are never replaceable)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        manifest = build_manifest(
            args.sources,
            base_dir=args.base_dir,
            title=args.title,
            author=args.author,
            version=args.version,
            portable=args.portable,
        )
        _write_output(_render_manifest(manifest), args.output, args.sources, force=args.force)
    except (ManifestError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
