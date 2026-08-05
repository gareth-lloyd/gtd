---
area: null
completed_at: 2026-08-05 15:07:22.681524
contexts: []
created: 2026-08-05 14:06:57.939538
defer_until: null
due: null
energy: low
id: 2026-08-05T1406-read-andrea-s-analysis
order: null
output: |
  ## Agent run 2026-08-05T14:30:00+03:00

  Read Andrea's analysis. Slack post (2026-08-04, #ent channel):
  https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1785852366136769
  Notion doc: "ENT Support & Triage Ticket Analysis — Jun 22 – Aug 3, 2026"
  https://app.notion.com/p/canarytechnologies/ENT-Support-Triage-Ticket-Analysis-Jun-22-Aug-3-2026-3b2814686151813cb2c8e53d73992dd4
  (Written by Claude with Andrea's guidance; inspired by Laura's earlier analysis. Adversarially
  spot-checked: 45/48 agree, 0 disputes.)

  ### Headline numbers (217 triage tickets over 6 weeks, vs 208 prior 6 weeks)
  - ~373 engineer-hours ≈ 62 h/week ≈ 1.5 FTE on reactive triage.
  - Latency halved vs baseline: p50 2.2d → 1.1d, p90 25.1d → 12.0d. Volume up ~9%.
  - Action modes: 53% needed NO code change, 26% one-off DB scripts, only 20% PRs.
  - Blocked tickets (42, 19%) carry 8x latency; 57% of blocked time is waiting on CUSTOMERS.

  ### Top effort sinks (68% of hours in 6 clusters)
  1. SSO 65h/28 tickets — biggest sink, 10 blocked on customer IdP/IT.
  2. User access 47.5h/47 — 42/47 CS-servable; the SAG / trained-L2 target; not shrinking.
  3. Loyalty 45.8h/17 — 3x baseline, single root cause: Wyndham Tally alert storm (15
     recurring alerts re-ticketing every firing). Fix once, delete the category.
  4. PMS integration 42h/9 — p50 latency 59 DAYS; misroute cluster that should go to
     INT/PMS-Gateway per catalog rule that isn't being applied.
  5. Wyndham onboarding script failures 28.5h/10.
  6. Transitions/rebrands 27.8h/17 — doubled vs baseline, DB-script + tribal-knowledge heavy.

  ### Solution levers proposed (A–G)
  A. SAG + trained L2 for user access/portfolio (~40h/6wk addressable) — rollout underway.
  B. Root-cause Wyndham Tally alert storm + monitor dedup (~40h/6wk) — NEEDS OWNER.
  C. Enforce cluster-9 PMS misroute routing + straggler review in cycle planning (~42h + tail).
  D. SCIM/SSO auto-provisioning + diagnostics (ENT-6491, currently low priority — data argues
     for raising it).
  E. Promote recurring DB scripts to admin tools/mgmt commands (portfolio add/remove,
     deactivations, user merge — 57 DB-script tickets).
  F. KB articles for catalog gaps (clusters 6/9/12 + flaky-test triage + brand onboarding ops).
  G. Customer-wait hygiene: request templates + nudge/auto-close (~427 blocked-days visible).

  ### Notable for you
  - Levers B (needs owner) and C (routing rule exists but unenforced) are management calls —
    cheapest wins on the list.
  - Lever E overlaps the existing "run analysis of what we can automate from CS scripts"
    next-action already in your GTD.
  - D is ammunition to reprioritize ENT-6491 (SCIM/SSO) — SSO is the single biggest effort sink.
  - Full 217-ticket appendix is a child page of the Notion doc.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: read andrea's analysis
updated: 2026-08-05 15:09:32.005083
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1785852366136769