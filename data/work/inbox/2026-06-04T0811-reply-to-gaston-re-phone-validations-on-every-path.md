---
area: null
contexts:
- react
created: 2026-06-04 08:11:39.827273
defer_until: null
due: null
energy: low
id: 2026-06-04T0811-reply-to-gaston-re-phone-validations-on-every-path
order: null
output: |
  ## Agent run 2026-06-04T10:23:59Z

  ### Context reconstructed
  - Gaston's DM (Jun 3) is a reply to your "validation blast radius" note in the
    voice-setup-stack review (VOX-2622). You flagged that moving the schema checks
    into validate_data/upsert would make them run for *every* caller (CSV import,
    SF sync), not just admin. Gaston is pushing back: "do we not want them on every
    path? The initiative was partly motivated by hotels that ended up with invalid
    phone numbers... different PR but likely within scope."
  - The initiative = strict E.164 forwarding-number validation (VOX-2562 / PR #46599,
    "Strict E.164 phone validation on direct write paths"; consolidate commit
    2d93074624d). It swapped the regex-only PhoneNumberValidator for
    `format_strict_e164` (libphonenumber is_valid_number) with actionable reasons.

  ### Where strict validation runs TODAY (verified in code)
  Direct/interactive paths only — `format_strict_e164` appears in:
  - voice/services/forward_number.py `ForwardNumberService.update_by_category`
    (PATCH /api/voice/{slug}/configuration — the hotel/CS-facing voice config UI)
  - onboarding/plans/configure_voice_plan.py (plan pre-run)
  - the onboarding-values endpoint path (onboarding/views/onboarding_value.py)
  - (also notifications/* portfolio SMS block, unrelated)

  ### Where it does NOT run — the gap Gaston is pointing at
  Bulk/automated write paths bypass the strict check entirely:
  - onboarding/import_export_resources.py (CSV import)
  - Salesforce sync via configuration providers (default_voice_config_provider.py,
    wyndham_voice_ai_config_provider.py, etc.)
  - management commands (update_or_create_onboarding_values, prep_onboarding_values,
    replace_csv_column, the tmp/ import scripts) and Django admin
  Note: `OnboardingValueService.validate_data` is *type* validation only, not phone
  validation. Strict phone validation is NOT in the shared upsert() layer.

  ### My read / scope decision
  Gaston is right that it's in scope for the PROJECT, and right that it's a different
  PR. The bad numbers almost certainly entered via the bulk/automated paths (SF sync,
  CSV, scripts) — exactly the paths that still don't validate — so direct-path
  validation alone doesn't close the hole that motivated the work. BUT: same intent
  on every path, different enforcement per path. Hard-failing a whole SF sync / CSV
  batch on one bad row (e.g. by dropping format_strict_e164 into upsert()) turns a
  data-quality issue into an onboarding-blocking incident with no user present to fix
  it — that's the blast-radius concern, and it's the wrong rollout.
  Recommendation:
  1. Land the current stack as-is (strict hard-reject on the direct/interactive paths).
  2. Separate ticket: validate on bulk paths (CSV import + SF sync) with PER-RECORD
     skip/quarantine + reporting, NOT batch-abort. Keep it out of upsert().
  3. Separate one-off audit/backfill: validation going forward won't fix hotels that
     ALREADY have invalid numbers (the motivating cohort). Query to find + remediate.

  ### DRAFT reply to Gaston (NOT sent — awaiting Gareth's approval)
  > Yeah, agreed — we do want invalid numbers caught on every ingestion path, and
  > you're right that's the heart of the initiative. The nuance is *how* each path
  > enforces it:
  >
  > • Direct/interactive paths (voice config tab, the onboarding-values endpoint, the
  >   plan pre-run) — hard reject with the libphonenumber reason; a human's there to
  >   fix it. That's what VOX-2562 already does and where it should stay.
  > • Bulk/automated paths (CSV import, SF sync, the management commands) — these are
  >   almost certainly where the existing bad numbers came in, so they're the ones
  >   that actually matter for the original problem. But we can't hard-fail a whole
  >   batch/sync on one bad row — no user to correct it, and it'd turn a data-quality
  >   issue into an onboarding-blocking incident. Those need per-record handling:
  >   validate, skip/quarantine the bad record, surface it (report/log), not abort.
  >
  > So same intent everywhere, different enforcement — which is exactly why I'd keep
  > it out of OnboardingValueService.upsert() (dropping the strict check into the
  > shared low-level write is the version that blows up SF sync mid-batch) and do it
  > as its own PR with the per-record design.
  >
  > Two follow-ups worth a ticket:
  > 1. Strict validation on the bulk paths (CSV + SF sync) with per-record skip +
  >    reporting.
  > 2. A one-off audit/backfill — validation going forward won't fix the hotels that
  >    *already* have invalid numbers, and those are the ones that motivated this.
  >
  > So: land the current stack as-is, and spin the bulk-path validation into a
  > separate ticket — you called it, different PR, in scope for the project.

  ### Handoff
  Reply is drafted only. I have NOT sent anything to Slack. Review/edit the draft,
  then send it yourself (or tell me "send it" to post to D0ARTEGEE6R). If you want,
  I can also file the two follow-up tickets once you approve the scope.
project: null
source_id: https://canarytechnologies.slack.com/archives/D0ARTEGEE6R/p1780500410873219
tags:
- morning-gtd
- slack
time_minutes: 10
title: 'Reply to Gaston re: phone validations on every path'
updated: 2026-06-04 10:23:59.088013
waiting_on: null
waiting_since: null
working_on: false
---

DM (Jun 3): 'do we not want them on every path? The initiative was partly motivated by hotels that ended up with invalid phone numbers. Might be a different PR now but likely within scope.' Decide scope + reply. https://canarytechnologies.slack.com/archives/D0ARTEGEE6R/p1780500410873219