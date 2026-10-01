---
area: null
completed_at: 2026-10-01 15:26:16.276767
contexts: []
created: 2026-10-01 11:07:10.934415
defer_until: null
due: null
energy: low
id: 2026-10-01T1107-on-booking-payments-add-security-deposit-should-be
order: null
output: "## Agent run 2026-10-01T11:09\n\n### Why \"Security deposit\" exists twice
  on Booking -> Payments\n\nTwo different components, two different backing entities,
  built in two different work streams, both titled \"Security deposit\":\n\n1. **Top
  card (inside \"Payments\")** - `frontend/src/features/bookings/components/PaymentTrack.tsx`
  rendered with `trackName=\"security\"` by `tabs/PaymentsTab.tsx`. Backed by `GET
  /bookings/{id}/security` -> `TrackSerializer.for_booking_purpose` (`django_res/payments/serializers/track.py:101`),
  which aggregates the **Payment ledger rows** with purpose SECURITY_DEPOSIT: scheduled/paid
  amounts, next due, latest status (`\"none\"` when no rows), last request. Same generic
  component as Deposit and Balance, with Request payment / Mark received / Waive.
  Gate: reservations role. Origin: `091636fb` (original Payments tab, three-track
  model).\n\n2. **Bottom section (after Transactions and Damage)** - `components/SecurityDepositPanel.tsx`.
  Backed by `GET /bookings/{id}/security/deposit` -> the **SecurityDeposit lifecycle
  row** itself (reference, kind pre-auth/bank-transfer, status awaiting/held/captured/released,
  hold expiry, release schedule, captured/refunded amounts) with Release / Capture
  for damages. Gate: accounts role. Origin: `9b2f4a75` (BUG-008 wf8 slice 2); it was
  placed after Damage claims because it shipped alongside them and Capture consumes
  open claims.\n\nGAP-071 (`06a93f5f`, 2026-10-01) then put \"Add security deposit\"
  in the panel's empty state because that is where \"No security deposit\" is displayed.
  Net effect with no SD: the top card reads \"£0.00 of £0.00 - none\" and the add
  button sits three sections lower. `PaymentsTab.test.tsx:171` already carries a comment
  acknowledging the duplicate label.\n\n### Recommended fix - option B: move the panel
  up and demote its heading (one small FE commit, ~1h)\n\n1. `PaymentsTab.tsx`: render
  `SecurityDepositPanel` immediately after the `security` `PaymentTrack`, inside the
  tracks list (group the security track card and the panel in one wrapper). Resulting
  order: Payments [Deposit, Balance, Security deposit card + SD row / empty state
  + Add] -> Transactions -> Damage -> Refunds.\n2. `SecurityDepositPanel.tsx`: drop
  its own `<h3>Security deposit</h3>` (or make it a sub-heading such as \"Deposit
  on file\") so the tab has exactly one \"Security deposit\" heading; style as a sub-card
  of the track.\n3. Safe to move above Damage: `CaptureForDamagesDialog` fetches open
  claims itself and already says \"File a claim first\" when none.\n4. Tests: `__tests__/PaymentsTab.test.tsx`
  \"renders all three tracks\" -> `getAllByText(...)[0]` becomes `getByText`; add
  an ordering assertion that the SD empty state / Add button sits between the security
  track card and the Transactions heading. `__tests__/SecurityDepositPanel.test.tsx`
  asserts on panel content, not the heading, so it should only need the heading change
  if retitled.\n5. i18n: `security_deposit.title` becomes unused or is retitled -
  update en + el (`i18n/locales/*/bookings.json`).\n6. Quality gate: vitest, eslint,
  prettier --check, tsc --noEmit.\n\n### Alternatives considered\n\n- **Option A -
  merge into one card (bigger):** extend the security `PaymentTrack` with the SD row
  details and Add / Release / Capture, delete `SecurityDepositPanel`. Cleaner end
  state but mixes two role gates and two queries into a component shared by Deposit/Balance;
  needs a security-only slot. Suggest as a follow-up ticket if B feels like a half-step.\n-
  **Option C - only move the Add button into the track card:** leaves two sections;
  does not answer the \"why two places\" complaint. Not recommended.\n\n### To confirm
  during implementation\n\n- Whether a legacy-imported booking can have SECURITY_DEPOSIT
  Payment rows without a SecurityDeposit row (a grep of `django_res/data_migration`
  for such a purpose assignment found nothing, but not exhaustive). If it cannot,
  a further simplification is possible: when the SD query returns null, hide the \"£0.00
  of £0.00 - none\" track card and show only the empty state + Add.\n- Whether to
  file this as a BUG ticket in `django_res_design/todo/` per project process. I did
  not create one.\n\nNo code was changed. Nothing was written to any external service.\n\n##
  Agent run 2026-10-01T11:11 - follow-up: the two sections contradict each other\n\nScreenshot
  (2026-10-01 11:10): after a manual add, the \"Security deposit\" track card reads
  \"Not scheduled - €0.00 of €0.00 paid - No due date\", while the \"Security deposit\"
  panel below reads \"SD-2026-2 - Refundable bank transfer - Awaiting bank transfer
  - Amount €2,187.50 - Release scheduled 1 Jul 2027\".\n\n### Root cause (confirmed
  in code, not GAP-071-specific)\n\n- The track card is `GET /bookings/{id}/security`
  -> `TrackSerializer.for_booking_purpose` (`django_res/payments/serializers/track.py:116-154`).
  It sums **Payment rows** with purpose SECURITY_DEPOSIT: `scheduled_amount` = non-terminal
  rows, `paid_amount` = succeeded rows, `status` = latest row's status or `\"none\"`
  (the FE labels `\"none\"` as \"Not scheduled\").\n- `SecurityDepositService` never
  writes a *pending* Payment row when a deposit is opened. `_open` (`payments/services/security_deposit.py:190`)
  creates only the `SecurityDeposit` row, for both the auto path (`create_for_booking`)
  and the manual path (`create_manual`). Security-purpose Payment rows appear only
  on `hold` (line 418), `mark_paid` (468), `claim` (588) and `_supersede_active_hold`
  (720).\n- So for every bank-transfer deposit still awaiting payment, auto or manual,
  the track card has nothing to aggregate and shows 0 of 0 / Not scheduled, while
  the real scheduled figure (€2,187.50) and due/release dates live on the SecurityDeposit
  row shown in the panel. The deposit and balance tracks don't have this problem because
  the scheduler writes a PENDING Payment row for each at confirmation.\n- The backend
  test `test_get_security_track` (`payments/tests/test_api_security_track.py:136`)
  asserts only the booking id, so the zero figures are not a deliberate decision.\n\n###
  Related latent bug found on the way\n\nThe track card offers **Waive** on the security
  track. The FE posts `/bookings/{id}/security:waive` (`frontend/src/features/bookings/api.ts:355`),
  but `security_track_action` (`payments/views/track.py:290-336`) only handles request-payment,
  mark-paid, release and claim, and raises `UnknownAction` for anything else. Waiving
  a security deposit from the Payments tab therefore always fails.\n\n### Revised
  recommendation\n\nPrefer the merge, but **the panel absorbs the track, not the other
  way round**: the SecurityDeposit row is the authority for the security track, and
  the generic Payment-row aggregate is the wrong lens for it.\n\n1. **Frontend:**
  stop rendering the generic `PaymentTrack` for `security`. Render `SecurityDepositPanel`
  as the third card in the Payments list (after Balance), with a single \"Security
  deposit\" heading. Delete the bottom section.\n2. **Panel gains the track actions
  it is missing:** \"Request payment\" (POST `security:request-payment`, already SD-aware
  in `RequestPaymentService.request`, bank-transfer kind only) and \"Mark received\"
  (POST `security:mark-paid`, already acts on the active SD). Keep Release / Capture
  / Add. Drop Waive for security unless a backend `waive` is added (none exists today).
  Role gates: request/mark-paid stay reservations-gated as on the track today; release/capture/add
  stay accounts-gated.\n3. **Panel shows the figures the track used to promise:**
  amount, paid-so-far (from the SD's succeeded Payment rows or `captured`/`refunded`
  fields), due date (`SecurityDeposit.due_at` - currently not surfaced by the panel),
  release scheduled, and \"Link sent\" from `last_requested_at`. The `security` track
  endpoint can stay for the guest payment page and tests, or the FE can keep reading
  it only for `paid_amount` / `last_requested_at`.\n4. **Transactions table** is unchanged:
  settled SD money still appears there as Payment rows.\n5. **Backend (optional, small):**
  make `for_booking_purpose` overlay the active SecurityDeposit for the security purpose
  (`scheduled_amount` = sd.amount, `due_at` = sd.due_at when no non-terminal Payment
  row exists) so API consumers other than this tab stop seeing 0 of 0. Add a test
  asserting the figures after `create_manual`.\n6. **Tests:** `PaymentsTab.test.tsx`
  (three-track assertions, zero-amount request-disabled case at line 216, cancelled-track
  case) and `SecurityDepositPanel.test.tsx` gain request/mark-paid cases; `PaymentTrack.test.tsx`
  loses the security-specific cases.\n\nEffort: roughly half a day FE, plus an hour
  backend if step 5 is taken. The earlier option B (just move the panel up) would
  put the two contradicting cards next to each other, which makes the contradiction
  more visible, not less - no longer recommended on its own.\n\nNo code was changed.
  Nothing was written to any external service.\n\n## Agent run 2026-10-01T11:14 -
  ticket filed\n\n- Created `django_res_design/todo/bug-049-security-deposit-track-card-contradicts-sd-panel.md`
  (BUG-049) with the root cause, the Waive fault, the merge-into-panel fix, acceptance
  criteria and dependencies (GAP-071, GAP-136, GAP-061, GAP-137, Q-033).\n- Added
  its row under \"\U0001F534 Bugs\" in `django_res_design/todo/INDEX.md` after BUG-048
  and extended the headline: 59 open (54 ⬜, 5 \U0001F7E8), 200 in done/.\n- Both files
  are uncommitted on `main`; no commit was made.\n"
project: 2026-05-25-villa-collective
source_id: null
tags: []
time_minutes: 5
title: On booking -> Payments, "Add security deposit" should be close to the "Security
  deposit" payment line
updated: 2026-10-01 15:26:16.276759
waiting_on: null
waiting_since: null
working_on: false
---

Order of screen sections:
* Payments
  * Deposit
  * Balance 
  * Security deposit
* Transactions
* Damage
* Security deposit. 

Why does it exist in two places? Plan fix.