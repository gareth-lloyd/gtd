---
area: null
completed_at: 2026-10-27 14:45:30.625674
contexts:
- react
created: 2026-10-27 06:02:09.299400
defer_until: null
due: 2026-10-27
energy: medium
id: 2026-10-27T0602-follow-up-on-ent-7947-wyndham-qr-booking-critical
order: null
output: |-
  ## Agent run 2026-10-27

  Read-only research. Nothing was posted anywhere.

  ### Where things stand
  - Andrés's ask in #epd-enterprise-engineers (https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1793035064601639): Andrea's only reply says it will take a while. Nobody has posted context yet.
  - ENT-7947 (https://linear.app/canary-technologies/issue/ENT-7947) is In Review and assigned to Andrés.
  - PR #60962 (https://github.com/canary-technologies-corp/canary/pull/60962) is by Golem and is open and no longer a draft (+858/-74). Andrea left 6 review comments last night, all drafted by Claude. Two checks are failing: "Check frontend translations are up to date" and merge_gatekeeper.
  - PR #61406 (https://github.com/canary-technologies-corp/canary/pull/61406) was Andrés's minimal cut (backend only, no frontend message). It is **closed**, so he has gone back to #60962.

  ### The key context: this is probably a config regression, not old code
  - `BookingGatewayConfig` is OneToOne per hotel. Voice, chat and QR/guest-web booking all share one gateway.
  - On 2026-09-24, Stephen merged EV-276, PR #57591 (https://github.com/canary-technologies-corp/canary/pull/57591). It added `migrate_wyndham_to_crs_only_gateway` (backend/canary/voice/management/commands/migrate_wyndham_to_crs_only_gateway.py). The command moves every Wyndham hotel that has a CRS account from "CRS Availability / PMS Booking" (b90f9819…) to "CRS Only" (6c9b8f51…). Its own PR body warns: "The gateway is per hotel, so chat and guest-web booking switch too."
  - The timing matches Manuel's impact comment on the ticket: "Before Sep 24, OHIP hotels failed earlier in the flow, on reserve with PMSGatewayBadRequest; since then they fail on confirm with MissingReservation."
  - Connor commented on the ticket last night (2026-10-26 23:23 UTC): QR booking should never go through Mulesoft/CRS, and its gateway should be "PMS Only". That questions the whole premise of #60962. Nobody has answered him.
  - Separately, Andrés's own #51892 (2026-09-01) makes Wyndham Connect+ onboarding create CRS/CRS gateways (onboarding/configuration_providers/wyndham/wyndham_booking_gateway_provider.py). New hotels start as CRS-only too.

  ### Caveat to the "just revert to PMS" idea
  Manuel's numbers show 0 of 74 OHIP QR bookings succeeded since Sep 10. Before Sep 24 they also failed on PMS reserve (PMSGatewayBadRequest). So moving these hotels back to PMS booking would not fix QR either, unless the PMSGatewayBadRequest has its own cause that gets fixed. Voice wants CRS (Stephen: "which wyndham prefers and best addresses availability issues"). A single per-hotel gateway cannot be CRS for voice and PMS for QR. That is a product/architecture decision, not something Andrés should settle alone at EOD.

  ### Open review points on #60962 (Andrea)
  1. The `booking_already_confirmed` raise leaves the guest stuck: the frontend has no branch for it, so they see a generic toast.
  2. Cancelling stays local-only when the CRS confirm fails. The CRS reservation stays live with no card, which is the exact state Wyndham reported.
  3. The CRS number filter is exact match; the selectors use `value__iexact`. Andrea also asks whether the OHIP reservation actually carries the CRS number once it lands.
  4. When there are multiple PMS matches, the code silently falls back. It should raise or log.
  5. Nothing counts bookings that are "confirmed with no reservation" for good.
  6. Nit: show the CRS confirmation number on the success screen.
  Also unverified: the staging-wyndham-46495 end-to-end test is still an open checkbox in the PR. The live branch could not exercise the CRS path.

  ### Suggested reply to Andrés (draft, NOT sent)
  > Hey Andrés, some quick context so you're not blocked:
  > • Root cause of the recent spike: on Sep 24, EV-276 (#57591) moved Wyndham hotels with a CRS account to the "CRS Only" booking gateway for voice. The gateway is per hotel, so QR booking switched to CRS too. OPERA gets CRS reservations async, so the PMS lookup at confirm finds nothing → MissingReservation → cancel. Manuel's comment shows the failure mode changing on that date.
  > • Connor says QR booking should be "PMS Only". But before Sep 24, OHIP QR bookings were also failing (PMSGatewayBadRequest on reserve), so reverting isn't a clean fix either.
  > • Before going deeper on #60962, get a decision from Connor/Stephen: does QR stay on CRS (then #60962's approach is right, but Andrea's points 1–2 need fixing) or go back to PMS (then the PMSGatewayBadRequest needs its own fix and a way to split voice vs QR gateway)? Happy to jump on a call.

  ### Suggested next steps for Gareth
  - Send (or adapt) the reply above in the thread. It needs your approval.
  - Get Connor and Stephen to reconcile "PMS Only for QR" with EV-276 in the ticket.
project: 2026-08-31-ihg
source_id: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1793035064601639?thread_ts=1793035064.601639&cid=C0B1MN8F869
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 20
title: 'Follow up on: ENT-7947 Wyndham QR booking critical path — Andrés needs context'
updated: 2026-10-27 14:45:30.625667
waiting_on: null
waiting_since: null
working_on: false
---

Andrés picked up ENT-7947 (Wyndham QR code booking fails to confirm when the PMS has not received it). It's critical path, and Golem has opened PR #60962. Andrea is gathering context, but it won't be done before Andrés's end of day.
https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1793035064601639?thread_ts=1793035064.601639&cid=C0B1MN8F869
https://linear.app/canary-technologies/issue/ENT-7947/wyndham-qr-code-booking-fails-to-confirm-when-the-pms-has-not-received