---
area: management
contexts: []
created: 2026-06-24 16:07:10.236137
defer_until: null
due: 2026-06-25
energy: high
id: 2026-06-24T1607-perform-a-top-to-bottom-read-through-of-pii-audit
order: null
output: "## Agent run 2026-06-24T16:30 — top-to-bottom read-through\n\n**Artifact:**
  Notion — \"\U0001F512 PII Storage: Organization-Wide Audit (2026-06-04)\"\nhttps://www.notion.so/canarytechnologies/PII-Storage-Organization-Wide-Audit-2026-06-04-3758146861518135add9eaed3bc2cda1\nStatus:
  **In-review** · Authors: Bernard Pietraga (Security Eng) & Martijn Dekker (EMEA)
  · Classification: Internal-Confidential · viewed as-of 2026-06-24. Read in full
  (all ~64k chars across all 6 parts + callouts).\n\nThis is the discovery groundwork
  for the \"Deletion of all PII data\" project\n(https://linear.app/canary-technologies/project/deletion-of-all-pii-data-287fcf6516b1).
  Driven by EMEA GDPR commitments + enterprise asks (Danubius, IHG). Plan = tokenise/anonymise
  guest PII on a per-property configurable retention policy modelled on the existing
  `id_retention_days` / `id_purge_strategy` pattern.\n\n### Executive headline numbers\n-
  **Vendors:** 16 checked, 5 mishandle guest data; worst = Twilio & Amplitude.\n-
  **Logs:** passport details, phones, emails still in plaintext across 4 systems.\n-
  **S3:** 9 storage areas hold passports/ID photos/card images — none KMS-encrypted,
  most never auto-deleted.\n- **Warehouse (Snowflake):** hundreds of unprotected fields
  + millions of voice transcripts in plaintext; RAW DB has no masking at all.\n- **DB
  models:** 50+ tables store guest PII, mostly unencrypted and never fully deleted.\n-
  **Admin tools:** staff screens show full card numbers + contact details with no
  view-audit.\n\n### Part-by-part\n- **Part 1 — Vendors.** OpenAI/Groq (LOW, ZDR unverified).
  **Twilio (CRITICAL)** — message bodies + phones persisted ~1yr, no redaction → EMEA-325
  (pilot ContentRetention=discard on Statler, then Message Redaction + ~30d retention).
  **Amplitude (MEDIUM)** — raw `ocr_text` (govt-ID OCR, 558 events), `fullName`, freeform
  feedback, Auto Capture still firing, 0 PII classifications → EMEA-322. **Sentry
  (CRITICAL)** auto-attaches IP/cookies/full request bodies. Stripe/Marketo/Asana
  (Travel-Agents + scrapers, incl. hardcoded Asana token) → EMEA-328. NONE: Deepgram,
  Rekognition, Mindee, Incode, ElevenLabs/Cartesia, Livekit.\n- **Part 2 — App logging.**
  Canary & PMS Gateway **CRITICAL** — full request/response bodies, whole objects
  bound to log context, free-text/transcripts/passport text uncovered; today the redactor
  reliably scrubs only emails. Tickets: SEC-389 (passport/ID/pre-check-in), SEC-383
  (initial fix + field-name redactor), SEC-388 (close gaps), EMEA-320 (AI CI auditor).
  PMS Scrapers MEDIUM (plaintext passwords, hardcoded admin creds) → EMEA-327 (deprecate).
  Travel Agents (CC# logged before purge) → EMEA-328.\n- **Part 3 — S3.** No KMS/CMK
  on any bucket; no Block-Public-Access enforcement. Key gap: media/uploads bucket
  (`ArrivalReportFile.file`, email attachments = full guest lists) and incoming-email
  bucket have **no expiration → indefinite**. RDS Aurora backups = 7d, encrypted.
  → SEC-391 (KMS + lifecycle).\n- **Part 4 — Snowflake.** 13 confirmed unmasked ANALYTICS
  columns (passport metadata, DOB, nationality, PAYMENT_LINKS_* email/phone, AUTH_USER.USERNAME).
  **RAW DB fully unmasked** (LOADER/TRANSFORMER/ENGINEER roles), Airbyte syncs whole
  Postgres with no field filtering. Voice transcript surface entirely unmasked (VOICE_TURN/CALL/SEGMENT
  — millions of rows). Large JSON blobs (registration-card values ~149K, GATEWAY_DELTAS
  payload, ID-verification raw_response). → EMEA-326.\n- **Part 5 — DB models.** 5.1
  Canary (~6 weeks): the bulk of the inventory across check-in/identity, kiosk, guest-core,
  chat/messaging, voice, payments/PCI, authorization/forms, hotels/staff/HR. Notable
  offenders: `documents.IdVerificationRequest` (richest OCR record, not SoftDelete
  → indefinite), `check_in.AdditionalGuest`, `kiosk.SubmittedValue` (no session FK
  → orphan PII forever), `guest.Guest`, `chat.Message`, `credit_card.CreditCard` (VGS
  alias only), `four_seasons.ReservationChangeLog` (old+new identity, append-only).
  Plaintext CC#+CVV in Travel-Agents (5.4) and authorization Doubletree/Queen form
  models = **PCI red flags**. Proposed fix: dedicated **PII Purge Service** reusing
  PMS-gateway `ObfuscationPolicy` (irreversible random overwrite), region-based defaults
  via ConfigurationRuleEngine (EMEA-308 eng design; EMEA-354..364 backlog). 5.2 PMS
  Gateway: 60-day Protel cleanup exists but OperationLog/ArrivalReportFile/ProtelAsyncAction
  never purged; **obfuscation adoption gap — ~99% of guests on `Default (none)` no-op
  policy** (4.2M EU + 67.5M US), only 9 accounts genuinely obfuscated → EMEA-348 (retention)
  + EMEA-350 (region defaults).\n- **Part 6 — Event queues.** Well-bounded/self-expiring
  (SQS 4-day, DB queue hard-deletes, Aurora 7-day). Only open item: **Kafka CDC topic
  retention not in Terraform** — needs Strimzi KafkaTopic review in GitOps.\n\n###
  Observations worth a second look (not errors, just flags)\n- Section numbering is
  inconsistent in Part 1 (jumps 1.2 → \"Amplitude\" unnumbered → 1.4 → unnumbered
  NONE vendors → 1.6/1.7/1.8/1.10; no 1.3/1.5/1.9). Cosmetic, but makes \"Audit ref
  §x.y\" cross-links from tickets slightly fragile.\n- The original umbrella audit
  ticket **SEC-382** (\"GDPR: PII exposure audit across PMS scrapers and integrations
  gateway\") was **Canceled (2026-06-19)** — work appears to have been re-scoped into
  the EMEA-3xx / SEC-388/389 tickets, so that's expected, not a dropped thread.\n-
  Several open TODOs still embedded in the doc: confirm OpenAI/Groq ZDR (Sudarshan
  contacted), confirm Mindee \"Delete When Fetched\", decide 365-day large-log retention,
  confirm Kafka topic retention.\n- PCI items (plaintext PAN+CVV in Travel-Agents
  `Card` and authorization form models) are the highest-severity legal exposure in
  the doc and are folded into EMEA-328 alongside lower-severity log fixes — may warrant
  its own tracked priority.\n\nNo external writes made. Read-only research only. This
  was a read-through/comprehension task — no code or ticket changes performed.\n"
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 30
title: Perform a top to bottom read-through of PII audit.
updated: 2026-07-02 16:07:26.460383
waiting_on: null
waiting_since: null
working_on: false
---