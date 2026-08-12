---
area: null
completed_at: null
contexts:
- react
created: 2026-08-11 09:56:34.775834
defer_until: null
due: 2026-08-12
energy: medium
id: 2026-08-11T0956-look-at-ent-7018-wyndham-crs-only-booking-config
order: null
output: |
  ## Agent run 2026-08-12T08:03:03Z

  Investigated the open design call. **Bottom line: Andrés's blocker is real, but the
  answer is a ~5-line service fix, not a data cleanup or a schema change. Nothing here
  needs Stephen.**

  ### State of play
  - Ticket: ENT-7018 (In Progress, Andrés, Low/1pt)
    https://linear.app/canary-technologies/issue/ENT-7018/update-wyndham-onboarding-to-use-crs-only-booking-config
  - PR #51892 — **draft, open since 2026-07-31, zero reviews, single commit bd8e657, no CI run**
    https://github.com/canary-technologies-corp/canary/pull/51892
    Diff is one line + test updates: `booking_provider=BookingVendorKind.PMS` → `CRS` in
    `backend/canary/onboarding/configuration_providers/wyndham/wyndham_booking_gateway_provider.py`.
  - Sibling backfill EV-276 — **still in Triage, never started, assigned to Stephen (not an engineer)**
    https://linear.app/canary-technologies/issue/EV-276/move-all-wyndham-booking-config-to-crs-only
  - Origin Slack thread (private channel):
    https://canarytechnologies.slack.com/archives/C0BKXF4KH2L/p1785295840493069

  ### The blocker, precisely
  `BookingGatewayConfigurationService.update_or_create_booking_gateway_configuration`
  (`backend/canary/booking_gateway/services/configuration.py:36`) does a bare
  `BookingGateway.objects.get(availability_provider=..., booking_provider=...)`.
  It catches `DoesNotExist` and maps it to the actionable `ERROR_NO_BOOKING_GATEWAY_EXISTS`
  onboarding error — but **nothing catches `MultipleObjectsReturned`**. With two CRS/CRS rows
  in prod (id=166 "CRS Only" w/ the 117 pilot hotels, id=67 "LiveKit Wyndham OHIP"), the first
  Wyndham onboarding after this PR merges throws an unhandled exception instead of a useful error.

  The CRS/PMS `.get()` working today is luck, not design — the pair has no unique constraint.

  ### The design question answers itself: which row gets attached is irrelevant
  Verified by reading every consumer. `BookingGatewayService.get_provider`
  (`backend/canary/booking_gateway/services/booking_gateway.py:145-150`) is the *only* routing
  path, and it does `getattr(hotel_config.config, f"{operation_kind.value}_provider")` — it reads
  the enum pair and nothing else. The other three consumers
  (`voice/services/booking_authform_service.py:405,498,582`) all just check
  `config.booking_provider == PMS`. **Nothing anywhere reads `BookingGateway.name`, `.id`, or
  `.uuid` for behaviour.** A CRS/CRS row is a CRS/CRS row. The duplicate is cosmetic.

  This is already codified in the codebase. `BookingAgentEnablementService._resolve_or_create_booking_gateway`
  (`backend/canary/voice/services/booking_agent_enablement.py:269-282`) does
  `.filter(pair).order_by("id").first()`, with a docstring that spells it out:
  > "Routing reads only the coarse config.booking_provider, so any row for the pair is
  > interchangeable and the lowest-id match is picked deterministically. The pair has no unique
  > constraint and can carry duplicate rows (14 (pms, pms) in prod US)."

  ### Recommendation — fix the service, not the data
  In `configuration.py:36`, replace the `.get(pair)` with
  `.filter(pair).order_by("id").first()` and raise `NoSuchBookingGatewayError` on `None`,
  mirroring `_resolve_or_create_booking_gateway`. That:
  - unblocks the CRS/CRS switch with **no prod data change**
  - kills the latent `MultipleObjectsReturned` for *every* pair, not just this one
  - still fails loudly with the actionable error code in the only case that matters (zero rows)

  Add a test — `booking_gateway/tests/services/test_configuration.py` currently has **no**
  duplicate-row case (checked; fixtures only ever create one row per pair).

  **Do not** delete or rename gateway id=67. Functionally pointless (routing is by pair), risks
  the LiveKit test setup, and `voice/testing/livekit/full_flow/hotels.py:150` does `get_or_create`
  so it would just come back.

  **Rejected**: adding `unique_together` on (availability_provider, booking_provider). Would
  require cleaning the 14 duplicate (pms,pms) prod rows and repointing their `BookingGatewayConfig`
  FKs first — big job, zero functional gain, and the `_resolve_or_create` docstring already
  decided against it.

  **Cosmetic caveat worth stating up front**: `.order_by("id").first()` picks id=67
  ("LiveKit Wyndham OHIP") over id=166 ("CRS Only"), so newly onboarded Wyndham hotels will show
  the LiveKit name in Django admin. Zero functional impact. If it bugs people, rename id=67 to
  something neutral — nicety, not a blocker.

  ### Loose ends for whoever picks this up
  1. PR #51892 is still a **draft with no CI run**. Needs the service fix + test, then un-draft.
  2. PR description claims "Existing hotels are updated separately by EV-276's backfill command"
     — **that command does not exist and EV-276 hasn't been started.** ENT-7018 is safe to ship
     first (only affects newly onboarded hotels), but Stephen's actual ask — "target the CRS for
     everything" — is *not* delivered until EV-276 lands. EV-276 needs an engineer assigned.
  3. PR test-plan box "Confirm a CRS/CRS BookingGateway row exists in prod before merge" is
     already satisfied by Andrés's own comment (id=166, 117 hotels). Can be ticked.

  ### Draft Linear reply — NOT POSTED, needs your approval
  > Answering my own question from the 3rd — the duplicate turns out not to matter.
  >
  > `BookingGatewayService.get_provider` is the only routing consumer and it reads just the
  > (availability_provider, booking_provider) enum pair; nothing reads the gateway's name or id.
  > So id=166 and id=67 are interchangeable for behaviour. `BookingAgentEnablementService`
  > already handles this by taking `.filter(pair).order_by("id").first()`.
  >
  > Plan: make `BookingGatewayConfigurationService` do the same instead of a bare `.get()`,
  > plus a test for the duplicate case. No prod data change, and it removes the latent
  > `MultipleObjectsReturned` for every pair rather than just this one.
  >
  > Separately — EV-276 is still in Triage and unstarted. This PR only covers *new* onboardings,
  > so we don't hit "CRS for everything" until that backfill has an owner.

  Say the word and I'll post it (or a trimmed version).
project: 2026-04-16T1210-unblock-team
source_id: https://linear.app/canary-technologies/issue/ENT-7018/update-wyndham-onboarding-to-use-crs-only-booking-config
tags:
- morning-gtd
- linear
- from-awareness
time_minutes: 20
title: 'Look at ENT-7018: Wyndham CRS-only booking config'
updated: 2026-08-12 11:47:36.286238
waiting_on: null
waiting_since: null
working_on: false
---

Stephen replied after OOO: "We can do whatever you think is best! The output we need is just that we target the CRS for everything." In Progress, Andrés assigned — the design call is effectively open.
https://linear.app/canary-technologies/issue/ENT-7018/update-wyndham-onboarding-to-use-crs-only-booking-config