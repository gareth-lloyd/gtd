---
area: null
completed_at: null
contexts: []
created: 2026-08-04 12:06:07.984538
defer_until: null
due: null
energy: low
id: 2026-08-04T1206-pms-gateway-project-for-gdpr-take-a-look
order: null
output: |
  ## Agent run 2026-08-04T14:15

  The project is "GDPR: PMS data anonymisation" (https://linear.app/canary-technologies/project/gdpr-pms-data-anonymisation-4a24518aa6a7) — cross-team EMEA + Security + PMS Engineering, lead Yauheni Danchanka, status Implementation, target 2026-08-31, Q3 Block 1. It operationalises §5.2 (PMS Gateway) of the June PII audit: three failure modes — adoption (~99% of accounts on a no-op "Default (none)" policy, ~71M guests never anonymised), coverage (stores never obfuscated), retention (no cleanup for OperationLog, ArrivalReportFile, Protel async-action tables).

  ### Work ahead (open issues, all High unless noted)

  In progress (Yauheni, current cycle):
  - PMS-9792 Deprecate PMS Scrapers (https://linear.app/canary-technologies/issue/PMS-9792) — plaintext passwords, hardcoded admin creds, guest-PII console dumps; removing the whole attack surface
  - PMS-9783 Understand the project scope (https://linear.app/canary-technologies/issue/PMS-9783) — empty description; Yauheni's orientation ticket

  Todo — a fresh batch carved out 2026-08-03, looks like the concrete implementation plan:
  - PMS-9837 [Cleanup] GDPR Policy framework: one policy driving redaction and retention (https://linear.app/canary-technologies/issue/PMS-9837)
  - PMS-9838 [Cleanup] Protel: orphaned SOAP responses and async-action payloads (https://linear.app/canary-technologies/issue/PMS-9838)
  - PMS-9839 [Cleanup] Arrival reports: database PII stores (https://linear.app/canary-technologies/issue/PMS-9839)
  - PMS-9840 [Cleanup] Arrival reports: S3 copies and bucket lifecycles (https://linear.app/canary-technologies/issue/PMS-9840)
  - PMS-9841 [Cleanup] OperationLog retention and S3 offload lifecycle (https://linear.app/canary-technologies/issue/PMS-9841)
  - PMS-9834 Scheduled obfuscation never covers per-reservation GuestInformation (https://linear.app/canary-technologies/issue/PMS-9834)
  - PMS-9835 Identity documents, guest tags, loyalty numbers not obfuscatable (https://linear.app/canary-technologies/issue/PMS-9835)
  - PMS-9836 Obfuscation beat has no heartbeat monitoring (https://linear.app/canary-technologies/issue/PMS-9836)
  - PMS-9830 Delete PMS Scrapers AWS resources — manual, not IaC-managed (https://linear.app/canary-technologies/issue/PMS-9830)

  Backlog (correctness/design questions, not yet scheduled):
  - PMS-9787 PMS syncs re-introduce PII on obfuscated guests — bug (https://linear.app/canary-technologies/issue/PMS-9787)
  - PMS-9788 Obfuscation records retain a re-identification key (https://linear.app/canary-technologies/issue/PMS-9788)
  - PMS-9790 Find & obfuscate historical records (https://linear.app/canary-technologies/issue/PMS-9790)
  - PMS-9791 Un-obfuscate guest when a new future reservation arrives (https://linear.app/canary-technologies/issue/PMS-9791)
  - PMS-9793 [Eng design] National/International guest policies (https://linear.app/canary-technologies/issue/PMS-9793)
  - PMS-9802 Check-in ingestion ignores obfuscation — bug, Medium (https://linear.app/canary-technologies/issue/PMS-9802)

  ### Things worth knowing

  - EMEA-350 "Country-based default retention" — the headline Gap-1 fix (migrate ~71M guests off the no-op via the Enterprise ConfigurationRuleEngine) — was MOVED OUT of this project into "GDPR: Anonymisation schedule - configurable by property" and sits in "To Refine". Its git branch is glloyd/emea-350-gdpr-country-based-default-retention — i.e. it appears to be pointed at you. (https://linear.app/canary-technologies/issue/EMEA-350)
  - EMEA-350 carries a rollout precondition: the Snowflake PII deletion job hard-codes lag = 7 days (gdpr/services/snowflake_deletion.py:72), so any other default window gets no warehouse cleanup; same hard-coding in Opera fetch exclusion. Sequencing interacts with PMS-9787's commit-layer lock.
  - Old umbrella tickets EMEA-348/349, PMS-9789, SEC-382, EMEA-305 (Track 2A purge-after-sync, Danubius-specific) are all canceled — superseded by the PMS-98xx breakdown above. Eng design EMEA-307 is Done.
  - Project has no milestones and no status updates posted yet.
  - Forcing functions: Danubius (€80k + ~€500k Ensana upside) and IHG.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: PMS gateway/EMEA team Linear project for GDPR. Look through the work ahead
updated: 2026-08-05 14:34:17.010008
waiting_on: null
waiting_since: null
working_on: false
---