---
area: null
contexts: []
created: 2026-06-02 12:09:27.828469
defer_until: null
due: null
energy: low
id: 2026-06-02T1209-prep-handover-for-wcp
order: null
output: |
  ## Agent run 2026-06-04T10:20:53Z

  ### What this task is (Slack context)
  Thread: Marta Ziaei's "Upcoming WCP Activations for June & July" (CC Ani, Connor,
  Gareth, Jessica Cervantes, Andrea). WCP = **Wyndham Connect Plus** (adds Voice AI +
  WhatsApp/SMS messaging to *existing* Wyndham hotels; does NOT create new hotels).
  Wave schedule:
    - Tue Jun 9  — ~25 properties, proactive wave, BAU (NOT new-property-openings/NPO)
    - Mon Jun 29 — ~145, assumptive wave, includes NPO sites
    - Tue Jul 7  — ~60, assumptive wave
    - Tue Jul 22 — ~20, proactive wave, BAU
  Handover driver: Marta is OOO Mon 6/29, so she'll train **Jessica Cervantes** on the
  Jun 9 batch so Jessica can support the Jun 29 go-live. (Open question in thread:
  Ani thought Christi wanted one big June batch — Marta has a Q out to Christi, who is
  OOO. Worth confirming before treating Jun 9 scope as final.)

  ### Pre-requisites for a full WCP cohort run → go-live
  Verified against backend/canary/onboarding/. The WCP onboarding flow runs as a Cohort
  of sequential OnboardingScriptBatches (OnboardingType.WYNDHAM_CONNECT_PLUS):
    Stage 1 ASSIGN_PHONE_NUMBER  (WyndhamAssignPhoneNumberProvider)
    Stage 2 BASE_CONFIGURATION_NEW (Booking GW, CRS GW, Chat settings, Configure Voice)
    Stage 3 UPDATE_PMS_CONFIGURATION (OHIP guarantee codes)
    Stage 4 GOLIVE (WyndhamConnectPlusGoLiveProvider) — terminal, can be scheduled at a
            cohort go_live_date/time/timezone; cron_run_onboarding_script_batches runs
            scheduled batches every 30 min.
  Go-live was made runnable as a *custom batch* for WCP under ENT-3971.

  **The hard prerequisite is seeding OnboardingValues correctly BEFORE the cohort runs.**
  OnboardingValue is a key-value store keyed by (account_id, kind) with a unique
  constraint; account_id here is the **Salesforce account ID** (IdType.SF_ACCOUNT_ID) and
  needs the SF checksum (add_sf_id_checksum / the testing stubs handle it). Defined in
  backend/canary/onboarding/models/onboarding_values.py.

  WCP-relevant OnboardingValue kinds (all keyed by SF account id):
    - VOICE_AI_INBOUND_PHONE_NUMBER (str)            — Bandwidth voice number per hotel
    - VOICE_AI_OUTBOUND_FORWARDING_CONFIG (list)     — forwarding rules (FRONT_DESK,
                                                       RESERVATION_MODIFICATION, RESERVATION_BOOKING)
    - WYNDHAM_MOVE_TO_WHATSAPP_APPROVED_SUBACCOUNT (str) — target Twilio subaccount SID
    - INTENDED_SMS_PHONE_NUMBER (dict)               — intended SMS number per hotel
    - TWILIO_REGISTRATION_DATA (dict)                — brand/campaign registration data

  How the values get seeded (the actual handover-able procedure):
    1. dev_create_wcp_onboarding_values_csvs --input-csv <WCP properties.csv>
       --twilio-subaccount <SID> --output-dir <dir>
       Reads the WCP Properties CSV (cols: "SFDC ID", "Bandwidth (Wyndham)",
       "SmartSheet - Front Desk/Reservation Modifcation/Reservation Booking (SRS)") and
       emits 3 CSVs:
         - voice_numbers.csv            → VOICE_AI_INBOUND_PHONE_NUMBER
         - subaccount_onboarding_values.csv → WYNDHAM_MOVE_TO_WHATSAPP_APPROVED_SUBACCOUNT
         - forwarding_numbers.csv       → forwarding config
       (Skips any row missing SFDC ID or Bandwidth number — check the WARNING output.)
    2. update_or_create_onboarding_values --s3-uri s3://... (or --local-csv) to import.
    3. INTENDED_SMS_PHONE_NUMBER values are seeded separately from the Twilio export
       (Rami built a Google Sheet for this — see ownership below).

  ### Go-live readiness gate (WyndhamConnectPlusGoLiveProvider + checks/wyndham_connect_plus.py)
  Per hotel, all must be healthy before GOLIVE:
    - CRS gateway configured; Twilio configured w/ a phone number; voice number configured
    - INTENDED_SMS_PHONE_NUMBER matches the hotel's actual configured SMS number
    - Hotel is on an APPROVED Twilio subaccount (WYNDHAM_APPROVED_TWILIO_SUBACCOUNTS)
    - Hotel has NO legacy messaging service (twilio_messaging_service_sid is null)
    - SMS-capable number exists on the subaccount
    - WhatsApp config complete: allow_send_whatsapp=True, disable_sms_channel=False,
      whatsapp_phone_number / whatsapp_business_account_id / twilio_whatsapp_sender_sid set
    - WhatsApp sender status == ONLINE
    - Twilio brand approved + campaign approved
    - Payment gateway configured (US/Canada only)
  GOLIVE itself: sets hotel.has_authorizations=True, has_formweaver_auth_or_contract_flow
  =True, migrates hotel to Authorization UI v2.
  Note: hotels onboarded after WYNDHAM_CONNECT_PLUS_SMS_CUTOVER_DATE skip the
  WhatsApp/Twilio-brand provisioning path — confirm which side of the cutover the Jun 9
  cohort is on, as it changes which checks apply.

  ### Known gotchas to flag in the handover
    - Phone-number mismatches (intended vs in-use) are the recurring failure. Rami has a
      `fix_wcp_numbers_mismatch.py` gist to detect/repair them — get this from Rami.
    - The OnboardingValue Django Admin form has NO JSON schema validation yet (hardening
      item, was in flight) — malformed values can be saved silently. Double-check seeded
      data rather than trusting the form.
    - WhatsApp subaccount move only happens AFTER brand registration completes —
      sequencing matters.
    - Cohort tooling auto-adds hotels to go-live on cohort creation / membership change,
      so be deliberate about cohort membership.

  ### Ownership / references for the handover doc
    - Rami Nieto has been the hands-on operator for WCP batches (incl. edge cases, the
      INTENDED_SMS seeding sheet, and the mismatch-fix gist) — natural co-owner/SME.
    - Jessica Cervantes is the trainee for Jun 9 → Jun 29.
    - Notion doc "WCP Monitoring checks" documents when each monitoring check turns on
      during the WCP process — link it in the handover.
    - Pod capacity previously noted as Lauta + Ryan.

  ### Suggested handover-doc skeleton (for the user to fill/confirm)
    1. Scope of the Jun 9 cohort (25 SFDC IDs; confirm w/ Christi re: one-big-batch Q)
    2. WCP Properties CSV location + the 3-CSV generation + import commands above
    3. OnboardingValue seeding checklist (5 kinds) + how to verify each in admin
    4. Cohort creation (OnboardingType.WYNDHAM_CONNECT_PLUS, go_live date/time/tz)
    5. Stage-by-stage run + the go-live readiness checklist above
    6. Gotchas + Rami's mismatch-fix gist + WCP Monitoring checks doc

  ### Caveats
    - Stage wiring / go-live checks read from property_configuration_processes.py,
      wyndham_connect_plus_go_live_provider.py, checks/wyndham_connect_plus.py via an
      exploration agent; OnboardingValue model + dev_create_wcp_onboarding_values_csvs.py
      were read directly and verified. Bear/Slack context summarized, not deep-read line
      by line.
    - Did NOT post anything to Slack/Linear/Notion. Did not query staging/prod.

  ## Agent run 2026-06-04T12:48:48Z

  ### Task: scope a ticket so CS can self-serve VOICE_AI_OUTBOUND_FORWARDING_CONFIG

  TL;DR — Most of the self-service plumbing already exists in Django admin. The ONLY
  thing that still forces an engineer to run `dev_create_wcp_onboarding_values_csvs` for
  *forwarding config specifically* is **phone-number normalization** (raw Google-Sheet
  numbers → E.164). Close that one gap in the admin CSV-import path and CS can do the
  forwarding step themselves. This is a small, well-bounded ticket.

  ### What already exists (verified in code, no engineer needed)
  The OnboardingValue admin (`onboarding/admin/onboarding_value.py`) already ships TWO
  CS-usable, UI-only paths for forwarding config:
    1. **Bulk CSV upload** ("Convert CSV to Onboarding Values"): upload-csv -> map-fields.
       - VOICE_AI_OUTBOUND_FORWARDING_CONFIG is registered in KIND_SCHEMAS, so it's a
         selectable kind.
       - `ForwardNumberSpecSchema.get_csv_fields` / `transform_csv_data`
         (configuration_providers/configs/voice.py) already auto-detect the WIDE format
         `sf_id, FRONT_DESK, RESERVATION_MODIFICATION, RESERVATION_BOOKING` and pivot it
         to long rows, then group by account and upsert
         (`OnboardingValueService.process_grouped_rows_to_onboarding_values`).
       - The field-mapping step lets CS map arbitrary sheet column names (e.g.
         "SmartSheet - Front Desk") onto the category fields, and the onboarding_type
         dropdown already resolves enterprise hotel IDs -> SFDC account IDs + checksum.
    2. **Single-account friendly form** (`create_value_view`, KIND_FORMS): pick
       account_id + kind, then a `ForwardingConfigFormSet` with category dropdown +
       to_number per row. Already wired ONLY for VOICE_AI_OUTBOUND_FORWARDING_CONFIG.

  So bulk import of forwarding config through the admin is already possible in principle.

  ### The actual gap (the reason the mgmt command still runs)
  `dev_create_wcp_onboarding_values_csvs` does exactly two transforms the admin path does
  NOT do, and only one matters for forwarding config:
    - **Phone normalization**: it runs `format_phone_number(x, "US")` on every number
      (lines 100-102). The admin import path takes the strings verbatim --
      `transform_csv_data` only does `.strip()`, and `ForwardNumberSpecSchema.to_number`
      is a bare `fields.String()` with NO format/validation. So raw sheet values like
      "(202) 555-1234" or "202.555.1234" would be saved un-normalized and silently break
      voice forwarding (or only get caught at go-live by the FRONT_DESK-number check).
    - (The command also emits the voice-number and subaccount CSVs, but those are
      separate kinds and out of scope for this ticket.)

  ### Recommended ticket (smallest correct change)
  Title: Let CS import Wyndham voice forwarding config from the Google Sheet without an
  engineer -- normalize/validate phone numbers in the OnboardingValue admin import
  Goal: CS uploads the WCP Properties sheet export directly in the admin CSV-import UI
  and gets correctly-normalized VOICE_AI_OUTBOUND_FORWARDING_CONFIG values, with no
  `dev_create_wcp_onboarding_values_csvs` step.
  Scope:
    1. Normalize `to_number` to E.164 on import. Cleanest: do it in
       `ForwardNumberSpecSchema` (a `@post_load`/`@pre_load` that runs
       `format_phone_number(value, "US")`), so BOTH the bulk CSV path and the
       single-account formset get it for free. Reuse
       `canary.utilities.format_phone_number.format_phone_number`.
    2. Validate it: reject blank/unparseable numbers with a clear per-row error
       (the map-fields view already surfaces `invalid_rows` with messages). Today a bad
       number saves silently -- fail loud instead.
    3. (Optional, nice-to-have) Document for CS the exact sheet columns to map, or add a
       small column-name alias so the SmartSheet Front Desk / Reservation Modifcation /
       Reservation Booking (SRS) columns map onto FRONT_DESK / RESERVATION_MODIFICATION /
       RESERVATION_BOOKING without manual mapping.
  Explicitly out of scope: voice inbound number + WhatsApp subaccount seeding (still via
  command/other flows), the go-live cohort run, RBAC changes.
  Acceptance: a CS member, given the raw sheet export, imports forwarding config for a
  multi-hotel batch through admin only; numbers land in E.164; malformed rows are
  rejected with actionable errors; no shell/management-command step.
  Est: small (S) -- one schema hook + validation + a test in
  `tests/admin/test_onboarding_value_form.py` / service test. US-only `format_phone_number`
  matches current command behavior (WCP is US/Canada).

  ### Open questions for the user before filing
    - Confirm country assumption: command hardcodes "US"; any CA-numbered WCP hotels that
      need a different region hint? (format_phone_number may still parse +1 CA fine.)
    - Does CS already have Django-admin access to the OnboardingValue model, or is an
      access/permission grant a prerequisite (separate ticket)? Worth confirming w/ Rami.
    - Which team owns this -- same pod as the WCP onboarding work (Lauta/Ryan), with Rami
      as SME?
    - Want me to also fold in the voice-number + subaccount CSV steps so the WHOLE
      `dev_create_wcp_onboarding_values_csvs` command can be retired, or keep this ticket
      narrowly on forwarding config as the task states?

  ### Caveats
    - Read directly + verified: admin form, voice schema, both mgmt commands,
      OnboardingValue model, process_grouped_rows_to_onboarding_values. Did NOT run code
      or create the Linear ticket. No external writes.

  ## Agent run 2026-06-04T13:13:54Z

  ### Follow-up: source forwarding config BROADLY from the sheet, not per-batch
  Gareth's concern: a CSV generated from the Google Sheet contains ALL WCP rows, not just
  the upcoming batch. Reframed question: can we just source from the source-of-truth sheet
  and seed onboarding values broadly + repeatably, avoiding stale intermediate CSVs?
  Short answer: YES, and it's the better model. Read the sheet directly to verify.

  ### Read the actual sheet (Google Drive, read-only)
  Sheet: "Wyndham Connect Plus..." id 1Pbqkt5c41IN05wYP39l-6nn31j2I7UV84HsbUkwDD3g.
  Parsed the **"Scheduled Sites - Updated"** tab authoritatively (xlsx export, sheet2.xml).
    - 2,761 data rows; **1,356 are complete** (have SFDC ID + Bandwidth + all 3 SmartSheet
      forwarding numbers). The other ~1,405 are blank/spacer rows.
    - Data is CLEAN: 100% of rows that have an SFDC ID also have Bandwidth AND all three
      forwarding numbers. Numbers are already in +E.164 form (e.g. +17153555501).
    - Go-Live Date column spans many batches (2025-07 through 2026-05+ in the sample), i.e.
      this tab is the full historical + scheduled WCP roster, not one batch.

  ### Cross-reference vs `dev_create_wcp_onboarding_values_csvs`
  The command reads exactly these input columns; the sheet has every one (incl. the
  "Modifcation" misspelling), so the tab is already the command's input shape:
    - "SFDC ID"                              -> sheet col [8]
    - "Bandwidth (Wyndham)"                  -> [10]
    - "SmartSheet - Front Desk"              -> [18]
    - "SmartSheet - Reservation Modifcation" -> [19]
    - "SmartSheet - Reservation Booking (SRS)"-> [20]
  Bonus finding: the command takes ONE `--twilio-subaccount` for the whole batch, but the
  sheet has a populated PER-ROW "Twilio Subaccount" col [12]. Sourcing the subaccount kind
  from the column is strictly more accurate than the command's single-value arg.

  ### Why broad pre-seeding is SAFE (the key insight)
  Seeding an OnboardingValue is fully DECOUPLED from go-live activation:
    - VOICE_AI_OUTBOUND_FORWARDING_CONFIG is read in exactly ONE place —
      `WyndhamVoiceAIConfigProvider.__init__`, which only runs when a hotel's configure-voice
      plan executes during ITS cohort run. The value sits inert until then.
    - Seeding values does NOT add anyone to a cohort. (The "cohort auto-adds hotels to
      go-live" gotcha from the prior run is about COHORT membership, not OnboardingValue
      writes — so broad seeding cannot accidentally schedule a go-live.)
    - Upsert is idempotent and keyed on (SFDC account_id, kind). Re-running is safe.
    - Already-live hotels: the value is not re-read post-go-live, so re-seeding them is
      functionally inert (only a cosmetic data-drift consideration, not operational risk).
  => Exporting/seeding all 1,356 rows is safe and is the cleaner model: pull from source of
     truth, upsert broadly, repeat whenever the sheet changes. No per-batch scoping needed,
     no intermediate-CSV staleness.

  ### What this changes about the ticket (refines the 12:48 scope)
  The "all rows vs batch" worry is a non-issue once seeding != activation is understood.
  Two ways to deliver the repeatable broad-seed; pick one:

  OPTION A (recommended, smaller — "truly hand to CS"): make the existing admin CSV
  importer ingest the raw "Scheduled Sites - Updated" tab export directly.
    1. Recognize the sheet's column names: alias "SmartSheet - Front Desk" /
       "...Reservation Modifcation" / "...Reservation Booking (SRS)" -> FRONT_DESK /
       RESERVATION_MODIFICATION / RESERVATION_BOOKING in
       `ForwardNumberSpecSchema.get_csv_fields` / `transform_csv_data`. Today it only
       auto-detects columns literally named FRONT_DESK etc., which is why the command's
       rename step is currently required.
    2. Skip incomplete rows (transform already drops blank-number cells — confirm/keep).
    3. Normalize + validate `to_number` to E.164 (defensive; this tab is already clean,
       but other tabs/manual edits aren't). Reuse `format_phone_number`.
    4. Document for CS: "Download the 'Scheduled Sites - Updated' tab as CSV -> admin
       'Convert CSV to Onboarding Values' -> kind VOICE_AI_OUTBOUND_FORWARDING_CONFIG ->
       import. Uploading the whole roster is intended and safe."
    Result: CS self-serves the full broad seed, repeatably, no engineer, no mgmt command.

  OPTION B (bigger — fully automated): a scheduled job that reads the sheet via the Google
  Sheets API and upserts forwarding config (+ optionally voice number & per-row subaccount)
  for all complete rows. Truest "no human" version, but needs Sheets API creds/integration
  and ongoing ownership. Probably a follow-up, not the first ticket.

  ### Open questions for Gareth
    - A or B? (Recommend A first; B as a later "full sync" if desired.)
    - Should the same broad-seed approach also cover VOICE_AI_INBOUND_PHONE_NUMBER (col 10)
      and WYNDHAM_MOVE_TO_WHATSAPP_APPROVED_SUBACCOUNT (per-row col 12), retiring
      `dev_create_wcp_onboarding_values_csvs` entirely? The sheet supports all three.
    - Confirm: is re-seeding already-live hotels acceptable (it's inert), or should the
      importer skip hotels past go-live to avoid drift noise?

  ### Caveats
    - Sheet read read-only via Google Drive MCP; parsed "Scheduled Sites - Updated"
      (sheet2.xml) directly. "Seeding != activation" verified by single consumer of the
      kind (WyndhamVoiceAIConfigProvider). Did NOT run backend code, query prod, or create
      any ticket. No external writes.
project: null
source_id: null
tags: []
time_minutes: 5
title: Scope a ticket to allow CS to handle voice forwarding config for Wyndham Connect
  Plus cohorts
updated: 2026-06-04 16:24:19.002031
waiting_on: null
waiting_since: null
working_on: false
---

VOICE_AI_OUTBOUND_FORWARDING_CONFIG onboarding value
Why engineers need to set this: We have to run a management command to convert a CSV downloaded from the google sheet to onboarding values
It's a quick job. 
But we should have a way to truly hand this to CS