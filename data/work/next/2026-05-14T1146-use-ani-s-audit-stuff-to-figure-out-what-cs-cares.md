---
area: null
contexts: []
created: 2026-05-14 11:46:53.108421
defer_until: null
due: null
energy: low
id: 2026-05-14T1146-use-ani-s-audit-stuff-to-figure-out-what-cs-cares
order: -23
output: |
  ## Agent run 2026-05-21T09:52:00Z

  ### Source
  - Slack: Ani Ghazarossian in #cs/eng partnership-ish channel, 2026-05-05 — announcement of a Wyndham audit system she's built in CoWork over the last few weeks.
  - Notion: "Wyndham Audit Workspace" under Customer Success Homebase → Enterprise → Wyndham Connect. Two databases: **Audit Runs** (14 runs visible, 2026-04-13 → 2026-05-18) and **Tickets** (Notion + Linear).
  - Linear teams she's routing into: **CSANA** (CS Analytics) and **CUSTOPS** (CustOps). Notion tickets go to Jessica Cervantes or Marta Ziaei.

  ### What Ani built
  A rules-based audit framework run in **CoWork natural language** (not code yet) that cross-references:
  - **Omni** (Canary's source of live config — Property Activation, Messaging Status, PMS Integrations)
  - **Salesforce** (commercial source of truth — go-live dates, opp status, room counts)
  - **Wyndham SmartSheets / Master Site List (MSL)** (Wyndham's source of truth for which properties should be live, opt-outs, Status 11 closures)

  Each run produces a P1/P2/P3 finding list per rule, then auto-creates Notion or Linear tickets routed to the right human (Jessica/Marta for CS; CSANA/CUSTOPS for eng-actionable). Already cited as having dropped Wyndham CS's "what's going on with this site?" inbound enquiries significantly. Goal stated in the Slack thread: move from CoWork to real code once rules stabilise — token cost is the main driver.

  ### What CS actually cares about (the rules, decoded)
  These are the recurring rules across runs, in rough order of how much volume they generate:

  1. **Cross-system live/active-state consistency** — sites flagged as live in one system but not another:
     - Opt-out violations: MSL says opted-out but Canary still sending (typically 30–60 sites/run; sometimes 128 in EU).
     - Status 11 closures: Wyndham officially closed the property but Canary is still live (treated as P1 Critical — e.g. 00737 Days Inn Fort Wright).
     - Sites missing from Smartsheet entirely (~10 per EU run).
     - Sites live in Canary but MSL marks inactive (Status 7) — 100+ in some NAMER runs.

  2. **Product enablement gaps on already-live sites**:
     - "Partial enablement" — site has some WCP products but not others (the biggest single bucket — 90–95 sites/EU run).
     - Voice AI gaps on sites past go-live (22 in one delivery audit).
     - Authorizations gaps on sites past go-live (7 in same audit).
     - Sites with products on but 0 messages sent (R9).

  3. **Premature / late activation timing**:
     - Future go-live sites already sending messages (R6).
     - Sites with no go-live date but sending (R10).
     - PMS mismatches between Omni and Smartsheet (R7) — usually on pre-live sites and often false positives once date-filtered.

  4. **Room-count discrepancies** — Wyndham Voice is billed per-room-per-month, so MSL ↔ SF room mismatches directly hit billing. Examples called out by name: La Quinta Nashville Airport/Opryland (MSL 134 vs SF 82), Reside Seattle Downtown (55 vs 50). Routes to CSANA in Linear.

  5. **Message deliverability degradation**:
     - SMS sites with <90% success / ≥60% failure — 74 of 126 sites in the 2026-05-18 run, 13 of those at 100% failure.
     - Same audit for WhatsApp — 10 sites flagged, 5 at 100% failure (Wyndham Grand Carvoeiro Algarve: 276 msgs, 0.7% delivery).
     - Sites with messaging enabled but 0 delivery (R9 cross-cut).
     - Generates consolidated CUSTOPS tickets (e.g. CUSTOPS-3093, 3094, 2580).

  6. **GJM (Guest Journey Message) configuration drift** — R4 in the rules, lower volume but recurring.

  ### Audit types in the catalog
  Data Quality Audit (the bulk), Message Delivery Audit, Status 11 Update, plus placeholders for QA/Compliance/Integration/Security/Performance/Process/Configuration/Message Deliverability — those last ones look aspirational, not yet running.

  ### Themes worth pulling into eng work
  - **Single source of truth alignment** is the meta-concern. Ani's audits exist because Omni/Salesforce/Wyndham MSL drift constantly and there's no automated reconciliation in product. The repeated rule re-runs (v1→v2→v3→v6→v6.1→v7) show how much rule tuning is needed just to filter false positives — strong signal that "deviation from happy state" is a real product gap, not just a CS process gap. (Matches the existing Linear project framed exactly this way per Bear notes.)
  - **Billing-adjacent data quality** (room counts → Voice charges) is the highest-leverage finding type. If Canary had authoritative room-count sync from PMS/SF, this whole bucket goes away.
  - **Opt-out + Status 11 propagation** is a recurring P1. A Wyndham closure should hard-stop messaging in Canary; today CS has to manually run a "cut parent ties script" via Jessica Cervantes after Ani's audit flags it.
  - **Deliverability monitoring** is something CS is doing in spreadsheets via Ani — would be a natural fit for our existing Datadog/observability stack as a proper alert rather than weekly CSV review.
  - Ani's longer-term ask in the Slack thread is **"a proactive audit layer across our customer data, regularly reviewing our systems and raising issues to the appropriate CSM."** That's basically the brief for a productised version of what she's prototyping in CoWork.

  ### Pointers for follow-up
  - Slack: canarytechnologies.slack.com/archives/C0B1DFKN7V1/p1777974956596889
  - Notion DB (Audit Runs): /canarytechnologies/2a41fd1409f74f339e42d442286fef33
  - Notion DB (Tickets): /canarytechnologies/2fda7f7d30984d198396ab6373e1f9d4
  - Workspace parent: "Wyndham Audit Workspace" → Wyndham Connect → Enterprise → Customer Success Homebase
  - Linear example tickets surfaced: CUSTOPS-3093, CUSTOPS-3094, CUSTOPS-2580, CSANA-186
  - Key humans: Ani Ghazarossian (author), Gurtej Gill (CoWork/CS-eng), Jessica Cervantes & Marta Ziaei (action owners), Nensy Auzina (asking the "why move to code" question)
project: 2026-04-16T1348-ideas
source_id: null
tags: []
time_minutes: 5
title: Use Ani's audit stuff to figure out what CS cares about
updated: 2026-05-21 09:52:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C0B1DFKN7V1/p1777974956596889
