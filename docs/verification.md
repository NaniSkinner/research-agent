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
