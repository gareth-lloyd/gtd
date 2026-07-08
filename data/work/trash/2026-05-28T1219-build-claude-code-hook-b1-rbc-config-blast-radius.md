---
area: null
contexts:
- craft
created: 2026-05-28 12:19:17.870962
defer_until: null
due: null
energy: high
id: 2026-05-28T1219-build-claude-code-hook-b1-rbc-config-blast-radius
order: null
output: ''
project: 2026-04-16T1348-ideas
source_id: null
tags: []
time_minutes: 90
title: 'Build Claude Code hook (B1): rbc config blast-radius diff on rule edits'
updated: 2026-07-07 14:06:20.747086
waiting_on: null
waiting_since: null
working_on: false
---

Claude Code hook for the rules_based_configuration app. Most novel idea from the hooks exploration — my top pick for impact.

**Problem:** rbc is a rules engine. A one-line edit to a consistency/conformity rule can silently re-resolve configuration for whole cohorts of hotels. Neither CLAUDE.md nor CI surfaces *which* resolved configs changed — the blast radius is invisible at edit-time.

**Feature:** A `PostToolUse` hook scoped to edits of conformity/consistency rules. It:
1. Snapshots `ConformityService` resolved settings across representative `(MSA x brand x country)` combinations BEFORE the edit (or reads a cached baseline),
2. Re-resolves AFTER the edit,
3. Injects a DIFF as `additionalContext`: e.g. "your change flipped tokenize_cards true->false for Wyndham/US and IHG/CA".

This turns an opaque rules edit into an observable behavioral diff while the model is still working.

**Why it's safe:** `ConformityService.get_all_possible_setting_combinations()`, `hotel_conforms()`, and `get_setting_value_for_hotel_attributes()` operate on the IN-MEMORY rule trees + HotelAttributes — NOT hotel DB rows. So this runs with zero prod/staging access. It's essentially `detect_drift` logic minus the production hotel loop.

**Anchors (already exist):**
- `services/conformity.py` — ConformityService with the combination/resolution API.
- `management/commands/detect_drift.py` — reference for the resolve-and-compare pattern.

**Open questions:**
- How to capture the "before" snapshot — git stash the file and re-import? run in a subprocess against HEAD vs working tree? A pre-edit baseline cached in SessionStart?
- Which combinations to enumerate (all is likely too many — pick representative MSAs/brands or diff only combinations whose resolved value actually changed).
- Output formatting so the diff is readable and bounded.
**Effort:** ~90 min (the before/after snapshot mechanism is the hard part). Pure-local.