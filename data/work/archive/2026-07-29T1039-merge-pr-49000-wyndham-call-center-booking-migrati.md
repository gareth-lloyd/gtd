---
area: null
contexts:
- autopilot
created: 2026-07-29 10:39:59.865507
defer_until: null
due: null
energy: low
id: 2026-07-29T1039-merge-pr-49000-wyndham-call-center-booking-migrati
order: null
output: |-
  ## Agent run 2026-07-30T10:11:47Z
  Already done — no action needed. PR #49000 (https://github.com/canary-technologies-corp/canary/pull/49000)
  was merged to master by gareth-lloyd on 2026-07-29 at 12:47 UTC (merge commit 75ef9b703bb),
  about two hours after this item was captured. No conflicts or comments remained to address.

  Note on the stacked follow-up: PR #48994 (https://github.com/canary-technologies-corp/canary/pull/48994,
  "ENT-6664: Wyndham call-center booking onboarding type + seed rollout") is still OPEN and its
  merge state is DIRTY — it now has conflicts with master and needs a rebase/conflict resolution
  before it can merge. That looks like the real remaining work; consider a separate action for it.

  ## Agent run 2026-07-30T10:30:02Z — user redirected to stacked PR #48994
  Worked PR #48994 (https://github.com/canary-technologies-corp/canary/pull/48994) in the
  existing worktree .claude/worktrees/ent-6664-wyndham-cc-booking. Pushed f5ca8bb7166; PR is
  now MERGEABLE (was DIRTY). Did NOT merge (user merges manually) and did NOT post any
  review replies (drafts below need approval).

  1. Committed pre-existing uncommitted comment-tightening edits found in the worktree
     (addresses abrad's approval nit about comment phrasing).
  2. Resolved the master merge conflict in onboarding/tests/models/test_script_config.py
     (both sides added test methods at the same spot; kept both).
  3. Macroscope solution-review finding was VALID: WYNDHAM_CALL_CENTER_BOOKING was missing
     from CANARY_REGION_COUNTRY_MAP_BY_ONBOARDING_TYPE, so a Mexican (LATAM) Wyndham account
     would pass batch-creation validation on the US region. Added US/CA-only entry
     (mirrors WYNDHAM_AI_VOICE) + tests; reworded the misleading "US/CA guard" inline comment.
  4. abrad's question "do we throw an error if one of the hotels happens to be live?" —
     answer was NO (LIVE-subset check skipped for SALESFORCE_IDS; can_create_new_hotels types
     skip the exists-check). Made it YES: prepare_batches now raises
     SeedPopulationContainsLiveHotels when a pasted ID maps to a Canary hotel with
     is_live=True; not-live existing shells still accepted so re-runs work. Tests added.
  5. stephenreddek's CRS-only booking gateway thread: left alone — his latest comment
     (2026-07-29) says "actually, trying to work around that right now", so it's in his court.

  Verified: 269 tests pass across onboarding rollouts/batch/region-validation/script-config;
  ruff clean; pyrefly clean on changed files. (A full onboarding/tests/services run hit mass
  Postgres connection errors at fixture setup — environmental, tests pass when run per-file.)
  CI running: https://github.com/canary-technologies-corp/canary/pull/48994/checks

  TODO for Gareth: approve/post the two draft review replies (in session transcript),
  check CI, merge.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/49000
tags:
- morning-gtd
- github
time_minutes: 5
title: 'Merge PR #49000: WYNDHAM_CALL_CENTER_BOOKING migrations'
updated: 2026-07-30 14:39:58.659281
waiting_on: null
waiting_since: null
working_on: false
---

Approved; only non-blocking Playwright shard 4/4 failing. Merge before #48994 (stacked).
https://github.com/canary-technologies-corp/canary/pull/49000

resolve conflicts
address comments