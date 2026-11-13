---
area: null
completed_at: null
contexts: []
created: 2026-11-05 17:51:45.336951
defer_until: null
due: null
energy: low
id: 2026-11-05T1751-view-this-thread-ani-s-work-and-see-how-to-incorpo
order: null
output: |
  ## Agent run 2026-11-05T18:40+02:00

  ### Blocker: I could not open Ani's flowcharts
  - The artifact (https://claude.ai/artifact/GwhQkgRjjmnU8z9rSF6wkY) returns "not found" from your account too.
  - The fallback she posted is an HTML export, not a PDF: "Enterprise Activation and Auditing Customer Success Workflow.html", Slack file F0CECEY7QMR, 422 KB, in the thread at https://canarytechnologies.slack.com/archives/C0CEA2R2XSP/p1793725201989989?thread_ts=1793714332.835959&cid=C0CEA2R2XSP
  - Two download attempts (curl with the gtd Slack token, then a script reusing the gtd fetcher's _api helper) were blocked by the auto-mode permission classifier as credential use. To unblock: download it from Slack into /private/tmp/claude-501/-Users-garethlloyd-projects-canary/4941a23a-ed1b-426a-a96f-f1a251d8efbc/scratchpad/ani_dl/ and relaunch, or allow the Bash call.
  - Everything below is from the thread plus her Notion "Wyndham Audit Workspace", which is the running system behind the flowcharts.

  ### What Ani has built (Notion, not the artifact)
  - Workspace: https://app.notion.com/p/344814686151803bb2cfeab4219193ef (Customer Success Homebase / Enterprise / Wyndham Connect). Project plan: https://app.notion.com/p/35081468615180b691ecd3c16e58ca3d. Rule tracker: https://app.notion.com/p/5ea3b2f562214e329f88d2b913b64a07. Audit runs, tickets, exceptions and themes are sibling databases; Trails-generated triage/fix playbooks per rule.
  - Data sources: Omni (Canary analytics), Smartsheet Master Site List (MSL), Salesforce go-live dates, Twilio/WhatsApp state. It is cross-system reconciliation, run on a weekday cadence per flow (NAMER Mon, delivery rate Tue, Connect Plus Wed, International Thu).
  - 27 rules across three flows. NAMER and International share R1-R11: opt-out in MSL but live in Canary (R1), live in MSL but missing expected products (R2), partial enablement (R3), GJM config mismatch Omni vs Smartsheet (R4), messaging still active on opted-out site (R5), future go-live already sending (R6), PMS type mismatch (R7), in Omni but missing from MSL (R8), products on but zero messages (R9), sending with no go-live date (R10), go-live set but zero messages / fully unprovisioned (R11). Connect Plus: AUTH-001 auth gap, VOICE-001 voice gap, COV-001 live on MSL not live in Canary, OPT-001 opt-out/live conflict, OPTCON-001 Salesforce vs MSL conflict, S11-001 Status 11 closure still live.
  - Her new ask in the thread: extend from auditing live state to Enterprise activation workflows (Wyndham first, then Best Western), low-risk workflows this/next week, complex ones late November, December review. Human review at every stage to start. She wants alignment on which steps may be fully automated.

  ### How it relates to drift detection and your rules work
  - Drift detection (Tincho, project P-ENT-1910 https://linear.app/canary-technologies/project/configuration-drift-detection-364d47914acc) takes the cohort from Salesforce (MSA_HOTEL_PROVIDERS -> WyndhamConnectSelector.should_have_gone_live_according_to_salesforce in rules_based_configuration/services/drift.py) and checks settings against the brand tree. It assumes membership and checks configuration.
  - Ani's rules are almost all about membership and lifecycle: should this site be on at all, is it opted out, has it gone live, is it actually sending. That is the input drift takes for granted. The two are complementary, not duplicates. Andrea's "fold it in" is right for a subset only.
  - Direct overlaps worth moving into drift so they run nightly with DriftAcknowledgement as the exception store: R2, R11, AUTH-001, VOICE-001, COV-001 (required-product gaps; ENT-7100 and ENT-7116 already added an audit shortlist as FINAL rules, so check what is left), R4 GJM mismatch (blocked on the GJM drift design ENT-8066, which depends on your binding-rules value reader), R7 PMS mismatch (capability-driven drift doc https://app.notion.com/p/3b18146861518073a23dd5241ddc8b6b).
  - Things drift cannot see and should stay in her layer: Smartsheet MSL, Omni message counts, Twilio/WhatsApp status, opt-outs, Status 11 closures. R1, R5, R6, R8, R9, R10, OPT-001, OPTCON-001, S11-001.
  - One bridge already exists in Canary: WyndhamConnectSelector.active_hotels_from_latest_batch reads the latest Wyndham properties CSV batch (is_active flag). R1-style "in Salesforce cohort but inactive in latest Wyndham feed" could be a Canary-side rule without Smartsheet.
  - CS-facing audit tooling she may not know about: management command audit_hotel_config (fleet-wide, read-only, CSV fix list) and HotelConfigHealth (pre-go-live health check) in rules_based_configuration. These are the activation-time checks her North Star probably wants.
  - Design tension to name on Friday: she treats Smartsheet MSL as truth and Salesforce as a cross-check (OPTCON-001 exists because they disagree); drift uses Salesforce only. Pick one canonical cohort source or the two tools will flag each other.
  - Ryan Rogers raised the same convergence on 2026-10-09 (onboarding scripts and drift sharing definitions, https://canarytechnologies.slack.com/archives/D07MJEGGV19/p1791512082628469). Ani's activation automation is a third consumer of "expected configuration", which strengthens the case for binding rules as the single source.
  - Bear has nothing on Ani's workflow itself; the 2025 lineage is your ENT-3503 audit, the Wyndham active/inactive Salesforce vs Smartsheet note, and the happy-state monitoring project.

  ### Draft thread reply (not sent, needs your OK)
  > Had a look at the audit workspace. I'd split it by question rather than merge the tools: Ani's rules answer "should this site be live, with which products, and is it actually sending" from MSL/Omni/Salesforce/Twilio; drift detection answers "given it's live, is the config to brand standard" from Salesforce + the rules tree. The overlap is the product-gap rules (R2/R11/AUTH/VOICE/COV) and GJM mismatch (R4), which I'd move into drift so they run nightly and exceptions live in one place (DriftAcknowledgement). R7 PMS mismatch fits the capability rules. The rest needs data Canary doesn't hold, so it stays in Ani's layer, and her "should be live" output is a better cohort feed than Salesforce alone. One thing to settle Friday: MSL vs Salesforce as the canonical cohort source, since they disagree today. Also, audit_hotel_config and the pre-go-live health check already exist for activation-time checks.

  ### Loose ends for you
  - No calendar invite for Andrea's Friday knowledge share showed up on your calendar for 2026-11-07; ask Andrea to add you if you want to be there.
  - Get the HTML export so the current vs North Star activation flow can be mapped step by step; the above only covers the auditing half.

  ## Agent run 2026-11-05T19:05+02:00 (HTML export read)

  Export read from ~/Downloads (copy at /private/tmp/claude-501/-Users-garethlloyd-projects-canary/4941a23a-ed1b-426a-a96f-f1a251d8efbc/scratchpad/ani_dl/ani.html). Seven tabs: Wyndham today, North Star, Phase 1, Timeline, Audit workflows, Deliverability, Salesforce records, Lifecycle events.

  ### What the flowcharts say
  - Today: every build, activation and lifecycle change is hand-worked on set activation days. New openings loop through parked partial builds while PMS or imagery is outstanding. Support "why is this site on/off" tickets need a manual check across Smartsheet, Canary and Salesforce. Claude only audits after the fact, Wyndham only, from reports swept out of Ani's inbox into a dated Drive folder.
  - North Star: files land in one central location (feed, email, sheet or Salesforce); ingest; site exists? auto-build or update; log every attempt to a system of record; retry daily within 7 days of activation, every 2 days after, escalate to a person after 3 failures; activate on designated day; validate; process opt-outs automatically. Humans only on exceptions (retries exhausted, PMS flip conflict, significant deviation). Customer still owns the "should be live" list.
  - Phase 1 (four automations): missing header / room upgrade image checks off the existing audit; assigned tipping activations scripted; new properties auto-built as they appear in the data; BAU site activations run from the Smartsheet by script, with the team confirming the activation list before go-live. Stays manual: completing partial builds, lifecycle events, new-opening activation.
  - Timeline: week of Nov 9 low-impact (image checks, tipping activations, deliverability screening and ticket filing, low-impact Salesforce field updates); Nov 16 complex with human confirmation (BAU activations from Smartsheet, new property builds, new Salesforce records and exits); Nov 23 observe; December move confirmed activations to full automation; January complex workflows end to end.
  - Audit tab adds to the Notion picture: 13 NAMER rules now (R12 Tip Active consistency, R13 Can Be Tipped consistency added; R3 retired; R10 "two definitions in use, confirm before running"); pre-checks for stale source (>10 days), no change since last run, and required columns by name; standing-exception suppression and new/recurring/resolved deltas; outputs are an Excel report, Notion run + per-rule tickets, one Linear ticket per run for MSL vs Salesforce room-count mismatches (GTM Analytics). Status 11 has been missing from the Salesforce reports since about v11.
  - Deliverability: separate weekly screen per site (SMS US/CA last 7 days from Omni US; international SMS and WhatsApp last 30 days from Omni EU; 10+ messages, success <90% and failure >=60%), top Twilio error code bucketed (21612 carrier blocks 38% of failing sites, landline/invalid 25%), one CustOps ticket per failing site with 90-day repeat handling. Email not audited. Files carry no site ID, so matching is by hotel name.
  - Salesforce target: Claude drafts every new hotel record and record change from source data; low-impact field updates apply on their own and are logged; new accounts and exits wait for Marketing Database / CustOps approval.
  - Lifecycle table: new opening, BAU, closure, opt-out, activation delay, PMS flip, brand flip all move to auto or auto-with-confirm; flag change and individual site setup out of scope.

  ### What this changes in the engineering picture
  - Canary already has the North Star's ingest half, with the activation branch deliberately switched off. onboarding/services/vendor/wyndham_properties_job.py pulls the Wyndham properties feed from SFTP into a BatchUpdateRun; WyndhamPropertiesBatchUpdateService._process_update matches on Wyndham site ID, adds reactivated sites to the portfolio, updates phone numbers, and on Status 11 termination auto-creates a removal OnboardingScriptBatch and posts "Wyndham Status 11 Batch Created" to Slack with a /manage/onboarding/script-batches link. The active-and-not-present and active-and-inactive branches log "This script should not be activating hotels at this time" and stop. Her "auto-build new properties as they come in" is that disabled branch.
  - Her Phase 1 automations map onto existing OnboardingScriptBatch types rather than needing a Claude workflow to drive scripts from Smartsheet: BASE_CONFIGURATION_NEW, GOLIVE, TIPPING_GOLIVE, REACTIVATE_MSA_HOTEL, DEACTIVATE_MSA_HOTEL, UPDATE_PMS_CONFIGURATION (PMS flip), REMOVE_HOTEL_FROM_PARENT_BRAND (exit), CONFIGURE_TWILIO, plus plans for main hotel image, room upgrades, tipping and deactivate-tipping. The /manage script-batches review step is the "team confirms activation list" gate she wants. The retry engine and system of record she plans to build are OnboardingScriptBatch/OnboardingScriptHotel plus BatchUpdateRun; building them in Drive duplicates this.
  - Source-of-truth conflict is sharper than I wrote earlier. Her flow treats the Smartsheet MSL as truth for who should be live; Canary's feed job treats the Wyndham SFTP properties file as truth and drift detection treats Salesforce as truth. Three cohorts. Status 11 is a concrete example: missing from her Salesforce reports, but arriving in Canary from the feed and already generating removal batches.
  - The Salesforce write plan (automatic low-impact field updates, drafted accounts and exits) needs a flag from you: drift cohorts are read from Salesforce Onboarding Status / go-live via CohortHotelService, so automated edits there move drift cohorts and "live counts" reporting. Also no-write Salesforce is a standing rule in this GTD setup; I did not and will not touch it.
  - Image checks: no header or room-upgrade image check exists in rules_based_configuration (grep of hotel_fleet_audit and hotel_config_health is empty), so that one is net new and small; configure_main_hotel_image plan is the fix path.
  - Deliverability screening has no Canary equivalent and matches by hotel name because Omni exports lack site ID; adding the Wyndham site ID (HotelAssociationIdType.WYNDHAM_SITE_ID) to the Omni export would remove a whole class of mismatches.

  ### Revised position for Friday (replaces the earlier draft reply)
  1. Audits: split by question as before. Product-gap, GJM and PMS rules move into drift; lifecycle and opt-out rules stay with Ani; deliverability stays with Ani.
  2. Activation: do not build the auto-build / retry / system-of-record in Drive. Turn on the disabled branch of the Wyndham feed job under OnboardingScriptBatch with the /manage review as the confirmation gate. That is the Phase 1 "new property builds" and "BAU activations" with less new code and with audit logging. Needs an owner on the Enterprise pod and a decision from CS on whether the SFTP feed or the Smartsheet MSL is the activation trigger.
  3. Cohort source: pick one of SFTP feed, MSL, Salesforce as canonical for "should be live" and make the other two audits of it. Today each tool uses a different one.
  4. Salesforce writes: keep Claude to drafts with human apply, at least until drift cohort reads are decoupled from the fields it would edit.
  5. Quick wins engineering can hand her now: site ID on Omni exports; Status 11 from the feed instead of Salesforce; audit_hotel_config CSV as the pre-activation check.

  ### Draft thread reply v2 (not sent, needs your OK)
  > Read the flowcharts, thanks Ani. Two reactions. Auditing: your rules and drift detection ask different questions (should this site be live vs is a live site configured to standard), so I'd move only the product-gap, GJM and PMS rules into drift and leave lifecycle, opt-out and deliverability with your workflow. Activation: most of the North Star already exists in Canary as the Wyndham properties feed job plus onboarding script batches; the auto-build branch is deliberately disabled and the /manage script-batch review is the confirmation gate you describe. I'd rather we switch that on than rebuild retries and a system of record in Drive. The thing to settle Friday is which source is canonical for "should be live": your flow uses the Smartsheet MSL, the feed job uses the Wyndham SFTP file, drift uses Salesforce, and they disagree today (Status 11 is a live example). On Salesforce, I'd keep it to drafts with a human applying for now, since drift and live counts read those fields.

  ## Agent run 2026-11-06T10:30+02:00 (correction + input mapping)

  Gareth's correction: the "activation already exists in Canary" finding overreaches. Salesforce is the source of truth and the Wyndham SFTP feed carries no training or go-live dates (fields: HOTEL_ID, SITE_STATUS 7 active / 8,9,11 terminated, anticipated termination date, GM and owner contacts, legal and property address, phone, TAX_ID, SYNXIS_ID). The feed job can detect and terminate, not activate.

  ### Ani's inputs mapped to Canary
  - Smartsheet NAMER/INTL MSL (Canary Active, opt-out, scheduled/actual go-live, tip date, Tip Active) -> onboarding.models.SalesforceOpportunity per OnboardingType (WYNDHAM_MSA, WYNDHAM_CONNECT_PLUS, WYNDHAM_TIPPING, WYNDHAM_AI_VOICE, WYNDHAM_CALL_CENTER_BOOKING): go_live_date, target_activation_date, training_date, training_state, onboarding_status, onboarding_blocked_reasons (PROPERTY_OPTED_OUT), stage, active_products, last_salesforce_sync. Joined via SalesforceHotelAccount.hotel.
  - Salesforce reports (go-live, guestrooms, Status 11) -> same mirror for dates; Status 11 from the SFTP feed site_status; guestrooms NOT mirrored (gap).
  - Omni product activation -> Hotel.has_* flags, is_active, Wyndham portfolio membership.
  - Omni messaging status -> Twilio configuration, GuestJourneyMessage enabled types (R4 "fewer than 4"), ScheduledMessage.sent_at (R6/R9/R10 zero messages).
  - Omni PMS integrations -> PMS integration config on the gateway side (not confirmed where the vendor string lives in canary).
  - Omni deliverability -> notifications SMS/WhatsApp notification rows with status and error code (notifications/models/sms_notification.py, whatsapp_notification.py, notification_status.py); keyed by hotel, so no name matching.
  - Email NPO International reports -> new rows in the SFTP feed.
  - Join keys: HotelAssociation WYNDHAM_SITE_ID (feed, MSL site ID), SalesforceHotelAccount.salesforce_account_id (Salesforce), hotel_id (everything Omni).

  ### Where each rule would live
  - monitoring app (CohortHotel + MonitoredCheckType + monitoring/tasks/refresh_monitoring_state.py; CohortHotelService filters by training/go-live date and training state): lifecycle rules R1, R5, R6, R9, R10, R11, OPT-001, OPTCON-001, S11-001. Existing checks already cover HAS_ALL_MSA_PRODUCTS, HAS_NON_MSA_PRODUCTS, guest journey messages sent, TWILIO_IS_CONFIGURED / BRAND_APPROVED / CAMPAIGN_APPROVED, HAS_ROOM_UPGRADE_IMAGES (her Phase 1 image check), EXPECTED_ONBOARDING_PLANS_RUN.
  - drift detection (rules_based_configuration): configuration rules R2, R4, R7, R12, R13, AUTH-001, VOICE-001, COV-001.
  - Example expressions: R1 = PROPERTY_OPTED_OUT on the WYNDHAM_MSA opportunity AND hotel.is_active AND any MSA product flag on. R6 = go_live_date > today AND messages sent last 7 days > 0. S11-001 = feed site_status in {8,9,11} AND hotel.is_active (feed job already builds the removal batch). OPTCON-001 = go_live_date <= today AND PROPERTY_OPTED_OUT on the same opportunity (pure mirror check).

  ### Real gaps
  - Guestrooms not in the Salesforce mirror; room mismatch needs a field on SalesforceHotelAccount/Opportunity compared with Hotel.room_count.
  - Sync freshness: mirror refreshes per account during batch runs and from the /manage property sync view; no scheduled full sync found (unverified). Stale-source pre-check becomes a last_salesforce_sync age check.
  - Email deliverability: no data in Canary or Omni.
  - Smartsheet-only hand-typed columns, if any, cannot be reconstructed. Ask Ani for the MSL column list.
  - No export of MonitoredCheckTransition / DriftAcknowledgement to Notion or Linear; Canary MCP is the cheapest read path for her workflow.
project: null
source_id: null
tags: []
time_minutes: 5
title: View this thread, Ani's work and see how to incorporate her stuff
updated: 2026-11-12 12:21:55.752875
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C0CEA2R2XSP/p1793714332835959

artifact is inaccessible, but ani has shared a pdf