---
area: null
contexts: []
created: 2026-05-15 14:28:53.647331
defer_until: null
due: null
energy: low
id: 2026-05-15T1428-set-pms-flags-for-ihg-hotels-when-onboarding
order: -14
output: "## Agent run 2026-05-15T16:05Z\n\n### Answer to the open question\n\"Is it
  'Has cards tokenization using hotel payment gateway' or Check-In\" →\nIt is BOTH:
  `is_tokenizing_with_hotel_payment_gateway` is a field ON the\nCheck-In Configuration
  model. Defined at\n`backend/canary/check_in/models/configuration.py:392` (the `Configuration`\nmodel,
  accessed as `hotel.check_in_configuration`). So the new flag belongs\nin the existing
  \"Check-In Configuration\" block of\n`IHGPilotEnableMsaProductsProvider.perform_hotel_configuration()`.\n\n###
  Where the flags are set today\nAll flags in this ticket are owned by\n`onboarding/configuration_providers/ihg/enable_msa_products_provider.py`\n→
  `IHGPilotEnableMsaProductsProvider.perform_hotel_configuration()`\n(gated to `OnboardingType.IHG_PILOT`).
  This provider already sets the\nbulk of the list. Cross-check below.\n\n### Already
  set (no work needed) ✅\n- integration_auto_post_to_pms / _marketing_consent / _phone
  / _notes\n  (lines 58,59,63,64) and the extra _passport/_dob/_nationality/_udf/\n
  \ _id_submitted/_check_in_time variants\n- push_registration_card_email_to_pms (68)\n-
  require_preexisting_reservations (69)\n- disable_view_full_card_info (76)\n- Add-On:
  AddonConfigurationService.enable(..., integration_push_purchases\n  _to_notes=True)
  (87-91) sets integration_enabled,\n  integration_push_purchases_to_charges, integration_push_purchases_to_notes\n\n###
  Gaps — actual scope of the ticket\n1. **`check_in_configuration.is_tokenizing_with_hotel_payment_gateway
  = True`**\n   — NOT currently set by the IHG provider. This is the real new line.\n
  \  Precedent: Wyndham sets it at\n   `wyndham/wyndham_enable_msa_products_provider.py:101`.\n
  \  ⚠️ Ordering/validation constraint: Configuration.clean()/save validation\n   (configuration.py:1010-1021)
  raises ValidationError if no payment gateway\n   is configured OR vendors are added
  to the gateway. So the IHG payment\n   gateway plan (FreedomPay) MUST run before
  this flag is flipped. Confirm\n   plan ordering in ONBOARDING_TYPE_CONFIG (IHG_PILOT)
  before implementing,\n   or set it in a later ScriptType than payment-gateway config.\n2.
  **`check_in_configuration.integration_precheckin_method = PrecheckinMethod.PREREG`**\n
  \  — listed in ticket. Model default is ALREADY `prereg`\n   (configuration.py:236-239),
  so this is a no-op for fresh configs.\n   Value only as an explicit idempotent set
  for reactivation/drift. Low\n   priority — call out, decide whether to bother.\n3.
  **`check_in_configuration.has_check_in_mobile = True`** — \"Has check in\n   mobile\".
  Field default is ALREADY True (configuration.py:184). Same as\n   #2: explicit-set
  only matters for reactivation/drift. (Note: distinct\n   from `hotel.has_check_in`
  which the provider already sets at line 43.)\n4. Add-On `integration_push_purchases_to_charges`
  — already covered by\n   AddonConfigurationService.enable() BUT guarded by\n   `if
  hotel.integration_secret_key:` (addon_configuration.py:15). If\n   integration_secret_key
  is empty when the provider runs, ALL add-on\n   integration flags silently skip.
  Verify the secret key is populated\n   before this provider runs (ordering dependency),
  else add-on flags\n   won't stick. Worth a validation/assertion.\n\n### Recommended
  ticket scope (1 implementation point + 2 checks)\n- Add one line: `hotel.check_in_configuration.is_tokenizing_with_hotel_\n
  \ payment_gateway = True` in the Check-In Configuration block of\n  IHGPilotEnableMsaProductsProvider,
  AFTER confirming FreedomPay payment\n  gateway plan runs first (validation ordering).\n-
  Optionally add explicit `integration_precheckin_method = PREREG` and\n  `has_check_in_mobile
  = True` for idempotency (both are already defaults\n  — minor, decide if reactivation
  safety justifies the lines).\n- Add a guard/assertion that `hotel.integration_secret_key`
  is set before\n  AddonConfigurationService.enable so add-on flags don't silently
  no-op.\n- Tests: extend\n  `onboarding/tests/configuration_providers/ihg/` (or the
  integration\n  test added in d047d00081e) to assert is_tokenizing flag + add-on
  flags.\n\nNo code changed — scoping only. Ready to file as an implementation ticket.\n"
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: 5
title: 'Scope ticket: set  flags for IHG hotels during onboarding scripts, when setting
  IHG pilot'
updated: 2026-05-15 15:07:14.095782
waiting_on: null
waiting_since: null
working_on: false
---

Is it "Has cards tokenization using hotel payment gateway"
or Check-In

General

:white_check_mark: Has check in mobile
Integrartion Pre-CheckIn Method  = PreReg
PMS Integration / Auto-Post

:white_check_mark: Integration auto post to pms
:white_check_mark: Integration auto post to pms marketing consent
:white_check_mark: Integration auto post to pms phone
:white_check_mark: Integration auto post to pms notes
:white_check_mark: Push registration card email to pms
Reservations

:white_check_mark: Require preexisting reservations   (optional)
Credit Card / Payment

:white_check_mark: Has cards tokenization using hotel payment gateway (is_tokenizing_with_hotel_payment_gateway)
:white_check_mark: Disable view full card info




For Add-On


:white_check_mark: Integration enabled
:white_check_mark: Integration push purchases to notes
:white_check_mark: Integration push purchases to charges