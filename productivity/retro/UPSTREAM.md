# Upstream provenance

- Upstream URL: https://github.com/mattpocock/skills
- Commit: `abeeaf9` (`abeeaf95660ba9e8b7c753eb38f441ca707a8823`)
- Original path: `skills/engineering/retro/`

## Local changes

- Relocated the skill from the upstream engineering category to the local productivity category; kept its name, description, and manual invocation.
- Added a YAML-list `metadata.requires` for `writing-for-agents` and explicitly load that skill before the retrospective.
- Made session input host-neutral: prefer the user-specified session or export, otherwise use the current session. Replaced machine-log searching with supported host access/export, including an optional sanitised-export example and a warning that exports may remain sensitive.
- Added Steering-file scope to detect changing task status, deployment records, and authorisation records in steering files and suggest moving them to project-owned status or log files. Historical records do not grant new permissions.
- Routed workflow, check commands, standards, and document locations through project steering files. Removed assumptions about a particular build tool, mandatory lint infrastructure, universal review stages, and universally available files; defaults are proposals only when the project declares none.
- Kept mechanical constraints in deterministic project tooling rather than prose rules; adapted standards and global-steering candidates accordingly.
- Changed the implementation/review reference to depend on the project's actual roles and evidence instead of assuming every reviewer receives sufficient context or owns all standards enforcement.
- Kept the retrospective advisory: present candidates without changing files, tooling, global instructions, or access absent authorisation, and make host-dependent skill discovery explicit.
- Omitted `agents/openai.yaml`, which is host-specific display metadata, and added this provenance and complete license record.

## License

MIT License

Copyright (c) 2026 Matt Pocock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
