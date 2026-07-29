---
area: null
contexts: []
created: 2026-07-28 14:43:26.523902
defer_until: null
due: null
energy: low
id: 2026-07-28T1443-read-and-digest-this-document-conclusions
order: null
output: |-
  ## Agent run 2026-07-28T15:05:00

  Read and digested https://pages.cnry.cloud/2026-07-27-oncall-analysis (Oncall Analysis Brief, July 27 2026; data window Sep 25 2025 – Jul 27 2026, Linear issue data incl. archived, ~95% label coverage).

  ### Core thesis
  AI routing (launched Feb 23) has hollowed out the Oncall queue: intake is stable at ~870 issues/month, AI routes 74% (3,382 issues) to 29 teams, and 71% of those are already completed at their destination. Hand-moves fell 2,553 → 400 per five-month window. What remains (800 kept issues, down from 1,617) is no longer an engineering queue — it is an account-administration queue: 81% user/access management (652 issues), 8% troubleshooting (62, down 86%), 5% config (41), 3% compliance exports (23), <1% product bugs (5). User creation is the only growing category.

  ### The real headline: Kevin is a single point of failure
  651 of the 800 kept issues (81%) are handled by one person (Kevin), ~130/month, median resolution 2.5h. His early-July vacation redistributed the queue across six people and hand-moves jumped 56 → 84 over his eight working days away, with routine work leaking into product teams. The system works because of one person, not because of process.

  ### Recommendations in the doc
  1. Transfer user management to Support with admin permissions; automate form-driven creation (363 requests arrived via structured forms — highly automatable); self-service portfolio management + SCIM provisioning.
  2. Automate recurring compliance exports (TOOL-457, TOOL-458 already in progress).
  3. Expose admin tooling to customer-facing teams for config work (follow the custom-domain self-service model).
  4. Keep only the ~8-9 genuine engineering troubleshooting issues/month in engineering.

  ### My conclusions
  - The AI routing project has succeeded at its goal (74% auto-routed, 7.8% misroute rate — 263 flagged and re-homed, and those were corrections between product teams, not returns to Oncall). The remaining queue problem is organizational, not routing.
  - The right next move is NOT more routing improvement — it's moving user management out of engineering Oncall entirely (Support + admin tooling + SCIM). That eliminates ~81% of the kept queue and defuses the Kevin dependency in one motion.
  - The Kevin SPOF should be treated with urgency: the July vacation was a live fire drill and it degraded measurably. If he leaves, the queue model breaks immediately.
  - Caveats worth remembering when quoting numbers: assignment ≠ effort; buckets use fixed priority-order (edge cases are judgment calls); intake label covers ~95% of Oncall issues so totals run a few % low; priority values are current-state not creation-time; password resets assumed non-engineering though some may hide real bugs.

  Possible follow-ups (user's call): track TOOL-457/TOOL-458 progress; check whether a SCIM/self-service provisioning initiative exists in Linear; raise the Kevin SPOF in the next eng-leadership sync.
project: null
source_id: null
tags: []
time_minutes: 5
title: Read and digest this document. Conclusions?
updated: 2026-07-28 15:41:18.582027
waiting_on: null
waiting_since: null
working_on: false
---

https://pages.cnry.cloud/2026-07-27-oncall-analysis