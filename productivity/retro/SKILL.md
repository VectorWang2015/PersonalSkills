---
name: retro
description: "Conduct a retrospective on a coding session."
disable-model-invocation: true
metadata:
  requires:
    - writing-for-agents
---

The user has asked for a **retrospective**. You are suggesting improvements to the coding agent's **environment** to improve future runs.

## Steps

1. Load the `writing-for-agents` skill for the writing style guide.

2. Read the session or exported files the user specifies; if neither is specified, use the current session. When the host stores sessions, use its supported access or export mechanism rather than assuming a storage path. For example, OpenCode can export a session with `opencode session export --sanitize <id>`. Treat exports as potentially sensitive even after sanitisation; do not publish them without permission.

3. Look for candidates for improvement in these categories. Read the project's `AGENTS.md` / `CLAUDE.md` first for its workflow, standards sources, check commands, and documentation locations; use existing project tooling and conventions rather than prescribing a new toolchain.

- **Navigation**: how easy was it for the agent to find the right files? Are there hidden dependencies between files? Would a **navigation pointer** make it easier? _Use when_ the session took a long time to find a piece of information.
- **Automated checks**: are there automated checks that could catch errors the agent made? Read the project's existing check commands and how they are run, so a check that already exists but sits unwired or silently broken is the finding, not a reinvention. _Use when_ the agent made a mistake an automated check could have caught, or the project requires a guardrail that is absent.
- **Coding standards**: should a documented standard be removed, clarified, or added? Classify the violation first: a **mechanical** one belongs in a deterministic check using the project's own tooling. Reserve written standards for genuine **judgement calls** that automation cannot substitute for, at the standards location declared by the project; if none is declared, propose `CODING_STANDARDS.md`. _Use when_ a standards-related mistake escaped the project's checks or review.
- **Steering-file scope**: do `AGENTS.md` / `CLAUDE.md` contain changing task status, deployment records, or authorisation records? If so, suggest moving those entries to the project's own status or log files, keeping stable workflow instructions and navigation pointers in steering files. Use the locations declared by the project; if none are declared, ask the user where those records belong. A historical authorisation record is not a new grant of permission.
- **Global steering files**: are there any steering instructions that should be moved to project standards, reference docs, or automated checks instead? _Use when_ a project or global `AGENTS.md` / `CLAUDE.md` is particularly large. Suggest changes outside the project rather than assuming permission to edit them.
- **Tool economy**: did the agent make expensive tool calls that could be streamlined? Is there any custom tooling (CLI's, MCP's) that is particularly token-inefficient? _Use when_ the agent made an expensive tool call.
- **No-ops**: look for instructions in steering files that don't modify the agent's behavior. _Use when_ the steering files are large and unwieldy.
- **Information access**: look for opportunities to increase the agent's access to information. Teeing dev server logs, readonly access to third-party services. _Use when_ a crucial piece of information was not available to the agent. Any additional access remains subject to the user's permissions.

4. Present these candidates to the user, in order of severity. Suggest improvements; do not modify instructions, tooling, or access without authorisation.

## Reference

### Implementation vs Review

Follow the project's declared workflow rather than assuming separate implementation and review stages or agents. When a separate reviewer exists, consider which context and evidence each role actually receives before proposing where a judgement-based standard belongs. Mechanically enforceable constraints belong in tools, not duplicated prose rules.

### Files

Use the files and locations declared by the project's `AGENTS.md` / `CLAUDE.md`. When none are declared, these are possible defaults to propose, not assumptions that the files already exist:

- `CLAUDE.md`/`AGENTS.md`: stable steering instructions and **navigation pointers**, used sparingly. Their discovery and loading depend on the host.
- `CODING_STANDARDS.md`: judgement-based standards, consulted at the stages required by the project.
- Docs: use docs as reference files, pointed to by other files. Look for existing docs before writing new ones.
- Skills: use skills for reusable workflows, reference material, or user-invoked commands. Follow the loaded `writing-for-agents` skill and the host's discovery and invocation conventions.
