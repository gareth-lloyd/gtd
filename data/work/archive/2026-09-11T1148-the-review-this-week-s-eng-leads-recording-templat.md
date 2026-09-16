---
area: null
completed_at: 2026-09-16 09:14:52.320868
contexts: []
created: 2026-09-11 11:48:18.172023
defer_until: null
due: null
energy: low
id: 2026-09-11T1148-the-review-this-week-s-eng-leads-recording-templat
order: null
output: |-
  ## Agent run 2026-09-11T11:49

  **Cause:** weekly templates have no weekday field. `gtd_core/recurring.py` anchors
  the schedule on `last_spawned` and walks forward in 7-day steps. The template's
  `last_spawned` was 2026-09-07 (a Monday), so it kept spawning on Mondays.

  **Fix (data only, no code change):** in
  `data/work/templates/2026-07-13T1042-review-eng-leads-recording.md`, changed
  `last_spawned: 2026-09-07` → `2026-09-04` (a Friday).

  Checked against the real `next_upcoming_spawn_date`:
  - today (Fri 2026-09-11) → due today, so the next Sync/snapshot spawns it
  - then Fri 2026-09-18, Fri 2026-09-25, …

  I picked 09-04 rather than today's date on purpose. The Monday 09-07 instance
  (already archived) covered the 09-03 meeting, so spawning today covers
  yesterday's (Thu 09-10) meeting with no week skipped. If you'd rather not get
  one today, set `last_spawned: 2026-09-11` and it starts next Friday.

  **Not done yet:** I haven't run a snapshot or commit. The template edit is
  uncommitted and will go in with your next Sync.

  **Related:** "Review Friday's show & tell recording"
  (`templates/2026-06-23T1336-review-friday-show-and-tell-recording.md`) is also
  anchored on Monday 09-07. I left it alone because that wasn't this task. Say
  the word if you want it moved to Fridays too.

  **Possible follow-up:** "spawn on day X" only lasts as long as nobody edits
  `last_spawned`. An optional `weekday:` field on templates would make it
  explicit and editable in the Templates UI.
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: The "Review this week's Eng Leads recording" template should spawn on friday
updated: 2026-09-16 09:14:52.320854
waiting_on: null
waiting_since: null
working_on: false
---