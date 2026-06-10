---
area: null
contexts: []
created: 2026-06-09 12:31:55.947525
defer_until: null
due: null
energy: low
id: 2026-06-09T1231-look-through-prd-for-martijn-gdpr
order: null
output: |
  ## Agent run 2026-06-09T14:52
  Found the PRD in Notion.

  **Document:** PRD: PII Minimisation & Retention — GDPR Compliance
  https://app.notion.com/p/35d814686151815a96cfcf07ae7edc35
  - Last updated within the last week (search timestamp "Past day", 2026-06-09).
  - Author caveat: Notion page metadata did NOT expose the author. Martijn
    Dekker ownership is INFERRED — he is lead on the linked Linear project
    "Deletion of all PII data" and is assigned the blocking PMS-sync spec (Q9).
    Could not literally confirm him as page author from Notion. Worth a quick
    manual check if author attribution matters.

  ### Overview
  - **Problem:** Canary lacks provable PII minimisation / purpose-limited
    retention required by GDPR Arts. 5(1)(c) & 5(1)(e). EMEA properties wrongly
    assume it's already handled. Surfaced as a blocker by Danubius (€80k,
    ~€500k upside) and IHG (multi-million) deals.
  - **Proposed solution:** Obfuscate/tokenise all guest PII once a configurable
    retention policy fires — NOT hard delete — preserving referential integrity
    and audit trails. New `pii_retention_days` / `pii_purge_strategy` config
    (separate from ID-doc retention), a dedicated PII Purge Service, and a
    read-only dashboard in Check In Settings (CSM-managed).
  - **Scope:** Track 1A tokenisation; 1B downstream vendors (Snowflake, Datadog,
    Amplitude, Groundcover, Mindee); Track 2A (ON HOLD) Danubius purge-after-
    PMS-sync; Track 3 org PII policy/governance; Track 4 free-text PII in
    messages/chat/voice. Out of scope: backfill of checked-out guests, staff
    PII, hard deletion.
  - **Timeline:** 1A ~2wk, 1B ~1wk eng + vendor lead time, 2A ~2wk (TBC),
    3 ~0.5wk + ongoing, 4 TBD (EMEA-303). Linear project due 2026-09-30.
  - **Open questions:** Q1 (Legal) is obfuscation sufficient or is true deletion
    required — blocks architecture; Q7 (CX) post-obfuscation support workflow —
    blocks rollout; Q9 (Martijn) purge-after-sync spec, re-ingestion blocking,
    failure handling — blocks Track 2A.

  ### Related Notion docs
  - GDPR Sprint Hub [Jun 2026] — parent hub:
    https://app.notion.com/p/37981468615180f0a62af2065fee5b44
  - GDPR Compliance — Kickoff: State of Play & Gap Analysis (Sebastian Cahill,
    upd. 2026-05-20): https://app.notion.com/p/366814686151811996a9eb8113323f40
  - 2026-05-13 — Cooley — GDPR Compliance Requirements (outside counsel,
    anonymisation vs deletion): https://app.notion.com/p/35f8146861518047812ff07f205dbc10
project: null
source_id: null
tags: []
time_minutes: 5
title: Look through PRD for Martijn GDPR
updated: 2026-06-09 14:59:47.183456
waiting_on: null
waiting_since: null
working_on: false
---

find in notion. Author martijn dekker, recent document (<1 week old), addressing GDPR compliance issues. 

Overview hte document