---
area: null
contexts:
- consume
created: 2026-06-09 07:02:18.789733
defer_until: null
due: null
energy: low
id: 2026-06-09T0702-read-voice-onboarding-streamlining-prd-pr-stack-ga
order: null
output: |
  ## Agent run 2026-06-09T11:55Z

  TL;DR: You already reviewed the original stack (46600–46604) and posted architecture
  feedback in the Slack thread on Jun 2. Gaston has since reworked it into a NEWER stack
  (47408 / 47420 / 47421 / 47422, on top of migration 46727) that directly addresses your
  feedback. The original 46600–46604 PRs are still open but effectively superseded — read
  the new stack, not the old one.

  ### What the feature does (VOX-2622, "Voice / Integrations Tab")
  Streamlines CS voice onboarding. Two thrusts:
  1. Make the catch-all `forward_call_to` number an explicit REQUIRED voice input; the
     granular per-category `ForwardingConfig` (`VOICE_AI_OUTBOUND_FORWARDING_CONFIG`)
     becomes optional. Motivation: many hotels don't use front-desk as their default
     forwarding number, so deriving it implicitly was wrong.
     - Non-Wyndham: `forward_call_to` now mandatory.
     - Wyndham: left as-is, keeps deriving from the FRONT_DESK entry (already required).
       Connor Swords confirmed in-thread (Jun 1) that front_desk == forward_call_to always
       holds for Wyndhams, so the Wyndham carve-out is safe.
  2. Adminland "Voice Setup" modal (Integrations/Messaging tab) so an operator can enable
     voice for a hotel inline — surfacing missing/optional values with libphonenumber
     validation — WITHOUT a Salesforce onboarding-script run. The modal is a wrapper over
     the same config behavior; script behavior is meant to stay undisturbed.

  PRD: notion.so/canarytechnologies/PRD-Voice-Setup-Integrations-Tab-359814686151811ca425f923cb5dc685
  Demo looms: Wyndham https://www.loom.com/share/a7c8c27106c74210a4f59c8a6ad246c6 ·
  non-Wyndham https://www.loom.com/share/06a2a090871f49aaafeb0d81d3efae84

  ### Your Jun-2 feedback (from the thread) and whether the rework addresses it
  You raised three architecture points on the OLD stack:
  - (a) Refactor pulls voice-specific logic into the onboarding-values service. — bad coupling
  - (b) Config providers shouldn't need a common voice-config-provider base class; should
        work through `VoiceAIConfig`.
  - (c) Using onboarding scripts to run tasks for hotel staff is far from their intent. Hoist
        voice logic out of `ConfigureVoicePlan` into a service callable from BOTH
        `ConfigureVoicePlan` and the adminland endpoints.

  The new PR #47421 ("Decouple voice config from onboarding + adminland voice setup") claims
  to do exactly this:
  - (a) → "no OnboardingValues; the OnboardingValue-driven missing-values machinery is removed."
  - (b) → `VoiceAIConfig` + Default/Wyndham variants with a pure `build(...)`; providers become
          "thin shims calling <Variant>.build." No base class.
  - (c) → `VoiceActivationService.activate(hotel, config)` extracted from `ConfigureVoicePlan`;
          `ConfigureVoicePlan` now delegates to the service; adminland calls the same service.
  Net: the rework looks like a faithful response to all three points. Worth a re-review of
  47421 specifically to confirm the decoupling is clean (it's large: +2375/-1304, 40 files).

  ### The two stacks (all OPEN as of this run)
  NEW (review this — supersedes old):
  - 46727  migration: add VOICE_AI_FORWARD_CALL_TO kind (draft; ⚠️ DB migration, coordinate)
  - 47408  require forward_call_to as onboarding value (draft, +618/-70, 18 files)
  - 47420  extract shared ForwardNumbers.vue component (draft, +534/-212, 5 files)
  - 47421  decouple voice config from onboarding + adminland voice setup (draft, +2375/-1304, 40f) ← the big one
  - 47422  typed per-variant VoiceSetupModal — Default vs Wyndham forms (draft, +907/-2, 7 files)

  OLD (the Slack thread links these; now superseded):
  - 46600 forward_call_to required value · 46601 shared ForwardNumbers · 46602 per-hotel
    missing values + schema registry · 46603 voice_setup service + status/activate endpoints ·
    46604 adminland VoiceSetupModal. (46599 / VOX-2562 strict E.164 validation is standalone.)

  ### Open questions / things to verify on re-review
  - 47421 is the crux and is large — confirm `VoiceActivationService` is genuinely the single
    shared path (no residual voice logic left in ConfigureVoicePlan or onboarding-values).
  - Wyndham parity: confirm the activated config via the new adminland path produces the same
    Configuration as the script path (47421 mentions a `voice_wiring`/drift test; check it
    covers Wyndham).
  - Migration 46727 needs merge-coordination (DB). New stack re-bases on master rather than the
    chained-branch approach of the old stack.
  - Andrea Bradshaw asked (Jun 1) whether ENT/Wyndham impact needs a walk-through with Connor &
    Ani — Connor confirmed the front_desk rule; no further ENT sign-off recorded in-thread.

  Nothing here required an external write; no comments posted. This is a read-only briefing.

  ## Agent run 2026-06-09T12:40Z — /review-pr (5 specialized agents, read-only)

  Reviewed the new stack (46727 / 47408 / 47420 / 47421 / 47422). Nothing posted to GitHub.
  Headline: the rework genuinely delivers your three feedback points (a) no onboarding-values
  coupling, (b) no provider base class / works through VoiceAIConfig, (c) activation hoisted
  into a shared VoiceActivationService called by both paths — code-reviewer + type-analyzer
  verified the import graph and the deleted base class. BUT the new adminland activation
  boundary has serious, independently-corroborated safety gaps the old 46603 stack guarded
  and this rework DROPPED.

  ### CRITICAL (block merge)
  - C1 Irreversible Twilio purchase inside a rollback-able transaction. voice_setup.py:~128
    wraps VoiceActivationService.activate in transaction.atomic(), but
    voice_activation.py::_provision_voice_number -> twilio_voice_configuration.py
    buy_voice_number_if_necessary makes a billable, non-transactional Twilio purchase inside
    it. Any later failure (LiveKit/geocode/forward-number IntegrityError) rolls back the DB but
    not the purchase -> orphaned paid number; the Configuration row that recorded it is gone.
  - C2 No re-POST / concurrency guard on activate. activate_voice_for_hotel never re-checks
    is_configured and takes no select_for_update lock — can_activate is computed only in the
    STATUS endpoint (advisory, separate request). Double-click / concurrent POST re-runs the
    Twilio buy + create_forward_numbers + LiveKit + WhatsApp dispatch -> second number bought,
    duplicate forward rows, last-writer-wins, both requests return success. Two agents flagged
    independently. This is the fail-fast/lock guarantee the old 46603 stack had; rework regressed it.
  - C3 Duplicate/conflicting migration. 47408 adds 0149_alter_onboardingvalue_kind AND edits
    onboarding_values.py to add VOICE_AI_FORWARD_CALL_TO; 46727 adds 0146 + the IDENTICAL model
    edit. Both landing => textual conflict + two AlterFields on `kind`. 47408 should depend on
    46727, or close 46727.
  - C4 (frontend) en.json deletes two in-use keys segmentConditions.groupCodeHelper.exists /
    .notExists, still referenced at useSegmentConditions.ts:660,663. Unrelated — bad rebase. Restore.

  ### IMPORTANT
  - Twilio configure errors (MissingTwilioSubAccountError, PhoneNumberNotFoundError) not in the
    translated catch sets -> generic 500 in adminland (not the 422 the frontend expects),
    untranslated in script path. Make them VoiceActivationError subclasses or add to both catches.
  - voice_wiring drift test under-covers: pins only one of two Wyndham wirings
    (property_configuration_processes.py:559-560 AND 1102-1103); doesn't tie portfolio->onboarding_type.
  - _enable_livekit_for_hotel broad `except Exception` collapses programming bugs (AttributeError)
    and transient outages into one non-retryable LiveKitConfigurationFailed — Sentry can't distinguish.
  - Wyndham field-error remap: forwarding_configuration and forward_call_to map to the same form
    key in a dict comprehension; one error message silently clobbers the other.
  - ForwardNumberSpecData anemic: no validation mirroring ForwardNumber.clean (CUSTOM requires
    display_name/description; missing sip_address). Invalid specs pass validate_forwarding_specs and
    blow up at save() AFTER the Twilio number is bought.
  - on_commit WhatsApp dispatch is caller-dependent — safe today (both callers atomic) but fires
    immediately if activate is ever called non-atomically. Assert connection.in_atomic_block or self-wrap.
  - i18n regression (frontend): Call Settings strings, previously localized in ForwardNumbersLegacy.vue,
    now hardcoded English in shared ForwardNumbers.vue + VoiceSetupModal.vue.
  - Test gaps that let a real regression ship: rollback boundary (partial writes after LiveKit
    failure), re-POST/duplicate activation, on_commit under the real transaction wrapper, and
    script-path vs adminland PARITY (equivalent inputs -> field-for-field equal configs, esp. Wyndham
    front-desk derivation) — all untested.

  ### SUGGESTIONS
  - Default/Wyndham subclasses are no-field factory buckets; `is WyndhamVoiceAIConfig` switching at
    3 sites makes polymorphism decorative. Prefer separate *Inputs types -> one VoiceAIConfig, or at
    least move Wyndham invariants into __post_init__ (currently only enforced in build(), bypassable
    by direct construction).
  - _to_specs reports only the first bad forwarding category, short-circuiting the accumulate model.
  - Frontend activate uses raw axios.post instead of a Bridge ActivateVoiceSetup action.

  ### VERIFIED CLEAN
  Decoupling (a)(b)(c) achieved; VoiceAIConfig.__post_init__ accumulates AND raises per-field errors;
  ConfigureVoicePlan error translation lossless for handled categories; pms_config_schemas split is a
  legit cycle break; Wyndham forward_call_to-from-FRONT_DESK preserved; Call Settings behavior preserved;
  frontend error handling loud (no swallowed activation errors); country_code (not free-text country) used.

  ### CAVEAT
  C1/C2 specifics came mainly from the silent-failure agent's read of twilio_voice_configuration.py;
  duplicate-activation (C2) corroborated separately by the test agent. Concrete with file:line, but worth
  Gaston confirming the exact transaction boundary before framing as definitive. The MISSING
  already-configured/lock guard is unambiguous regardless.

  Follow-up offered (not yet done): draft review comments for 47421 for your approval before posting.
project: null
source_id: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1780081180659859?thread_ts=1780081180.659859&cid=C047K6WSUJY
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 15
title: 'Read: voice onboarding streamlining PRD + PR stack (Gaston)'
updated: 2026-06-10 14:49:19.619715
waiting_on: null
waiting_since: null
working_on: false
---

PRD + demo looms (wyndham/non-wyndham) + backend 46600/46602/46603, frontend 46601/46604. https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1780081180659859?thread_ts=1780081180.659859&cid=C047K6WSUJY