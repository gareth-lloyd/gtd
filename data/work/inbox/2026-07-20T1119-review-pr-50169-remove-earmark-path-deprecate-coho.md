---
area: null
contexts:
- react
created: 2026-07-20 11:19:04.428356
defer_until: null
due: null
energy: medium
id: 2026-07-20T1119-review-pr-50169-remove-earmark-path-deprecate-coho
order: null
output: |
  ## Agent run 2026-07-20T13:52 (local)

  Reviewed PR #50169 (https://github.com/canary-technologies-corp/canary/pull/50169)
  — [TOOL-396] Remove earmark path, stop writes and deprecate CohortHotel.onboarding_type.
  Author: ramironieto. +30 / -227, 7 files. State: OPEN, MERGEABLE.
  Linear: https://linear.app/canary-technologies/issue/TOOL-396
  NOTHING POSTED TO GITHUB — local review only.

  **Verdict: request changes.** The direction is right and the removal is thorough
  (no stale reads/writes of `cohort_hotel.onboarding_type` remain outside tests).
  Two things should be resolved before merge, one of which is a data-loss ordering
  risk that is easy to miss.

  ### 1. Orphaned earmark rows have no cleanup step, and the window closes at column DROP (main issue)

  `get_or_create_cohort_hotels_for_cohort` previously adopted a cohort-less row for
  the same SalesforceHotelAccount. The PR replaces that with `existing = None`
  (backend/canary/onboarding/services/cohort_hotel.py:317), so it now always creates
  a NEW row. The updated test
  `test_get_or_create_cohort_hotels_for_cohort__leaves_cohortless_row_untouched`
  asserts exactly this, so it is deliberate — but the consequence for rows already
  in prod is not addressed anywhere in the PR or the deprecation plan:

  - Existing cohort-less rows are never adopted → orphaned permanently.
  - After this PR they serialize with `onboarding_type: null` (the schema test was
    updated to assert this), while still appearing on the "To be onboarded" page via
    the `has_cohort=false` filter — i.e. visible rows with a blank onboarding type.
  - When a cohort is later created for the same account, a duplicate row appears.
    There is no unique constraint stopping this (migration 0094 dropped
    `unique_onboarding_type_per_salesforce_account_id`).

  Critically: `cohort_hotel.onboarding_type` is the ONLY remaining record of what
  those rows were earmarked for. Once the follow-up DROP migration runs, that
  information is gone and the rows become unidentifiable. **Cleanup (delete or
  adopt) must happen before the column drop, not after.** Ask Ramiro to either add
  a cleanup step to the deprecation plan between this PR and the DROP, or state
  explicitly why leaving the orphans is acceptable.

  ### 2. ValueError when cohort.onboarding_type is NULL (Macroscope's blocking finding — real, but lower probability than it reads)

  New code at backend/canary/onboarding/services/cohort_hotel.py:439:

      if cohort_hotel.cohort is None:
          return None
      return OnboardingType(cohort_hotel.cohort.onboarding_type)

  The old code was defensive (`OnboardingType(raw) if raw else None`); the new code
  is not. `Cohort.onboarding_type` is `null=True` (backend/canary/onboarding/models/cohort.py:27),
  so NULL is schema-permitted.

  I checked reachability: the only Cohort creation path, `CohortService.create_cohort`
  (services/cohorts.py:53), requires a non-null `OnboardingType` and rejects DEFAULT,
  so no current code writes NULL. Risk is legacy rows only — I did not (and should
  not) query prod to confirm whether any exist.

  Still worth fixing: the caller is `CohortHotelSchema.get_onboarding_type`
  (schemas/salesforce_hotel_account.py:92), which renders the "To be onboarded"
  list — a single NULL cohort would 500 the entire page. One-line fix restoring the
  falsy guard, and it costs nothing. Note `stub_cohort` defaults to
  `OnboardingType.DEFAULT`, so no test exercises the None branch — add one with the fix.

  ### 3. Dead frontend code pointing at the deleted endpoint

  `createCohortHotels` and `CreateCohortHotelsParams`
  (frontend/packages/shared/api/onboarding/CohortHotel.ts:146-162) have zero callers
  — the modal went in #50165 — and now POST to a route that no longer exists. Should
  be deleted in this PR so nobody wires it up to a 405 later.

  ### 4. Deploy ordering, not just merge ordering

  #50403 (https://github.com/canary-technologies-corp/canary/pull/50403) is still
  OPEN and is this PR's base, so merge order is enforced. But `deprecate_field` stops
  the ORM selecting/writing the column, so the nullable migration must be APPLIED in
  prod before this code deploys — otherwise INSERTs fail on the NOT NULL constraint.
  The PR body says "must merge first"; worth confirming the deploy sequencing too.
  #50165 merged 2026-07-14, so that gate is satisfied.

  ### Things I checked that are fine

  - No remaining non-test reads/writes of `cohort_hotel.onboarding_type`.
  - The `onboarding_type` list filter uses `opportunities__onboarding_type`, not the
    deprecated column — `deprecate_field` does not break it.
  - `OnboardingType` import in views/cohort_hotels.py is still used (lines 52, 121)
    after the schema removal — not an unused import.
  - `deprecate_field` usage matches existing precedent across chat/, payment_links/,
    mobile_key/. Canary linter warning about data-warehouse deprecation is expected
    and needs the Notion process followed before the DROP.
  - PR is correct that the v1 `validate_request` endpoint never appeared in
    openapi.yml — no spec change needed.

  ### Drive-by nit (pre-existing, not introduced here)

  `get_or_create_cohort_hotels_for_cohort` has `@transaction.atomic` ABOVE
  `@staticmethod`; `add_to_cohort` has the correct order. Unchanged by this PR, so
  optional, but it's adjacent and cheap to fix while in the file.

  ### Suggested next action

  Post a review requesting (1) a cleanup plan for orphaned cohort-less rows before
  the DROP, (2) the null guard + test, (3) frontend dead-code removal. Nothing has
  been sent — say the word and I'll draft the comment for approval.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/50169
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #50169: Remove earmark path, deprecate CohortHotel.onboarding_type'
updated: 2026-07-20 13:52:06.166637
waiting_on: null
waiting_since: null
working_on: false
---

ramironieto, personally requested, mergeable, unreviewed since 7/16. Follow-up to #50165 for TOOL-396.
https://github.com/canary-technologies-corp/canary/pull/50169