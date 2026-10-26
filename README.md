# Research Agent

A personal brownfield researcher for Codex. It establishes project context, investigates code and documentation, recovers prior work with Nessie, uses Exa when external evidence helps, and returns factual findings checked by a fresh independent worker.

The caller's plan is context for broader research, not something this role approves. Pstack owns workflow routing; Evidence First owns research quality. This package changes neither. Other installed skills, including BMAD, can support research when useful and available.

## Status

Version 0.1.0 is prepared for isolated testing, not promoted for general use. Structural/package checks are separate from behavioral reliability and actual Codex desktop dispatch. No default model or credential is included. No global Codex settings or hooks are changed.

## Contents

- `project-research/SKILL.md`: thin discovery and dispatch entry.
- `project-research/references/contract.md`: canonical mandatory research instructions.
- `project-research/references/pstack.md`: integration with installed workflows.
- `project-research/references/review.md`: fresh independent-review and parent fallback protocol.
- `scripts/manage.py`: project-scoped staging, consistency, rollback, dependency and structural receipt checks.
- `docs/testing.md`: testing steps, boundaries and pending acceptance.
- `docs/desktop-startup.md`: startup-only desktop acceptance.

Requires Python 3.12+ for management commands; no third-party runtime packages. The optional upstream Skill Creator validator uses its host-provided PyYAML.

```sh
python3.12 -m unittest discover -s tests -v
python3.12 scripts/manage.py stage --workspace /absolute/path/to/disposable-workspace
python3.12 scripts/manage.py check --workspace /absolute/path/to/disposable-workspace
```

Staging only creates this package's project-scoped skill link, generated profile and ownership receipt. It refuses conflicts and does not edit config.toml, enable features, copy credentials, modify hooks or make shell/network isolation claims. The parent provides real protections. Open that workspace in Codex for startup acceptance; a fresh session may be needed for discovery.

No deployment license has been selected. External sources are references, not bundled framework code.
