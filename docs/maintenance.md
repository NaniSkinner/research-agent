# Maintenance and rollback

Maintain the mandatory contract once in project-research/references/contract.md. The staging helper embeds it in a generated Codex TOML profile and records hashes of skill resources. Existing staged copies intentionally fail when source changes. Reconcile changes, remove the unchanged owned registration with the helper, and deliberately restage; do not hand-edit a generated profile or forge a receipt.

To remove an unchanged staged registration:

```text
python3.12 scripts/manage.py remove --workspace <isolated-workspace>
```

Only the owned skill link, profile and receipt are removed. Research reports, unrelated files, source and empty parent directories remain. Changed source contents do not prevent removal of an unchanged owned registration. Modified or ownership-mismatched installed registrations are not deleted automatically. Inspect and preserve them before an explicitly authorized repair.

The management helper does not install globally. Normal user-scope installation needs a separately reviewed operation and desktop acceptance after source/behavior checks. Preserve existing registrations and backups. Re-run affected structural and behavioral checks when contract, Pstack, dependency versions or host dispatch changes. A validator checks structure; reviewers check meaning.
