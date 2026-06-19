---
area: null
contexts: []
created: 2026-06-17 20:29:01.474305
defer_until: null
due: null
energy: low
id: 2026-06-17T2029-review-gaston-s-sequence
order: null
output: |
  ## Agent run 2026-06-18T05:24

  Reviewed Gaston's execution of the 6-PR split you proposed in the Slack thread
  (https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1781717299013149?thread_ts=1781533255.750639).
  He had Claude perform the split + verify. Original PR: #47421
  (https://github.com/canary-technologies-corp/canary/pull/47421).

  ### Bottom line
  The split is faithful and complete. The six PRs form a correct linear stack
  (each based on the previous), the scope of each matches your plan, and the line
  totals almost exactly reconstruct the original diff:
  - sum of additions 177+263+534+997+116+1149 = 3236 vs original 3235
  - sum of deletions 119+48+9+1083+1+10 = 1270 vs original 1269
  That ~1-line delta is strong evidence nothing was dropped or invented.
  Most of the embedded fixes you asked for landed. But three of the fold-in fixes
  are missing or partial, and PR-1 is not green standalone. Details below.

  ### PRs (stack order)
  - #48227 (1/6) https://github.com/canary-technologies-corp/canary/pull/48227 — schema-module move
  - #48228 (2/6) https://github.com/canary-technologies-corp/canary/pull/48228 — centralize OnboardingValue validate
  - #48229 (3/6) https://github.com/canary-technologies-corp/canary/pull/48229 — VoiceAIConfig core + drift test
  - #48230 (4/6) https://github.com/canary-technologies-corp/canary/pull/48230 — VoiceActivationService cutover
  - #48231 (5/6) https://github.com/canary-technologies-corp/canary/pull/48231 — support-access predicate
  - #48232 (6/6) https://github.com/canary-technologies-corp/canary/pull/48232 — adminland Voice Setup feature

  ### Issues to raise before these merge

  1. **M1 fix is missing (PR-2 / #48228).** You asked to fold in "guard/log the
     silent-skip for scalar kinds." The new `validate_with_registered_schema()`
     still does `if expected_type is bool: return` with no log/guard — bool/scalar
     kinds are silently skipped exactly as before. This was the one behavior fix
     this PR was supposed to carry, and it didn't land.
     (onboarding/services/onboarding_value_schemas.py — the bool early-return.)

  2. **H1 fix is only half-done (PR-4 / #48230).** The domain exceptions now pass
     structured context instead of a flattened bare string (good), e.g.
     `raise TwilioSubAccountCreationFailed("...", context=str(e))`, but none of them
     use `raise ... from e`. So `__cause__`/the original traceback is lost — which
     was the explicit ask. Same at NoAvailableVoiceNumbers and
     LiveKitConfigurationFailed. (voice/services/configuration/voice_activation.py.)

  3. **PR-1 (#48227) is not green on its own.** `onboarding/tests/services/test_values.py:173`
     does a local `from onboarding.admin.onboarding_value import BoolFlagSchema`.
     PR-1 moves BoolFlagSchema out of the admin module and — unlike pms_config.py —
     leaves NO re-export shim in admin, so that import only gets fixed in PR-2.
     PR-1's CI will hit a failing test. Each stacked PR should be independently
     green; either add a re-export shim for the moved schema symbols in
     onboarding/admin/onboarding_value.py, or pull the test-import fix back into PR-1.

  4. **Minor scope bleed PR-1 → PR-2.** `validate_with_registered_schema()` is new
     logic your plan assigned to PR-2, but it actually landed in PR-1. Harmless
     (additive, unused until PR-2) but it means PR-1 isn't strictly "100% moved
     lines." Worth a one-line note, not a blocker.

  ### What's good (verified, not just claimed)
  - PR-1 pms_config.py keeps a proper re-export shim (DynamicOhip/Sph + service +
    WYNDHAM_SPH_CREDENTIALS_IDENTIFIER); all real importers stay green.
  - PR-3: VoiceAIConfig is `frozen=True` and self-validates in `__post_init__`;
    brand policy is isolated in the Wyndham variant's `build()` (not the generic
    `__post_init__`); validate_forwarding_specs docstring fixed; and the DRIFT TEST
    exists (test_voice_wiring.py, TestVoiceConfigClsMatchesOnboardingWiring) and
    genuinely cross-checks adminland selection vs the onboarding script wiring.
  - PR-4: H2 fix present — orphan-resource log includes `livekit_trunk_id` (and
    dispatch_rule_id); Twilio-subaccount exception wrapping present; plan is now thin.
  - PR-5: predicate is correct and secure — filters `status=ACTIVE` AND `ends_at__gt=now`
    (timezone-aware, exclusive bound, defensive against un-swept rows), hotel-scoped;
    tests cover active/expired/revoked/wrong-hotel/legacy-period/plain-user.
  - PR-6: activation gates on `has_temporary_support_access` at both view and
    service layers; race guard is an advisory `lock_instance(hotel)` + in-transaction
    re-check of `Configuration.objects.filter(hotel=...).exists()` (avoids pinning the
    row across Twilio/LiveKit calls); audit event emitted post-success; tests cover
    gating, the double-submit race, validation, and happy path.

  ### Notes
  - Dependency nuance: your plan had PR-3 depend on PR-1 only; the stack puts PR-3
    on top of PR-2. Fine for a linear stack — just means 3 can't merge before 2.
  - Andrea's earlier comments were addressed per Gaston (his last thread message).

  Suggested reply to Gaston: approve the structure, but ask for (1) the M1 log/guard
  in #48228, (2) `raise ... from e` in #48230, and (3) make #48227 green standalone
  (shim or pull the test fix forward). I have NOT posted anything to Slack/GitHub —
  happy to draft a thread reply if you want.
project: null
source_id: null
tags: []
time_minutes: 5
title: review Gaston's sequence
updated: 2026-06-18 15:50:34.448229
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1781717299013149?thread_ts=1781533255.750639&cid=C047K6WSUJY