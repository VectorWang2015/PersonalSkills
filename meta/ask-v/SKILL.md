---
name: ask-v
description: List this project's manually invoked skills and suggest when to use them.
disable-model-invocation: true
---

# Manual skill guide

1. Run this skill's `scripts/skillctl list --manual --installed --json`, passing `--project` as the current project root. Resolve the executable relative to this skill's directory. If the command fails, report the error and stop.

2. Exclude this router and dependency skills from every user-facing list. If no manual choices remain, say that this project has no installed manual skills and go to step 5. Otherwise, briefly list the installed choices and when each is useful.

3. If the user has already described their situation, recommend the best 1–2 installed choices and explain why. Otherwise, ask exactly one question about what they are doing now; use the answer without starting a multi-round interview.

4. Base recommendations on each skill's own description. Read that skill's `SKILL.md` when more detail is needed. Read [FLOWS.md](FLOWS.md) for combinations and timing; do not treat it as a substitute for descriptions.

5. Offer installation guidance when the installed list is empty. If the user asks what else can be installed, or a suitable choice is not installed, run `scripts/skillctl list --manual` with the same project and catalog. Show only uninstalled manual choices, excluding this router and dependency skills, and provide `scripts/skillctl --project <project> install <name>` commands. Execute installation only after the user confirms the specific choices and target. Relay all Git warnings and the new-session discovery notice; never silently change ignore rules.

6. Keep read-only guidance short, in the user's current language, using a table or list. Describe available workflows; do not perform their tasks as part of this router.
