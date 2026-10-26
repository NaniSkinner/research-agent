# Research Agent Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans for inline execution; fresh independent review before delivery.

**Goal:** Commit the approved personal brownfield researcher and prepare isolated testing without changing Pstack or global agent registrations.
**Architecture:** One canonical research contract, thin discovery skill, generated Codex profile, explicit staging/check tooling and private acceptance material. Reuse installed workflows.
**Tech Stack:** Markdown, Codex TOML, Python 3.12 standard library, unittest, Git/GitHub.
**Spec:** docs/design.md (approved in the originating Codex chat).

## Global Constraints

- Brownfield factual research supports ongoing plans; no plan approval or automatic fixes.
- Installed Pstack stays unchanged. Flexible skill selection, Nessie continuity and relevant Exa research.
- Existing inspected isolated checks only; no default new tests/product writes.
- New reviewer with fork_turns none before every substantive verified return.
- Codex desktop actual profile selection is a separate acceptance requirement.
- No normal user-scope installation in this task; stage project-scoped resources for testing.

## Review Focus

- Conflicting existing registrations must survive staging/rollback unchanged.
- A contract/profile mismatch must fail consistency checks.
- A missing required dependency must not pass a readiness check.
- A claimed completed review with missing fresh-context evidence must not pass structural validation.
- A missing runtime capability must remain blocked, not become a generic-profile substitution.

### Task 1: Package and local controls

**Files:** project-research/SKILL.md, project-research/references/contract.md, project-research/references/review.md, scripts/manage.py, tests/test_manage.py.
**Interfaces:** stage(source, workspace) -> receipt; check(workspace) -> receipt; remove(workspace) -> result; validate_report(report) -> None.
- [x] Write behavior tests for stage/consistency/conflict/rollback and review-receipt validation. Run and record missing implementation failure.
- [x] Implement minimal explicit-target staging, exact-profile rendering, consistency checks and report validation. No command runner or replacement Pstack engine.
- [x] Run full suite and skill validation; inspect rendered profile and real dependency resources.
- [x] Commit implementation with approved design and provenance, without private conversation exports or hidden acceptance answers.

### Task 2: Isolated acceptance setup

**Files:** docs/testing.md, docs/desktop-startup.md, docs/maintenance.md, acceptance fixtures and private local grading material.
**Interfaces:** staged .codex/agents/project-researcher.toml and .agents/skills/project-research, startup receipt, research report with exact snapshot.
- [x] Create sanitized example projects and organic task prompts outside candidate-visible acceptance criteria. Baseline/agent behavioral comparison remains explicit pending work; no invented failures or reliability claims.
- [x] Stage the package in an isolated workspace and run consistency checks. Do not copy credentials, personal config or hook trust.
- [x] Have a fresh reviewer inspect implementation and prepared setup; fix consequential findings and rerun affected checks.
- [x] Create private GitHub repository, push committed source, record completed structural checks and pending behavioral/desktop gates.

## Execution ledger

- Spec approved; user explicitly requested repository creation, commit and test preparation. Proceed inline rather than asking again for implementation approval.
- Ruling: new empty repository is already isolated from development repos; use dedicated build branch. No existing checkout or developing agent is touched.
- Ruling: use Python 3.12 for built-in TOML parsing; do not install dependencies.
- Pre-flight: stage/check/remove share receipt paths and hashes; tests pin ownership, conflict and stale-state behavior. Report validation checks structure, not truth.

- Initial source review found two packaging defects. Added four failing checks, corrected linked-directory validation and separated ownership-only removal from freshness checking; full suite now passes 12 tests. A new final reviewer is checking current source without prior verdicts.

- Final fresh source review found no blockers for private source release and isolated setup. 12 tests passed. Desktop startup and behavioral runs remain pending and are not marked complete.
