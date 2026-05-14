---
area: null
contexts:
- react
created: 2026-05-13 11:28:24.218561
defer_until: null
due: null
energy: medium
id: 2026-05-13T1128-review-pr-45249-exclude-above-property-users-from
order: null
output: '## Agent run 2026-05-13T17:45:00Z


  **Verdict: Approve** — clean, well-structured PR. Ready to approve once out of draft.


  ### What it does

  Replaces legacy `getUsers` call in the unanswered-messages escalation settings card
  with `useHotelUsersAndDepartments({ includeAboveProperty: true })`. Corp users are
  fetched so existing rules (42 in prod) that reference them keep rendering. The "Add
  staff" picker filters them out via a new `is_above_property` flag on the `with_permissions`
  endpoint response.


  ### Backend (6 files, +52/-22)

  - `StaffUser` struct gains `user_id`, `email`, `phone`, `is_above_property` fields

  - `above_property_user_ids` query moved outside conditional so it populates the
  flag for all responses

  - `select_related("userprofile")` added — fixes latent N+1

  - Tests cover new fields and `is_above_property` for both property and portfolio-only
  users


  ### Frontend

  - Card: `getUsers` + `data()` → `useHotelUsersAndDepartments` composable in `setup()`.
  Mixes Options/Composition API but the existing component already does this.

  - Modal: `getNonSelectedStaff` adds `!user.is_above_property` filter

  - Modal: dropdown value `s.id` (string!) → `s.user_id` (number) — **this is a latent
  bug fix**. Old `User.id` was `string` while `selectedStaff` stores `number` via
  `user_id`. The new code is type-consistent.

  - Composable: backward-compatible `options.includeAboveProperty` parameter (defaults
  `false`); existing callers in ThreadAssignmentFilter and AssignToUserOrDepartmentSelect
  unaffected.


  ### Verified

  - No performance regression: `above_property_user_ids` query already ran for existing
  callers (who pass `false`); only the new caller (passing `true`) is new and needs
  it.

  - `phone_no` is `CharField(blank=True)` → always string, never None. `StaffUser.phone:
  str` is safe.

  - `users` ref from composable auto-unwraps in Options API `this.users` context —
  correct Vue 3 behavior.

  - Access-regression analysis in description is solid (zero rows with SETTINGS but
  not PRODUCT across all regions).


  ### No blocking issues found. Minor observations:

  - `email` and `phone` now returned to all `with_permissions` callers, not just escalation
  card. Low risk — staff contact info was already exposed via legacy `getUsers` endpoint,
  so no new data exposure vector.

  - The `s.id` → `s.user_id` fix is worth calling out in the PR description as a bonus
  correctness fix.

  '
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/45249
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #45249: Exclude above-property users from Unanswered Messages'
updated: 2026-05-13 13:09:03.864401
waiting_on: null
waiting_since: null
working_on: false
---

Andres requested review (draft). Replaces legacy getUsers with useHotelUsersAndDepartments + includeAboveProperty:true. https://github.com/canary-technologies-corp/canary/pull/45249