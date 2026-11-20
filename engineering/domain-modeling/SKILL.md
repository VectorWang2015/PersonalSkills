---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, or recording or editing an ADR.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `GLOSSARY.md` for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

Read the project's `AGENTS.md` / `CLAUDE.md` first for the declared glossary and ADR locations. When no locations are declared, use the upstream defaults: `GLOSSARY.md` at the repository root and `docs/adr/` for ADRs. If the project prohibits development documentation in particular repositories, follow that restriction, including any external documentation location; do not create the default files in a prohibited repository.

If a glossary map is declared, follow it to the relevant context. With the default layout, read a root `GLOSSARY-MAP.md` if one exists; the map points to each context's glossary and decisions. Do not infer the context from a directory name alone when the mapping is unclear.

Create files lazily: only when you have something to write. Create the glossary when the first term is resolved, and the ADR directory when the first ADR is needed, at the permitted project locations. References to `GLOSSARY.md` below mean the glossary for the current context at its resolved location.

## Existing decision documents

First list any existing decision or naming documents, including scattered ones. Inventory them without rewriting them.

When a particular decision or term actually comes up in the discussion, propose that individual decision for an ADR or that term for the glossary, as appropriate. Confirm the proposed conversion with the user before making it. Do not batch-rewrite the documents or delete the originals. After a conversion, leave a link in the original document pointing to the new location, subject to the project's documentation-location restrictions.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `GLOSSARY.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Separate overloaded terms

When one term is being used for more than one meaning or level of abstraction, pause and ask the user to clarify which meaning is intended. Record the distinct meanings separately in the glossary, with explicit names and boundaries, rather than allowing one entry to stand for both.

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update GLOSSARY.md inline

When a term is resolved, update `GLOSSARY.md` right there. Don't batch these up: capture them as they happen. Follow the project's declared glossary format; when none is declared, use [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).

`GLOSSARY.md` should be totally devoid of implementation details. Do not treat `GLOSSARY.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Follow the project's declared ADR format; when none is declared, use [ADR-FORMAT.md](./ADR-FORMAT.md).
