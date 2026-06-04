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
project: null
source_id: null
tags: []
time_minutes: 5
title: Prep handover of WCP batch June 9th
updated: 2026-06-04 10:20:53.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1780336505845529

What are the pre-requisites of a full WCP cohort run through to go-live?
Particularly around OnboardingValues?