---
area: null
contexts:
- craft
created: 2026-05-28 12:19:17.841054
defer_until: null
due: null
energy: medium
id: 2026-05-28T1219-build-claude-code-hook-a1-auto-check-rbc-setting-t
order: null
output: ''
project: 2026-04-16T1348-ideas
source_id: null
tags: []
time_minutes: 30
title: 'Build Claude Code hook (A1): auto-check rbc setting-type codegen staleness'
updated: 2026-07-07 14:06:17.938727
waiting_on: null
waiting_since: null
working_on: false
---

Claude Code hook for the rules_based_configuration app. Cheapest first win from the hooks exploration.

**Problem:** `rules_based_configuration/services/conformity.pyi` is a generated type stub. If you edit the setting definitions in conformity.py without regenerating, the stub goes stale and CI rejects it (the `generate_setting_types --check` mode already enforces this in CI). The model only finds out at CI time.

**Feature:** A `PostToolUse` hook scoped to `Edit|Write` on the rbc setting-definition source. After the edit, run:
`direnv exec . python manage.py generate_setting_types --check`
If the stub is stale, either (a) inject the failure as `additionalContext` so the model regenerates, or (b) auto-run `generate_setting_types` (no `--check`) to regenerate in place. Prefer (a) first; (b) is a nicer UX but mutates files behind the model.

**Anchors (already exist):**
- `rules_based_configuration/management/commands/generate_setting_types.py` — has `--check` CI mode + writes `conformity.pyi`.
- `services/setting_type_generator.py` — the generator.

**Scope decision:** per-developer (project `.claude/settings.json`, opt-in) vs org-enforced (managed settings). Start opt-in.
**Perf note:** generate_setting_types shells to pyright/ruff — measure runtime; only fire on edits to the definition source, not all of rbc.
**Effort:** ~30 min. Pure-local, no prod access.