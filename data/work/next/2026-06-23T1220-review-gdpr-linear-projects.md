---
area: management
contexts: []
created: 2026-06-23 12:20:44.842275
defer_until: null
due: 2026-06-23
energy: high
id: 2026-06-23T1220-review-gdpr-linear-projects
order: null
output: |
  ## Agent run 2026-06-24T13:05Z — Overview of work tracked in the GDPR projects

  All four projects sit under the **EMEA – Compliance & Data Privacy** initiative,
  inside the umbrella project **Deletion of all PII data**
  (https://linear.app/canary-technologies/project/deletion-of-all-pii-data-287fcf6516b1),
  all labelled "2026 Q3 Block 1", all currently in **Backlog** status, lead **Martijn Dekker**.
  Everything operationalises the **PII Storage Org-Wide Audit (2026-06-04)**
  (https://app.notion.com/p/3758146861518135add9eaed3bc2cda1) and the
  **WIP PRD: PII Minimisation & Retention — GDPR Compliance**
  (https://www.notion.so/canarytechnologies/WIP-PRD-PII-Minimisation-Retention-GDPR-Compliance-35d814686151815a96cfcf07ae7edc35).
  Forcing functions: Danubius (€80k + ~€500k Ensana upside) and IHG.

  Track map: **1A** = core-Canary anonymisation (PMS + Omnichannel), **1B** = downstream/
  third-party systems, **2A** = purge-after-PMS-sync (deferred). The shared mechanism is the
  PMS-Gateway `ObfuscationPolicy`/`ObfuscatableField` framework, being ported into the monolith
  in the separate **User input data** project under EMEA-354 (not one of the four below).

  ---

  ### 1. GDPR: Downstream systems anonymisation  (Track 1B — eng design DONE)
  https://linear.app/canary-technologies/project/gdpr-downstream-systems-anonymisation-c5110566cbb5/overview
  Teams: Security + EMEA · Priority High · Dates 2026-08-24 → 2026-09-13 · 13 issues.
  Scope: remediate guest PII OUTSIDE the core Canary DB — vendors, app logs, S3, Snowflake (Audit Parts 1–4, 7).

  Most-advanced project of the four. Status by issue:
  - EMEA-304 [Track 1B] Eng design — **DONE** (https://linear.app/canary-technologies/issue/EMEA-304)
  - SEC-383 Strip guest PII from canary + pms-gateway app logs — **In Progress** (https://linear.app/canary-technologies/issue/SEC-383)
  - SEC-422 Reversible/correlatable PII pseudonymization in logs (Presidio + AES-SIV) — **In Progress**, newly created 2026-06-23, follow-up to SEC-383 (https://linear.app/canary-technologies/issue/SEC-422)
  - SEC-392 Strip PII via Groundcover log pipelines — **Todo** (https://linear.app/canary-technologies/issue/SEC-392)
  - SEC-388 Close PII-in-logs gaps beyond SEC-383 (object binds, free-text, structlog) — **Backlog** (https://linear.app/canary-technologies/issue/SEC-388)
  - SEC-389 Strip passport/ID/pre-check-in PII from logs (CRITICAL) — **Backlog** (https://linear.app/canary-technologies/issue/SEC-389)
  - EMEA-320 AI PII-in-logs auditor in CI — **Backlog** (https://linear.app/canary-technologies/issue/EMEA-320)
  - SEC-391 KMS encryption + S3 lifecycle policies on all buckets — **Backlog** (https://linear.app/canary-technologies/issue/SEC-391)
  - EMEA-322 Amplitude: remove guest PII + disable autocapture — **Urgent**, Backlog (https://linear.app/canary-technologies/issue/EMEA-322)
  - EMEA-325 Twilio: message redaction + reduce retention — **Urgent**, Backlog (https://linear.app/canary-technologies/issue/EMEA-325)
  - EMEA-326 Snowflake: remediate unmasked PII across ANALYTICS + RAW — **Backlog** (https://linear.app/canary-technologies/issue/EMEA-326)
  - EMEA-266 Obfuscating PII from Datadog — **To Discover** (https://linear.app/canary-technologies/issue/EMEA-266)
  - SEC-8 Groundcover Log PII masking/cleanup — **Triage** (https://linear.app/canary-technologies/issue/SEC-8)
  - NOTE: the project description cites **EMEA-328** (Stripe/Marketo/Asana, hardcoded API token) but no
    such ticket is filed in the project — either uncreated or living elsewhere; worth confirming.

  ### 2. GDPR: PMS data anonymisation  (Track 1A-PMS + deferred 2A)
  https://linear.app/canary-technologies/project/gdpr-pms-data-anonymisation-4a24518aa6a7/overview
  Teams: EMEA + Security + PMS Engineering · Priority High · Dates 2026-07-02 → 2026-07-31 (earliest target) · 7 issues.
  Scope: close PMS-Gateway obfuscation adoption/coverage/retention gaps (Audit §5.2); deprecate PMS Scrapers.
  Headline finding: ~99% of accounts point at a no-op `Default (none)` policy; only 9 accounts genuinely obfuscate.

  - EMEA-307 [Track 1A] Eng design — Core Canary PII anonymisation (PMS only) — **In Review** (https://linear.app/canary-technologies/issue/EMEA-307)
  - EMEA-350 Region-based default retention via ConfigurationRuleEngine (the adoption fix) — **Backlog** (https://linear.app/canary-technologies/issue/EMEA-350)
  - EMEA-348 Extend deletion/cleanup (retention gap) — **Backlog** (https://linear.app/canary-technologies/issue/EMEA-348)
  - EMEA-327 Deprecate the PMS Scrapers — **Backlog** (https://linear.app/canary-technologies/issue/EMEA-327)
  - EMEA-305 [Track 2A] Eng design — purge after PMS sync — **DEFERRED** (Low, Backlog; blocked on Danubius customer confirmation) (https://linear.app/canary-technologies/issue/EMEA-305)
  - EMEA-349 Extend obfuscation coverage (ArrivalReportFile/OperationLog/ProtelAsyncAction) — **CANCELED** 2026-06-21 (https://linear.app/canary-technologies/issue/EMEA-349)
  - SEC-382 PII exposure audit across PMS scrapers + gateway — **CANCELED** 2026-06-19 (https://linear.app/canary-technologies/issue/SEC-382)
  - NOTE: EMEA-349 and SEC-382 are still described as active "Gap 2 / coverage" and "Urgent audit" items in
    the project description, but both tickets are now Canceled — the project body is stale vs. the board.

  ### 3. GDPR: Webchat / Voice AI anonymisation  (Track 1A — core Canary, densest free-text PII)
  https://linear.app/canary-technologies/project/gdpr-webchat-voice-ai-anonymisation-4db266cc6167/overview
  Team: EMEA · Priority High · Dates 2026-09-10 → 2026-10-02 · 2 issues.
  Earliest-stage of the three substantive projects. Covers chat.Message bodies, voice transcripts/turns/
  summaries, sent GMS messages — the surfaces a fixed field-list redactor structurally cannot catch.
  Open design problems: drop-vs-entity-scrub per field; post-anonymisation guest lookup (PRD Q7);
  EventableModel audit-trail integrity.

  - EMEA-303 [Track 1A] Eng design — Core Canary PII anonymisation (Omnichannel) — **Todo** (not started) (https://linear.app/canary-technologies/issue/EMEA-303)
  - EMEA-360 Anonymise chat & messaging free-text PII (ObfuscatableFields) — **Backlog** (https://linear.app/canary-technologies/issue/EMEA-360)
    (project note flags an ownership overlap: EMEA-360 currently sits under the User-input project lineage — reconcile)

  ### 4. GDPR: Communication consent management  (placeholder)
  https://linear.app/canary-technologies/project/gdpr-communication-consent-management-ee8f921bfac8/overview
  Team: EMEA · **No priority, no lead, no dates, 0 issues.** Description is just "PRD to be written" with a
  bullet list of intended scope (reg-card consent config + PMS sync, user flow, GMS/guest-journey messaging,
  upsells). Effectively unstarted — nothing tracked yet.

  ---

  ### Overall picture
  - **Design phase, nearly complete:** Track 1B design DONE (EMEA-304); Track 1A-PMS design In Review (EMEA-307);
    Track 1A-Omnichannel design still Todo (EMEA-303); 2A deferred.
  - **Only active implementation today** is in the Downstream project's logs leg: SEC-383 (In Progress) and its
    follow-up SEC-422 (In Progress), plus SEC-392 queued (Todo). Everything else is Backlog/Todo/Triage.
  - **Two urgent vendor items not yet started:** EMEA-322 (Amplitude) and EMEA-325 (Twilio).
  - **Sequencing per target dates:** PMS (Jul) → Downstream (Aug–Sep) → Webchat/Voice (Sep–Oct) →
    Consent management (unscheduled).
  - **Data-hygiene flags for you to chase:** (a) EMEA-349 & SEC-382 canceled but still written up as live in the
    PMS project body; (b) EMEA-328 (Stripe/Marketo/Asana) referenced in Downstream body but no ticket exists;
    (c) EMEA-360 ownership overlap between this project and the User-input project.

project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 30
title: Create an overview of the work already tracked in GDPR projects
updated: 2026-06-24 13:05:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://linear.app/canary-technologies/project/gdpr-downstream-systems-anonymisation-c5110566cbb5/overview
https://linear.app/canary-technologies/project/gdpr-pms-data-anonymisation-4a24518aa6a7/overview
https://linear.app/canary-technologies/project/gdpr-webchat-voice-ai-anonymisation-4db266cc6167/overview
https://linear.app/canary-technologies/project/gdpr-communication-consent-management-ee8f921bfac8/overview