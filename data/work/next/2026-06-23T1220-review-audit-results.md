---
area: management
contexts: []
created: 2026-06-23 12:20:26.851068
defer_until: null
due: 2026-06-23
energy: high
id: 2026-06-23T1220-review-audit-results
order: null
output: |
  ## Agent run 2026-06-24T14:05Z — Overview of the PII Storage Org-Wide Audit

  **Source:** "🔒 PII Storage: Organization-Wide Audit (2026-06-04)"
  https://www.notion.so/canarytechnologies/PII-Storage-Organization-Wide-Audit-2026-06-04-3758146861518135add9eaed3bc2cda1
  Authors: Bernard Pietraga (Security Eng) & Martijn Dekker (EMEA). Status: Draft. Classification: Internal-Confidential.
  Read in full (all 7 parts). This is the discovery groundwork for the Linear project
  **"Deletion of all PII data"** (https://linear.app/canary-technologies/project/deletion-of-all-pii-data-287fcf6516b1),
  driven by EMEA GDPR commitments + enterprise asks (Danubius, IHG).

  ### What it is
  A code-level inventory of *every* place guest PII is stored, logged, transmitted, or replicated across the
  stack, with the masking/encryption/retention controls assessed on each. The goal: turn "minimise our PII
  footprint" into a trackable checklist, feeding a per-property configurable retention policy modelled on the
  existing `id_retention_days` / `id_purge_strategy` pattern.

  ### Headline numbers
  - Vendors: 16 checked, 5 mishandle data; worst = Twilio + Amplitude.
  - Logs: passport details, phones, emails still in plaintext across 4 systems.
  - File storage: 9 areas hold passports/ID photos/card images — none encrypted, most never auto-deleted.
  - Warehouse: hundreds of unprotected fields + millions of voice transcripts in plaintext; RAW DB has no masking at all.
  - Databases: 50+ tables store guest data unencrypted, most never fully deleted.
  - Admin tools: staff screens show full card numbers + contact details, no access audit log.

  ### CRITICAL items (act first)
  - **Twilio (Part 1.2, ~2d)** — message bodies + phones persisted ~1yr unredacted. Plan: enable Message
    Redaction (24h fixed, irreversible) + shorten account retention to ~30d. Pilot at Statler first. → EMEA-325.
  - **Sentry (1.6)** — auto-attaches client IP, cookies, full request bodies on every error.
  - **Amplitude (1.3, MEDIUM but urgent sub-item)** — raw OCR of govt IDs (`ocr_text`, 558 events/30d),
    full guest names, freeform feedback flowing in clear; Auto Capture still firing (leaks names/chat/consent
    text). Zero PII classifications exist. → EMEA-322 (urgent: stop `ocr_text`, ties to SEC-389).
  - **App logging — Canary & PMS Gateway (2.1, ~1wk+)** — full request/response bodies, whole reservation/
    guest objects, passport OCR, voice transcripts all hit Groundcover/Datadog/Sentry. Redactor today
    reliably scrubs *only emails*. → SEC-389 (passport/ID), SEC-383 (initial fix), SEC-388 (remaining gaps),
    EMEA-320 (CI AI-auditor to stop regressions).
  - **Plaintext PAN + CVV** in `authorization.DoubletreeFormModel`/`QueenFormModel`, `demos.DemoFormModel`,
    and Travel-Agents `Card` model (5.4). QueenFormModelAdmin shows ccnumber+cvv in list_display (Part 6).
  - **Hardcoded credentials** — PMS Scrapers AdminJS (`canary`/`Likethebird1!`), Asana token in source,
    admin creds in `admin.js`. Mitigation route: deprecate PMS Scrapers entirely → EMEA-327.

  ### The rest by layer
  - **Part 1 Vendors:** Stripe/Marketo/Asana (Travel-Agents repo) → consolidated EMEA-328. Clean/low-risk:
    Deepgram, Rekognition, Mindee, Incode, ElevenLabs/Cartesia, LiveKit, OpenAI/Groq (ZDR verification TODO).
  - **Part 3 S3 (~2d):** No KMS encryption on *any* bucket; media/uploads + incoming-email buckets (arrival
    reports = full guest lists) have no expiration → indefinite. RDS backups 7d, encrypted. → SEC-391.
  - **Part 4 Warehouse (~1wk):** ANALYTICS has 13 confirmed-unmasked columns (passport meta, DOB, nationality,
    PAYMENT_LINKS_*). **RAW DB fully unmasked** — LOADER/TRANSFORMER/ENGINEER can read everything (Airbyte
    1-1 full-DB sync). Voice transcript surface (~millions of rows across VOICE_TURN/SEGMENT/CALL) entirely
    unmasked. Large free-text/JSON blobs (registration cards ~149K, gateway deltas, ID-verification raw). → EMEA-326.
  - **Part 5 DB models (~6wk Canary, ~2wk PMS-GW):** the biggest surface. Most sensitive models (`documents.
    IdVerificationRequest`, `check_in.AdditionalGuest`, `kiosk.SubmittedValue`, `guest.Guest`, `chat.Message`,
    `voice.*`) are on plain TimeStampedModel with NO soft-delete/purge → indefinite retention.
    `kiosk.SubmittedValue` has no session FK so cascade delete never reaches it.
    - **PMS-Gateway obfuscation adoption is the standout finding:** ~99% of guests sit on a no-op
      `Default (none)` policy (4.2M EU / 67.5M US). Only **9 accounts** are genuinely being obfuscated
      (Marriott, Rosewood, Capella/Patina). → EMEA-350 (region-based default via ConfigurationRuleEngine),
      EMEA-348 (extend retention/cleanup to OperationLog, ArrivalReportFile, Protel async tables).
  - **Part 6 Admin:** full card numbers + contact PII visible, no audit logging of who viewed.
  - **Part 7 Queues:** mostly well-bounded (SQS 4-day, DB queue hard-deletes). Only open item: Kafka CDC
    topic retention lives in GitOps, unconfirmed — needs review.

  ### Proposed remediation (the "unblock" decision)
  Build a **dedicated PII Purge Service (Track 1A, EMEA-308)** reusing the proven PMS-Gateway
  `ObfuscationPolicy` framework rather than per-app logic. Technique = irreversible random overwrite
  (UUID/XXXX + `obfuscated_at` marker) so data leaves GDPR scope (legally equiv to deletion). Data-driven
  per-property lag config, region-based defaults via Enterprise ConfigurationRuleEngine. Hard design
  constraints flagged: (1) EventableModel event payloads keep PII copies even after the live row is
  anonymised; (2) historical lookup/re-identification UX (Voice AI + CX search by name/email) breaks
  post-anonymisation; (3) PII not linked to a reservation must still be wiped.

  ### Ticket map (for tracking)
  - Project: GDPR: User input data — anonymisation
    https://linear.app/canary-technologies/project/gdpr-user-input-data-reg-card-kiosk-sessions-upsells-ids-anonymisation-ef83a5a80e32
  - **EMEA-354** = eng design, BLOCKS all 5.1 implementation tickets. EMEA-364 (enablement) ships before
    EMEA-363 (CI linter gate).
  - Per-area: EMEA-355 check-in, 356 ID docs, 357 kiosk, 358 upsell/forms, 359 guest-core, 360 chat,
    361 EventableModel/search indexes, 362 unlinked-PII sweep.
  - Other tracks: EMEA-322 (Amplitude), 325 (Twilio), 326 (warehouse), 327 (deprecate PMS Scrapers),
    328 (Travel-Agents), 348/350 (PMS-GW retention/adoption), 308 (purge service); SEC-383/388/389 (logging),
    SEC-391 (S3 encryption), EMEA-320 (CI log auditor).

  ### Open questions surfaced in the doc
  - OpenAI/Groq ZDR enablement unverified (contacted Sudarshan).
  - Mindee "Delete When Fetched" unconfirmed.
  - Do we need 365-day large-log retention?
  - Kafka CDC topic retention unknown.

  **Note:** No external writes made (read-only review per task rules). No action taken on tickets/Notion —
  handing back for you to decide next steps (e.g. which tracks to prioritise for the Unblock-team push).
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 30
title: Overview the audit results
updated: 2026-06-24 14:05:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://www.notion.so/canarytechnologies/PII-Storage-Organization-Wide-Audit-2026-06-04-3758146861518135add9eaed3bc2cda1?source=copy_link