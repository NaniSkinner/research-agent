# Research Agent maintainer notes

Not runtime instructions. Preserve these requirements for implementation, evaluation and installation.


### Package and launch

Keep the durable source in a versioned personal package, proposed at /Users/nani.skinner/Dev/Personal/research-agent, following the Auditor Agent’s source/registration separation. Proposed profile: ~/.codex/agents/project-researcher.toml; entry skill: project-research. No files at those destinations have been created by this draft.

Keep one canonical contract and a thin entry skill. If contract text is embedded into a generated profile, check its consistency at startup. Keep repository-specific inputs outside the generic profile. Resolve dependencies from the installed catalog, not a fixed plugin cache version. Preserve Pstack, Evidence First, Auditor Agent and verify-pr unchanged.

Core instructions remain model-neutral. Codex-specific dispatch, fresh-context settings and permissions belong in its integration. No Claude integration or fixed model selection is part of the current work.

Before accepting installation, prove actual profile selection and matching contract loading from a fresh Codex desktop chat, without a CLI subprocess or generic-profile substitute. Separately prove an end-to-end research return with fresh independent review. Profile-file presence and CLI tests alone do not establish desktop operation. Back up changed personal registrations and document rollback.

### Verification before installation

Use installed Pstack Eval guidance for behavioral testing: organic requests, hidden expected evidence, fixed revisions, fresh candidates/reviewers, inspected outputs and a held-out task from another repository. Do not show candidates prior review findings or desired answers.

Cover fresh research, broader research supporting a caller’s plan, a plan that misses an existing mechanism, stale docs, prior Nessie work, a correct claim that should not attract invented defects, missing runtime proof, unavailable tools, clarification, unsafe checks, changing revisions, context recovery, second-pass freshness and parent-arranged review. Keep project-specific examples such as C2.25 in fixtures, not permanent role instructions.

Include cases with an indirect dependency or alternate consumer, an existing equivalent hidden behind a partial migration, checked-in configuration that does not establish runtime state, passing tests with inadequate assertions, and a concise handoff that must retain a material contradiction. These test the five research additions without disclosing expected findings to candidates.

Promotion blocks on unsupported consequential facts, unauthorized effects, fabricated review evidence, silent profile substitution or a verified return without independent review. Structural checks cannot establish semantic reliability. Report actual test results and limits before requesting installation approval.

### Implementation questions to establish through inspection

- Actual desktop profile selection and dependency availability.
- Parent-arranged review protocol when nesting is unavailable: partial return must include the standalone reviewer brief, claims, baseline and raw evidence; parent dispatches the fresh reviewer, inspects its results, reconciles findings itself or returns them to the researcher, and issues no verified answer before reconciliation.
- Actual isolation of credentials, network, caches and state. A worktree alone is insufficient.

### Review status and provenance

The current revision adds five conditional brownfield investigation lenses following the Exa research and Nani’s authorization. Earlier reviews in independent-review.md and revised-independent-review.md are historical and do not establish acceptance of the current draft. Record the new review separately with its reviewed artifact hash and limits. The Auditor pattern remains a packaging reference, not proof of Research Agent runtime behavior.

Implementation is authorized by Nani following design approval. Initial staging is project-scoped and isolated; general user-scope promotion remains pending acceptance.
