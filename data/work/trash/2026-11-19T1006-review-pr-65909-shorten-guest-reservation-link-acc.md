---
area: null
completed_at: null
contexts:
- react
created: 2026-11-19 10:06:56.575311
defer_until: 2026-11-19 21:38:00
due: null
energy: medium
id: 2026-11-19T1006-review-pr-65909-shorten-guest-reservation-link-acc
order: null
output: |
  ## Agent run 2026-11-19T12:47

  PR #65909 (https://github.com/canary-technologies-corp/canary/pull/65909), by in15. Nothing was posted to GitHub.

  **Verdict: the code is correct and safe to approve as code. I would hold approval until the product questions below have an owner, because the PR has no Linear ticket and no production numbers.**

  ### What it does
  - One constant: `RESERVATION_ACCESSIBLE_AFTER_DEPATURE_DAYS` 45 -> 7 in `backend/canary/guest/views/guest_reservations_view.py:82`.
  - It gates two places: the by-slug/uuid read (`:383-386`) and the confirmation-number lookup (`:667-675`). The name-and-dates lookup stays at 1 day.
  - Day 7 after departure still opens; day 8 returns 404. The two new tests pin both sides with literal offsets and frozen time, which is better than the old test that derived its offset from the constant.
  - Removing `test_lease_null_once_departure_buffer_exceeded` is justified: the lease buffer is also 7 days (`check_in/services/check_in.py:108`), so this view now 404s before it could return a null lease. The service-level test still covers the rule.

  ### Concerns, most important first
  1. **Post-stay folio and receipt access is not mentioned in the PR.** The guest app charges page (`frontend/guest/src/views/MyReservationCharges.vue`) reads from the reservation store, which is null once the reservation read 404s. A guest who returns to their link after day 7 for a receipt loses that page. I did not confirm this in a browser.
  2. **Hotel-scheduled messages at 2, 3 and 4 weeks will now carry a dead link** when they use `{{ guest_url }}`. The author flags this and says the count of affected hotels needs a production query. Nobody has run it. This is the number that decides whether 7 is acceptable or whether 30 (covers every "weeks" option) is the better value.
  3. **The window is only enforced at the bootstrap read, so the exposure reduction is partial.** Sibling guest endpoints keyed by the same reservation uuid or slug have no departure check that I could find:
     - `guest_api/hotels/<slug>/reservations/<uuid>/e_folio` (`guest/views/guest_e_folio.py:141`) returns charges and card details.
     - `v1/reservations/<slug>` (`guest/views/reservation_external_view.py`), deliberately lightweight.
     - `guest_api/reservations/<slug>/<slug>/purchase_orders` POST (`guest/views/guest_reservation_purchase_orders.py:58`).
     Pre-existing and not a blocker, but the "lowers the exposure of guest data" claim only holds for the main payload. Worth a follow-up ticket.
  4. **No Linear ticket** ("none yet"). Repo rules require one, and it is unclear who asked for 7 days or why 7.
  5. Minor, pre-existing: the by-slug read compares the UTC date while the lookup compares the hotel-local date. At 7 days a one-day skew matters more than it did at 45. The two 7-day constants (link window, lease buffer) are now equal by coincidence, with nothing tying them together.

  ### Not verified by me
  - I did not run the tests locally. CI shows 39 checks passing and the only failure is the missing approval. The backend test job appears in the skipped list under a templated name, so I could not confirm from the rollup that the backend suite ran on this PR.
  - I read the e-folio request schema only for departure checks, not its full validation.

  ### Draft review comment (not posted)
  > Code and tests look right, and the boundary tests are a real improvement. Before I approve:
  > 1. Can we get a Linear ticket with who asked for 7 days and why 7?
  > 2. Can we run the production query you mention: hotels with a post-departure custom message at 1 week or later that uses `{{ guest_url }}`? If it is more than a handful, 30 days would cover every "weeks" option.
  > 3. Guests returning for their folio after day 7 lose the charges page (`MyReservationCharges.vue` depends on the reservation read). Is that intended?
  > 4. Follow-up, not for this PR: `guest_api/.../e_folio`, `v1/reservations/<slug>` and the purchase orders POST have no post-departure window, so a holder of the uuid can still reach charges after day 7.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/65909
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #65909: Shorten guest reservation link access after departure to
  7 days'
updated: 2026-11-20 12:52:24.175141
waiting_on: null
waiting_since: null
working_on: false
---

https://github.com/canary-technologies-corp/canary/pull/65909
Author in15, branch in15/shorten-post-departure-link-window. Requested this morning; Dana, Blake and Andrew Monroe also requested.