---
area: null
contexts:
- react
created: 2026-06-11 09:52:59.751347
defer_until: null
due: null
energy: medium
id: 2026-06-11T0952-review-ent-6362-bw-loyalty-member-number-andrea-s
order: null
output: |
  ## Agent run 2026-06-11T13:59:30

  Reviewed Andrea's Option 3 plan on ENT-6362 (https://linear.app/canary-technologies/issue/ENT-6362/best-western-loyalty-member-number-in-fact-check-in) against the code. Verdict: the correction is right and the plan is sound, but the recommended fix as written has ONE MATERIAL GAP — it must blank TWO outbound channels, not one.

  ### Confirmed (her correction is correct)
  - `guests.Membership`: UniqueConstraint(vendor_id, account_id) — backend/pms-gateway/guests/models/membership.py:64-69. Blanking vendor_id at the loader would collapse all AutoClerk loyalty guests per account onto one row.
  - `reservations.MembershipInformation`: UniqueConstraint(reservation_id, vendor_id) + delta_identifiers = ("vendor_id",) — backend/pms-gateway/reservations/models/membership_information.py:46-55. Blanking breaks delta tracking.
  - Minor accuracy nit (doesn't change the conclusion): `guests.Membership` does NOT declare vendor_id as a delta identifier — it has no `delta_identifiers` tuple at all (only MembershipState does, on source_entity_kind/source_entity_id). The unique constraint alone makes loader-blanking unsafe.

  ### The gap: memberships reach Canary via TWO channels, and Canary prefers the one her plan doesn't name
  1. Per-guest `memberships` in the reservation webhook payload: `ReservationsSchema.dump_guests` -> `GuestService.get_guest_pool` (guests/services/guest.py:33-66, prefetches `guests.Membership` rows) -> guest schema `memberships` field (guests/schemas/guest.py:99).
  2. Reservation-level `membership_information`: `ReservationsSchema.dump_membership_information` (reservations/schemas/reservation.py:170) via MembershipInformationSchema.

  Canary's translator PREFERS channel 1 and only falls back to channel 2 when guest memberships are empty — backend/canary/guest/services/reservation_ingestion/reservation_translator.py:142-145. So blanking only `membership_information` changes nothing in the common case. The fix must blank the per-guest memberships dump (gate on account.type == autoclerk; Account.type at gateway/models/account.py:167, reachable from both reservation and guest). Suggest raising this on the ticket before implementation starts.

  Bonus: blanking at the gateway guest-schema dump also fixes the kiosk enrollment sync path (backend/canary/kiosk/utils/post_membership.py:112,145 -> sync_guest_memberships), which writes memberships from a gateway guest payload outside reservation ingestion.

  ### Safety check on blanket-blanking AutoClerk (passed)
  autoclerk/capabilities.py declares NO add-membership capability, so Canary BW enrollment can never push a real BWR number into gateway memberships for AutoClerk — blanket blank cannot destroy real numbers today. Caveat: revisit if AutoClerk ever gains ADD_MEMBERSHIPS or option 1 (real number from AutoClerk) lands.

  ### Other notes
  - Self-heal claim is correct but only for reservations that sync again (vendor_id is in Canary update_or_create defaults). Departed-guest MembershipProgram rows keep the stale profile ID until/unless the guest returns — same bucket as the warehouse-snapshot caveat she already flagged.
  - Blanked guest memberships still carry raw_kind/raw_level, so the translator's `if not memberships` fallback won't accidentally kick in and the loyalty level is preserved — consistent with her claim.
  - Her "alternative" (flag plumbed through the load payload) is unnecessary: the PMS=AutoClerk discriminator is directly available at the outbound serializer via account.type, so the serializer approach is strictly simpler. Agree with her recommended option.
  - Agree the discriminator must be PMS=AutoClerk, not raw_kind==BWR.

  Suggested next action: comment on ENT-6362 flagging the two-channel gap (per-guest memberships is the primary path) before Andrea implements.

  Update 2026-06-11T14:15: user approved; review comment posted to ENT-6362 (https://linear.app/canary-technologies/issue/ENT-6362/best-western-loyalty-member-number-in-fact-check-in) as a reply in the investigation thread, flagging the two-channel gap, the capability safety check, and the delta_identifiers nit. Awaiting Andrea's response.
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-6362/best-western-loyalty-member-number-in-fact-check-in
tags:
- morning-gtd
- linear
- from-awareness
time_minutes: 15
title: 'Review ENT-6362: BW loyalty_member_number — Andrea''s Option 3 plan'
updated: 2026-06-11 14:17:55.543890
waiting_on: null
waiting_since: null
working_on: false
---

Andrea's plan with correction: blanking vendor_id in the AutoClerk loader is unsafe (UniqueConstraint(account_id, vendor_id) + delta identifier on gateway).
https://linear.app/canary-technologies/issue/ENT-6362/best-western-loyalty-member-number-in-fact-check-in