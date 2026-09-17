---
area: null
completed_at: 2026-09-17 12:27:11.489452
contexts: []
created: 2026-09-16 11:07:28.510710
defer_until: null
due: null
energy: low
id: 2026-09-16T1107-try-to-get-up-to-speed-on-accord-deal-wrt-mobile
order: null
output: |
  ## Agent run 2026-09-16 14:38:38.275688

  Notion-only search (as requested). "Accord" resolves to the **Accor** hotel group; no separate "Accord" entity exists in Notion.

  ### Deal in one paragraph
  Accor wants a wallet-first NFC + BLE digital key delivered inside their ALL app via Canary's mobile SDK. Sized at ~EUR 1-2M ARR across ~5,700 hotels. The deal is currently in contract redlines (Canary draft dated 16 Aug; last cross-reference call 9 Sep). Contract scope: BLE + NFC/Wallet modules, iOS/Android SDK support, Opera Cloud/OHIP, staff dashboard, analytics, support. Pilot plan, pilot properties, PMS, and lock vendors are still undefined.

  ### Key Notion pages
  - Accor Enterprise Runbook 2026 (canonical account overview): https://app.notion.com/p/3aecc138ea1f4971be5466c1077d3701
  - Accor contract changes, 9 Sep call cross-reference (latest status, 7 open points before next legal call on Wed): https://app.notion.com/p/25ea5aba812a47e4bcb34150f0631ec1
  - Accor Questions (technical Q&A with Accor's app team on SDK/BLE/wallet/China/lock matrix; source of truth for what was promised): https://app.notion.com/p/37581468615180b69421e295f60131ee
  - Accor RFP: Mobile Key prep doc (7 May in-person RFP meeting, Paris): https://app.notion.com/p/34d8146861518014a77ce0c0aa6172e8

  ### Mobile-relevant decisions / constraints
  - ALL enrollment must be skippable and non-blocking; key goes to members and non-members alike (Runbook).
  - China/Huawei: no Google dependency; in-app BLE is the path; Samsung/Huawei Wallet out of scope (Accor Questions).
  - SDK keeps BLE scanning/credentials internal; host app gets a themed screen or CustomViews, no raw unlock API yet (Accor Questions).
  - NFC open-failure KPI dropped (no telemetry); BLE failure KPI retained (Contract changes).

  ### Open threads (mobile-specific)
  - P0: Accor app team (Bertrand Magnien) lacks SDK docs to integrate the ALL app. Canary must justify deleted SDK language and confirm 30-day release notice / 6-month backward compat. Owner: Mehul (Contract changes).
  - P0: ServiceNow vs Zendesk support model, 24/7 EN/FR; pen test on pilot property (Mercure Dunkirk candidate) (Contract changes).
  - P1: 20% activation KPI (Bryan), key-sharing vendor caveat, current-vs-roadmap feature dates, revenue reporting by hotel (Contract changes).
  - Lock vendor wallet support still pending: SALTO wallet (Q3 2026), Onity wallet (Q4 2026), Dormakaba Android wallet certification (Accor Questions).
  - Day-to-day Canary owner unconfirmed (Jean-Charles expected) (Runbook).

  ### Suggested next steps (not done; Notion only per task)
  - Read the "Accor contract changes" page in full before the Wed legal call if you are expected to weigh in on SDK terms.
  - Follow up with Mehul on the SDK docs gap for Accor's app team; that is the most engineering-adjacent P0.
  - Widen to Slack / Linear / Granola for anything after 9 Sep if needed.
project: 2026-09-08-mobile
source_id: null
tags: []
time_minutes: 5
title: try to get up to speed on Accord deal wrt mobile
updated: 2026-09-17 12:27:11.489446
waiting_on: null
waiting_since: null
working_on: false
---

Start with Notion search only and report back