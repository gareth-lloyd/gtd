---
area: null
contexts: []
created: 2026-06-10 15:31:37.594071
defer_until: null
due: null
energy: low
id: 2026-06-10T1531-review-gaston-s-new-prs
order: null
output: |
  ## Agent run 2026-06-10T15:42:44+0300

  Reviewed Gaston's two PRs from the Slack DM (VOX-2622 stack). Review-only; nothing
  posted to GitHub/Slack/Linear. Ran pr-review-toolkit agents (code review, test
  coverage, silent-failure hunt) against the remote branches and hand-verified the
  load-bearing findings.

  ### PR #47481 — VOICE_AI_FORWARD_CALL_TO enum + migration
  Clean, approve-ready. Enum + KIND_TYPES(str) + ID_TYPE(SALESFORCE_ACCOUNT_ID) +
  agent_context EXCLUDED list + no-op migration (choices-only AlterField, CI SQL
  confirms no DDL). The earlier triage-test CI failure is fixed on head; checks green.

  ### PR #47408 — require forward_call_to, demote forwarding list to optional
  Good shape overall (Wyndham path is safe — its provider derives forward_call_to
  from FRONT_DESK and has its own error). Three things worth raising before approving:

  1. REAL BUG (cheap fix): in OnboardingValueService.upsert the new
     `assert isinstance(data, list)` + normalize runs BEFORE validate_data, so a
     wrong-typed payload (e.g. CSV import path passes raw strings) now raises a
     bare AssertionError instead of the curated ValueError; under `python -O` a
     str would be char-split into a list and stored corrupted. Fix: run
     validate_data first, drop the assert.
  2. STALE COHORT READINESS LISTS (verified on head): cohort_hotel.py
     DEFAULT_REQUIRED_ONBOARDING_VALUE_KINDS still requires the now-optional
     VOICE_AI_OUTBOUND_FORWARDING_CONFIG, and VOICE_AI_FORWARD_CALL_TO — now the
     hard requirement — is missing from both required list and
     ONBOARDING_VALUE_KIND_ORDER (so it's filtered out of the response even when
     set; the new frontend label is dead in that view). Operator sees "ready",
     plan fails with missing_forward_call_to. Not fixed in follow-up #47421 either
     — ask Gaston whether adminland voice setup replaces this flow or the lists
     need updating in this PR.
  3. VALIDATION WINDOW (Gaston already flagged): forward_call_to is truthiness-
     checked only; enable() does save() without full_clean(), so a garbage string
     reaches live telephony (LiveKit default/fatal-error transfer destination) and
     fails on a guest call; >18 chars = raw DataError mid-plan after Twilio side
     effects. Follow-up draft #47421 does add validate_e164_phone + registered-
     schema write validation, so this closes — but suggest either merging #47421
     promptly behind it or adding the 3-line format_strict_e164 guard in
     ConfigureVoicePlan.execute now (validator already imported in that file).

  Minor: review-bot failing on #47408 — 4 new @patch decorators in
  test_configure_voice_plan.py lack autospec/spec (lines ~819-820, ~846-847);
  test_validate_data__forwarding_config__accepts_value_form_category is vacuous
  (validate_data only checks isinstance list for this kind); normalize docstring
  claims "validation flags them" but no write-boundary validation exists until
  #47421; comment-rot nits ("the decouple PR", unnamed design doc). Old error code
  missing_forwarding_config fully removed in-repo (worth a 2-min check for
  out-of-repo monitors/runbooks string-matching it).

  Strengths worth saying in review: clean migration/behavior split, thorough
  behavior-first tests (missing/only/both combinations at provider + plan level),
  TOnboardingValueData coverage meta-test, actionable admin hint on the new error.

  Suggested next action: reply to Gaston — approve #47481; for #47408 request the
  validate-before-normalize fix + autospec lint, and ask about the cohort
  readiness lists and #47421 merge ordering. Draft review comments available on
  request (not posted anywhere).
project: null
source_id: null
tags: []
time_minutes: 5
title: Review gaston's new prs
updated: 2026-06-10 15:43:30
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/D0ARTEGEE6R/p1781035616025979