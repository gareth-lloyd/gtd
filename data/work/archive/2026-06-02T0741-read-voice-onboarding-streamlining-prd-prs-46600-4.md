---
area: management
contexts:
- consume
created: 2026-06-02 07:41:51.378950
defer_until: null
due: 2026-06-02
energy: medium
id: 2026-06-02T0741-read-voice-onboarding-streamlining-prd-prs-46600-4
order: null
output: |
  ## Agent run 2026-06-02T14:15

  Read Gaston's "voice onboarding streamlining for CS" PRs + surrounding context.
  Linear epic: VOX-2622 (project "Improve voice onboarding script(s) with clear
  input instructions for CS", Voice team, target 2026-05-29).

  ### TL;DR
  Voice onboarding moves from an eng/Voice-driven config script into a self-serve
  "Voice Setup" modal on the adminland Integrations/Messaging tab, so CS can
  activate a hotel's voice product without Voice/Eng in the loop. The modal is a
  thin wrapper over the existing configure-voice script (script behavior is
  largely unchanged). The core data change: make the general `forward_call_to`
  number a REQUIRED onboarding value for non-Wyndhams (and demote the granular
  `ForwardingConfig` to optional). Driven by hotels going live with no forward
  number -> calls fail silently while still counting as "handled" (Meritage
  incident, VOX-2511).

  ### Links
  - PRD (Notion, needs auth — I could not read it this session):
    notion.so/canarytechnologies/PRD-Voice-Setup-Integrations-Tab-359814686151811ca425f923cb5dc685
  - Demo Looms: wyndhams loom.com/share/a7c8c27106c74210a4f59c8a6ad246c6 ;
    non-wyndhams loom.com/share/06a2a090871f49aaafeb0d81d3efae84
  - Slack thread: C047K6WSUJY p1780081180659859 (2026-05-29)

  ### The PR stack (all OPEN, author gdelarrechea; base = #46727 kind+migration)
  Backend:
  - #46600 (1/3) Add `forward_call_to` as a required onboarding value. Default
    provider sources it from VOICE_AI_FORWARD_CALL_TO; Wyndham keeps deriving it
    from its FRONT_DESK entry; ConfigureVoicePlan fails fast if missing. (+560/-73)
  - #46602 (2/3) Per-hotel missing/invalid onboarding-value detection +
    `OnboardingValueSchemas` registry; `voice_onboarding_values` module
    (check_kinds_for_hotel, serialize_missing_kind — omits current_value for
    secrets); unifies admin + API validators. (+672/-146)
  - #46603 (3/3) `voice_setup` service + `voice_wiring` resolver; endpoints
    GET /voice/setup/status and POST /voice/setup/activate. Activate does value
    upserts + batch/hotel/run rows in one transaction, runs the configure-voice
    script inline after commit, takes a per-hotel lock + fails fast if voice
    already configured (no duplicate batches). (+855/-0)
  Frontend:
  - #46601 (1/2) Extract `ForwardNumbersLegacy.vue` + libphonenumber
    `forwardNumbersValidation` into packages/shared/components/voice/, shared by
    CallSettingsPage and the new modal. Based on #46600. (+903/-212)
  - #46604 (2/2) Adminland `VoiceSetupModal` — surfaces missing/optional voice
    onboarding values, inline-edits with E.164 validation, posts to
    /voice/setup/activate via Bridge. Diamond dep: needs #46603 AND #46601;
    GitHub base is #46603, so its frontend CI stays red until #46601 merges
    (expected for stack tip). (+1492/-0)
  - (also: #46599 strict E.164 phone validation, standalone; #46727 the
    VOICE_AI_FORWARD_CALL_TO kind + migration, base of the chain.)
  Merge order: #46727 -> #46600 -> {#46602, #46601} -> #46603 -> #46604.

  ### Wyndham angle — DIRECTLY RELEVANT TO ME (I'm cc'd / mentioned in thread)
  - Gaston deliberately left Wyndhams unchanged (script still uses the required
    FRONT_DESK entry as the forward number) to avoid disrupting workflows I had
    flagged.
  - Open question he raised: is "front_desk == forward_call_to" a rule that
    ALWAYS holds for Wyndhams? -> Connor Swords CONFIRMED (2026-06-01): yes, the
    default/fallback forward_call_to for all Wyndhams should equal their
    front_desk number. So the Wyndham derivation is sound; no action needed from
    me unless I want to revisit. Relates to my ENT-6360 Wyndham work.

  ### What Gaston wants from ENT (Andrea asked)
  - Eyes mainly on the BACKEND PRs. Frontend labels/cosmetics still in flux but
    nothing functional. He noted the integrations-tab form is just a wrapper over
    the config script, so no separate Wyndham config-script review needed.

  ### Status
  Read-only digest only — no code reviewed for correctness, nothing pushed, no
  Slack/Linear/GitHub writes made. Notion PRD body not read (MCP not
  authenticated this session) — open the link directly if the narrative is needed.

  ## Agent run 2026-06-03T12:18 — backend review + architecture critique

  Reviewed the 3 backend PRs (#46600/#46602/#46603) in full + read the actual
  Notion PRD this time. Conclusion escalated from "good stack, some questions" to
  "the stack has a fundamental category error rooted in the PRD."

  ### The core finding — category error
  Onboarding scripts are INTERNAL Canary-staff tooling for configuring hotels
  (Salesforce-account-keyed, batch/run records, dashboards). The Integrations tab
  is a CUSTOMER/hotel-staff surface. PR #46603 wires the Integrations-tab "save"
  to literally trigger an onboarding SCRIPT RUN: it manufactures
  OnboardingScriptBatch/Hotel/Run rows and calls script_run_attempt ->
  onboard_hotel_from_salesforce_account -> ConfigureVoicePlan. So a customer
  action drives the staff onboarding engine. Tells: SFDC-keyed (hard-fails with no
  SF metadata), creates onboarding records in staff dashboards, Wyndham path
  routes through script_type BASE_CONFIGURATION_NEW (a forwarding-number edit
  going through the "base config / new hotel" stage).

  ### Is it Gaston's bad impl, or the PRD's seed? -> The PRD seeds it.
  PRD says 3x: UI "triggers the onboarding flow" / "triggering the voice
  onboarding flow" / "Hotel admin can add a forwarding number to trigger the
  onboarding flow." Its mental model = "Integrations tab is a new front door onto
  the EXISTING onboarding flow." It conflates a CAPABILITY (provision voice for a
  hotel) with a MECHANISM (the staff onboarding script), and asks to expose the
  mechanism to a 2nd audience. Easy mistake because today they're the same object.
  Gaston implemented that framing faithfully — too literally (synthetic batch) —
  and confirmed it in Slack: "the integrations tab form is a wrapper to the config
  script." So: PRD plants the error, implementation entrenches it. Fix needs a
  PRD-level reframe, not just code review.

  ### Correct seam (recommended direction)
  Extract a voice-domain provisioning service: voice/services/voice_provisioning.py
  `provision_voice(hotel, *, forward_call_to, inbound_number=None, forwarding=None)`
  — hotel-keyed, no Salesforce, no batch/run records; does the Twilio purchase +
  LiveKit + writes voice.Configuration. BOTH callers depend on it: the staff
  onboarding ConfigureVoicePlan delegates to it (unchanged externally), and the
  Integrations-tab save calls it directly (never enters onboarding). Two callers of
  one capability, not one flow with two front doors. This also dissolves most of
  the validation concern (voice values stop being OnboardingValues on an SFDC key).

  ### Smaller-scope options also discussed (if full reseam is deferred)
  Validation (concern: voice rules + blast radius landed in onboarding/services/values.py):
  - A1 (small): revert validate_data to generic type-check; move E.164/forwarding
    rules to a voice-owned validator; voice validates at its boundaries. Kills the
    CSV/SF-sync blast radius; voice rules live in voice.
  - A2 (bigger): make validate_data a pure dispatcher to a per-kind validator
    registry that each domain registers into (inverts onboarding->voice import).
    Cleans ownership for ALL branded kinds but keeps central blast radius.
  Execution (concern: synthetic batch + inline run on web thread):
  - B1: call onboard_hotel_from_salesforce_account directly, no batch rows. NOTE:
    superseded by the provision_voice seam — B1 still rides onboarding machinery.
  - B2: create a real SCHEDULED-style batch, run async via worker, modal polls
    status -> "Connected". PRD-native (PRD's "Connected" terminal state fits async);
    removes web-thread timeout risk + long lock. Keeps the batch though.

  ### Other review points (from full backend read)
  - Auth: activate endpoint gated on hotel-facing VOICE_HAS_SETTINGS_ACCESS. After
    reading PRD this is INTENDED (PRD: hotel admins trigger via forwarding number).
    Caveat: when non-US inbound-number entry lands (CS-only per PRD), ensure hotel
    admins can't set the Twilio number.
  - Inline run blocks the web request through Twilio/LiveKit calls (timeout risk).
    lock_instance is a DISTRIBUTED lock (not select_for_update) so no DB pinning.
  - Failed run leaves the synthetic batch IN_PROGRESS (success path finalizes via
    mark_as_processed_if_batch_is_complete; fail_run doesn't). Cron only picks up
    SCHEDULED so likely just dashboard noise — confirm.
  - #46602 moves KIND_SCHEMAS validation into validate_data -> now runs on EVERY
    upsert caller (CSV import, SF sync), not just admin. Confirm those paths emit
    conformant data.

  ### PRD coverage gaps (vs the 5 PRs)
  - Hotel-FACING Integrations row not in this stack — all 5 PRs are adminland-only
    (frontend/adminland/...). PRD shows customer-facing screens; this ships the
    CS/adminland half only. Confirm hotel-facing piece is a later phase.
  - Non-US/CAN inbound (Twilio) number not enforced server-side: the hook exists
    (required_onboarding_value_kinds_for_hotel) but DefaultVoiceConfigProvider
    doesn't override by country -> returns [FORWARD_CALL_TO] regardless.
  - Incident coverage: fully closes Meritage class (missing/malformed). Only
    PARTIALLY the Dupont Circle class (wrong-but-valid number) — real fix is
    VOX-2512 (validate voice_number against Twilio subaccount), not in this stack.

  ### Urgency / impact
  - SPLIT the stack. Safety core (#46727 + #46600 = make forward_call_to required,
    fail fast) is the urgent, low-risk Meritage fix -> ship on its own, fast.
  - Streamlining layer (#46602/#46603/#46604) is valuable but deferrable (no live
    outage; preventive). It carries ALL the architecture concerns above -> take the
    time to land it on the correct seam. PRD gives latitude (doesn't mandate the
    script machinery). Project target 2026-05-29 already passed; pressure is "finish
    in-flight," not "ship tonight."

  ### Suggested next actions (NOT taken — need my go-ahead)
  - Raise the category-error / provision_voice reframe with Gaston (+ likely the
    PRD owner) before more of the stack merges.
  - Greenlight #46727+#46600 to merge independently as the safety fix.
  - Decide: full reseam now vs A1+B2 interim. Capture non-US + hotel-facing gaps as
    their own tickets. No PR/Linear/Slack comments drafted or posted yet.
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1780081180659859?thread_ts=1780081180.659859&cid=C047K6WSUJY
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 15
title: 'Read: voice onboarding streamlining PRD + PRs #46600-46604'
updated: 2026-06-03 12:18:32.337517
waiting_on: null
waiting_since: null
working_on: false
---

Gaston's voice onboarding (Integrations Tab) streamlining — PRD + backend/frontend PRs.
https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1780081180659859?thread_ts=1780081180.659859&cid=C047K6WSUJY