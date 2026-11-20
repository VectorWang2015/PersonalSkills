# Upstream provenance

- Upstream URL: https://github.com/mattpocock/skills
- Commit: `abeeaf9` (`abeeaf95660ba9e8b7c753eb38f441ca707a8823`)
- Original path: `skills/engineering/code-review/`

## Local changes

- Added `disable-model-invocation: true` and updated the description to match manual invocation and a single reviewer.
- Removed the Fowler smell baseline and all reviewer-prompt references to it: this skill governs the review workflow rather than teaching generic code-quality heuristics.
- Replaced the two parallel reviewers with one fresh-context review sub-agent. Kept Standards and Spec separate through report structure, evidence, and within-axis summaries, without merging or reranking findings. Model selection belongs to the host or project.
- Removed the `setup-matt-pocock-skills` prerequisite, tracker-document dependency, and guessed specification directories. Requirements lookup now follows user input, project-declared sources, commit issue references, then a user question. Spec is omitted only when the user confirms no requirements document exists.
- Made standards sources explicit: applicable project steering files, contribution guidance, coding standards, and other project-declared standards. Mechanically enforceable checks belong to project tooling.
- Added project-declared default integration-branch lookup, then a user question if needed. Resolve the starting reference once to an immutable commit SHA so all review commands share one fixed point.
- Added optional Delivery hygiene only for a checklist declared in project steering. It reviews every commit's patch, because a later deletion does not erase earlier content from history; an empty final diff cannot bypass this check.
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
