---
area: admin
contexts:
- react
created: 2026-05-31 07:45:57.150239
defer_until: null
due: 2026-06-01
energy: medium
id: 2026-05-31T0745-plan-with-connor-andrea-to-run-ihg-hotelkey-onboar
order: null
output: |
  ## Agent run 2026-06-01T15:35:00

  Prepared the plan for running the IHG HotelKey onboarding script with Connor & Andrea
  (target: Monday; Taylor back Wed). Scope clarification + required onboarding values +
  pre-run drift check. NOTE: did NOT touch production or any external service — research only.

  ### Scope clarification (important)
  - The 9 sites in the ENT-6357 body (BTVSA, TMBPW, MLBWP, MCOSW, SRQJB, ACTIN, TIWWA,
    PFNBH, SJCDA) are IHG **Opera** sites — being done **manually**, NOT via the script.
    (The IHG PMS provider no-ops PMS config unless Salesforce PMS = "hotelkey"/"hotel key",
    so the script wouldn't write HotelKey config for an Opera site anyway.)
  - **FHKEX (Holiday Inn Express Fishkill) is the single HotelKey property** Dianna flagged
    ready for the script (Linear comment 2026-05-29). This run = FHKEX only, HotelKey + FreedomPay.
  - Connor's stated concern (2026-05-28): "risk we might overwrite something the properties
    don't want overwritten" — that IS the drift check below.

  ### How the script runs (config-driven, not a one-shot CLI)
  Two `OnboardingValue` records keyed by Salesforce account_id, then a batch run.
  - Code: backend/canary/onboarding/ (configuration_providers/ihg/ + plans/)
  - Values loaded via Admin CSV upload (/admin/onboarding/onboardingvalue/upload-csv/)
    or stubbed programmatically; executed by `cron_run_onboarding_script_batches`
    (every ~30m) or `OnboardingService.onboard_hotel_from_salesforce_account(...)`
    with onboarding_type=IHG_PILOT.
  - Plan order for IHG_PILOT: ConfigurePMSIntegrationCreateConfigurationPlan (HotelKey)
    → ConfigurePaymentGatewayIntegrationPlan (FreedomPay).
  - Hard dependency: Salesforce account PMS field must = "HotelKey" (case-insensitive).
    Confirm FHKEX's SF PMS is set before running.

  ### Required onboarding values to collect BEFORE Monday
  Source these from HotelKey (Mohak/Taylor) + FreedomPay (Lilly) + the master sheet
  (Google Sheet 1xvcbeohp... tab 2). Verified against the marshmallow schemas in code.

  1) HOTEL_KEY_CREDENTIALS  (onboarding/.../integrations_schemas/hotelkey.py — ALL 9 required, non-empty):
     - property_id        (HK UUID; FHKEX known historically as f178201a-… — confirm current)
     - property_code      (FHKEX)
     - api_host           (https://00.us-west-2.na.ihg.hkclients.com/ for IHG)
     - username           (canary-<code lowercase>; data-ingestion UN from HK)
     - password           (UUID from HK)
     - webhook_username   (hotelkey-<PROPERTY_CODE>; Canary-controlled)
     - webhook_password   (short opaque string; Canary-controlled)
     - brand_identifier   ("ihg")
     - environment_name   (must resolve to HotelKeyEnvironment "IHG - PRODUCTION 2-WAY" / env id 166)

  2) FREEDOMPAY_CREDENTIALS  (.../integrations_schemas/freedompay.py):
     - store_id           (required — from FreedomPay/Lilly)
     - terminal_id        (required — from FreedomPay/Lilly)
     - token_type         (optional; IHG defaults to "99")
     - enable_charging    (optional; defaults true → also wires charging vendor config)
     If the FreedomPay value is absent the payment-gateway plan no-ops (records "skipped"),
     it does NOT fail the batch — so decide explicitly whether FHKEX gets FreedomPay this run.

  ### Pre-run drift check on FHKEX (the core ask — do together, READ-ONLY, before writing)
  FHKEX is a Wave-0 property that was already manually configured (env 166, 2-way) and was
  401-storming on the V4 PMS Core API as of mid-May (per-property HK activation regression,
  ENT-6032). So expect pre-existing state. Critical idempotency behavior to know:
  - ConfigurePMSIntegrationCreateConfigurationPlan only upserts a vendor config when
    `getattr(account, vendor.value) is None` (create_configuration_plan.py:82). If FHKEX
    ALREADY has a HotelKey config, the script will **silently SKIP the credential upsert** and
    only reconcile account_groups / ignored_room_type_codes. So new credentials in the
    OnboardingValue will NOT overwrite a divergent live config — drift persists silently.
  - Payment-gateway plan: if an existing gateway config is a DIFFERENT vendor it resets &
    recreates; if same vendor (FreedomPay) it mutates in place. A pre-existing Elavon/other
    config would be replaced — confirm what's live first.

  Checklist to verify before running (Django admin / read-only shell on prod — do NOT write):
  [ ] Does FHKEX already have a pms-gateway Account + HotelKey config? (if yes, script skips creds)
  [ ] If config exists: does its property_id / username / webhook creds match the OnboardingValue
      we're about to load? Any mismatch = silent drift the script won't fix → fix manually/escalate.
  [ ] Account env = 166 ("IHG - PRODUCTION 2-WAY") and brand_identifier = "ihg" (empty breaks
      can_use_pms_core_api)?
  [ ] Existing payment gateway vendor on the hotel (FreedomPay vs Elavon vs none)?
  [ ] Salesforce PMS field = "HotelKey"?
  [ ] HK confirmed per-property V4 activation for FHKEX is LIVE (it regressed before — was 401ing).
      The script cannot fix this; HK (Mohak) must (re)activate. Verify with a read-only V4 probe.
  [ ] account_groups expected: ["IHG Onboarding Project", "IHG"] (provider sets
      ONBOARDING_IHG + BRAND_IHG) — will be reconciled on run.
  [ ] DCI / Upsells / Messaging / checkout already live (per ticket) — confirm script won't
      disturb check_in_configuration (it does set is_tokenizing_with_hotel_payment_gateway=True
      when a payment gateway config exists).

  ### Agenda for the Monday session (Gareth + Connor + Andrea)
  1. Confirm FHKEX is the only property in scope this run (HotelKey); Opera 9 stay manual.
  2. Walk the drift checklist above against live FHKEX state together (Connor has the
     "don't overwrite" context Taylor usually owns).
  3. Decide: if FHKEX already has a HotelKey config that matches → low value re-running; the
     real blocker is likely HK V4 activation, not our config. If it diverges → fix path.
  4. Confirm FreedomPay store_id/terminal_id are in hand (else payment plan no-ops).
  5. Run via batch and watch run results / pre-run checks; verify gateway via
     verify_configuration post-hook.

  ### Open questions to raise (do NOT action externally without approval)
  - Is FHKEX's HotelKey config already present in prod, and does it match the values we'd load?
    (Needs a read-only prod check — get explicit OK first.)
  - Has HK re-activated V4 for FHKEX since the mid-May 401 storm? (Mohak/Yauheni)
  - Are FreedomPay store/terminal IDs for FHKEX delivered yet? (Lilly)
project: 2026-04-16T1210-unblock-team
source_id: https://linear.app/canary-technologies/issue/ENT-6357/ihg-properties-to-be-added-to-pilot-poc
tags:
- morning-gtd
- linear
time_minutes: 15
title: Plan with Connor & Andrea to run IHG HotelKey onboarding script (ENT-6357)
updated: 2026-06-01 16:42:06.956332
waiting_on: null
waiting_since: null
working_on: true
---

Connor: let's do this together Monday; not pressing. FHKEX (Holiday Inn Express Fishkill) now ready for the script.
https://linear.app/canary-technologies/issue/ENT-6357/ihg-properties-to-be-added-to-pilot-poc

Notes:
* Requires onboarding values - list required for hotel key pms config and payment gateway
* check hotel state beforehand for drift