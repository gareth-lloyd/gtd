---
area: null
contexts: []
created: 2026-06-15 14:49:34.634135
defer_until: null
due: null
energy: low
id: 2026-06-15T1449-review-the-pii-obfuscation-catalog-document-for-ap
order: null
output: |
  ## Agent run 2026-06-15T15:05 — Sizing of the PII obfuscation/audit work

  Source: Notion "🔒 PII Storage: Organization-Wide Audit (2026-06-04)" by Bernard Pietraga (Sec Eng) & Martijn Dekker (EMEA), status Draft.
  https://www.notion.so/canarytechnologies/PII-Storage-Organization-Wide-Audit-2026-06-04-3758146861518135add9eaed3bc2cda1
  Parent project: "Deletion of all PII data" — https://linear.app/canary-technologies/project/deletion-of-all-pii-data-287fcf6516b1

  TL;DR on size: The audit is *discovery*, not the build. The remediation it enumerates is already broken into ~10 Linear tickets. Rough total for the **catalogued remediation tickets is ~6–9 eng-weeks**. The genuinely large piece — the per-property tokenisation/retention engine (Track 1A / Part 5, "Deletion of all PII data") — **has not started and is a multi-month project on its own**, not yet scoped in the doc ("TODO: Everything (see open eng design ticket)").

  ### Workstream-by-workstream estimate

  | Area | Ticket(s) | Rough size | Notes |
  |---|---|---|---|
  | App logging leaks (canary + PMS GW) | SEC-389, SEC-383, SEC-388, EMEA-320 | **~2 wks** (doc's own estimate) | Strip passport/ID/pre-checkin from logs, pipeline scrubbing, extend redactor to names/phones/free-text, + CI AI-auditor to prevent regressions. The redactor today only reliably scrubs emails. |
  | Twilio | EMEA-325 | ~3–5 d | Pilot ContentRetention=discard on Statler → account-level redaction (24h fixed, irreversible) + reduce 1yr retention to ~30d. Mostly config + careful rollout. |
  | Amplitude | EMEA-322 (ties SEC-389) | ~3–5 d | URGENT stop ocr_text (raw ID OCR), stop fullName/feedback, disable Auto Capture on guest surfaces, add property classifications. |
  | Sentry | (CRITICAL, no ticket yet) | ~2–3 d | Disable default PII attach (IP/cookies/request bodies), stop extra-context body dumps. Overlaps Part 2. |
  | Travel-Agents repo (consolidated) | EMEA-328 | **~1–2 wks** | Covers Stripe, Marketo, plaintext CC+CVV (PCI!), Asana hardcoded token, S3 docs, Client/Card models. Biggest single vendor/logging ticket; PCI angle raises priority. |
  | PMS Scrapers | EMEA-327 | medium (resolve by **deprecation/removal**) | Removing the app resolves 2.2, 1.10 Asana, Part 6 AdminJS hardcoded creds. Size depends on whether deprecation is already planned. |
  | S3 buckets | SEC-391 | ~1 wk | KMS/CMK encryption (currently none) + lifecycle/expiration on media + incoming-email buckets (currently indefinite). Terraform/terragrunt work. |
  | Data warehouse (Snowflake) | EMEA-326 | **~2–3 wks** | Extend DBT fact_table_pii to 13 unmasked cols + voice-transcript surface (~millions of rows), lock down RAW (fully unmasked, Airbyte 1-1 sync), decide drop-vs-entity-scrub for free-text/JSON blobs. Largest of the remediation tickets. |
  | Admin interfaces | (Part 6, no ticket yet) | ~1 wk | Mask ccnumber/cvv in QueenFormModelAdmin, mask contact fields, add audit logging on PII access. |
  | Event queues | (Part 7) | ~1–2 d | Mostly self-expiring already; only open item is confirming/capping Kafka CDC topic retention in GitOps. |
  | **DB model tokenisation / retention engine** | **Track 1A / Part 5 — NOT STARTED** | **multi-month (own project)** | The actual "Deletion of all PII data" build: per-property configurable retention modelled on id_retention_days/id_purge_strategy, across 50+ tables. Part 5.1 (canary) is "TODO: Everything". PMS GW (5.2) already has an obfuscation policy but only **9 accounts** are genuinely obfuscated (EU default policy covers 174 accts / 4.2M guests at ~0%). Needs eng design ticket first. |

  ### Bottom line for planning
  - **Catalogued remediation (the tickets above, excl. Track 1A): ~6–9 eng-weeks**, parallelisable across Sec Eng / EMEA / Data. Several are config-heavy (Twilio, Sentry, S3) and quick wins; warehouse + travel-agents + logging are the heavier ones.
  - **The tokenisation/retention engine is the real cost** and is unscoped — needs its own design doc + estimate before it can be sized. Treat the audit's Part 5 as a pointer, not a plan.
  - Highest-urgency / lowest-effort first: Amplitude ocr_text kill, Travel-Agents plaintext CC+CVV (PCI), Sentry default PII attach.
  - Open TODOs in the doc that gate accurate sizing: ZDR confirmation (OpenAI/Groq), RAW DB Snowflake sweep not yet done, Mindee "delete when fetched" unconfirmed, Kafka retention unconfirmed.

  Linear tickets referenced (read-only, not opened by me): SEC-383, SEC-388, SEC-389, SEC-391, EMEA-320, EMEA-322, EMEA-325, EMEA-326, EMEA-327, EMEA-328.
project: null
source_id: null
tags: []
time_minutes: 5
title: REview the PII obfuscation catalog document for approximate size of work
updated: 2026-06-15 15:05:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://www.notion.so/canarytechnologies/PII-Storage-Organization-Wide-Audit-2026-06-04-3758146861518135add9eaed3bc2cda1?source=copy_link