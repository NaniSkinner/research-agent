# Independent review and compact return

For each substantive report, arrange a new independent worker using supported fresh-context delegation. In Codex explicitly set fork_turns: none. No inherited author conversation or old reviewer verdicts. The selected installed Pstack guidance owns research verification; do not reproduce a PR-review rubric or pretend every research question is a diff review.

## Standalone brief

Include the original question, authoritative requirements, allowed actions, exact baseline/snapshot, relevant guidance, complete proposed answer and claim ledger (including resource-availability and limitation assertions), material conflicts and safe source/artifact locators. Tell the worker to inspect decisive sources independently and try to refute consequential claims. The claims are untrusted objects to check, not established ground truth. Do not include author self-assessment or reasoning transcript.

Return checked claim IDs, actual sources opened, findings with IDs, missing evidence, reviewed baseline, reviewer identity and supported fresh-context metadata. Bare agreement and wording review do not satisfy source verification. The lead opens decisive evidence, reconciles each finding and preserves unresolved disagreements. Review coverage must include consequential prose outside numbered claim rows. Do not append an unreviewed missing-tool or missing-source assertion after the review. Recheck affected claims after material corrections; a different baseline requires a new fresh independent pass before an independently checked return.

## Parent-arranged route

When the Research Agent cannot spawn its reviewer, return this envelope through normal completion:

- status: review-required (not independently checked);
- question, requirements, baseline, proposed report and safe evidence locators;
- standalone reviewer brief and the exact capability limitation.

The calling parent dispatches a fresh reviewer, waits and inspects results. It either reconciles claims itself against decisive sources or sends results to the same researcher for reconciliation within the existing assignment. Do not confuse continuing the researcher with reusing the independent reviewer. Preserve the original independent findings. If no supported fresh lane exists, final status is verification-blocked; do not silently replace it with a persona or ask another developing chat to stop.

## Optional machine-readable receipt

Use this shape alongside the readable research report. The helper checks declared fields and coverage, never truth or actual runtime settings. Do not fabricate metadata to pass it.

```json
{
  "status": "independently-checked",
  "baseline": "exact repository revision plus relevant snapshot identity",
  "claims": [
    {"id": "c1", "category": "observed-current-fact", "status": "supported", "source": "src/example.py:12"}
  ],
  "review": {
    "reviewer_id": "observed worker identity",
    "fork_turns": "none",
    "baseline": "exact repository revision plus relevant snapshot identity",
    "checked_claims": ["c1"],
    "findings": [],
    "dispositions": []
  }
}
```

Claim categories: observed-current-fact, historical-record, external-evidence, reported-not-reverified, inference, unknown. Claim outcomes: supported, contradicted, unverified. Unknowns still need a source/scope locator describing where the gap was established. Final statuses: independently-checked, verification-blocked, needs-clarification. The review-required envelope is intermediate, not a final validated report. Each review finding needs a disposition with finding_id, resolution (corrected, rejected-with-evidence, unresolved), and evidence. Independently checked can contain unverified claims or unresolved conflicts clearly labeled; it does not mean product readiness.

Keep the readable answer compact, with the system path and key facts first. Store the detailed ledger and raw check outputs in the declared output directory. Do not hide counterevidence or revision limits when compressing the return.
