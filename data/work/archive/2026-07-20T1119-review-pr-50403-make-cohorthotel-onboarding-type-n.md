---
area: null
contexts:
- react
created: 2026-07-20 11:19:04.361274
defer_until: null
due: null
energy: medium
id: 2026-07-20T1119-review-pr-50403-make-cohorthotel-onboarding-type-n
order: null
output: |
  ## Agent run 2026-07-20T14:05

  Reviewed PR #50403 (https://github.com/canary-technologies-corp/canary/pull/50403)
  — ramiro nieto, +20/-0, 2 files. Linear: TOOL-396
  (https://linear.app/canary-technologies/issue/TOOL-396/delete-the-onboarding-type-field-on-cohorthotel)

  **Verdict: approve.** Nothing blocking. Review is local only — no GitHub comment
  posted (needs your go-ahead).

  ### What it does
  `AlterField` on `cohort_hotel.onboarding_type` → `blank=True, null=True`, plus the
  matching model change in `backend/canary/onboarding/models/cohort_hotel.py:32`.
  Step 2 of a 4-step column deprecation (1: #50165 merged, 2: this, 3: #50169
  remove reads/writes + `deprecate_field`, 4: column drop).

  ### Verified
  - **Migration is safe.** `DROP NOT NULL` in Postgres is a catalog-only change —
    no table rewrite, ACCESS EXCLUSIVE lock held for microseconds. Fine on a large
    table.
  - **No numbering collision.** `origin/master` is at `0159_remove_cohorthotel_deployment_detail_and_more`,
    which is exactly this migration's dependency. `0160` is free (usual merge-race
    caveat if another onboarding migration lands first).
  - **Deploy ordering is safe.** Migrations run ahead of code; old code always
    supplies a value, and a nullable column accepts it. No rows become NULL from
    this PR alone.
  - **PR is migration-only** (migration + model), so it satisfies the repo's
    migration-PR linter rule.
  - **CI green**: 64 success / 192 skipped / 1 neutral / 0 failures.
  - **Matches in-file precedent** — every other deprecated field on `CohortHotel`
    (`training_state`, `deployment_segment`, `onboarding_status`, …) is
    `blank=True, null=True`. Same shape as #49415.

  ### Two things worth raising with Ramiro (both are #50169 concerns, not blockers here)

  1. **"Write-only" isn't quite accurate — there's a live read.**
     `CohortHotelService.get_onboarding_type_for_cohort_hotel`
     (`backend/canary/onboarding/services/cohort_hotel.py:439-448`) still reads
     `cohort_hotel.onboarding_type` as the fallback for cohort-less "earmark" rows.
     It's already None-safe (`... if raw_onboarding_type else None`), so this PR is
     fine. But once #50169 stops writing the column, earmark rows return `None`, and
     the caller at line 457+ dispatches through a chain of `elif onboarding_type ==
     ...` with no else — so those rows silently fall through to "no required
     onboarding values". Worth confirming #50169 either kills the earmark path
     entirely or handles the None case loudly.

  2. **`onboarding_type` is part of a `get_or_create` lookup.**
     `CohortHotelService.add_to_cohort` (~line 412) does
     `CohortHotel.objects.get_or_create(salesforce_hotel_account=…,
     onboarding_type=cohort.onboarding_type, cohort=cohort)`. Once the column stops
     being written, the lookup becomes `WHERE onboarding_type IS NULL`, which won't
     match the pre-existing populated rows → duplicate `CohortHotel` rows in the
     mixed-state window. #50169 needs to drop `onboarding_type` from that lookup,
     not just from the create kwargs.

  ### Minor / take-it-or-leave-it
  - `blank=True` + `null=True` on a CharField gives two empty representations
    (`''` vs `NULL`). Normally worth avoiding, but the column is being dropped in
    two PRs' time, so not worth the churn.

  ### Suggested reply (NOT sent — say the word if you want it posted)
  > Approving. Migration is metadata-only, numbering is clean against master, and
  > it matches the `training_state` precedent.
  >
  > Two notes for #50169 rather than this PR:
  > 1. `get_onboarding_type_for_cohort_hotel` (services/cohort_hotel.py:439) still
  >    reads this column for cohort-less earmark rows. It's None-safe, but the
  >    caller's `elif` chain at :457 has no else — once writes stop, earmark rows
  >    will silently produce zero required onboarding values. Worth making that
  >    fail loud or removing the earmark path outright.
  > 2. `add_to_cohort` passes `onboarding_type` inside the `get_or_create` *lookup*.
  >    When it goes NULL, it won't match existing populated rows and you'll get
  >    duplicate CohortHotels. That kwarg needs removing from the lookup, not just
  >    from the create.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/50403
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #50403: Make CohortHotel.onboarding_type nullable'
updated: 2026-07-20 17:04:28.219657
waiting_on: null
waiting_since: null
working_on: false
---

ramironieto, personally requested, still unreviewed since 7/16. Prep step for TOOL-396 column deprecation.
https://github.com/canary-technologies-corp/canary/pull/50403