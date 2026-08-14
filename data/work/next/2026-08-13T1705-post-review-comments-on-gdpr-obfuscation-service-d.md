---
area: null
completed_at: null
contexts:
- craft
created: 2026-08-13 17:05:54.262064
defer_until: null
due: null
energy: medium
id: 2026-08-13T1705-post-review-comments-on-gdpr-obfuscation-service-d
order: null
output: ''
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 30
title: Post review comments on GDPR Obfuscation Service design doc before sealing
  approval
updated: 2026-08-14 06:57:18.647785
waiting_on: null
waiting_since: null
working_on: false
---

Doc: https://app.notion.com/p/canarytechnologies/Canary-GDPR-Obfuscation-Service-3a2814686151815ea78bc317e5a426a8
Ticket: EMEA-354. Status is already APPROVED in the Notion DB — these need to land before it's locked.

Nothing has been posted to Notion yet. Review drafted 2026-08-13.

## Blockers (change what gets built)

1. §6.2 recommends Option B (follow PMS Gateway only), whose own downside is no kiosk/authforms/chat/voice coverage. That contradicts §1, §3, §5, §7 and tickets EMEA-357/358/360/362, which all assume the scheduled sweep over all Canary PII. Likely a stale edit; should be Option A, or explicitly both (A for native PII, B as the mirror fast-path).
2. Toolkit home decided two ways: §6.1 + §11 Q2 say hoist to `shared` now; §7 v1 and the §4 code comment say Canary-local with shared as a follow-up. If shared wins, the CI shared-to-service import boundary work (registry, string keys, interfaces) has to be in v1 scope.
3. §6.4 conflates floor / ceiling / lock. Prose says legal floor, code comment says legal-minimum, dict is named `_PII_RETENTION_CEILING`, and prose elsewhere calls it `_PII_RETENTION`. GDPR usually caps retention (maximum) while FR/ES/IT police-registration law imposes minimums — opposite directions. Also `OverridePolicy.FINAL` (locked) contradicts the same paragraph calling `pii_retention_days` an override.
4. §10 says v1 ships a single turned-off default; §6.4 recommends a default active on every hotel. That is the difference between deleting production guest PII on night one and doing nothing.
5. Retention lookup keys on `hotel.country`, which is free text — verified `backend/canary/hotels/models/hotel.py:544` is `CharField(max_length=255)` with no choices, while `country_code` at line 514 has `choices=Country.choices`. A miss means no retention applied — silent compliance gap. Use `country_code`, and define the fallback for hotels where it is blank (it is `blank=True`); strictest floor plus an alert, never skip.

## Should fix

6. DSAR `get_subject_queryset` (§4) matches on `guest_name=subject.full_name` — one John Smith DSAR irreversibly erases every other John Smith in the region. Anchor on identity; name matches are dry-run candidates for human confirmation only.
7. `PiiPurgeStrategy.NONE` appears once, never explained — an unbounded-retention escape hatch that defeats the FINAL claim.
8. Downstream copies (Snowflake/warehouse, Kafka topics, S3 raw payloads, backups/PITR) are neither in scope nor in §10, yet §1 claims legally equivalent to deletion.
9. `event_event` (~1B rows/region) has no retention anchor; §6.5's no-index-needed argument relies on one existing.
10. Overlap with existing `security/services/identity_document_purge_service.py`, which already purges on `id_retention_days`. Does EMEA-356 replace it or run alongside?
11. §6.3 (full job record + state machine) vs §6.5 (small run-summary table) describe the audit artifact differently — name it once.
12. Open questions 1 and 3 have empty Decisions. Q3 (anonymising name/email breaks guest lookup) has no sign-off from voice/messaging.

## Nits

- §2 has idempotency inverted: `obfuscated_at IS NOT NULL` is done, not IS NULL.
- §9 labels both ticket rows EMEA-512; DSAR needs its own.
- Model is `CheckInConfiguration`, not `check_in.Configuration`.

§6.5's reasoning (per-row marker + run-summary table, rejecting both the polymorphic table and reservation-only anchoring) is the strongest part — leave it alone.