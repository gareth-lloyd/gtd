---
area: null
contexts: []
created: 2026-07-01 17:08:38.306671
defer_until: null
due: null
energy: low
id: 2026-07-01T1708-examples-of-good-patterns-for-enterprise-scripts-c
order: null
output: |
  ## Agent run 2026-07-01T14:11Z

  Slack thread (https://canarytechnologies.slack.com/archives/C0B4QD01GP8/p1782913027991959)
  is just your own "I'll pull some examples" — no replies. So this is prep material for
  that thread: a good-vs-bad comparison of how onboarding/enterprise scripts should touch
  product configuration. All paths under `backend/canary/`.

  ### The principle
  An onboarding script (a ConfigProvider / OnboardingPlan) should declare WHAT product
  state it wants by calling the owning domain's configuration service, and let that
  service decide WHICH fields to set and how to persist them. Scripts should NOT reach
  across into another domain's model fields and `.save()` them inline. The domain service
  is the "configuration API"; the script is just a caller.

  ### GOOD examples (script → typed config → domain service)

  1) Addons — `AddonConfigurationService.enable()`
     addons/services/addon_configuration.py:4-39
     - Single service owns "what does enabling addons touch." Callers pass intent via
       typed kwargs (room_upgrade_transaction_code, availability_rate_code, ...).
     - Precondition-guarded (only writes integration fields if hotel.integration_secret_key).
     - Scoped `save(update_fields=[...])` — never a blind full-row save.
     - enable()/disable() symmetry.
     - Reused by 4+ onboarding providers (ihg/best_western/wyndham enable_msa + pms_config),
       i.e. the API is the single source of truth, not copy-pasted field pokes.

  2) Booking gateway — `BookingGatewayConfigurationService.update_or_create_booking_gateway_configuration()`
     booking_gateway/services/configuration.py:18-55
     Called from onboarding/plans/booking_gateway_plan.py:25-31
     - Typed enum args (BookingVendorKind) prevent invalid vendor combos at the boundary.
     - Validates precondition (matching BookingGateway must exist) and raises a typed
       domain error `NoSuchBookingGatewayError`; the plan maps that to a user-actionable
       onboarding error (ERROR_NO_BOOKING_GATEWAY_EXISTS).
     - Idempotent `update_or_create`, returns (obj, created) so the caller can record it.
     - Plan carries a typed config dataclass (configs/booking_gateway.py) from provider →
       service; the plan itself sets zero model fields.

  3) CRS gateway — `CRSSetupService.setup_crs_for_vendor()`
     crs_gateway/services/crs_set_up.py:26-52
     Called from onboarding/plans/crs_gateway_plan.py:55-84
     - Validates vendor_kind up front, routes to vendor-specific setup, delegates
       persistence to MulesoftConfigurationService.
     - Raises typed domain exceptions (InvalidPropertyDataError, MissingEnvironmentError,
       InvalidBrandIdentifierError); the plan translates each into a specific onboarding
       error code. Caller never mutates model fields — it invokes and handles exceptions.

  Shared shape of the good ones: provider builds a typed config dataclass
  (configuration_providers/configs/*), plan hands it to a domain `*ConfigurationService`
  / `*SetupService`, service validates + persists + raises typed errors. Cross-domain
  field knowledge stays inside each domain.

  ### BAD examples (script mutates other domains' fields inline)

  A) PMS config — `configure_wyndham_hotel_for_pms_integration(hotel, vendor)`
     onboarding/configuration_providers/wyndham/wyndham_pms_config_provider.py:227-274
     - A free function inside the onboarding module directly sets ~15 fields across
       hotel.check_in_configuration and hotel.check_out_configuration (pms_payment_slot_identifier="3",
       precheckin_method=PREREG, every integration_auto_post_to_pms_* flag, ...).
       That's check-in/check-out domain policy hardcoded in a Wyndham onboarding script.
     - Blind full saves: `check_in_configuration.save()` and `check_out_configuration.save()`
       with no update_fields (lines 245, 255) — clobber risk, no scoping.
     - Only the addon slice is done right (delegates to AddonConfigurationService.enable at
       line 270). Everything else is inline — so if check-in changes its config schema,
       this script silently drifts and nothing fails loudly.
     - No check-in/check-out "configuration API" to call; the knowledge lives in onboarding.

  B) MSA config — `WyndhamEnableMsaProductsProvider.perform_hotel_configuration()`
     onboarding/configuration_providers/wyndham/wyndham_enable_msa_products_provider.py:100-173
     - Worst offender: inlines writes across many domains in one method — hotel product
       flags (has_addons, has_check_in, has_check_out, has_chat, is_demo, is_active,
       rollout_whatsapp_integration), ~6 check_in_configuration fields, outbound_url, etc.
     - `hotel.save()` at line 163 with NO update_fields — saves the entire row.
     - Sets `hotel.has_addons = True` directly (line 132) AND separately triggers the addon
       path via configure_wyndham_hotel_for_pms_integration (line 171) → two competing
       sources of truth for "addons enabled."
     - Inconsistent: it DOES use services for some things (HotelService.set_check_in_time,
       FeedbackConfigurationService.update_or_create) but hand-pokes fields for the rest —
       proving the good pattern exists and just isn't applied uniformly.
     - "What is the Wyndham MSA product bundle" is smeared inline in the provider instead of
       each product domain exposing an enable()/configure() API the provider composes.

  ### One-line takeaway for the thread
  Good = provider builds a typed config, plan calls a domain `*ConfigurationService.enable/
  setup/update_or_create` that validates + scopes its own saves + raises typed errors
  (addons, booking_gateway, crs_gateway). Bad = onboarding code reaches into check-in/
  checkout/hotel fields and blind-`.save()`s them, with duplicated enablement flags and no
  owning API (configure_wyndham_hotel_for_pms_integration, WyndhamEnableMsaProductsProvider).
project: null
source_id: null
tags: []
time_minutes: 5
title: Examples of good patterns for enterprise scripts calling out to configuration
  APIs
updated: 2026-07-01 17:30:13.936278
waiting_on: null
waiting_since: null
working_on: false
---

read thread context: https://canarytechnologies.slack.com/archives/C0B4QD01GP8/p1782913027991959

addons
CRS gateway
Booking gateway

Bad examples:
* MSA config
* PMS config configure_wyndham_hotel_for_pms_integration