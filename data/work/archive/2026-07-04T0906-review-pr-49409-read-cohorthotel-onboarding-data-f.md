---
area: null
contexts:
- react
created: 2026-07-04 09:06:17.741869
defer_until: null
due: null
energy: medium
id: 2026-07-04T0906-review-pr-49409-read-cohorthotel-onboarding-data-f
order: null
output: |
  ## Agent run 2026-07-06T14:35 — Review of PR #49409

  PR: https://github.com/canary-technologies-corp/canary/pull/49409
  "Read CohortHotel onboarding data from SalesforceOpportunity" (Ramiro Nieto). Refactor,
  +235/-476, no migration by design. Reviewers: gareth-lloyd + abrad + pod-enterprise.

  **Verdict: LGTM — approve with minor, non-blocking notes.** Clean, well-scoped refactor.
  I did NOT post anything to GitHub (no approval to). Draft comment below if you want to post it.

  ### What it does
  CohortHotel's opportunity-mirror columns (training/go-live/deployment/status) have been
  frozen since the Salesforce sync stopped dual-writing them (#41377). This PR stops reading
  those stale columns and instead dereferences the latest SalesforceOpportunity on the row's
  account matching the *cohort's* onboarding_type. Unblocks the actual field deprecation in a
  follow-up. Also deletes genuinely dead code (IHG go-live write-back, the
  create_or_update_cohort_hotels_from_opportunities sync method + its onetime command, and
  CohortHotel.gateway_account_url).

  ### Verified correct
  - **No orphaned callers.** The deleted `create_or_update_cohort_hotels_from_opportunities`,
    the `onetime_create_salesforce_hotel_accounts` command, and `CohortHotel.gateway_account_url`
    have no remaining references outside their own now-deleted tests (which the PR removes). The
    surviving `HotelSchema.get_gateway_account_url` is a different, kept method.
  - **No missed readers of the mirror columns.** Swept the onboarding app: the only other places
    touching `go_live_date_from_source_of_truth`/`onboarding_status`/`stage`/deployment fields
    read them off `SalesforceOpportunity` or the `OnboardingStateAccordingToSourceOfTruth`
    dataclass (e.g. `wyndham_connect_plus_service.py:201` → populated from `opportunity.go_live_date`
    in `get_onboarding_states`), not off CohortHotel. Deprecation should be safe.
  - **N+1 handled.** List view adds `prefetch_related("cohort_hotels__salesforce_hotel_account__opportunities")`;
    the service method filters `.opportunities.all()` in Python so it reuses that cache. The
    agent_context provider does its own single batch query per page (`__in=account_ids`). No per-row queries.
  - **Two code paths stay consistent.** Service `get_latest_opportunity_for_cohort_hotel`
    (`max` by `(created_at, id)`) and the provider (`order_by("created_at","id")`, last-wins)
    both resolve the same "latest matching opportunity" and both match on the cohort's onboarding_type.
  - **Runtime-safe annotation.** `get_latest_opportunity_for_cohort_hotel(cohort_hotel: CohortHotel)`
    uses a TYPE_CHECKING-only import, but `salesforce_opportunity.py` has `from __future__ import
    annotations` (line 1), so no NameError.
  - **dump_only conversions safe.** `onboarding_type`/`training_date`/`training_state` became
    Method dump_only fields. `CohortHotelSchema` is only ever `.dump()`ed (nested list + POST
    response) — never `.load()`ed — so no write path silently drops input.
  - **TrainingState enums identical.** `CohortHotel.TrainingState` and
    `SalesforceOpportunity.TrainingState` are the same TextChoices (unknown/untrained/completed);
    the msgspec `training_state: str` field accepts the member (str subclass). Fine.

  ### Notes (non-blocking) — worth raising with Ramiro
  1. **Test gap on the agent_context provider.** New coverage (`test_salesforce_hotel_account_schema.py`)
     is solid and covers the *schema* path well (latest-matching, no-match, cohortless). But the
     provider (`agent_context/provider.py`) now sources onboarding_status/stage/training_state from
     the opportunity via a batch query, and `agent_context/tests/test_cohort_provider.py` was NOT
     updated — it only asserts counts/pagination/identity, never the mirrored field values. Suggest
     one test asserting a provider-serialized hotel picks up the latest matching opportunity's fields.
  2. **Duplicated "latest matching opportunity" logic.** The Python-filter in the service and the
     inline batch query in the provider must stay in sync (ordering + onboarding_type match). The
     batch form is justified (avoids per-row prefetch across N accounts), but the drift risk is real
     — a shared comment/helper documenting the "latest = max(created_at, id), match cohort
     onboarding_type" rule would help.
  3. **Cohortless "earmark" rows now always render empty training/go-live** even when a matching
     opportunity exists on their account, because the match keys off `cohort.onboarding_type` and
     cohort is None. Intentional + documented + tested, and moot while the SF sync isn't dual-writing —
     but worth a one-line confirmation that no admin UI surfaces earmark rows expecting those values.
  4. **Cosmetic:** `get_training_state` returns `opportunity.training_state` (DB string) in one
     branch and the `TrainingState.UNKNOWN` enum member in the other; same for the provider. Both are
     str-equal so harmless, but returning `.value` consistently reads cleaner.

  ### Did NOT verify
  - Did not run the 412 tests locally (author reports green; ruff+pyright clean). My tree is on my
    own branch, not the PR branch — analysis is from `gh pr diff` + reading base files.
  - Frontend `CohortHotel.ts` change (dropped deployment_detail/segment/onboarding_status) only
    eyeballed; assumed no remaining frontend consumers per author's shared-typecheck-clean note.

  Draft GitHub review comment (NOT posted — say the word and I'll post it):
  > LGTM, nice cleanup. Verified there are no remaining CohortHotel mirror-column readers and no
  > orphaned callers, and the prefetch keeps the list view off N+1. Two small non-blockers:
  > (1) the agent_context provider now sources these fields from the opportunity but
  > test_cohort_provider.py wasn't updated to assert the sourced values — worth one test there;
  > (2) the "latest matching opportunity" rule is now implemented twice (service Python-filter +
  > provider batch query) and they need to stay in sync — a shared helper or a shared comment would
  > de-risk drift. Neither blocks merge.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/49409
tags:
- morning-gtd
- github
time_minutes: 25
title: 'Review PR #49409: Read CohortHotel onboarding data from SalesforceOpportunity'
updated: 2026-07-06 14:57:59.853459
waiting_on: null
waiting_since: null
working_on: false
---

Ramiro Nieto requested you + abrad. Refactor: CohortHotel dereferences onboarding data via SalesforceOpportunity.
https://github.com/canary-technologies-corp/canary/pull/49409