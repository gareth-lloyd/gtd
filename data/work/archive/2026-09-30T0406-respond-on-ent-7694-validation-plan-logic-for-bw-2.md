---
area: null
completed_at: 2026-09-30 13:18:10.559909
contexts:
- react
created: 2026-09-30 04:06:42.011151
defer_until: null
due: null
energy: low
id: 2026-09-30T0406-respond-on-ent-7694-validation-plan-logic-for-bw-2
order: null
output: |
  ## Agent run 2026-09-30 13:01:45.195202

  Draft reply for Andrea's thread on ENT-7694 (reply under Juan's comment, thread https://linear.app/canary-technologies/issue/ENT-7694/bw-property-29096-hotelkey-pms-validation-failing-despite-successful#comment-eac73034). NOT posted; needs your OK.

  ---
  Juan's read is right: fetch is healthy and the plan is doing what it was told. The problem is that what it was told is too narrow for a property that hasn't cut over yet. My thoughts on the logic:

  **The ±6-day window and the cancelled-exclusion are heuristics, not PMS constraints.** `FETCH_RESERVATION` is a lookup by confirmation number. HotelKey will return a HOLD booking for Feb 2027 by number just as happily as one arriving tomorrow. I added the ±6-day window in Feb 2025 (#21981) so we'd pick from a small pool of near-term, recently synced rows; the cancelled exclusion came in with ENT-6486 because archiving the previous PMS cancels its reservations and bumps their sync timestamp, so they'd outrank the new PMS's rows. Both were proxies for "a reservation the new PMS actually knows about". We now have a direct signal for that: the confirmation-number type (`RESERVATION_NUMBER` for HotelKey), which `_all_synced_by_another_pms` already uses.

  **Pre-cutover hotels are an expected state the rule can't pass.** A BW property mid-migration to HotelKey has HOLD (mapped to RESERVED in gateway) bookings months out and nothing this week. That's normal, not a data problem. It isn't just 29096: 17 script hotels hit `configure_pms_integration_validate.no_reservations` in the last 7 days, 16 of them in one wave on Sep 23 (this hotel alone 7 times). INCINT-64 is the same shape.

  **Proposal: widen candidate selection in tiers, keep the cap of 3 and the current error messages.**
  1. Tier 1 (today's rule): non-cancelled, non-demo, arrival within ±6 days, newest sync first.
  2. Tier 2: if empty, any non-cancelled, non-demo reservation arriving today or later whose confirmation numbers carry the current vendor's type, newest sync first. That picks up the four 2027 HOLD rows here and would have passed this hotel on Sep 25.
  3. Tier 3 (optional, last resort): cancelled rows carrying the current vendor's type. HotelKey cancelled its own test reservation, and it's still fetchable by number. I'd leave this out unless we see a vendor where it matters; a failed try just moves to the next candidate anyway.

  Only fall through to `no_reservations_in_canary` / `no_reservations_on_gateway` when all tiers are empty.

  **Error message:** agree with Juan that `pms_validation_no_reservations_in_canary` misleads. The message should say what Canary actually has, e.g. "Canary holds 9 reservations for this hotel: 5 cancelled, 4 arriving outside the ±6-day window", so CS can tell "wait" from "sync gap" without an engineer.

  This is a small change confined to `_perform_validation` in `configure_pms_integration_validate_plan.py`; happy to take it as an enterprise-pod PR this week. Until then the workarounds Juan listed stand: wait for cutover, or have HotelKey create a non-cancelled test booking inside the window and re-run Validate PMS Config.
  ---

  Evidence for the draft:
  - Code: backend/canary/onboarding/plans/configure_pms_integration_validate_plan.py `_perform_validation` (window at lines 287-288, cancelled filter line 292, cap FETCH_RESERVATION_CANDIDATE_COUNT=3).
  - Window origin: commit 337cb573bb9 "Stop permitting validation without all complete" (#21981, Gareth, 2025-02-26) https://github.com/canary-technologies-corp/canary/pull/21981
  - Cancelled exclusion origin: fa9c62c9f60 ENT-6486 (#49985) https://github.com/canary-technologies-corp/canary/pull/49985
  - Error-code split: ENT-7561 (#57017), ENT-7606 (#57524).
  - HotelKey HOLD -> RESERVED: backend/pms-gateway/vendors/integrations/hotelkey/maps/status.py
  - Groundcover, last 7 days, event `configure_pms_integration_validate.no_reservations` by CTX_onboarding_script_hotel_uuid: 17 script hotels, 26 events; 0c11f28b (bw-29096) 7 hits, last 2026-09-28T17:55Z; 16 others on 2026-09-23 16:29-17:49Z; one more on 2026-09-29T19:25Z.
  - Related: PMS-10334 (Done), INCINT-64 (open), ENT-5621 (Done).

  Next step for you: review/edit the draft, then post it as a thread reply. If you want the PR, say so and I'll open it (tiered candidate selection + counted error message, tests in onboarding/tests).
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-7694/bw-property-29096-hotelkey-pms-validation-failing-despite-successful#comment-eac73034
tags:
- morning-gtd
- linear
time_minutes: 10
title: 'Respond on ENT-7694: validation_plan logic for BW 29096 (HotelKey)'
updated: 2026-09-30 13:18:10.559899
waiting_on: null
waiting_since: null
working_on: false
---

Andrea: '@connor @glloyd - do you have thoughts about the logic for the validation_plan?' jbalian found fetch and validation work as designed: all 9 reservations are CANCELLED or HOLD (2027 arrivals); the only near-term one is a cancelled test reservation.
https://linear.app/canary-technologies/issue/ENT-7694/bw-property-29096-hotelkey-pms-validation-failing-despite-successful