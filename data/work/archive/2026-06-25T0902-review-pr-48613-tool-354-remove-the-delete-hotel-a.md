---
area: null
contexts:
- react
created: 2026-06-25 09:02:06.015482
defer_until: null
due: null
energy: medium
id: 2026-06-25T0902-review-pr-48613-tool-354-remove-the-delete-hotel-a
order: null
output: |
  ## Agent run 2026-06-25T06:27:38Z

  Reviewed PR #48613 "[TOOL-354] Remove the 'Delete hotel and recreate' button"
  by Ramiro Nieto. https://github.com/canary-technologies-corp/canary/pull/48613
  (Linear TOOL-354: https://linear.app/canary-technologies/issue/TOOL-354)

  **Verdict: APPROVE — clean, well-scoped, low-risk removal. No changes requested.**

  Scope: 6 files, +7/-92. Removes the staff-only hard-delete-and-recreate
  capability: the `DELETE /onboarding/hotels/<sfdc_account_id>` endpoint
  (`HotelView` in onboarding/views/common.py) plus its URL route, the export,
  and the two front-end "Delete & Recreate" buttons + modal recreate path.
  Plain "Create hotel" is unchanged.

  Rationale (per PR/ticket) is sound: the delete rarely worked
  (`OnboardingScriptHotel.hotel` is PROTECT → ProtectedError once a hotel is
  tied to a script batch), it was gated only by `is_staff`, and an irreversible
  hard delete is the wrong model.

  Verification I performed against the repo:
  - No `reverse()` / template references to the removed URL name `"hotel"` —
    safe to drop the route. (The remaining onboarding `reverse(...)` calls all
    target `admin:hotels_hotel_change`, unrelated.)
  - No dedicated backend test existed for the deleted endpoint — the only
    "HotelView" test-file matches are CohortHotelView / OnboardingScriptHotelView
    (substring collisions), so nothing was orphaned or silently dropped.
  - Backend import cleanup is correct and complete: PR removes the now-unused
    `ProtectedError`; `CompanyHotelUser`, `SalesforceHotelMetadata`, and
    `NotFound` all retain other usages in common.py, so they're correctly kept.
  - Front-end logic is consistent: OnboardingCreate.vue now hides the whole
    action `b-field` via `v-if="!account.hotel"` (no button when a hotel already
    exists); OnboardingRowDetails.vue gates the Create button with
    `&& !onboarding.hotel` and drops the `is-danger`/recreate branch;
    OnboardingCreateModal.vue removes the `recreateImmediately` prop and the
    `recreate()` function, always calling `create()` on mount. No dangling
    references to `recreateImmediately` / `recreate` remain on the branch.
  - No backward-compat concern: the only caller of the DELETE endpoint was the
    front-end code removed in the same PR. The remaining `hotels/` (POST, with
    trailing slash) route is untouched and does not collide.

  Nits / optional (non-blocking, did not request):
  - None material. The change is surgical and matches conventions.

  Note: I did NOT post this review to GitHub. CI status not checked. Say the word
  if you want me to (a) post an approving review/comment on the PR, and/or
  (b) check CI — I'll show exact text before sending anything outbound.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/48613
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #48613: [TOOL-354] Remove the "Delete hotel and recreate" button'
updated: 2026-06-25 12:17:58.240019
waiting_on: null
waiting_since: null
working_on: false
---

Rami requested your review (personal). Removes staff-facing hard-delete capability + DELETE /onboarding/hotels/<id> endpoint.
https://github.com/canary-technologies-corp/canary/pull/48613