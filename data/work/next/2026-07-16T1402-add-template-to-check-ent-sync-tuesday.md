---
area: null
contexts: []
created: 2026-07-16 14:02:51.584306
defer_until: null
due: null
energy: low
id: 2026-07-16T1402-add-template-to-check-ent-sync-tuesday
order: null
output: |-
  ## Agent run 2026-07-16T14:05

  Created weekly template `data/work/templates/2026-07-16T1404-check-ent-sync.md`
  ("Check ENT sync transcripts", contexts: [consume], energy: low, 10 min).

  The Notion link resolves to the Transcripts database under "ENT Sync — Transcripts"
  in the Enterprise Teamspace (https://app.notion.com/p/canarytechnologies/13c93352d06c4e88bb69af559237645c?v=5f62f3dba7234433870e5cfeb927403f) —
  the link is embedded in the template body so each spawned item carries it.

  Tuesday anchoring: weekly recurrence walks forward 7 days from `last_spawned`,
  so I set `last_spawned: 2026-07-14` (this past Tuesday). Verified via
  `gtd_core.recurring.is_due` over the next 14 days: due only on 2026-07-21 and
  2026-07-28, both Tuesdays. First item will spawn into the work inbox on the
  first snapshot/Sync on or after Tue 2026-07-21 (missed days are skipped, not
  caught up, so sync on Tuesdays to not miss a spawn).

  Template file is created but not committed — it'll be picked up by your next
  `manage.py snapshot` / Sync.
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: add gtd template to check ent sync every tuesday
updated: 2026-07-16 14:05:30
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/13c93352d06c4e88bb69af559237645c?v=5f62f3dba7234433870e5cfeb927403f&source=copy_link