---
area: null
contexts:
- react
created: 2026-05-27 01:38:03.513739
defer_until: null
due: null
energy: low
id: 2026-05-27T0138-respond-on-stay-3604-ids-next-special-treatment-in
order: null
output: |
  ## Agent run 2026-05-27T10:30Z

  ### Investigation

  The IDS_NEXT special treatment Joanne is asking about is narrow:
  `backend/canary/onboarding/configuration_providers/wyndham/wyndham_pms_config_provider.py:252-255`
  early-returns for `Vendor.IDS_NEXT` in `configure_wyndham_hotel_for_pms_integration`,
  skipping `AddonConfigurationService.enable(...)`. Reason given in the comment:
  "no transaction codes defined yet" — i.e. we don't have a Wyndham→IDS_NEXT
  `room_upgrade_transaction_code` mapping, so we don't enable addons at all.
  It says nothing about `availability_rate_code`.

  What `availability_rate_code` actually gates
  (`backend/canary/pricing/services/room_upgrade_quote_service.py:24-72`,
  `RoomUpgradeQuoteService.should_use_dynamic_pricing`):
  - is_room_upgrade_enabled AND trusts_dynamic_pricing AND availability_rate_code
    AND trusts_live_inventory AND a PMSGatewayConfig exists AND the hotel has the
    `GET_AVAILABILITY_LIVE_RATES` capability.
  - IDS_NEXT capability list (`backend/pms-gateway/vendors/integrations/ids_next/capabilities.py`)
    has zero availability capabilities. So the dynamic-pricing/live-availability path
    cannot fire for IDS_NEXT hotels regardless of rate code value.
  - On top of that, the onboarding-script skip means `is_room_upgrade_enabled` is also
    False for IDS_NEXT Wyndhams.

  Net: setting RROD on Wyndham-IDS_NEXT hotels is inert today.

  The PR (#46270) currently does not filter by vendor — it picks up all Wyndham-portfolio
  hotels whose `addons_configuration.availability_rate_code` is null/empty, which would
  include any IDS_NEXT Wyndham properties that happen to have an addons_configuration row.

  Connor already replied in-thread (15:39 UTC, 2026-05-26):
  "@jchevalier are you able to see the rate codes returned from these? I think they
  should still have RROD" — i.e. his lean is to NOT exclude IDS_NEXT.

  ### Recommendation

  Lean: do not exclude IDS_NEXT — match Connor's reply. RROD is the canonical Wyndham
  rate code per the issue description ("approved by Connor for all Wyndham properties"),
  the change is a no-op for IDS_NEXT today (no capability + no addon enablement), and
  if/when IDS_NEXT availability is wired up the data is already correct. The onboarding
  script's IDS_NEXT skip is about addon ENABLEMENT (missing transaction codes), not
  about which rate code Wyndham uses semantically.

  If we do want symmetry with the onboarding script, the one-line change is to filter
  by hotel.pms vendor in the queryset.

  ### Draft Linear reply (NOT YET POSTED — awaiting user OK)

  Thread: https://linear.app/canary-technologies/issue/STAY-3604 (reply to Joanne's
  question under Nico's top-level "cc @andrea @ishwar" comment)

  ---
  Looked into this. The IDS_NEXT special-case in the onboarding script
  (`configure_wyndham_hotel_for_pms_integration`, `wyndham_pms_config_provider.py:252`)
  is narrow: we early-return for IDS_NEXT to skip `AddonConfigurationService.enable(...)`,
  because there's no Wyndham→IDS_NEXT `room_upgrade_transaction_code` mapping yet.
  That skip is about addon ENABLEMENT (transaction codes), not about which rate code
  Wyndham uses.

  `availability_rate_code` gates `RoomUpgradeQuoteService.should_use_dynamic_pricing`,
  which also requires `is_room_upgrade_enabled`, `trusts_live_inventory`, a
  `PMSGatewayConfig`, and the `GET_AVAILABILITY_LIVE_RATES` PMS capability. IDS_NEXT's
  capability list has no availability capability, and the onboarding skip means
  `is_room_upgrade_enabled` is False anyway — so RROD on a Wyndham-IDS_NEXT property
  is inert today.

  My vote is to not exclude them, matching Connor's reply: RROD is the canonical
  Wyndham rate code (per the issue: "approved by Connor for all Wyndham properties"),
  the write is a no-op for IDS_NEXT now, and the data is already right if/when
  IDS_NEXT availability is wired up later. If we'd rather mirror the onboarding-script
  pattern instead, it's a one-liner to filter by `hotel.pms` in the queryset.
  ---

  ### Status of PR #46270
  PR does NOT currently exclude IDS_NEXT. No code changes recommended unless we decide
  to flip to the "exclude" answer.

  ### Pending user action
  - Approve / edit / reject the Linear reply above. I have NOT posted to Linear.
project: null
source_id: https://linear.app/canary-technologies/issue/STAY-3604/upsells-set-rate-code-for-live-availability-to-rrod-for-all-existing
tags:
- morning-gtd
- linear
time_minutes: 15
title: 'Respond on STAY-3604: IDS_NEXT special treatment in Wyndham onboarding script'
updated: 2026-05-27 13:57:57.097399
waiting_on: null
waiting_since: null
working_on: false
---

Nico tagged @connor @glloyd for context on Joanne's question — should IDS_NEXT hotels be excluded from the RROD backfill management command? https://linear.app/canary-technologies/issue/STAY-3604/upsells-set-rate-code-for-live-availability-to-rrod-for-all-existing