---
area: null
completed_at: 2026-10-20 21:53:37.897321
contexts: []
created: 2026-10-20 16:10:41.147692
defer_until: null
due: null
energy: null
id: 2026-10-20T1610-follow-up-on-workup-7d-accuracy-slip-19-right-next
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: null
title: Follow up on Workup 7d accuracy slip (19% right next step, Oct 14-20)
updated: 2026-10-20 21:53:37.897315
waiting_on: null
waiting_since: null
working_on: false
---

Investigated 2026-10-20 from agents.cnry.land/workup (7d) and #project-workup. No single regression; model still pinned to Sonnet 5.

Headline: right next step 12/64 (19%) vs 35% prior week, 33% for Sep 21-Oct 13. Hypothesis accuracy flat (67% vs 68%). n=64 so ~±10 pts noise.

Where it dropped:
- PMS tickets 2/23 (9%) vs 26% baseline; SDM 0/7; MSG 7/21 (33%) vs 48%.
- Config Change recs 29% right (was 52%), Duplicate 25% (was 56%), Ops Action 0/6 (was 32%).

Miss patterns (53 misses):
- 13 ended as Config Change on PMS gateway settings Workup can't read (parser version, folio window, push_down_reg_card_info_early, HotelKey property ID mappings). SQL tool can't reach PMS Gateway (Laura's Sept 18 gaps doc).
- 13 closed as No Action / working as expected where Workup said Escalate (5), Feature Request (3), Config Change (2). TOOL-833 only remaps expected_behavior/transient causes.
- Judge boundary calls: Ops Action vs Config Change (PMS-11273, PMS-11277); Oct 8 judge prompt change on unanswered asks (PMS-11224, SDM-5216, SDM-5231); 5 near-misses (right bucket, wrong object) counted as wrong.
- MSG-5578 hub: 3 tickets closed as dupes of it that Workup called Config Change/Code Fix; CUSTOPS-6129 Workup called dupe of it, resolver rejected and changed a setting.
- Context gaps correlate: 0 gaps 31% right vs 1+ gaps ~15%.

Changes in window, none confirmed as cause: Oct 8 judge prompt (#408), Oct 9 plugin 1.39 (TOOL-833/839), Oct 14 MCP opt-in + EU/AP SQL, Oct 15 compact report, Oct 16/19 config auto-close, Oct 19 config checks.

Slack: Mati's Oct 19 reports (MSG-6638 misclassified as integration-sync, Laura fixing; MSG-6643 multi-issue tickets) not graded yet.

Follow-up candidates: raise PMS gateway settings visibility with Laura/Asher; ask whether near-misses should count as partial; check if the judge's Ops-vs-Config line matches how PMS resolves tickets; watch whether next week's number recovers.

Data: scratchpad workup7d.json / workup30d.json (session 934b505d).