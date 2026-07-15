---
area: null
contexts:
- react
created: 2026-07-15 11:36:23.495412
defer_until: null
due: null
energy: medium
id: 2026-07-15T1136-triage-ent-6865-ent-6868-wyndham-tally-parse-error
order: null
output: |-
  ## Agent run 2026-07-15T11:10:58Z

  Triaged both alerts via Groundcover logs + codebase. Both are benign auto-resolved blips; neither indicates an ongoing Tally outage. No writes made to Linear — recommendations below are drafts for you to act on.

  ### ENT-6865 — us-west-2 parse errors (https://linear.app/canary-technologies/issue/ENT-6865/groundcover-wyndham-tally-api-unstructuredparse-errors-production-us)
  - Exactly ONE `tally.api_error.parse_failed` event in the last 3 days: 2026-07-14T16:46:15Z, hotel wyndham-60549. Tally returned an HTML "503 Service Temporarily Unavailable" page instead of JSON — a momentary Tally-side outage/proxy blip. Monitor fired 16:49Z, auto-resolved, zero recurrence since.
  - Impact: one guest enrollment marked FAILED (check-in ACD9HDMUKQ, reservation 6AXPBECH55, conf 6600423). `enroll_guest_in_membership` task has no retry (backend/canary/check_in/tasks/enroll_guest_in_membership.py), so it was never retried.
  - Recommendation: close as transient vendor blip. Optionally re-trigger enrollment for that single check-in.

  ### ENT-6868 — eu-central-1 enrollment error rate >= 10% (https://linear.app/canary-technologies/issue/ENT-6868/groundcover-wyndham-tally-enrollment-error-rate-10percent-production)
  - Known-noisy monitor on tiny EU overnight volume: in the hour before the 01:40Z alert there were only ~4 enrollment attempts, 2 errors -> 50% "rate". This is the SAME alert previously closed as noise: ENT-6803 ("noise due to low traffic. Only 11 errors in last 3 days" — Lautaro Mena, https://linear.app/canary-technologies/issue/ENT-6803/groundcover-unnamed-alert) and ENT-6854 ("Noise", https://linear.app/canary-technologies/issue/ENT-6854/groundcover-wyndham-tally-enrollment-error-rate-10percent-production). Standing backlog ticket ENT-6538 exists to tune/fix the monitor (https://linear.app/canary-technologies/issue/ENT-6538/investigate-recurring-alert-wyndham-tally-enrollment-error-rate).
  - The underlying errors are real but low-volume and data-quality-driven: Tally rejects enrollment with HTTP 400 code 0001 "size must be between 1 and 100" on `firstName` — we send an EMPTY first name. Root cause: backend/canary/check_in/services/check_in_membership.py:137 `first_name = reg_card_extracted_tag_values.first_name or primary_guest.first_name or ""` falls back to "" which Tally rejects. 14 occurrences across regions in last 2 days (5 EU, 9 US; hotels wyndham-54065/-60491/-59567/-55284 in EU), plus 1 `emailAddress` "Invalid format" in US. Each one = a guest who requested enrollment and silently didn't get it (check-in marked FAILED, no retry).
  - Recommendations:
    1. Close ENT-6868 as noise, same as ENT-6803/ENT-6854.
    2. Real monitor fix belongs on ENT-6538: add a minimum-attempts floor to the rate denominator (e.g. only alert when attempts >= 20 in window) so EU overnight volume can't trip it.
    3. Optional real fix for the residual errors: pre-validate first name before calling Tally (skip + distinct log event when empty), which would eliminate most non-duplicate Tally 400s and make this monitor meaningful.

  Side observations (no action needed): 85 `enroll_guest_in_membership.error` events in EU over 2 days are dominated by "Hotel is not configured for membership enrollment" from IHG-org hotels (indigo-london-k-west, ihg-manap, voco-oxford-*, etc., sso_org 235) plus wyndham-49448 — these are config-state warnings, not Tally API errors, and are excluded from the monitor.
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-6868/groundcover-wyndham-tally-enrollment-error-rate-10percent-production
tags:
- morning-gtd
- linear
- from-awareness
time_minutes: 20
title: 'Triage ENT-6865/ENT-6868: Wyndham Tally parse-error + enrollment-error alerts'
updated: 2026-07-15 14:10:58.013149
waiting_on: null
waiting_since: null
working_on: false
---

Groundcover alerts auto-resolved (us-west-2 parse errors; eu-central-1 enrollment error rate ≥10%) but flagged as possibly needing human investigation.
https://linear.app/canary-technologies/issue/ENT-6868/groundcover-wyndham-tally-enrollment-error-rate-10percent-production
https://linear.app/canary-technologies/issue/ENT-6865/groundcover-wyndham-tally-api-unstructuredparse-errors-production-us