---
area: null
contexts: []
created: 2026-06-03 10:56:31.230778
defer_until: null
due: null
energy: low
id: 2026-06-03T1056-booking-created-via-flow-has-no-payments-attached
order: null
output: |
  ## Agent run 2026-06-03T22:00 — root cause confirmed (investigation only, no code changed)

  **Confirmed real bug with production impact.** Any booking created through the
  live API gets ZERO Payment rows. The dev seeder masks this, which is why it
  hadn't surfaced before.

  ### Root cause
  `BookingService.create_from_quotation_line` (reservations/services/bookings.py)
  never schedules payments. Lines 95-96 are a stale TODO:

      # TODO: integrate with payments.PaymentScheduler.create_for_booking once
      # the payments app lands. For now the Booking just records the balance.

  The payments app HAS landed (payments/services/payment_scheduler.py with
  `PaymentScheduler.create_for_booking`), but nothing in the real flow calls it.

  ### Evidence
  - Production callers that create bookings and get no payments:
    - reservations/views/quotation.py:205 (accept-quotation API endpoint)
    - reservations/views/owner.py (owner-portal booking creation)
  - The ONLY thing wiring booking->payments is the seeder:
    seeding/_booking_helpers.py `populate_payments()` manually calls
    `PaymentScheduler.create_for_booking` + `SecurityDepositService.create_for_booking`
    after each seeded booking. That is why seeded data looks correct but
    API-created bookings have empty payment schedules.

  ### Why the naive fix is illegal
  The import spine (django_res/CLAUDE.md) is:
    comms > payments > reservations > pricing > properties > integrations > accounts
  `payments` sits ABOVE `reservations`, so `reservations.services.bookings`
  cannot import `payments.services.payment_scheduler` — import-linter (CI) would
  fail. That is the real reason the TODO was punted. The seeder gets away with it
  because seeding is a top-of-stack orchestrator outside the layers contract.

  ### Recommended fix (clean architectural fit)
  Wire it via the existing `booking_transitioned` signal
  (reservations/signals.py:34), the same way `comms/signals.py` already listens.
  `payments` is above `reservations`, so a payments-side handler importing the
  reservations signal is a clean DOWNWARD edge — no contract violation.

  - Add a handler in payments (e.g. payments/signals.py + connect in
    payments/apps.py `ready()`, mirroring comms/signals.py:389) that fires when
    a booking transitions INTO `AWAITING_DEPOSIT` (to_status check). That is the
    exact moment payments should exist:
      * auto_accept path: DRAFT -> AWAITING_DEPOSIT (no pre-approval)
      * pre-approval path: owner_approve eventually reaches AWAITING_DEPOSIT
    This matches the seeder's own logic, which skips PENDING_OWNER_APPROVAL and
    only schedules after approval (see populate_payments + advance_pre_approval).

  ### Gotchas the fix MUST handle (do not skip)
  1. **Idempotency.** `PaymentScheduler.create_for_booking` uses `bulk_create`
     with NO guard against existing rows. Wired to a signal it could double-create
     on any re-entry. Add a short-circuit (e.g. skip if Payment.objects.filter(
     booking=...).exists()) per the project's idempotency convention.
  2. **Seeder double-up.** Once the signal wiring lands, the seeder's explicit
     `populate_payments()` would run AND the signal would fire -> duplicate
     payments. Either make scheduling idempotent (preferred — covers both) or
     drop the seeder's manual call. Idempotency guard solves both at once.
  3. **Security deposit.** `PaymentScheduler.create_for_booking` already calls
     `SecurityDepositService.create_for_booking` internally (line 109), so the
     signal handler only needs the one call.

  ### Suggested next action
  TDD it: failing test asserting a booking created via
  `BookingService.create_from_quotation_line` (auto-accept property) has DEPOSIT +
  BALANCE Payment rows + a SecurityDeposit; then add the payments signal handler
  with an idempotency guard; remove the stale TODO. Est. ~1-2 hrs incl. quality
  gate (pytest + ruff + mypy + lint-imports). Not started — flagging for your call
  on scope/priority.
project: 2026-05-25-villa-collective
source_id: null
tags: []
time_minutes: 5
title: booking created via flow has no payments attached to it
updated: 2026-06-03 23:17:44.919669
waiting_on: null
waiting_since: null
working_on: false
---