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
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1780081180659859?thread_ts=1780081180.659859&cid=C047K6WSUJY
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 15
title: 'Read: voice onboarding streamlining PRD + PRs #46600-46604'
updated: 2026-06-02 14:48:18.622737
waiting_on: null
waiting_since: null
working_on: true
---

Gaston's voice onboarding (Integrations Tab) streamlining — PRD + backend/frontend PRs.
https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1780081180659859?thread_ts=1780081180.659859&cid=C047K6WSUJY