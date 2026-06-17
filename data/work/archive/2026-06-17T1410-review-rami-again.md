---
area: null
contexts: []
created: 2026-06-17 14:10:36.505837
defer_until: null
due: null
energy: low
id: 2026-06-17T1410-review-rami-again
order: null
output: |
  ## Agent run 2026-06-17T14:30 (re-review)

  PR #47477 — [TOOL-34] Track all non-PII Hotel fields via CONFIG_FIELDS
  https://github.com/canary-technologies-corp/canary/pull/47477
  Author: Ramiro Nieto. State: OPEN, mergeable. My prior review (2026-06-16) was
  CHANGES_REQUESTED with two comments. Both are now properly addressed.

  ### Comment 1 — FK fields trigger a DB fetch per relation (was the not-so-nitty one)
  ADDRESSED CORRECTLY, exactly as I suggested (commit db4f9630, lint follow-up 514a2d2).
  - `_Registration` now carries an `attnames` map (field name -> column attname, e.g.
    `company` -> `company_id`).
  - `_pre_save` snapshots via `getattr(old, attname)` and `only(*attnames)`; `_post_save`
    compares via `getattr(instance, reg.attnames[field])`. Both read the raw `_id` column,
    so the related object is never fetched (no per-relation query).
  - Bonus: added an `isinstance(field, models.Field)` guard in `register()` to skip reverse
    relations / GFKs (logs `change_tracker.skipping_non_field`).
  - He added the explicit regression test I asked for:
    `test_changing_a_field_does_not_load_tracked_relations` populates every tracked relation,
    changes a plain field, and uses `CaptureQueriesContext` to assert no related table is read.

  ### Comment 2 — hundreds of per-field tests are too slow
  ADDRESSED (commit 59ad547). Collapsed into one test,
  `test_every_config_field_change_is_tracked_and_json_serializable`: single hotel/transaction,
  loops all CONFIG_FIELDS, isolates each field in a savepoint, aggregates failures and reports
  them together (fails loud, doesn't poison the outer txn). Unhandled field types raise an
  AssertionError rather than being silently skipped — good.

  ### Verification
  - Read the PR-branch versions of change_tracker.py (514a2d2) and the test file directly via
    git show (my local worktree is on a different branch).
  - `_json_safe` imports (date, time, Decimal, FieldFile) all present at top of change_tracker.py.
  - Logic traced for FK (compare by id), FileField (FieldFile.name), and 2-distinct-instance
    relation cases — all sound.
  - CI: all completed checks pass, 0 failures. BUT `make test-backend` was still PENDING at
    review time — I have NOT confirmed the new/changed tests pass on CI yet. Worth a glance
    before approving.

  ### Recommendation
  My change requests are satisfied. Recommend APPROVE once `make test-backend` goes green.
  I did NOT post anything to GitHub (no approval/comment submitted) — say the word and I'll
  draft + post an approval review.
project: null
source_id: null
tags: []
time_minutes: 5
title: Review Rami again
updated: 2026-06-17 14:49:18.660610
waiting_on: null
waiting_since: null
working_on: false
---

https://github.com/canary-technologies-corp/canary/pull/47477