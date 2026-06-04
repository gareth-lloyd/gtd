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

  ## Agent run 2026-06-03T14:05:00

  Acted on the CHANGED requirements: (1) produce the exact onboarding-value spec to
  create, (2) a /debug_in_shell drift check, (3) extract values from the new Google
  Sheet. Items 1 & 2 done and verified against current code. Item 3 is BLOCKED — see
  end. NOTHING was written to prod or any external service; no credentials fabricated.

  ### 1) Onboarding values to create — VERIFIED against current code
  Both are `OnboardingValue` rows, `IdType = SF_ACCOUNT_ID`, keyed by the Salesforce
  account id with checksum (`add_sf_id_checksum` is applied automatically by both the
  admin form and `OnboardingValueService.upsert`). Both kinds are in `SECRET_VALUE_KINDS`.
  Code refs (this branch):
  - Kinds/IdType: onboarding/models/onboarding_values.py (HOTEL_KEY_CREDENTIALS,
    FREEDOMPAY_CREDENTIALS; both -> SALESFORCE_ACCOUNT_ID; both in SECRET_VALUE_KINDS).
  - Schemas: onboarding/configuration_providers/integrations_schemas/hotelkey.py
    and .../freedompay.py. Read by .../ihg/pms_config_provider.py and
    .../ihg/payment_gateway_config_provider.py.

  HOTEL_KEY_CREDENTIALS — data is a JSON object; ALL 9 fields required, each non-empty
  (validate.Length(min=1)):
    property_id, property_code, api_host, username, password,
    webhook_username, webhook_password, brand_identifier, environment_name
  (No defaults — if any field is missing/empty the IHG PMS provider raises
  ERROR_MISSING_HOTEL_KEY_CREDENTIALS and the batch fails.)

  FREEDOMPAY_CREDENTIALS — data is a JSON object:
    store_id      (required, non-empty)
    terminal_id   (required, non-empty)
    token_type    (OPTIONAL — IHG provider IHGFreedomPayCredentialsSchema defaults "99";
                   you can omit it for IHG)
    enable_charging (OPTIONAL bool, default true -> also wires the charging vendor)
  If this row is ABSENT the payment-gateway plan no-ops ("Skipped ... no vendor config")
  and the batch still succeeds — so absence is a valid explicit choice, not a failure.

  How to create (two supported paths):
  A) Admin CSV upload: /admin/onboarding/onboardingvalue/upload-csv/
     - Pick onboarding_type = IHG_PILOT, kind = the kind, then map columns.
     - CSV header = `account_id` + one column per schema field above (exact field names).
     - The flow checksums account_id for you.
  B) Programmatic (in a shell, WITH approval — this is a prod WRITE):
       from onboarding.models.onboarding_values import OnboardingValue
       from onboarding.services.values import OnboardingValueService
       OnboardingValueService.upsert(SF_ACCOUNT_ID,
           OnboardingValue.Kind.HOTEL_KEY_CREDENTIALS, { ...9 fields... })
       OnboardingValueService.upsert(SF_ACCOUNT_ID,
           OnboardingValue.Kind.FREEDOMPAY_CREDENTIALS, { store_id, terminal_id })
     upsert() validates type + applies the checksum; update_or_create on (account_id,kind).

  ### 2) Drift check via /debug_in_shell — DONE (read-only, copied to clipboard)
  Strictly read-only snippet for the CANARY prod shell. Set HOTEL_SLUG (default "fhkex").
  It prints, with try/except around every network/lookup so a missing account can't abort:
  - hotel id/uuid + hotel.sfdc_account_id (raw);
  - PMSGatewayService.get_account(hotel): account.type, account.hotelkey
    (property_id/property_code/is_enabled), account_groups, ignored_room_type_codes,
    capabilities. KEY GATE: create-plan upserts creds only when account.hotelkey is None
    (create_configuration_plan.py:82, getattr(account, Vendor.HOTEL_KEY.value="hotelkey")).
    If hotelkey EXISTS, credential upsert is SILENTLY SKIPPED -> drift persists.
    NOTE: the canary /accounts/me API only exposes property_id/property_code/is_enabled —
    username/password/webhook/api_host/brand_identifier/environment_name are NOT visible
    from canary; deep credential drift must be checked in the PMS-GATEWAY shell/DB.
  - payment: check_in_configuration.payment_gateway_config_id; if set,
    GatewayConfigService.get_config(uuid).tokenizing_vendor/charging_vendor +
    get_tokenizing/charging_vendor_config -> FreedomPay store_id/terminal_id. Flags when a
    NON-FreedomPay vendor is present (payment plan would reset/recreate, orphaning child rows).
  - check_in_configuration.is_tokenizing_with_hotel_payment_gateway.
  - existing HOTEL_KEY/FREEDOMPAY OnboardingValue rows (prints field-key NAMES only, never
    secret values), keyed by both raw and checksummed sfdc_account_id.
  The 130-line snippet is on the clipboard now; re-generate any time from this item.

  ### 3) Extract credentials from the Google Sheet — BLOCKED (needs you)
  Sheet: docs.google.com/spreadsheets/d/1qj6ohH9al_tf2IYORdVHbdQXFRsP0B9YpG_jIzTD1Q0
  (gid=623900634). This is a DIFFERENT sheet from the earlier master sheet (1xvcbeohp...).
  I cannot read it: WebFetch returns HTTP 401 (auth-gated) and I have no authenticated
  Google path. I did NOT fabricate or guess any credential values.
  To unblock, either:
   - paste the relevant row(s) for the in-scope hotel(s) here (or export the tab to CSV and
     share it), OR
   - tell me the column->field mapping and the values, and I'll assemble the exact JSON /
     CSV for each OnboardingValue and (only with your explicit OK) load them.
  When you share it I need, per hotel: the SF account id, then the 9 HotelKey fields and
  (if FreedomPay this run) store_id + terminal_id.

  ### Scope reminder (unchanged from prior run)
  In-scope-for-script today = HotelKey properties only (prior run: FHKEX). The 9 ENT-6357
  Opera sites are manual and the IHG provider no-ops them (SF PMS not "hotelkey"). Confirm
  the current HotelKey hotel list before loading values — requirements changed, so re-verify
  whether it's still just FHKEX or more HotelKey sites are now ready.

  ### Not done / needs your call
  - No prod writes, no external-service writes, no Linear/Slack/GitHub posts.
  - Real credential values: blocked on sheet access above.
  - Running the drift snippet against prod is your action (paste in shell); I can analyze
    the output if you paste it back.

  ## Agent run 2026-06-03T14:30:00 — LIVE drift results for FHKEX (prod, read-only)

  Ran the read-only drift check against prod. Hotel resolved: id=18519
  "Holiday Inn Express Fishkill, an IHG Hotel", sso_hotel_id=fhkex, org=ihg,
  sfdc_account_id=001f200001m5lP3AAI, pms-gateway account uuid 45a377df-...619da.
  (Secret credential values are NOT recorded here on purpose.)

  HEADLINE: FHKEX is ALREADY fully live. Running the onboarding script on it has NO
  upside and ONE verified destructive side effect. Recommend NOT running it as-is.

  Live state:
  - account.type = hotelkey. account.hotelkey EXISTS, is_enabled=True, with the full
    9-field credential set already populated and consistent with the IHG pattern
    (property_code FHKEX, username canary-fhkex, webhook_username hotelkey-FHKEX,
    brand_identifier ihg, environment_name "IHG - PRODUCTION 2-WAY", api_host us-west-2
    hkclients). => There is NO HotelKey credential drift to fix.
  - Because account.hotelkey is not None, the create-config plan SKIPS the credential
    upsert entirely (verified). So loading a HOTEL_KEY_CREDENTIALS value canNOT overwrite
    the live creds — good, but also means the value achieves nothing for FHKEX.
  - account.ignored_room_type_codes = ['PF','PI','PS','PM'] (live, non-empty).
  - account.account_groups = []  (provider expects ONBOARDING_IHG + BRAND_IHG).
  - Payment gateway ALREADY configured: FreedomPay, tokenizing+charging,
    store_id 16453041002 / terminal_id 26917094000; check_in_configuration
    .is_tokenizing_with_hotel_payment_gateway = True.
  - No HOTEL_KEY/FREEDOMPAY OnboardingValue rows exist yet for the account.
  - Also present: a disabled Opera v5_on_prem config (hotel_code FHKEX, is_enabled=False)
    and HotelKey validations "fetch_reservation"/"authenticate" still "incomplete".

  *** VERIFIED DESTRUCTIVE DRIFT (this IS Connor's "don't overwrite" concern) ***
  To run the script you MUST first create a HOTEL_KEY_CREDENTIALS value (else the IHG
  provider raises ERROR_MISSING_HOTEL_KEY_CREDENTIALS and the batch fails). Once that
  value exists, config.configs is non-empty, so the create-config plan calls
  PMSGatewayService.update_account on the already-existing account with the IHG provider's
  hardcoded ignored_room_type_codes=[] (ihg/pms_config_provider.py builds
  PmsIntegrationConfig(ignored_room_type_codes=[])). pms-gateway treats [] as an explicit
  CLEAR — `ignored_room_type_codes` is in ACCOUNT_ALLOWED_FALSY_FIELDS
  (accounts/services/account.py:56, comment says "[] should be updated to empty array").
  => Running the script would WIPE FHKEX's live ['PF','PI','PS','PM'] to []. There is no
  OnboardingValue knob to prevent this; it's hardcoded in the provider.

  Other mutations the run would make:
  - account_groups: [] -> [IHG Onboarding Project, IHG] (additive; benign/arguably desired).
  - payment: only if a FREEDOMPAY_CREDENTIALS value is created — same-vendor in-place update
    of FreedomPay store/terminal (overwrites live values with whatever you load; no reset
    since vendor family matches).

  Recommendation:
  - Do NOT run the onboarding script against FHKEX. Creds already present; the only net
    effect is wiping ignored_room_type_codes (regression) for no config gain.
  - If the two account_groups genuinely need to be set, do it surgically (admin/targeted
    update), not via the full script.
  - The real open item for FHKEX is HotelKey-side: validations still "incomplete" — that's
    a HotelKey activation/validation matter (Mohak), not a Canary onboarding-value gap.
  - For any OTHER HotelKey property that is NOT yet configured, the script + freshly created
    values is the right path AND the destructive-wipe risk does not apply (no pre-existing
    ignored_room_type_codes to clobber). So re-confirm the current ready-to-onboard HotelKey
    list before creating values.

  Code refs for the wipe finding (this branch):
  - onboarding/configuration_providers/ihg/pms_config_provider.py (ignored_room_type_codes=[])
  - onboarding/plans/configure_pms_integration_create_configuration_plan.py:61-67 (update_account
    on existing account) and :82 (skip cred upsert when account.hotelkey not None)
  - pms_gateway/services/pms_gateway.py update_account (passes [] through)
  - (pms-gateway) accounts/services/account.py:56 ACCOUNT_ALLOWED_FALSY_FIELDS includes
    ignored_room_type_codes; patch() writes it.

  ## Agent run 2026-06-03T15:00:00 — credential availability check + ticket comment posted

  Requirement shifted to: build the OnboardingValue CSV for the ENT-6357 hotels from the
  Google Sheet (1qj6ohH9, gid 623900634). Read the sheet via the authenticated Google Drive
  connector (WebFetch was 401). Findings:
  - ENT-6357 = 9 IHG **Opera** sites (BTVSA, TMBPW, MLBWP, MCOSW, SRQJB, ACTIN, TIWWA, PFNBH,
    SJCDA) + FHKEX. Ticket (Dianna) says handle manually, hold the script til Taylor's back.
  - CSV mechanics confirmed: admin upload needs account_id = **Salesforce account id** (for
    IHG_PILOT the tool does NO id translation — create_hotel_identifier_map returns identity).
    Header = account_id + schema fields. Both kinds in SECRET_VALUE_KINDS.
  - The sheet does NOT contain loadable IHG 2-way creds for these hotels: 5 of 9 absent
    entirely; TMBPW/MCOSW only property_id->hotel mappings; MLBWP/TIWWA only their existing
    LEGACY integrations under different codes (MLBWP<->BWICH env-2 1-way; TIWWA<->66143 on
    the Best Western env). No FreedomPay store/terminal, no SF account ids for any.
  - tmp/investigations/ENT-6032-consolidated.csv also lacks them (9 absent; FHKEX present but
    webhook-only). So creds are nowhere available yet — they must come from HotelKey (Mohak)
    + FreedomPay (Lilly). FHKEX is the only HotelKey site and is already fully configured.
  - Did NOT fabricate or build a populated CSV (data absent + Opera sites no-op the script).
  - POSTED a comment to ENT-6357 (with user approval) stating the above blocker. Linear
    comment id 7818ce22-cfca-45db-ad96-23d0d32ad8e5.
project: 2026-04-16T1210-unblock-team
source_id: https://linear.app/canary-technologies/issue/ENT-6357/ihg-properties-to-be-added-to-pilot-poc
tags:
- morning-gtd
- linear
time_minutes: 15
title: Onboarding values for scripts - ENT-6357
updated: 2026-06-03 15:01:10.447146
waiting_on: null
waiting_since: null
working_on: false
---

Requirements have changed:
* Just create the needed onboarding values - list required for hotel key pms config and payment gateway
* check hotel state beforehand for drift via /debug_in_shell
* Extract credentials / values from https://docs.google.com/spreadsheets/d/1qj6ohH9al_tf2IYORdVHbdQXFRsP0B9YpG_jIzTD1Q0/edit?gid=623900634#gid=623900634