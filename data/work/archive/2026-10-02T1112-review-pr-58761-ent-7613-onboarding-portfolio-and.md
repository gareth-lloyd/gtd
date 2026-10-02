---
area: null
completed_at: 2026-10-02 13:01:43.841433
contexts:
- react
created: 2026-10-02 11:12:14.444397
defer_until: null
due: null
energy: medium
id: 2026-10-02T1112-review-pr-58761-ent-7613-onboarding-portfolio-and
order: null
output: |
  ## Agent run 2026-10-02T09:31:46Z

  **Verdict: approve, with optional nits.** Nothing blocking in PR #58761
  (https://github.com/canary-technologies-corp/canary/pull/58761, head 7c6ef15aaa5).
  Nothing was posted to GitHub. A draft review body is at the bottom.

  **Your approval will not unblock it.** All three touched apps (`onboarding/`,
  `portfolios/`, `hotel_staff/`) are pod-enterprise in CODEOWNERS (lines 181, 184, 186),
  and you are not in that team. One of abrad, rrgrs, lmenaolivares or andresfigueira
  has to approve (membership re-checked today).

  ### What I checked

  - Read the full diff (13 files, +447/-31) against ENT-7613
    (https://linear.app/canary-technologies/issue/ENT-7613). Every site the ticket
    lists is converted, plus the readiness report form.
  - No direct `slug_name` hotel lookups remain in the three apps at the PR head
    (git grep; the remaining hits are writes and serialisation).
  - `HotelSlug.slug` has a unique constraint, so `Onboarding.objects.get(hotel__hotelslug__slug=...)`
    cannot return duplicates from the join.
  - `Hotel` uses a plain manager, so going through `HotelSlug` does not surface hotels
    that `Hotel.objects` used to hide.
  - Readiness form: `clean()` compares the returned dict keys to the input set, so it
    only works if `values_list("canary_hotel__hotelslug__slug", ...)` returns the matched
    slug and not every slug the hotel has. I printed the SQL locally: one join on
    `hotels_hotelslug`, so only the matched slug comes back.
  - Staff update view: the permission check in `validate_object` runs over the hotels
    resolved from `hotels_by_slug`, so an old slug gets the same permission check as the
    current one.
  - Child portfolio create: this closes a real hole on master. An old slug skipped the
    parent-membership check, and `PortfolioService.add_hotels` then auto-added the hotel
    to the parent. The new view test covers it.
  - `HotelSpecifiedByMultipleSlugs` is a `BadRequest`, and `load_schema` only catches
    `ValidationError`, so it reaches the error middleware as a 400.
  - CI on the head commit: `make test-backend`, backend linters, OpenAPI staleness and
    Macroscope correctness all passed. Macroscope's one finding (first assignment lost
    when a hotel is named by two slugs) was fixed in 7c6ef15aaa5.

  ### Not verified

  - I did not run the tests locally. I relied on CI.
  - I did not query prod for hotels missing a `HotelSlug` row for their current
    `slug_name`. The sibling PR #58479 (https://github.com/canary-technologies-corp/canary/pull/58479)
    did not either. `HotelsMiddleware` already depends on that row, so such a hotel would
    already be broken. If you want the check, against `CANARY_RAW.CANARY` (dedupe CDC rows first):
    `SELECT COUNT(*) FROM HOTELS_HOTEL h LEFT JOIN HOTELS_HOTELSLUG s ON s.hotel_id = h.id AND s.slug = h.slug_name WHERE s.id IS NULL`

  ### Optional nits (none blocking)

  1. The staff path still 500s on an unknown slug. `HotelAssignmentsArgs` has no
     missing-slug check, so `hotels_by_slug[...]` raises `KeyError` in
     `hotel_staff/views/hotel_staff_user.py:123` and in the service. The portfolio path
     got this fixed in the same PR. Existing behaviour, outside the ticket.
  2. The "resolve slugs to hotels, reject one hotel named twice" logic is written twice
     (`hotel_staff_user.py` and `portfolio_user_management.py`). One helper would do.
  3. The 400 for `hotel_specified_by_multiple_slugs` is only tested at service level.
     No test goes through a view.
  4. `__make_property_role_assignment_changes.hotel_not_found` logs at error level. That
     branch was dead on master and now fires on a mistyped slug, so warning may fit better.
  5. FYI: onboarding create for an existing hotel now reads the hotel through
     `HotelSelector.get_hotel_by_slug_name`, which is `@readonly_database()`. The router
     allows replica-to-primary relations, so the only exposure is replica lag.

  ### Existing authz gaps I noticed (not caused by this PR, read from code only, not exercised)

  These work with current slugs on master, so the PR does not widen them. Both deserve
  a ticket if one does not exist.

  - **PATCH portfolio, `added_hotel_slugs`.** Martin flags this in the PR caveats.
    `UpdatePortfolioRequestSchema` (`portfolios/views/portfolio.py:98`) has no
    parent-membership check, and `add_hotels` auto-adds missing hotels to the parent
    (`portfolios/services/portfolio.py:425-433`). A user with `PORTFOLIO_CAN_CREATE_CHILD`
    appears able to pull any hotel into a child and its parent by slug.
  - **Portfolio user create and update, `property_role_assignments[].hotel_slug`.**
    Neither schema checks that the hotel belongs to the caller's portfolio, and the PATCH
    target user is `NoAuthorize()`. Role grants are guarded (`grant_roles_to_user` requires
    the hotel to be in the role's portfolio), but the rest is not: an empty role list
    creates a `CompanyHotelUser` at any hotel, and `unassign` removes a user's
    portfolio-managed non-SSO grants at any hotel. Worth a quick repro before filing.

  ### Draft review body (not posted, needs your OK or post it yourself)

  > Looks good. I read every site against the ticket, and nothing in onboarding,
  > portfolios or hotel_staff still looks hotels up by `slug_name`. Good catch on the
  > child-portfolio check: on master an old slug skipped it and `add_hotels` pulled the
  > hotel into the parent.
  >
  > Optional, none blocking:
  > - `HotelAssignmentsArgs` still raises `KeyError` (500) for an unknown slug. The
  >   portfolio path now returns `NonExistentHotelsSpecifiedError`; the staff path could do the same.
  > - The resolve-and-reject-duplicates logic is in two places. A shared helper would keep them in step.
  > - No view-level test asserts the 400 for `hotel_specified_by_multiple_slugs`.
  > - `hotel_not_found` in portfolio user management logs at error level and is now reachable from a typo.
  >
  > Is there a ticket for the PATCH `added_hotel_slugs` gap in your caveats? I think the
  > portfolio user endpoints have a similar one: `property_role_assignments[].hotel_slug`
  > is never checked against the portfolio.
  >
  > Note my approval does not clear CODEOWNERS here, so this needs a pod-enterprise reviewer.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/58761
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #58761: [ENT-7613] Onboarding, portfolio, and staff views look up
  hotels by slug_name instead of HotelSlug'
updated: 2026-10-02 13:01:43.841425
waiting_on: null
waiting_since: null
working_on: false
---

https://github.com/canary-technologies-corp/canary/pull/58761 — author martinrodriguezcanary, requested from you personally and pod-enterprise. Only the bot has reviewed so far. Sibling AD fix #58479 already merged.