---
area: null
completed_at: null
contexts: []
created: 2026-10-28 16:16:43.844527
defer_until: null
due: null
energy: low
id: 2026-10-28T1616-review-doc-linked
order: null
output: |
  ## Agent run 2026-10-28T14:18Z

  Reviewed Andrea's design doc "Per-channel booking gateway (QR vs voice vendor)"
  (https://app.notion.com/p/canarytechnologies/Per-channel-booking-gateway-QR-vs-voice-vendor-407814686151810c9744f6e93cdacc4d),
  linked from the ENT-7947 comment (https://linear.app/canary-technologies/issue/ENT-7947/wyndham-qr-code-booking-fails-to-confirm-when-the-pms-has-not-received#comment-4bf00565).
  You, Andrés and Stephen are reviewers; status "REVIEW ME!". I checked its claims against master. Nothing posted.

  Verdict: the mechanism is sound and small (an optional per-channel override table; the hotel default is
  untouched and resolution falls back to it). But it does not fix ENT-7947 by itself, and three points need
  changes before approval.

  1. The blocking question is out of scope. Before Sep 24, OHIP hotels booking QR through the PMS failed at
     reserve with PMSGatewayBadRequest. Setting WEB = PMS Only brings that failure back unless someone fixes it.
     Answer "can OHIP QR book direct to OPERA at all?" before building. If the answer is no, this design doesn't
     help the incident, and the fix is PR #60962 (https://github.com/canary-technologies-corp/canary/pull/60962),
     still an open draft, plus linking the reservation once it arrives. Andrés's smaller PR #61406
     (https://github.com/canary-technologies-corp/canary/pull/61406) is closed.

  2. Resolve the vendor once per booking, not on every call. get_provider re-reads the config on reserve, confirm
     and payment link (booking_gateway/services/booking_gateway.py:145). With per-channel routing, an intent
     reserved through one vendor gets confirmed through another if a caller passes a different channel or None.
     That includes any future cancel, admin action or background task with no channel. Better: stamp the vendor
     (or channel) on BookingIntent at reserve, and route confirm, cancel and payment link from the intent. Then
     only availability and reserve need a channel argument, so less plumbing.

  3. The caller list is wrong for Wyndham voice. voice/services/wyndham_booking.py doesn't go through
     BookingGatewayService. It calls MulesoftBookingProvider.for_property directly (lines 974-1011), so it
     ignores BookingGatewayConfig entirely. Ask Stephen which voice flow EV-276
     (https://linear.app/canary-technologies/issue/EV-276) was for. If it was the call-center flow, the CRS Only
     switch wasn't needed for it, and resetting the QR hotels' default might be enough with no new model (point 1
     still applies). If it was the property voice agent (voice/services/booking.py, booking_authform_service.py),
     the design holds.

  Smaller points:
  - "Nobody else changes" isn't quite true. Today the voice enablement service re-points the hotel default when
    the admin picks a different source (voice/services/booking_agent_enablement.py:205-209), which also moves
    web and chat. Under the design, enablement writes only the VOICE row, so a non-Wyndham hotel that enables
    voice on a different source keeps web on the old vendor. That's probably right, but say it in the doc.
  - Every caller is updated in the same PR, so make `channel` a required keyword argument and let pyrefly enforce
    it, instead of `None` plus a channel_missing log.
  - The cancel_booking plumbing has no live caller. GuestBookingService.cancel_booking doesn't call the gateway,
    and nothing else calls BookingGatewayAPI.cancel_booking, so it can be left out (or covered by point 2).
  - The enablement code comment mentions a Wyndham "availability=CRS, booking=PMS" pair. Check whether some
    hotels are still on it, which would affect the OHIP cohort.

  Draft reply for the Linear thread or Notion doc, if you want it (not sent):
  > Direction looks right, and the override table with the default untouched is the minimal shape. Three things
  > before I'd approve: (1) the OHIP-via-PMS reserve failure (PMSGatewayBadRequest) decides whether this fixes
  > ENT-7947 at all, so I'd settle that first; (2) I'd stamp the vendor on BookingIntent at reserve and route
  > confirm and payment link from it, so a booking can't switch vendors mid-flight, and only availability and
  > reserve need the channel; (3) wyndham_booking.py hard-wires Mulesoft and never reads BookingGatewayConfig.
  > @stephen, which voice flow needed EV-276's CRS Only switch?

  ## Agent run 2026-10-28T16:25

  Follow-up asked: "does the design fix onboarding scripts so that hotels emerge correctly"

  No. The design doesn't change any onboarding code, so a newly onboarded Wyndham OHIP hotel still comes out
  with QR routed to the CRS, the setup that fails in ENT-7947. Its only onboarding line is "Update the Wyndham
  onboarding recipe" under Impact, which reads like a doc change. Nothing is in the plan, the test plan or the rollout.

  What onboarding does today (master):
  - WYNDHAM_CONNECT_PLUS -> stage BASE_CONFIGURATION_NEW runs BookingGatewayPlan with WyndhamBookingGatewayProvider
    (onboarding/models/property_configuration_processes.py:1434-1438).
  - The provider hard-codes availability=CRS, booking=CRS for every Wyndham hotel, whatever its PMS
    (onboarding/configuration_providers/wyndham/wyndham_booking_gateway_provider.py). Andrés changed it from the
    old value in #51892 (https://github.com/canary-technologies-corp/canary/pull/51892, 2026-09-01), three weeks
    before the EV-276 bulk migration. So onboarding was already producing the broken QR setup for new hotels
    before the bulk switch.
  - The plan calls BookingGatewayConfigurationService.update_or_create_booking_gateway_configuration
    (booking_gateway/services/configuration.py), which writes only the hotel default row.
  - setup_wyndham_voice_booking (voice/management/commands/setup_wyndham_voice_booking.py:62-67) refuses any
    hotel whose default isn't CRS/CRS. Once voice routing moves to a VOICE override, this check is checking the
    wrong row.

  What a new OHIP hotel looks like if the design ships as written:
  default = CRS Only (from onboarding), no WEB row, and a VOICE row only if someone later runs the voice enablement
  admin. So WEB/QR resolves to CRS and fails at confirm. It stays that way until someone runs
  set_booking_gateway_channel for that hotel by hand. The rollout's fleet step (step 4) covers the cohort that
  exists then, but every hotel onboarded afterwards comes out wrong again.

  What the design should add (suggested review point 4):
  1. Have onboarding write the channel rows. Extend the onboarding BookingGatewayConfig dataclass
     (onboarding/configuration_providers/configs/booking_gateway.py) with per-channel overrides, and have
     BookingGatewayPlan write them through a service method on BookingGatewayConfigurationService, the same
     service the ops command uses. The rule should live in one place, not be copied into a recipe.
  2. The Wyndham provider has to pick the WEB vendor per hotel by PMS (OHIP -> the agreed WEB gateway, SynXis
     PMS -> default). Today the provider's config is fixed at __init__ from OnboardingPlanData, which carries no
     PMS info, so this needs a hotel-aware hook (e.g. resolve in execute(hotel)). Unverified: whether the PMS
     integration already exists when BASE_CONFIGURATION_NEW runs. can_create_new_hotels=False suggests it does,
     but UPDATE_PMS_CONFIGURATION (OHIP guarantee codes) runs one stage later.
  3. Decide whether VOICE gets an explicit CRS row at onboarding or keeps inheriting the CRS default. Explicit is
     safer once the default and the channels can diverge, and setup_wyndham_voice_booking's not_crs_only check
     should then read the VOICE resolution, not the default row.
  4. Re-running the stage is safe under the design: update_or_create on the default leaves channel rows alone.
     But if onboarding writes channel rows, use update_or_create keyed on (config, channel) so a re-run doesn't fail
     on the unique constraint.
  5. Add an onboarding test: a WCP OHIP hotel comes out with WEB resolving to the agreed vendor and VOICE to CRS.
     tests/configuration_providers/wyndham/test_wyndham_booking_gateway_provider.py and
     tests/plans/test_booking_gateway_plan.py exist to extend.
  All of this still depends on review point 1 (can OHIP QR book through the PMS at all?). Until that's settled
  there's no correct WEB value for onboarding to write.

  Draft add-on to the review comment (not sent):
  > One more: onboarding. WyndhamBookingGatewayProvider hard-codes CRS Only for every WCP hotel (since #51892),
  > and BookingGatewayPlan only writes the default row. So under this design every newly onboarded OHIP hotel comes
  > out with QR on the CRS and needs a manual set_booking_gateway_channel run, and the fleet step goes stale
  > straight away. Can the plan write the channel rows itself (per-PMS WEB choice in the Wyndham provider, through
  > the same service the ops command uses), with an onboarding test? Also, setup_wyndham_voice_booking's
  > "not_crs_only" check reads the default row, so it should read the VOICE resolution instead.
project: null
source_id: null
tags: []
time_minutes: 5
title: review doc linked
updated: 2026-10-28 16:25:34.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://linear.app/canary-technologies/issue/ENT-7947/wyndham-qr-code-booking-fails-to-confirm-when-the-pms-has-not-received#comment-4bf00565