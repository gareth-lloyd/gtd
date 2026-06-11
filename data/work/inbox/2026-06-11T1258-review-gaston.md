---
area: null
contexts: []
created: 2026-06-11 12:58:05.558897
defer_until: null
due: 2026-06-11
energy: low
id: 2026-06-11T1258-review-gaston
order: null
output: |
  ## Agent run 2026-06-11T10:04:47Z

  Gaston's Slack DM (https://canarytechnologies.slack.com/archives/D0ARTEGEE6R/p1781138901891019)
  points at PR #47421 "VOX-2622: Decouple voice config from onboarding + adminland voice setup"
  (https://github.com/canary-technologies-corp/canary/pull/47421) — 41 files, +2683/−1267,
  stacked on `gdelarrechea/vox-2622/forward-call-to-required`. Reviewed at head fdc2df94693
  with 4 review agents (code, silent-failures, tests, type design). NOTHING was posted to
  GitHub — findings below are for you to relay/post.

  ### Verdict
  Solid architecture: one self-validating VoiceAIConfig built by a pure build(), shared by the
  onboarding script and the new adminland path; import-cycle decoupling claim verified (no
  voice/ → onboarding imports); the ~900-line test deletion in test_configure_voice_plan.py is
  a genuine relocation, not dropped coverage. Two blocking issues before merge.

  ### Blocking
  1. **No server-side re-activation guard** — voice/services/voice_setup.py
     `activate_voice_for_hotel` never checks `can_activate`; the status endpoint computes it
     client-side only. `VoiceConfigurationService.enable` is an upsert that RESETS tuned fields
     (tts_voice_id, excluded_abilities=[], welcome_message_template, pickup_delay…). A
     double-click/retry/race on an already-configured hotel silently clobbers months of
     hand-tuning, re-runs Twilio provisioning, and returns 200. Fix: raise VoiceSetupError
     (422) at top of activate when hotel already has voice_configuration; add a test.
  2. **CUSTOM forward-number rows can 500 after a Twilio purchase** —
     `validate_forwarding_specs` checks only E.164 + duplicate categories, but
     ForwardNumber.clean() requires display_name+description for CUSTOM (and forbids them
     otherwise). A CUSTOM row with empty display_name passes config build, then full_clean()
     raises Django ValidationError inside the atomic block — not caught by the
     `except (VoiceActivationError, MissingHotelLocationError)` clause → 500, DB rolls back,
     but the purchased Twilio number is orphaned. Fix: enforce CUSTOM rules in
     validate_forwarding_specs (or map ValidationError to 422).

  ### Important (should fix)
  - **Partial external side effects on rollback**: Twilio number purchase + LiveKit trunk
    creation happen inside transaction.atomic(); late failure rolls back DB but leaves the
    purchased number/half-created trunk orphaned, and the LiveKit trunk ID saved on the
    rolled-back row is lost. Pre-existing shape in the script path, but now operator-triggered
    and retried — at minimum log loudly which external steps completed before rollback.
  - **VoiceActivationError.context dropped**: voice_setup.py re-raises as
    `VoiceSetupError(reason=str(e))` — operator gets "Failed to configure LiveKit integration."
    with no context; MembershipKindNotFound/Twilio cases aren't logged on this path at all.
  - **Validated-but-unnormalized phone numbers persisted**: validate_e164_phone discards the
    formatted result, so "+1 202 555 0143" passes and is stored verbatim in forward_call_to /
    ForwardNumber.to_number / voice_number — the exact whitespace-in-phone class that has
    broken Twilio lookups before. Validator should return the normalized value and build()
    should store it.
  - **Wyndham field-error remap drops messages**: `_to_form_field_errors` maps both
    forwarding_configuration and forward_call_to → forward_numbers via dict comprehension;
    when both error, one message silently lost (last-wins). Also `_to_specs` aborts on first
    bad category, so multi-row errors surface one submit at a time.
  - **Audit event dispatch after the atomic block**: if EventService.dispatch_event raises,
    activation has committed but the view 500s — operator retry then hits issue #1.
  - **Lost integration test**: old test_execute__with_wyndham_config_provider__uses_config_values
    verified config→Configuration field mapping AND ForwardNumber row creation; no new test
    does — every activation test uses forwarding_configuration=[] (only asserts count()==0).
    If _apply_post_enable_configuration stopped creating forward numbers, all tests pass.
    Also missing: permission-denied (403) test on the activate endpoint (the only mutating
    one has no auth test), double-activation test, MissingHotelLocationError activation path.

  ### Suggestions
  - VoiceAIConfig is frozen but shallowly: forwarding_configuration is a list of mutable
    ForwardNumberSpecData — use tuple + freeze the spec dataclass. Wyndham brand-policy
    invariants (FRONT_DESK required, upsell override) live in build() not __post_init__, so
    dataclasses.replace() can produce a WyndhamVoiceAIConfig violating its own rules.
  - normalize_data/validate_data pairing enforced only by convention at 3 call sites —
    consider one normalize_and_validate entry point. Also confirm pre-existing stored
    OnboardingValue rows with VALUE-form categories don't blow up at script time (read-path
    normalization gap) — is a backfill part of the PR series?
  - DynamicSphValuesSchema uses deprecated `missing=` and loads None into non-optional
    str fields; view DCs' `status: str  # always "success"` should be Literal.
  - validate_with_registered_schema silently skips non-list/non-dict data (no else branch).

  ### Strengths worth telling Gaston
  Pure build() shared by both paths; __post_init__ invariant gate; the voice_wiring drift
  test tying portfolio variant selection to onboarding wiring is the standout test of the PR;
  WhatsApp dispatch correctly moved to transaction.on_commit with proper capture-on-commit
  tests; error catalog entries (ERROR_INVALID_FORWARD_CALL_TO etc.) have genuinely actionable
  WHAT_TO_DO text; 422 wire contract pinned by tests.

  Next step is yours: relay to Gaston in Slack / post on the PR (I drafted nothing externally;
  happy to draft a PR review comment or Slack reply on request).
project: null
source_id: null
tags: []
time_minutes: 5
title: review gaston
updated: 2026-06-11 13:04:47.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/D0ARTEGEE6R/p1781138901891019