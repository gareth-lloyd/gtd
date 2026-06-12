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
  ## Agent run 2026-06-11T10:04:47Z (filtered 2026-06-11T10:12Z for arch/enterprise-onboarding lens)

  Gaston's Slack DM (https://canarytechnologies.slack.com/archives/D0ARTEGEE6R/p1781138901891019)
  points at PR #47421 "VOX-2622: Decouple voice config from onboarding + adminland voice setup"
  (https://github.com/canary-technologies-corp/canary/pull/47421) — 41 files, stacked PR.
  Reviewed at head fdc2df94693 with 4 review agents; nothing posted to GitHub. Filtered to
  what matters for a secondary reviewer flagging architecture + enterprise onboarding impact.

  ### Overall architecture: sound
  One self-validating VoiceAIConfig built by a pure build(), shared by the onboarding script
  and the new adminland path. Import direction is clean (voice/ no longer imports onboarding;
  providers became thin shims over voice core). The voice_wiring drift test ties adminland
  portfolio-based variant selection to ONBOARDING_TYPE_CONFIG, guarding the two paths from
  silently diverging per-brand. The ~900-line test deletion is genuine relocation.

  ### Flag 1 — onboarding scripts now fail earlier and harder (enterprise impact)
  Validation moved from plan execute-time to config build/construction time, and it's
  stricter: forward_call_to is now E.164-validated at provider __init__ (previously only
  presence-checked). Any existing OnboardingValue rows with malformed phone numbers or
  VALUE-form forwarding categories that previously slipped through will now fail provider
  construction during a script run. No backfill/audit in this PR. Ask Gaston: is a data
  audit or backfill part of the PR series? This directly touches script-driven enterprise
  rollouts (e.g. ENT-6032 IHG wave is onboarding-script based; Wyndham scripts).

  ### Flag 2 — server doesn't own the activation invariant (architectural)
  The status endpoint computes can_activate, but activate_voice_for_hotel never re-checks
  it: enable() is an upsert that resets tuned config fields, so a double-submit/retry on an
  already-configured (e.g. long-live enterprise) hotel silently reverts hand-tuned voice
  settings and returns 200. The invariant lives client-side only. Fix is cheap: 422 guard
  at top of activate. This is the one item worth insisting on as a blocker.

  ### Flag 3 — external provisioning inside transaction.atomic (architectural, now amplified)
  Twilio number purchase + LiveKit trunk creation run inside the DB transaction; a late
  failure rolls back the DB but orphans the paid number / half-created trunk (trunk ID saved
  on the rolled-back row is lost). Pre-existing shape in the script path, but adminland makes
  activation operator-triggered and retryable, so frequency and orphan accumulation go up.
  Minimum ask: loud structured logging of completed external steps on the rollback path.

  ### Secondary (mention, don't fight for)
  - normalize_data/validate_data pairing is convention-enforced at 3 call sites; one
    composite entry point would remove the footgun.
  - validate_e164_phone discards the normalized number, so whitespace-laden numbers persist
    verbatim — the known Twilio-breakage class.

  Everything else (CUSTOM-row 500 path, field-error remap collisions, test gaps incl. missing
  403 test on the activate endpoint) left to the prime reviewer; full detail available on
  request. Next step yours: relay flags 1-3 to Gaston / on the PR — I can draft either.

  ## Agent run 2026-06-11T13:21 — posted to GitHub (user-approved)
  Flags 2 and 3 posted as inline review comments (COMMENT, no verdict) on
  voice_setup.py:101 (no server-side re-activation guard) and voice_setup.py:132
  (external Twilio/LiveKit provisioning inside transaction.atomic):
  https://github.com/canary-technologies-corp/canary/pull/47421#pullrequestreview-4477027454
  Flag 1 (stricter build-time validation vs existing OnboardingValue data / backfill
  question) NOT posted — still open if worth raising with Gaston directly.
project: null
source_id: null
tags: []
time_minutes: 5
title: review gaston
updated: 2026-06-11 13:21:30.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/D0ARTEGEE6R/p1781138901891019