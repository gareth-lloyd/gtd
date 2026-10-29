---
area: null
completed_at: 2026-10-29 13:23:09.537029
contexts:
- react
created: 2026-10-28 11:10:00.431624
defer_until: null
due: null
energy: medium
id: 2026-10-28T1110-make-sure-ev-proposes-the-wyndham-voice-booking-fl
order: null
output: |
  ## Agent run 2026-10-28

  **Status:** nothing sent. The steps for the 11/10 batch already exist in code, so EV mostly needs to say "run this command" in the thread. A draft reply is below.

  **Correction to the item:** the thread isn't stale. Marta's revert request, Stephen's "don't revert, have EV propose steps" and Andrea's "need exact instructions" were all posted Oct 27, yesterday (https://canarytechnologies.slack.com/archives/C0AJ1ENFSSU/p1792091759977949?thread_ts=1790703003.314659&cid=C0AJ1ENFSSU).

  **Why a revert is wrong:** PR #59263 (https://github.com/canary-technologies-corp/canary/pull/59263, merged 10/6) removed the auto-enable of `booking_link_enabled`. That flag drives the booking *link* flow, which texts a link and never quotes rates (the 9/24 batch problem). Reverting it would bring the link flow back. It would not turn on the booking *agent*, which is the "booking flow" Marta wants.

  **What turns on the booking agent:** the management command `setup_wyndham_voice_booking` (backend/canary/voice/management/commands/setup_wyndham_voice_booking.py). Stephen wrote it in PRs #59702, #60262, #59999 and #61649 (https://github.com/canary-technologies-corp/canary/pull/61649, merged 10/26). For each hotel it:
  - sets `booking_payment_gateway_config_id` to the shared Wyndham payment gateway
  - sets `has_booking_agent = True` (since #61649, this alone turns booking on; the GrowthBook slug lists are no longer needed)
  - sets `make_reservation_enabled = True`
  - sets `forwarded_call_transcription_mode = ALL`
  - adds the hotel to the voice booking portfolio

  It checks every hotel first and writes nothing if any of them fails a check. The checks: the hotel is in the Wyndham portfolio, it has a voice config, and its booking gateway is CRS/CRS. New WCP onboardings already meet the CRS/CRS check, because `WyndhamBookingGatewayProvider` sets CRS/CRS. So the command should succeed straight after the onboarding run. It is a dry run unless you pass `--commit`.

  `ConfigureVoicePlan` has no booking settings at all, so the onboarding script cannot do this itself today.

  **Proposed steps for the 11/10 batch (no revert):**
  1. Build and onboard the batch as usual. Leave `booking_link_enabled` off.
  2. After onboarding, run `setup_wyndham_voice_booking --hotel-slugs <comma-separated batch slugs>` as a dry run. Check for `hotels_not_ready`.
  3. Rerun the same command with `--commit`.
  4. Optional longer-term fix: add a booking toggle to the Wyndham onboarding config, so `ConfigureVoicePlan` makes the same settings and the separate step goes away. That needs a ticket and won't be ready by 11/4.

  **Open questions for Stephen/VOX:**
  - Who runs the command for new batches: ENT (Andrea's team) or VOX? It needs a prod management-command run.
  - #61649 left manual GrowthBook follow-ups. `voice-wyndham-booking-agent-variant` and `voice-welcome-message` should move from slug lists to a Wyndham-portfolio rule. If that hasn't happened, new hotels won't get the Wyndham variant or welcome message. I couldn't check GrowthBook from here.
  - Some Wyndham hotels have no `MembershipGatewayConfiguration`. Those book at the standard rate and log `wyndham_rewards_flow_disabled` (caveat noted in #61649).

  **Draft Slack reply (thread above). NOT SENT; needs your OK:**
  > <@U0A7PLXAU8N> <@U05G106T8S1> agree with Stephen, no revert needed. #59263 only stopped *booking links* (the text-a-link flow from the 9/24 batch). Reverting it would bring that back, not the booking agent.
  >
  > The booking agent is turned on by a separate command Stephen built: `setup_wyndham_voice_booking`. For 11/10:
  > 1. Onboard the batch as usual (booking links stay off)
  > 2. Run `setup_wyndham_voice_booking --hotel-slugs <batch slugs>` as a dry run, which checks every hotel is Wyndham, has a voice config and is CRS-only
  > 3. Rerun with `--commit`. That sets the payment gateway, `has_booking_agent`, `make_reservation_enabled`, call transcription and the booking portfolio
  >
  > <@U06JUDWS7LP> can you confirm that's the full list, and say who should run step 2/3 for new batches? Also whether the GrowthBook follow-ups from #61649 (Wyndham portfolio rule on the agent variant + welcome message flags) are done. If we want this folded into the onboarding script itself, we can ticket it, but it won't land before 11/4.
  ## Agent run 2026-10-28 (spec)

  Spec drafted locally (not filed): /Users/garethlloyd/projects/plans/wyndham-voice-booking-onboarding-spec.md
  Laid out like ENT-7947 (https://linear.app/canary-technologies/issue/ENT-7947).

  What the spec proposes:
  - Move the per-hotel write in `setup_wyndham_voice_booking` into a service. A new `ConfigureVoiceBookingPlan` calls it in WCP `BASE_CONFIGURATION_NEW` and in `WYNDHAM_AI_VOICE`, and hotels can be opted out by onboarding value.
  - Use the 11/10 batch to run the command by hand (dry run, then --commit). The plan comes after that batch.

  Found while researching:
  - The two ways to turn booking on set different fields. Adminland's `BookingAgentEnablementService.enable` never sets `make_reservation_enabled`, transcription or the booking portfolio. A hotel enabled there transfers every booking call.
  - Link to ENT-7947: each hotel has one BookingGatewayConfig shared by voice, chat and QR. Voice booking needs CRS/CRS, and QR booking on CRS/CRS fails at every OHIP hotel (0 of 74). WCP onboarding already sets CRS/CRS, so it adds no new breakage there. WYNDHAM_AI_VOICE hotels may need a gateway move, which breaks QR at OHIP hotels until PR #60962 (https://github.com/canary-technologies-corp/canary/pull/60962, draft) ships. If Connor's "QR should be PMS-only" stands, both cannot work without per-channel gateways.
  - Open decisions are listed in the spec: Stephen (field list), Product (QR gateway), Andrea (opt-out).
project: null
source_id: https://canarytechnologies.slack.com/archives/C0AJ1ENFSSU/p1792091759977949?thread_ts=1790703003.314659&cid=C0AJ1ENFSSU
tags:
- morning-gtd
- slack
time_minutes: 15
title: Make sure EV proposes the Wyndham voice booking-flow onboarding change before
  the 11/10 batch
updated: 2026-10-29 13:23:09.536682
waiting_on: null
waiting_since: null
working_on: false
---

Marta asked about the Oct 27 deploy (PR #59263 has shipped). She now wants it reverted for the 11/10 WAIC batch, which she builds on or after 11/4. Stephen says not to revert and to have EV propose different config steps; Andrea needs exact instructions. The thread has been quiet since then. Open 12 days, no reply from you.
https://canarytechnologies.slack.com/archives/C0AJ1ENFSSU/p1792091759977949?thread_ts=1790703003.314659&cid=C0AJ1ENFSSU