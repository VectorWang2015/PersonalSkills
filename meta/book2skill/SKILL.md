---
name: book2skill
description: Create or refresh book-derived agent skills from the source text. Use for systematic book distillation and for auditing an existing book-based skill through a source-first independent re-distillation before comparing and merging. Not for ordinary summaries, author role-play, or code/workflow skills whose authority is runtime behavior rather than a book.
metadata:
  workflow-version: "2.0"
  upstream-reference: "cangjie-skill v2.5.0"
---

# Book-to-skill distillation and refresh

Turn a source book into a small, traceable set of executable capabilities. For an existing skill, rebuild the capability map independently from the source before reading the legacy implementation, then compare, test, and merge on evidence.

## Boundaries

Use this skill for:

- a new skill derived substantially from a book or other stable long-form source;
- an audit or refresh of an existing book-derived skill;
- reconciling several old atomic skills into a clearer router plus internal capabilities.

Do not use it for a normal book summary, imitation of an author's persona, or a tool whose correctness comes primarily from APIs, code, current regulation, or an operational workflow. Audit those against their real runtime contract instead.

## Local authority and upstream reference

This directory is the repository's installed distillation workflow. `../cangjie-skill/` is the pinned upstream reference, not a second active entrypoint. Consult its Capability Bundle, promotion-gate, compilation, update, and rollback designs when needed; this local workflow remains authoritative for repository layout, validation, and refresh decisions.

Do not install or auto-activate both entrypoints for the same request. Do not copy upstream files mechanically without checking their dependencies and behavior.

## Required evidence

Before extraction, locate or obtain:

1. the actual source file, not a recollection or an old summary;
2. title, author, edition/publication information when known;
3. the intended user tasks and target skill location;
4. for a refresh, the existing skill tree and any real usage failures or successful outputs.

If these are already present in the workspace, discover them instead of asking the user to repeat them. Record each source with `scripts/build_source_manifest.py` before analysis.

## Choose a mode

- **Create:** no prior implementation exists. Follow stages 0–5.
- **Redistill and merge:** a book-derived skill already exists. Follow stages 0–5 plus the isolation and comparison protocol in `methodology/08-redistill-and-merge.md`.

The default deliverable is one discoverable router with internal capability references. Promote additional discoverable skills only when separate user intent, input/output contract, independent operation, and evaluation evidence justify them.

## Workflow

### Stage 0 — Source contract and overview

Read `methodology/01-stage0-adler.md`.

- Resolve explicit project, source, work, and target roots; never infer them solely from the current shell directory.
- Build `source-manifest.json` with hashes and parsing notes.
- Create a concise whole-book overview, argument map, terminology map, limitations, and intended task map.
- For scans, malformed text, formula-heavy books, or multiple editions, record extraction uncertainty before continuing.

### Stage 1 — Independent capability extraction

Read `methodology/02-stage1-parallel-extract.md` and only the extractor prompts relevant to the source.

- Divide work by evidence type and source coverage, not by a fixed agent count.
- Give every candidate a stable ID and exact source anchor.
- Label quotations, faithful paraphrases, and analyst inferences separately.
- In refresh mode, extraction agents must not read the old skill until the independent candidate set is frozen.

### Stage 2 — Evidence and product validation

Read `methodology/03-stage1.5-triple-verify.md` and `methodology/03b-stage1.6-promotion-gate.md`.

Keep a capability when it is source-faithful, executable, useful relative to a no-skill baseline, and bounded. Repetition and novelty increase confidence but are not automatic pass/fail gates. A one-off formula or procedure may still be essential.

Separate two decisions:

- whether knowledge deserves retention;
- whether it deserves its own discoverable skill entrypoint.

### Stage 3 — Build capability cards and routing

Read `methodology/04-stage2-ria-plus.md` and `methodology/05-stage3-zettelkasten.md`.

- Put the runtime contract, decision rules, procedure, output definition, and boundaries in the hot path.
- Put quotations, extended examples, provenance, and audit discussion under `references/` for progressive disclosure.
- Keep stable capability IDs across revisions.
- Prefer a compact router over many overlapping entrypoints.

For financial books, also read `methodology/09-financial-quality-gates.md`. Distinguish book doctrine from current accounting, regulation, market data, and empirical claims; verify every retained formula, unit, sign convention, and threshold.

### Stage 4 — Compare and merge existing work

Refresh mode only. Read `methodology/08-redistill-and-merge.md`.

After freezing the independent result, align it with the old skill at capability level and label each item `new-only`, `old-only`, `both-consistent`, or `conflict`.

- Preserve old-only material only when it has source evidence or documented operational evidence.
- Prefer the better execution contract rather than the longer explanation.
- Resolve conflicting formulas or claims against the source and current authoritative standards.
- Record removals and compatibility changes explicitly.

### Stage 5 — Independent evaluation and delivery

Read `methodology/06-stage4-pressure-test.md` and `methodology/07-stage5-deliver.md`.

Evaluate realistic tasks using held-out cases. For refreshes, compare anonymized old, new, and no-skill variants. Include sibling-routing distractors and mechanical assertions for calculations, required fields, citations, and refusal boundaries.

Generate the published source manifest with `scripts/build_source_manifest.py --portable`; keep the path-bearing working manifest only in the private work directory.

Validate the staged output before replacing the target:

```bash
python3 scripts/validate_skill_tree.py <staged-skill-directory>
```

Publish only after tests pass. Preserve the prior version until the replacement is verified, and keep the working artifacts needed to explain the merge.

## Working and final layout

Use an isolated work directory such as:

```text
<project-root>/books/<source-slug>/.book2skill/
├── pipeline-state.json
├── source-manifest.json
├── overview.md
├── independent/
│   ├── capability-bundle.json
│   └── cards/
├── comparison.json
├── eval-suite.json
└── staging/
```

The normal final skill is compact:

```text
<target-skill>/
├── SKILL.md
├── references/
│   ├── capabilities/
│   ├── evidence.md
│   └── source-manifest.json    # portable copy; local paths redacted
└── test-prompts.json
```

Use a compact pack only when promotion evidence supports multiple discoverable entrypoints. Keep internal cards reachable from the router even when they are not independently promoted.

## Hard gates

- No source text, no distillation.
- No legacy-skill exposure before the independent refresh result is frozen.
- No capability without a source anchor or an explicitly labeled operational extension.
- No fabricated quotation, occurrence count, formula, page number, or regulatory claim.
- No local absolute path in a published manifest or delivered skill.
- No unsupported top-level frontmatter fields; provenance belongs under `metadata` or `references/`.
- No placeholder text, broken relative references, unresolved conflict markers, or unparseable test JSON in a delivered skill.
- No claim of evaluation success without preserved cases, variant identity mapping, results, and environment/model information.
- Do not overwrite a working implementation until the staged replacement and rollback path are verified.

Ask the user only when a missing source, intended task, output-mode choice, or compatibility tradeoff would materially change the result. Otherwise continue and report stage-level evidence and decisions.
