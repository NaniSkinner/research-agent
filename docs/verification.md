# Initial package verification

Date: 2026-10-26.
Status: prepared for isolated testing; not promoted for general use.

## Observed checks

- Python 3.12 unittest suite: 12 tests passed. Real temporary filesystem operations exercise staging, profile generation, conflict refusal, consistency, ownership-safe rollback, linked resource rejection, missing dependency handling and structural review-coverage validation.
- Tests were written before the management implementation. The first attempt exposed a test syntax error, corrected before the missing-module failure was observed. A dependency error then exposed missing-root handling and was corrected. These are implementation checks, not agent behavioral baselines.
- The independent source review found source-directory symlink omission and removal coupled to source freshness. Four added checks reproduced both classes of failure before fixes, then the complete suite passed.
- Upstream Skill Creator validation passed using the host Python with PyYAML. The Python 3.12 attempt lacked PyYAML; no dependency was installed.
- Dependency doctor read and hashed required installed Pstack and Evidence First files. This establishes file availability only.
- The project-scoped package staged successfully in separate Cedar and Willow workspaces. Registration checks passed. No global Codex profile, skill, config, Pstack file, hook or development repository was changed.
- Git baselines in fictional workspaces: Cedar 17189f9; Willow 694d5c3. No application execution or real product data was used.

## Pending acceptance

Actual custom-profile selection in a fresh Codex desktop chat, instruction-loading observation, researcher baseline/treatment runs, fresh independent evidence verification during those runs, parent fallback, runtime isolation enforcement, Nessie/Exa end-to-end integration and second-repository generalization are not established. No baseline agent failure or measured improvement is claimed.

The current chat's selectable custom roles do not include project-researcher. The profile is staged for discovery from the isolated project's new session. Do not silently substitute a generic child or CLI subprocess and call it desktop acceptance.

Source review and passing tests do not establish that a real model obeys the contract, sees all relevant code or produces reliable research. Acceptance material is prepared outside candidate-visible workspaces; actual sandbox/read-access separation must be recorded before claiming stronger blinding.

## Independent implementation review

A fresh worker (/root/research_package_review, fork_turns none) inspected source and ran the original eight checks, finding two P2 packaging issues. The lead reproduced them with four new regression checks and fixed them. A second newly spawned worker (/root/research_package_final_check, fork_turns none), given current source and requirements without earlier verdicts, inspected the package and ran all 12 tests successfully. It found no blockers for an initial private source release and isolated test preparation.

Both reviews examined the pre-commit filesystem. Neither selected a live profile, called connectors, used product systems or established behavioral reliability. The source was committed after review; only documentation of results and task completion was added afterward.

## Later desktop startup resolution

The previous missing-role result is historical. A matching personal profile registration followed by a newly created desktop chat exposed and launched project-researcher. Supported child history records instruction reads. See desktop-startup-result.md for precise metadata limits and pending research acceptance. No implementation or contract changes accompanied this registration.

## Controlled Cedar correction, version 0.1.1

The ordinary fresh agent and dedicated researcher both recovered the main source mechanisms. The researcher then asserted an unavailable management helper without checking the package checkout root; the helper existed. Its source review covered numbered project claims but not that later operational assertion. Source-root instructions now name the checkout boundary and helper, personal-profile consistency has a direct read-only command, and complete-answer review explicitly covers operational limitations. A fresh implementation reviewer checked the five-file diff and ran the full 15-test suite successfully. Three new helper checks failed before implementation and passed afterward. Behavioral reruns and safeguards are recorded separately; no real-work run is authorized.

## First two controlled stages complete

See controlled-cedar-results.md. The corrected researcher found the source facts, used a different reviewer on a second pass and returned verification-blocked when delegation was prohibited. Full selected-Pstack compliance and context-configuration observability remain incomplete. No real-work run or general promotion was performed.

## Workflow evidence correction, versions 0.1.2–0.1.3

See workflow-verification-results.md for implementation changes, fresh source reviews, 23 passing package checks, four latest controlled Cedar cases and a fresh findings assessment. Selected-owner step receipts and honest context/persistence states are implemented. Actual initial/cold startup declarations precede source investigation in observed 0.1.3 traces. Complete review-input payloads, host isolation and explicit early cold-handoff contract reload remain incompletely evidenced. No material false final source claims were found; this is bounded source-research acceptance, not full workflow authentication or general promotion. All 320 installed Pstack files are unchanged. Real-work runs remain paused.

## Fixed packets and controlled integration, versions 0.1.4–0.1.5

See controlled-014-results.md. Five new packet checks brought the suite to 28 passing tests. A fresh source review, actual scoped Nessie/Exa research and a fresh behavioral assessment demonstrated fixed packet access, early canonical contract reading and supported source/history/documentation conclusions. A disclosed management isolation deviation prompted explicit helper-snapshot guidance in 0.1.5 and a separately assessed successful startup-only control. These are bounded controls, not full workflow authentication or general promotion. Original records and remaining limits are retained. No real-work run occurred; Pstack is intact.

## C2.29 evidence-preservation repair, 0.1.6

See c229-evidence-repair.md. New preservation instructions retain actual returned receipts and exact worker outputs before summaries, distinguish supported retrospective exports and authored transcriptions, and preserve truncation/missing fields. Existing C2.29 packet was repaired with three exact worker returns and 112 selected command records, then checked by a new fresh reviewer without repeating investigation. No new source contradiction/instruction defect was found; exact rejection and actual profile/context metadata remain unverified. All 28 package checks pass. Personal profile refreshed; no Pstack change or new full research run is claimed.

## Prior-work checkpoint, 0.1.7

See prior-work-checkpoint-results.md for six paired fresh-worker response exercises covering established work, existing ownership, failed approaches, changed paths, unavailable evidence and stale handoffs. Both variants handled all six cases correctly; no measured improvement or reproduction of the long-chat failure is claimed. The new explicit source-backed comparison applies to the researcher, caller and independent reviewer. All 28 package tests pass; full workflow and long-context acceptance are outside these controls.

## Hiro discovery and personal routing, October 28, 2026

Hiro is the display/name alias for stable project-researcher and $project-research identifiers. Entry metadata, profile generator labels and UI display identify Hiro without altering contract 0.1.8 or workflow obligations. ~/.agents/skills/project-research links to the maintained source; personal ~/.codex/AGENTS.md routes explicit Hiro/Research Agent and Audit Agent requests. Existing repo-audit link and repo-auditor profile were reused unchanged; audit self-check returned INSTALLATION_VALID. No development repository, active C2.29 chat, Pstack or hooks changed.

Fresh fork_turns-none routing-only test /root/agent_testing_hiro_routing inspected source and candidate guidance: dedicated Hiro, direct nondelegated research, explicit inspection-only audit, ordinary PR verification and unavailable-role handling were distinguished. No material routing defect found. No actual project research/audit was dispatched; fresh-session implicit selection remains untested. All 28 package checks and Skill Creator validation passed; installed research profile matches source; all 320 Pstack files unchanged. Supported review export, installation receipt and before-state backups retained under originating workspace outputs/agent-discovery-20261028. Metadata should refresh on a subsequent turn; active chats were not restarted.
