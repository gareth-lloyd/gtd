---
area: management
completed_at: null
contexts:
- consume
created: 2026-08-04 10:41:27.889744
defer_until: null
due: 2026-08-04
energy: high
id: 2026-08-04T1041-read-asher-s-pms-capabilities-driven-config-notes
order: null
output: |
  ## Agent run 2026-08-04T11:22:16

  Read both of Asher's Notion docs. Pre-sync briefing:

  **Docs**
  - Sync on PMS capabilities-driven configuration (meeting agenda): https://app.notion.com/p/3ac8146861518007b0f8e4fd9d5c416e
  - Capability-Driven Config Drift Detection (eng design, optional detail): https://app.notion.com/p/3b18146861518073a23dd5241ddc8b6b — superseding design for TOOL-294, replaces the abandoned v1 read-time-merge; crit-approved 2026-08-03, now up for team review.

  **Resolved decisions**
  - One system, not two; config columns stay authoritative (no reader migration); enterprise keeps script-based setup.
  - Keeping from Asher's project: kafka/observation pipeline, HotelConfigFieldOverride audit layer, capability-derived predicates, admin provenance. Reusing Drift Detection's tree-based rule resolution with a non-enterprise fallback root.
  - Design record D1-D6 + 21 decisions incl.: strict healing of deviations; admin edits auto-create override rows (reason required, FINAL rejected); writer runs inside sync_gateway_state (3h cron); migrating hotels auto-activate; kill switch = rollout flag that stops the writer.

  **Open questions for the sync**
  - Directed at ME (Gareth): when will drift-detection writes be implemented? Asher wants a shared approach or offers to take the lead. Have an answer ready.
  - Directed at Ian: is a write-based config approach okay?
  - Does the fallback root catching enterprise brands not yet in the tree matter?
  - Process gripe: design was approved then rejected twice after dev started; Asher proposes an eng-design-summaries Slack channel.

  Slack thread: https://canarytechnologies.slack.com/archives/C0AMJPBUH60/p1785803212077869?thread_ts=1785803212.077869&cid=C0AMJPBUH60
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C0AMJPBUH60/p1785803212077869?thread_ts=1785803212.077869&cid=C0AMJPBUH60
tags:
- morning-gtd
- slack
time_minutes: 30
title: Read Asher's PMS-capabilities-driven-config notes before today's meeting
updated: 2026-08-04 14:40:13.627886
waiting_on: null
waiting_since: null
working_on: true
---

Asher @mentioned me + Ian: skim the high-level overview of resolved decisions and open questions before the sync (eng design doc optional). Docs: 'Sync on PMS capabilities driven configuration' + 'Capability-Driven Config Drift Detection' in Notion.
https://canarytechnologies.slack.com/archives/C0AMJPBUH60/p1785803212077869?thread_ts=1785803212.077869&cid=C0AMJPBUH60