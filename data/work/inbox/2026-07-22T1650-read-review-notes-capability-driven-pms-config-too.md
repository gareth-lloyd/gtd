---
area: null
contexts:
- consume
created: 2026-07-22 16:50:42.921202
defer_until: null
due: null
energy: low
id: 2026-07-22T1650-read-review-notes-capability-driven-pms-config-too
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: 10
title: 'Read review notes: Capability-Driven PMS Config (TOOL-294) — CONSISTENCY fit
  & read-time-vs-write tradeoff'
updated: 2026-07-22 21:39:41.152292
waiting_on: null
waiting_since: null
working_on: false
---

Private Notion doc: https://app.notion.com/p/3a5814686151819086aff2e08a335da6

Reviewed doc: Capability-Driven PMS Config (TOOL-294).

Two findings from the review session:
1. The read-time merge is a strong use case for rules_based_configuration CONSISTENCY rules — the doc omits that layer entirely. Notes cover the one-method seam (as_settings_dict), four enforcement points, and a timely CapabilityDefaultRule tweak while T2 is unshipped.
2. Bigger finding: read-time merge reintroduces the read-site-migration cost that rules_based_configuration deliberately ruled out in favour of write-onto-columns + drift detection. Includes the circular-justification / silent-failure argument, where the doc is defensible (v1 = 17 fields) vs not (end-state = all readers), and the synthesis (keep observation-history + override audit — both portable to the write model — drop the read migration).

Ends with key forking points and a drafted (unsent) Slack message to the author.