---
area: null
completed_at: null
contexts:
- react
created: 2026-11-13 09:54:28.681434
defer_until: null
due: null
energy: medium
id: 2026-11-13T0954-review-andr-s-two-booking-prs-epd-voice
order: null
output: |
  ## Agent run 2026-11-13T10:09

  Read both diffs in full (non-test code line by line, tests skimmed), the existing review threads, and the CRS/PMS providers on the branch. Nothing was posted to GitHub or Slack. No tests were run locally; CI is green on both.

  **Verdict: no blockers on either PR. Both are already approved (rafa-canary + seporaitis on both, abranaf-canary on #63842), so your review is optional.** Two comments worth leaving on #63842, one question on #63948. Drafts are at the bottom.

  ### State
  - PR #63948 (https://github.com/canary-technologies-corp/canary/pull/63948), ENT-8162: base master, +219/-6, 4 files, approved, CI green. Author's own gate: do not merge before a staging cancel on a Wyndham CRS hotel and an OHIP hotel. Not done yet.
  - PR #63842 (https://github.com/canary-technologies-corp/canary/pull/63842), ENT-8101: +1532/-143, 30 files, approved, CI green. It is stacked on the #63948 branch, not master, so it sits behind that staging gate too. The two branches merge cleanly (checked with git merge-tree), including the later "log as warning" commit on #63948.
  - Slack ask (https://canarytechnologies.slack.com/archives/C07R45PP9AS/p1794501534318019) has no replies.

  ### #63948 Cancel the vendor reservation when a QR booking fails at confirm
  Small and does what it says. On a confirm failure the view calls `_cancel_at_vendor` (never raises, logs a warning), then the existing local cancel, then raises the same `BookingFailedToConfirm`. Reserve and finalize failures make no vendor call. Tests cover CRS and PMS, a raising cancel, an OHIP penalty refusal, and a failing local cancel.
  - Question (not blocking): the vendor cancel runs inside the guest request after a confirm that has usually just timed out. The description puts the added wait at up to 60 s (CRS) or 2x180 s (PMS). If the web worker or load balancer kills the request first, the local cancel never runs and the booking stays open with an ON_HOLD intent. I did not find the web timeout in the repo, so this is unverified. #63842's new `BookingAlreadyReserved` guard stops a retry from double-reserving in that case, which is a reason to land the pair close together.
  - Accepted by the author and I agree: a confirm that fails after the vendor committed (the refresh step) cancels a live card-backed reservation. The guest was told it failed, so vendor and Canary should match; the OHIP penalty check refuses when a penalty applies.
  - The real risk is the first production vendor cancel, which only the staging run answers. Code review cannot.

  ### #63842 Resolve the booking vendor per channel
  The claim "no hotel has a channel row yet, so every call reaches the same vendor as today" holds for availability and reserve: `BookingGatewaySelector.get_gateway` falls back to the hotel default, and every non-test caller of `BookingGatewayAPI` now passes a channel (grepped; none left that would hit the `booking_gateway.channel_missing` warning). The channel-config model has a unique constraint on (hotel_config, channel), so the `.get()` is safe.
  1. Comment: confirm, cancel and payment link now route by `BookingIntent.booking_vendor_kind` (CRS id present -> CRS, else reservation -> PMS, else config). That is a small behaviour change today, independent of channel rows: an intent on a CRS-configured hotel that has a linked reservation but no CRS id now goes to the PMS provider instead of raising `MissingCRSReservationID`. The CRS provider always returns the CRS id from reserve, so I could not construct this from the code, but #63948's description mentions 10 CRS bookings holding no CRS id. Worth asking whether those have a reservation set.
  2. Comment: `_is_pms_voice_booking(hotel)` in `voice/services/booking_authform_service.py` reads the VOICE channel config at call time. `_handle_form_submitted` and `finalize_voice_booking` run after reserve, where an intent exists, so they should use `booking_intent.booking_vendor_kind`, the same rule the gateway now follows. As written, a VOICE row change between reserve and submit picks the wrong confirmation number. No effect until channel rows exist.
  3. Note: the new `BookingAlreadyReserved` (422, `booking_already_reserved`) guard on the web payment view is a real behaviour change. A guest who retries after a `BookingFailedToFinalize` used to reserve a second time; now they get the generic "failed due to anomaly" toast, because `frontend/check-in/src/views/Booking/BookingPaymentForm.vue` has no branch for the new code. Better than a duplicate reservation, but the guest holds a confirmed vendor reservation and sees a generic error. Follow-up, not a blocker. The guard is also not under a lock, so two concurrent POSTs can still both reserve (existing behaviour).
  4. Nits: `channel` defaults to None on every facade method with a warning log rather than being required; `stub_booking(quote=...)` was renamed to `selected_quote` and no longer builds a quote (old behaviour moved to `stub_booking_with_quote`).

  ### Draft comments (not posted; say which to send)
  #63842, on `_provider_holding_booking` in `booking_gateway/services/booking_gateway.py`:
  > Routing by the intent is the right call. One edge: a CRS-configured hotel whose intent has `reservation` but no `crs_reservation_id` now goes to the PMS provider for confirm/cancel, where today it raises `MissingCRSReservationID`. #63948 mentions 10 CRS bookings with no CRS id. Do any of them have a reservation linked? If so this changes behaviour before any channel row exists.

  #63842, on `_is_pms_voice_booking` in `voice/services/booking_authform_service.py`:
  > `_handle_form_submitted` and `finalize_voice_booking` run after reserve, so they could read `booking_intent.booking_vendor_kind` instead of the channel config. Otherwise a VOICE row change between reserve and submit resolves the wrong confirmation number, which is the case `_provider_holding_booking` was added to prevent.

  #63948, on `_cancel_at_vendor` in `booking/views/guest_booking_payment_view.py`:
  > What is the web request timeout here? Confirm timeout plus up to 60 s (CRS) or 2x180 s (PMS) of cancel may outlive the worker, and then the local cancel never runs. Fine to ship as is if the answer is "long enough" or if the staging run shows cancels return quickly.
project: null
source_id: https://canarytechnologies.slack.com/archives/C07R45PP9AS/p1794501534318019
tags:
- morning-gtd
- slack
time_minutes: 30
title: Review Andrés' two booking PRs (#epd-voice)
updated: 2026-11-13 10:09:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

Andrés asked the group for review: #63948 Cancel the vendor reservation when a QR booking fails at confirm, #63842 Resolve the booking vendor per channel.
https://github.com/canary-technologies-corp/canary/pull/63948
https://github.com/canary-technologies-corp/canary/pull/63842
https://canarytechnologies.slack.com/archives/C07R45PP9AS/p1794501534318019