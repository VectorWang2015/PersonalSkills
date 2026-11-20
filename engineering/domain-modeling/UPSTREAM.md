# Upstream provenance

- Upstream URL: https://github.com/mattpocock/skills
- Commit: `abeeaf9` (`abeeaf95660ba9e8b7c753eb38f441ca707a8823`)
- Original path: `skills/engineering/domain-modeling/`

## Local changes

- Kept the upstream name, description, automatic invocation, and session workflow except for the adaptations below.
- Replaced illustrative fixed directory trees with project steering-file lookup for glossary and ADR locations, preserving the root glossary and ADR directory as fallbacks. Project restrictions on storing development documentation take precedence, including external documentation locations.
- Made glossary maps conditional and resolved glossary references relative to the current context, avoiding assumptions about project layout.
- Added Existing decision documents: inventory existing decision and naming documents first, propose individual conversions only when discussed, confirm them with the user, preserve originals, and leave links to converted material rather than batch-rewriting documents.
- Added Separate overloaded terms: clarify distinct meanings immediately and record them separately, so a single glossary entry cannot silently conflate concepts.
- Made project glossary and ADR formats take precedence over the bundled fallback formats.
- Adapted `ADR-FORMAT.md` and `GLOSSARY-FORMAT.md` to the same project-location, format, numbering, and documentation restrictions, preventing references from overriding the entrypoint. Marked multi-context layouts as defaults and examples rather than required structure.
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
