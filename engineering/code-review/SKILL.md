---
name: code-review
description: "Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/spec asked for?). Uses one fresh-context review sub-agent and reports the axes separately. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to \"review since X\"."
disable-model-invocation: true
---

Two-axis review of the diff between `HEAD` and a fixed point:

- **Standards**: does the code conform to this repo's documented coding standards?
- **Spec**: does the code faithfully implement the originating issue / spec?

Run a **single review sub-agent**, started with a fresh context window. Keep the two axes separate in its report. The host or project configuration chooses the model; this skill does not prescribe one.

## Process

### 1. Pin the fixed point

Use the commit, branch, tag, or merge-base the user supplied. If none was supplied, read the project's `AGENTS.md` for a declared default integration branch. If neither source provides a fixed point, ask the user; do not guess a branch name.

Resolve the chosen reference once with `git rev-parse --verify <ref>^{commit}`. Use the resulting commit SHA as `<fixed-point>` in every command below, so a moving reference cannot change the review's starting point.

Capture the diff command: `git diff <fixed-point>...HEAD` (three-dot, so the comparison is against the merge-base). Also capture the commit list with `git log <fixed-point>..HEAD --oneline`.

A bad reference should fail here, not inside the review sub-agent. If both the diff and commit range are empty, report that there is nothing to review. An empty final diff alone must not skip the historical Delivery hygiene check in step 4.

### 2. Identify the spec source

Look for the originating requirements, in this order:

1. A path or reference the user passed as an argument.
2. Requirements sources declared in the project's `AGENTS.md` / `CLAUDE.md`, such as a task list, plan directory, or issue tracker.
3. Issues referenced in the commit messages, retrieved using the project's conventions and the host's available tools.
4. Ask the user where the requirements are. If they say there is no requirements document, skip the **Spec** section and note that omission in the final summary.

If a referenced source cannot be accessed, ask for access or its contents rather than treating it as absent.

### 3. Identify the standards sources

Read the applicable project `AGENTS.md` / `CLAUDE.md`, `CONTRIBUTING.md`, `CODING_STANDARDS.md`, and any other standards the project declares. Include the files that exist and the scope in which each applies. Review against documented standards, not an added generic baseline. Leave mechanically enforceable checks to the project's tools.

### 4. Enable Delivery hygiene only when declared

Only enable **Delivery hygiene** if the project's `AGENTS.md` declares a delivery-hygiene checklist. Use that checklist as the review criteria; do not invent a default one.

Review **every commit since the fixed point** with `git log -p <fixed-point>..HEAD`, not just the final diff. A later deletion commit does not remove the earlier content from history.

### 5. Spawn one review sub-agent

Start one sub-agent with a fresh context window. Its prompt should include:

- The pinned fixed point, diff command, and commit list.
- The standards-source files and their applicable scopes from step 3.
- The path, reference, or retrieved contents of the requirements from step 2, or an explicit instruction to omit Spec if the user confirmed there is no requirements document.
- If enabled, the project's delivery-hygiene checklist and `git log -p <fixed-point>..HEAD` command.
- The brief below.

**Review brief:**

Report under two separate headings, `## Standards` and `## Spec` (omit Spec when instructed). Do not merge or rerank findings across the axes.

- **Standards**: report where the diff violates a documented standard. Cite the standard's file and rule, and identify the affected file/hunk. Distinguish clear violations from judgement calls. Leave checks already enforced by tooling to that tooling. Under 400 words.
- **Spec**: report requirements that are missing or partial, behaviour that was not asked for, and requirements whose implementation appears wrong. Quote the requirement for each finding and identify the affected file/hunk. Under 400 words.
- **Delivery hygiene**, only if enabled: add a separate `## Delivery hygiene` section. Apply the declared checklist to every commit in the historical range, citing the checklist item, commit SHA, and affected file/hunk for each finding. Keep these findings separate from both axes.

If an enabled section has no findings, say so explicitly.

### 6. Present the report

Present the review's sections verbatim or lightly cleaned. Preserve their order and the order of findings within them. Do **not** merge or rerank findings across axes or fold Delivery hygiene into either axis.

End with a one-line summary: total findings per enabled section, and the worst issue **within each section** (if any). Note if Spec was skipped because the user confirmed there was no requirements document. Do not pick a single winner across sections.

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**

The axes are isolated by the **report structure**, not by separate agents or context windows. Separate sections, evidence, and within-axis summaries stop one axis from masking the other; combining or reranking their findings would undo that separation.
