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
    [Correction from the 2026-06-24T15 run below: EMEA-328 DOES exist — it's filed in the umbrella
    "Deletion of all PII data" project, not in the Downstream project, which is why it didn't show
    in the Downstream issue list.]

  ## Agent run 2026-06-24T15:10Z — Audit cross-reference: is every finding tracked? + structure critique

  Read the full PII Storage Org-Wide Audit (2026-06-04), all of Parts 1–7
  (https://app.notion.com/p/3758146861518135add9eaed3bc2cda1) and cross-referenced every finding
  against Linear, including the two parent projects and the fifth sibling project.

  ### Framing correction (important)
  The audit spawned **FIVE** child projects, not four, all under the umbrella **Deletion of all PII data**
  (https://linear.app/canary-technologies/project/deletion-of-all-pii-data-287fcf6516b1 — status Eng Design,
  target 2026-09-30). The fifth — and the FLAGSHIP — is **GDPR: User input data anonymisation**
  (https://linear.app/canary-technologies/project/gdpr-user-input-data-anonymisation-ef83a5a80e32), which
  builds the shared `ObfuscatableField` framework (EMEA-354) and owns audit §5.1, the single largest section
  (tickets EMEA-354–364). It is NOT in the four-project list this task was scoped to, but any judgment of
  "do the projects match the audit" must include it.

  ### Coverage map (audit part -> ticket -> status)
  TRACKED & well-covered:
  - 1.2 Twilio (CRITICAL) -> EMEA-325 (Backlog, Urgent)
  - 1.3 Amplitude -> EMEA-322 (Backlog, Urgent)
  - 1.7/1.8 Stripe/Marketo + 5.4 Travel-Agents (plaintext CC+CVV, PCI) -> EMEA-328 (Backlog; in umbrella project)
  - 1.10 Asana + 2.2 scrapers + Part 6 scrapers AdminJS -> EMEA-327 deprecate PMS Scrapers (Backlog)
  - 2.1 App logs (CRITICAL) -> SEC-383 (In Progress), SEC-388, SEC-389, EMEA-320, +SEC-422 (the only active code work)
  - 2.4 Travel-Agents logs -> EMEA-328
  - 3.1 S3 (9 buckets, no CMK/lifecycle) -> SEC-391; travel-agents S3 -> EMEA-328
  - 4.1-4.4 Snowflake (13 cols, voice transcripts, RAW, blobs) -> EMEA-326
  - 5.1.1-5.1.3 / 5.1.7 / guest-side 5.1.8 -> EMEA-355/356/357/358/359 (User-input project)
  - 5.1.4 chat -> EMEA-360
  - 5.1 cross-cutting -> EMEA-361 (EventableModel), EMEA-362 (non-res-linked), EMEA-363 (CI linter),
    EMEA-364 (enablement), EMEA-354 (framework), EMEA-308 (design, In Review)
  - 5.2 PMS retention + adoption -> EMEA-348, EMEA-350
  - 7.1/7.2 SQS + DB queue, and all NONE-rated vendors (Deepgram/Rekognition/Incode/ElevenLabs/Livekit/Opensearch)
    -> no action needed (bounded/self-expiring)

  NOT tracked (gaps) — ranked by significance:
  1. **Sentry (Part 1.6, rated CRITICAL)** — NO dedicated ticket. Folded into "logs" but the leak is SDK-config
     (send_default_pii, request-body/cookie/IP auto-capture, beforeSend) — orthogonal to scrubbing log strings;
     SEC-383/388/389 do NOT fix it. A CRITICAL finding with no owner = clearest miss.
  2. **Mindee** — umbrella calls it "highest strategic priority" (no removal endpoint -> accelerate in-house OCR),
     but exists only as a TODO. Strategic and unowned. (Also 1.1 OpenAI/Groq ZDR verification = TODO only.)
  3. **Part 6 admin interfaces (main monorepo + integrations-gateway)** — ccnumber/cvv in QueenFormModelAdmin
     list_display + NO audit logging on PII access. Untracked (only the scrapers AdminJS slice is, via EMEA-327).
  4. **Kafka CDC retention (7.3)** — untracked open item. Small GitOps check, but CDC carries full reservation
     payloads and the umbrella itself flags CDC-replay re-landing PII after anonymisation as load-bearing.
  5. **Guest Insights (5.5)** — GuestProfile + RawFullContact/RawClearBit JSON. Untracked; confirm if product live.
  6. **5.1.6 Payments guest PII** — cardholder identity/billing-address plaintext, WalletProfile DOB not clearly in
     EMEA-355–359. Some legitimately out of scope (VGS tokenises PAN, CVV not stored, staff-billing excluded) but
     guest cardholder identity IS in-scope — confirm deferred vs dropped.
  7. **Voice source-model implementation (5.1.5)** — only design EMEA-303 (Todo); no impl ticket yet (early-stage, expected).

  STALE / needs reconciliation:
  - **EMEA-349 (PMS obfuscation coverage, §5.2 Gap 2) is CANCELED** — it was the only ticket covering Gap 2.
    EMEA-348 covers deletion/cleanup, NOT obfuscation of retained-but-needed records. Either deletion now
    supersedes obfuscation for those stores (fine — say so) or Gap 2 is silently unowned.
  - **SEC-382 (PMS PII audit, Urgent) CANCELED** — confirm completed-then-closed vs abandoned.

  Net: the high-volume / high-severity findings (logs, S3, Snowflake, §5.1 models, PMS adoption) are ALL tracked.
  Misses cluster in the long tail (vendors beyond the top two, admin tooling, queue config, niche products).
  Two are significant by their STATED severity, not size: Sentry (CRITICAL) and Mindee ("highest priority").

  ### Structure critique — do I agree with the project layout?
  Largely yes. The Track 1A (source models) / 1B (downstream copies) / vendor split mirrors the audit's own model,
  and the remediation owners/techniques genuinely differ (obfuscation framework vs DBT masking vs vendor console
  vs IaC). PMS Gateway as its own project is correct (separate ObfuscationPolicy framework + unique ~99% no-op
  adoption story). Carving free-text comms (5.1.4/5.1.5) out into Webchat/Voice is defensible (can't column-mask
  free text). Dependency spine is clean: EMEA-354 blocks every 1A impl ticket; cross-cutting risks live once in the umbrella.

  Three reservations:
  1. **"Downstream systems" is overloaded** — bundles vendor-console (Twilio/Amplitude), app-code log scrubbing
     (the only ACTIVE work), S3 Terraform, Snowflake DBT, and Kafka: 4 teams/skill sets under one banner. The
     app-logs leg (Part 2) is mature enough to deserve its own project rather than sitting in dormant vendor backlog.
  2. **Snowflake placement contradicts a stated principle** — umbrella says Snowflake "must be part of the CORE
     obfuscation flow, NOT a follow-up," yet EMEA-326 sits in 1B/Downstream Backlog (Aug–Sep) like any vendor.
  3. **Consent management is the odd one out — not from this audit at all.** This audit is storage/masking/retention;
     consent (opt-in/out, reg-card consent config, GJM/upsell) is a different workstream. No PRD, no lead, no dates,
     0 issues, no audit section maps to it. Fine as a FUTURE project, but listing it among four audit-derived ones
     overstates how much is scoped — it's a placeholder with zero audit backing.

  ### Suggested next actions (not yet created — awaiting go-ahead)
  Draft tickets to fill the significant gaps: (a) Sentry SDK PII config; (b) Part 6 admin access-logging + PAN/CVV
  display; (c) Kafka CDC retention cap; (d) Guest Insights retention. Plus reconcile EMEA-349/SEC-382 cancellations.
  NOTHING has been written to Linear — read-only research only.

  ## Agent run 2026-06-24T15:40Z — Verification pass (two subagents: Linear audit + codebase audit)

  Verified the three "untracked" findings above with one subagent searching Linear exhaustively (all teams,
  not just GDPR projects) and one reading the canary monorepo at file:line level. One finding was materially
  CORRECTED; two held up.

  ### Finding 1 — Sentry (CORRECTED — my earlier "clearest miss / no owner" was OVERSTATED)
  Refined verdict: **PARTIALLY TRACKED, with a not-yet-merged fix and a residual gap.**
  - SEC-383 DOES scope the two headline Sentry SDK risks the audit named. Its confirmed-leak table lists
    `settings/sentry.py:62 send_default_pii: True` and `canary/sentry.py:45-49 with_sentry_context decodes the
    full request body into Sentry context`, and its acceptance criteria (checkboxes ticked) are
    "[x] send_default_pii flipped to False" and "[x] with_sentry_context no longer captures raw request bodies".
    So the "client IP / cookies / full request bodies" SDK risks ARE owned by SEC-383 — contradicting my claim
    that SEC-383/388/389 don't fix Sentry.
  - BUT two real caveats remain: (i) **the fix is not actually merged** — code still shows
    `settings/sentry.py:62 send_default_pii: True` and SEC-383 is only *In Progress*, so the ticked acceptance
    boxes are ahead of the codebase; verify before trusting. (ii) The `_before_send` hook in `settings/sentry.py`
    does **no PII scrubbing** (only filters ddtrace-429 and LiveKit-teardown noise), and the structlog
    redactor (`redact_sensitive_query_parameters`, wired only into `STRUCTLOG_SHARED_PROCESSORS` at
    `settings/base.py:1329`) is narrow — redacts only `token`/`signature` query params on request_started/finished
    log lines and never runs over SDK-captured events (unhandled exceptions, breadcrumbs, local variables).
  - SEC-388 explicitly EXCLUDES the already-fixed sentry call sites; SEC-389 doesn't mention Sentry. Two old
    dedicated Sentry-PII tickets (ENT-36 2022, PAY-57 2023) are both Canceled.
  - **Net:** the headline Sentry SDK fix is owned (SEC-383, pending merge); the residual — a PII-scrubbing
    `before_send` for SDK-captured events/breadcrumbs — is genuinely untracked, but it's a smaller, lower-severity
    gap than I first wrote. Downgrade Sentry from "clearest miss" to "verify SEC-383 lands + optional residual ticket".

  ### Finding 2 — Admin interfaces (CONFIRMED true & untracked, with one caveat)
  - Code confirms `QueenFormModelAdmin.list_display` (`authorization/admin/admin.py:386-389`) includes
    `nameoncard, ccnumber, expiration, cvv`, backed by **unencrypted** `CharField`s (`models.py:1370,1372`).
    `DoubletreeFormModelAdmin` is identical. CAVEAT: both models are docstring-marked `"""Demo-only"""`
    (`models.py:1358`) — so the raw PAN/CVV changelist exposure is on demo forms; weigh severity accordingly.
  - Real guest PII IS broadly exposed in other admins: `GenericAuthInformationAdmin`, `CreditCardAdmin`
    (cardholder_name + name/address search_fields), `GeneratedFormAdmin` (client name/email) — all in
    list_display/search_fields.
  - No read-access audit logging exists: the only audit path is `HistoryService` (`canary/admin/history.py`)
    writing Django `LogEntry` rows on ADDITION/CHANGE/DELETION only — i.e. **writes, never views**. Confirmed.
  - Linear: NO dedicated ticket. EMEA-327 = scrapers AdminJS only; SRE-333 (Separate Django Admin) is a
    memory/cost split; TOOL-330 captures acting-admin only for one Auto-Config save flow. Finding stands.

  ### Finding 3 — Kafka CDC retention (CONFIRMED untracked; one detail unverifiable here)
  - Linear: NO dedicated ticket to cap/confirm CDC topic retention. Nearby tickets are provisioning
    (TOOL-325/342 define KafkaTopic CRs in `apps/canary/kafka/values/_shared/topics.yaml` for Auto-Config),
    monitoring (SRE-298), or Groundcover retention (SRE-314) — none set/cap Kafka topic retention. Finding stands.
  - Code: this monorepo has no Strimzi `KafkaTopic` CRs, no `*.tf`, and no `retention.ms` anywhere — only
    Kafka producers/consumers + `docs/kafka-cdc.md`. So "retention isn't in this repo" is confirmed, but the
    audit's specific "lives in GitOps, not Terraform" claim CANNOT be verified from here (that infra config is
    in a separate repo). The untracked-ness is solid; the GitOps-location detail is plausible but unconfirmed.

  ### Verification bottom line
  - Finding 2 (admin) and Finding 3 (Kafka) verified — genuinely untracked. Admin caveat: headline ccnumber/cvv
    exposure is on demo-only models, but the no-view-audit-logging gap and real-guest-PII admins are valid.
  - Finding 1 (Sentry) was the one I got wrong: it's PARTIALLY tracked by SEC-383 (pending merge), not unowned.
    Action shifts from "file a Sentry ticket" to "confirm SEC-383's Sentry changes actually land, then decide if
    the residual before_send scrubbing warrants its own ticket."
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 30
title: Create an overview of the work already tracked in GDPR projects
updated: 2026-06-24 15:40:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://linear.app/canary-technologies/project/gdpr-downstream-systems-anonymisation-c5110566cbb5/overview
https://linear.app/canary-technologies/project/gdpr-pms-data-anonymisation-4a24518aa6a7/overview
https://linear.app/canary-technologies/project/gdpr-webchat-voice-ai-anonymisation-4db266cc6167/overview
https://linear.app/canary-technologies/project/gdpr-communication-consent-management-ee8f921bfac8/overview