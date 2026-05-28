---
area: null
contexts:
- craft
created: &id001 2026-05-28 12:19:17.900215
defer_until: null
due: null
energy: medium
id: 2026-05-28T1219-build-claude-code-hook-c1-onboarding-plan-registry
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: 60
title: 'Build Claude Code hook (C1): onboarding plan registry-coherence Stop check'
updated: *id001
waiting_on: null
waiting_since: null
working_on: false
---

Claude Code hook for the onboarding app. Kills the "new plan silently never runs" class of bug.

**Problem:** A new `OnboardingPlan` subclass must be registered in BOTH `KNOWN_PLANS` (services/plan.py) AND wired into `ONBOARDING_TYPE_CONFIG` (models/property_configuration_processes.py). Miss either and the plan silently never executes — no error, just a no-op. Easy to forget; documented as a footgun in onboarding/CLAUDE.md.

**Feature:** A `Stop` hook (fires when a turn ends) that, when files under `onboarding/` were touched this turn, runs a coherence check and BLOCKS turn-end (`decision: "block"`) on failure so the model fixes it before finishing. Check should:
1. Run the existing `check_config_provider_required_fields` management command.
2. Assert every `OnboardingPlan` subclass is present in both `KNOWN_PLANS` and `ONBOARDING_TYPE_CONFIG`.
3. (Optional stretch) Verify `raise_expected_error` codes referenced in edited plans exist in BOTH `exceptions.py` WHAT_HAPPENED and WHAT_TO_DO dicts.

**Anchors (already exist):**
- `management/commands/check_config_provider_required_fields.py` — reuse directly.
- `services/plan.py` (KNOWN_PLANS), `models/property_configuration_processes.py` (ONBOARDING_TYPE_CONFIG), `exceptions.py`.

**Notes:**
- Stop hooks fire on every turn end — gate the expensive check on "did this turn edit onboarding/?" (inspect transcript or a touched-files marker) to avoid running it constantly.
- Could be implemented as a small custom mgmt command (`check_plan_coherence`) that the hook invokes, which is also reusable in CI.
**Effort:** ~60 min. Pure-local, no prod access.