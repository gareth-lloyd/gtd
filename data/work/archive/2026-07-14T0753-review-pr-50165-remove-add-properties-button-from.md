---
area: null
contexts:
- react
created: 2026-07-14 07:53:55.674988
defer_until: null
due: null
energy: medium
id: 2026-07-14T0753-review-pr-50165-remove-add-properties-button-from
order: null
output: |
  ## Agent run 2026-07-14T14:45:24+01:00

  Reviewed PR #50165 (https://github.com/canary-technologies-corp/canary/pull/50165)
  "Remove Add properties button from hotels to be onboarded page" — TOOL-396
  (https://linear.app/canary-technologies/issue/TOOL-396), author ramironieto.

  **Verdict: LGTM — safe to approve.** Clean frontend-only deletion, 4 files,
  +1/−157. No blocking issues found.

  What I verified:
  - All removed symbols (`AddCohortHotelsModal`, `createCohortHotels`,
    `Manage.Onboarding.HotelsOnboarded.AddProperties` analytics event) have zero
    references outside the files this PR deletes/edits — grepped the whole
    frontend tree.
  - Kept shared pieces (`HotelIdentifierInput`, `OnboardingTypeSelect`,
    `useCohortErrorHandling`, `useIdentifierProcessing`) still have live
    consumers (`AddCohortModal`, `CustomScriptModal`, `RolloutInputForm`), as
    the PR description claims.
  - The `CohortHotel` type import removal in
    `frontend/packages/shared/api/onboarding/CohortHotel.ts` is correct — the
    deleted `createCohortHotels` was its only remaining user in that file.
  - PR-head version of `CohortHotelsPage.vue` fetched and inspected: no stale
    `modalStore`/`CanaryButton`/`ref` imports left behind.
  - No test/e2e/cypress files reference the removed button or event.
  - Deploy ordering is right: backend endpoint (`CohortHotelsView.post`) stays
    until a follow-up PR after this frontend deploys.
  - CI fully green (typecheck, eslint, knip, a11y all pass; rest skipped as
    frontend-only).

  One optional nit (non-blocking, fine to fold into the follow-up backend PR):
  `defineExpose({ refresh })` in `CohortHotelsTable.vue` (~line 386) loses its
  last consumer with this PR — `CohortHotelsPage` was the only caller of the
  exposed `refresh()`; `CohortDetail.vue` doesn't use a template ref on the
  table.

  Not done (needs your approval): no GitHub review/comment posted. If you want,
  I can draft an approving review with the nit above for you to confirm, or you
  can just approve it yourself.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/50165
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #50165: Remove Add properties button from hotels to be onboarded
  page'
updated: 2026-07-14 14:48:03.140819
waiting_on: null
waiting_since: null
working_on: false
---

TOOL-396, author ramironieto — removes the last opportunity-duplicated CohortHotel field path. Personally requested.
https://github.com/canary-technologies-corp/canary/pull/50165