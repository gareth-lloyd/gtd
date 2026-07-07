---
area: null
contexts:
- react
created: 2026-07-04 09:06:17.672407
defer_until: null
due: null
energy: medium
id: 2026-07-04T0906-review-pr-49415-make-cohorthotel-training-state-nu
order: null
output: |
  ## Agent run 2026-07-06T14:30 — Review of PR #49415

  PR: https://github.com/canary-technologies-corp/canary/pull/49415
  Author: Ramiro Nieto (chore). Already approved by abrad (2026-07-02). E2E passed.

  **Verdict: LGTM / safe to approve.** Clean, minimal, backward-compatible prep migration. No blocking issues.

  ### What it does
  - `CohortHotel.training_state` gains `blank=True, null=True` (default `UNKNOWN` retained).
  - Migration `0157_alter_cohorthotel_training_state` = single `ALTER TABLE ... ALTER COLUMN training_state DROP NOT NULL`.

  ### Verified
  - **Migration is metadata-only.** `DROP NOT NULL` in Postgres is a catalog change — no table rewrite/scan, only a brief ACCESS EXCLUSIVE lock. Safe on the populated table.
  - **No migration conflict.** `0157` depends on `0156_alter_onboardingvalue_kind`, which is the current single leaf on origin/master (confirmed it has no other children). Clean linear chain.
  - **Backward compatible.** Default `UNKNOWN` is kept, so the ORM still writes `'unknown'` on insert — this PR introduces zero NULL values. Existing readers keep getting a value. Reasoning in the PR body (must go nullable before `deprecate_field()` stops the ORM writing the column, since there's no DB-level default) is sound.
  - No test changes needed since runtime behavior is unchanged.

  ### Minor notes (non-blocking, FYI for the follow-up deprecation)
  1. **PR body is slightly ahead of reality.** It says "all reads were removed in #49409," but #49409 (https://github.com/canary-technologies-corp/canary/pull/49409) is still OPEN, not merged, and reads of `CohortHotel.training_state` still exist on master — notably `onboarding/agent_context/provider.py:66` (`training_state=ch.training_state`) plus the create/update paths in `onboarding/views/cohort_hotels.py`. Doesn't affect this PR's safety (default retained), just means the deprecation is not yet a DB no-op until #49409 lands.
  2. **Watch for the actual `deprecate_field()` PR:** `onboarding/agent_context/schemas.py:32` types `training_state: str = ""` (non-optional). Once the column can hold NULL after the ORM stops writing it, `ch.training_state` → `None` would flow into a `str` field. The deprecation PR should coalesce/remove that read.

  ### Recommendation
  Approve. No changes requested. (Did not post to GitHub — awaiting your call on whether to leave a review comment.)
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/49415
tags:
- morning-gtd
- github
time_minutes: 15
title: 'Review PR #49415: Make CohortHotel.training_state nullable'
updated: 2026-07-06 14:58:01.709970
waiting_on: null
waiting_since: null
working_on: false
---

Ramiro Nieto requested your review personally (chore).
https://github.com/canary-technologies-corp/canary/pull/49415