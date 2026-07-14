---
area: null
contexts: []
created: 2026-07-14 14:24:16.894020
defer_until: null
due: null
energy: low
id: 2026-07-14T1424-review-rami-pr
order: null
output: |
  ## Agent run 2026-07-14T14:35:00+01:00

  Reviewed PR #49640 (https://github.com/canary-technologies-corp/canary/pull/49640)
  — "[TOOL-108] Drop deprecated CohortHotel opportunity-mirror columns" by Ramiro
  Nieto. **Verdict: LGTM — safe to approve and merge.** Nothing posted to GitHub;
  review below is local only.

  What it does: final phase of the CohortHotel cleanup chain
  (#49180 → #49409 → #49415 → #49533 → this). 2 files, +62/−84: removes the 11
  `deprecate_field()` definitions from `CohortHotel` and adds migration
  `onboarding/0159` with 11 `RemoveField` ops +
  `IgnoreMigrationLintRules(codes=["DROP_COLUMN"])`.

  Verified:
  - Correct deprecate_field 3-phase flow per docs/backwards-compatible-migrations.
    Predecessor #49533 (deprecation, https://github.com/canary-technologies-corp/canary/pull/49533)
    merged 2026-07-07 with AUTO_DEPLOY — the "do not merge until #49533 is deployed
    and stable" gate has had 7 days; satisfied barring any known revert risk.
  - No remaining production references to the dropped columns: no Django admin
    registers CohortHotel; model Meta only carries the search index; the one DB
    index on a dropped column (idx_cohorthotel_go_live_sot) was already removed
    concurrently in 0158; search_text/search_vector don't derive from these fields.
    All other grep hits are SalesforceOpportunity's same-named fields (the data's
    new home) or stub-helper kwargs in testing.py — both intentional.
  - Migration-only PR (migration + model file), dependency on 0158 correct, no
    competing 0159 on current master. CI green, 3058 tests reported passing.

  Minor notes (none blocking):
  1. Several `backend/canary/tmp/repeatable/` scripts still query the dropped
     CohortHotel columns (monitored_hotel_state_utils.py:31,
     bw/correct_best_western_portfolio_memberships.py,
     bw/analyze_inconsistencies.py,
     find_cohort_hotels_no_longer_active_from_salesforce.py, tmp/unmigr.py).
     They were already broken at ORM level by #49533's deprecate_field, so not a
     regression of this PR — but "repeatable" implies re-run intent; worth a
     follow-up cleanup to route them via salesforce_hotel_account.opportunities.
  2. Cosmetic: the migration comment says the columns "were deprecated via
     deprecate_field() in 0157/0158" — 0157 is an AlterField (nullable
     training_state) and 0158 an index drop; deprecate_field itself generates no
     migration. Harmless misattribution.
  3. Column drop is physical — if any out-of-band SQL consumer (warehouse ETL,
     Metabase) selects these cohorthotel columns it will break; presumably vetted
     in the earlier phases, just flagging.

  Suggested next step: approve on GitHub (I did not post anything) and remind Rami
  of note 1 as an optional follow-up.
project: null
source_id: null
tags: []
time_minutes: 5
title: review rami pr
updated: 2026-07-14 14:49:16.156863
waiting_on: null
waiting_since: null
working_on: false
---

https://github.com/canary-technologies-corp/canary/pull/49640