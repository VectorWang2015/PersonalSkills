#!/usr/bin/env python3
"""Dependency-free package checks, not a CFD or model-behavior certification."""
from pathlib import Path
import re
root = Path(__file__).resolve().parents[1]
entry = root / 'SKILL.md'
text = entry.read_text(encoding='utf-8')
assert text.startswith('---\n')
front = text.split('---', 2)[1]
assert re.search(r'^name: starccm-engineering$', front, re.M)
assert re.search(r'^description: .+', front, re.M)
assert len(text.splitlines()) <= 150
files = list(root.rglob('*.md'))
assert 1 <= len(list((root/'references').glob('*.md'))) <= 5
for path in files:
    body = path.read_text(encoding='utf-8')
    for link in re.findall(r'\]\(<?([^)>]+)>?\)', body):
        if '://' in link or link.startswith('#'): continue
        target = (path.parent / link.split('#')[0]).resolve()
        assert target.is_relative_to(root), (path, link)
        assert target.is_file(), (path, link)
    for pattern in [r'/home/', r'192\.168\.', r'\btrain6\b', r'cczh', r'session-[0-9a-f]{8}', r'podkey\s*=']:
        assert not re.search(pattern, body, re.I), (path, 'private-project marker', pattern)
assert (root/'tests/behavior-cases.md').read_text().count('|') >= 50
print(f'PASS: frontmatter, {len(files)} Markdown files, local links, private-marker screening, behavior cases. Not CFD/LLM behavior validation.')
