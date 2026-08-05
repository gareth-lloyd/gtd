---
area: null
completed_at: null
contexts: []
created: 2026-08-04 15:12:27.373761
defer_until: null
due: 2026-08-05
energy: low
id: 2026-08-04T1512-read-stephanie-s-user-management-notion
order: null
output: |
  ## Agent run 2026-08-05T13:40:00
  Read the doc in full: "User Management & Triage Efficiency — Aggregated Overview"
  (https://app.notion.com/p/canarytechnologies/User-Management-Triage-Efficiency-Aggregated-Overview-3b18146861518163a0d4cff07c3389e3),
  compiled 2026-08-03 by Stephanie from the Q3 Block 2 goal, Lautaro's Managed Support
  Access proposal, the SAG PRD/eng design, the User Management Ticket Analysis, and
  Support <-> Internal Tools Slack threads.

  Framing: Canary spends 20-30% of eng time on triage/oncall — the Q3 Block 2 focus.
  For Internal Tools, user management IS the triage load, so the pod goal maps ~1:1
  to "get user management off the rotation". Metrics being made visible: # Oncall
  issues, % Zendesk->Oncall, resolution latency p50/p90, Workup agent "next step"
  acceptance rate.

  Key data (Laura's 810-ticket audit + Lauta's July cross-team cut):
  - User management = 78% of the Oncall queue (606 tickets in scope).
  - 93% of those are self-serviceable by a trained agent (no eng, no chain SSO).
  - 83% concentrate in just TWO actions: grant/modify role+permissions, and
    create-user/link-to-property.
  - 38% are bulk requests -> any tool must be batch-first, not one-at-a-time.
  - ~50 tickets blocked by chain SSO governance (Marriott/Wyndham/IHG) -> a
    SCIM/provisioning lever, not a support-agent lever.
  - Sources: 46% structured intake (CSM form), 40% Zendesk, 14% ad-hoc Linear.
  - Op-level cut of 691 ENT+ONC tickets: create-new-user 34%, bulk 24%, link
    user->hotel 12%, role change 10%, above-property role 9%.

  Nine problem groups tabulated with "eligible for trained support?" verdicts.
  Eng-only remainders: SSO/org-mapping issues, duplicate-account merges (no safe
  tooling), and permission-model gaps that are real bugs. Portfolio changes are
  partial (ENT is giving CS Django access to manage portfolios now).

  Four solution tracks:
  - A. SAG (Support Access Grant): phased rollout underway, open to all staff
    (PR #48223, TOOL-313); 24h ephemeral PM user via Slack approval. ENT blocks
    being added. PRD: https://app.notion.com/p/4150b263e21c41c6bbf16cbe2461bbf0
  - B. Managed Support Access (Lauta's proposal — granular audited actions
    instead of impersonation): proposal stage.
    https://app.notion.com/p/3ae81468615181abbf82ea4f92ef9794
  - C. SCIM/SSO auto-provisioning for big chains: eng design In Review
    (ENT-6491, https://linear.app/canary-technologies/issue/ENT-6491), low
    priority, implementation not scoped.
  - D. Trained L2 support + single intake route: direction agreed, needs
    Blake sign-off then Nensy. 1-pager:
    https://app.notion.com/p/3b181468615181379feaf4829fa5355b

  My read / possible follow-ups (not actioned): the ENT-relevant hooks are the
  "ENT giving CS portfolio access in Django" work (row 7), the ENT SAG blocks,
  and the ~50 chain-SSO tickets ENT absorbs today that option C would drain.
  Option D is the near-term unlock and is only blocked on sign-off. Note the
  doc has an open discussion thread on the data table ("Value" column).
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Read Stephanie's user management Notion
updated: 2026-08-05 13:41:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/User-Management-Triage-Efficiency-Aggregated-Overview-3b18146861518163a0d4cff07c3389e3?source=copy_link