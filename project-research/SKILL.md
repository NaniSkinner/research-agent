---
name: project-research
description: Use when investigating a brownfield project's current mechanisms, surrounding dependencies and prior work, including broader factual research supporting an existing development plan. Not for implementing changes, approving plans, or managing PRs.
---

# Project research

Use the dedicated `project-researcher` profile for factual brownfield research. When already running as that actual selected profile, follow the contract and supporting resources directly; do not redispatch this entry skill into another researcher. The dispatch steps below belong to the caller.

1. Read [the mandatory contract](references/contract.md), [workflow integration](references/pstack.md) and [independent review protocol](references/review.md). On resume reload them and reconcile the actual baseline.
2. Resolve the question, repository, requirements, revision, output directory and authority from the current task. Ask only for consequential missing information. A caller's plan supplies context, not an answer to confirm.
3. Check the staged registration with `python3 <source>/scripts/manage.py check --workspace <workspace>`. Discover required installed resources and run its `doctor` command with resolved paths. File checks do not prove compliance. For other supported installations, use equivalent source/profile consistency evidence.
4. Inspect the host's actual profile-selection capability. Launch `project-researcher` with `agent_type: "project-researcher"`, `fork_turns: "none"`, this skill's absolute path, and a standalone question and live context. Do not launch a CLI subprocess, generic persona, or parent substitute if actual selection is unavailable. Return a startup limitation.
5. Wait for the report. Inspect its decisive sources and fresh-review receipt before conveying independently checked findings. If the child returns `review-required`, arrange the review described in references/review.md. Do not turn partial findings into verified conclusions.

The source is the package containing this SKILL.md, resolved through any installation link. No target repo or model is a permanent role default. Missing profile/dependency/review capabilities remain visible. Do not install this package or change Pstack automatically.
