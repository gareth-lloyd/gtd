---
area: null
contexts: []
created: 2026-07-29 15:13:23.375502
defer_until: null
due: null
energy: low
id: 2026-07-29T1513-adjust-hte-gtd-task-to-not-pull-out-triage-items
order: null
output: |
  ## Agent run 2026-07-30T13:35:00+01:00

  Done. Modified the /gtd skill (~/.claude/skills/gtd/) so ENT triage items no longer
  become inbox actions, while the triage queue is still analyzed for serious issues.

  Changes:

  1. fetchers/linear.py — added a procedural ENT triage-queue scan (new GraphQL query
     for ENT issues in triage state, emitted as new kind `ent_triage` with priority,
     labels, assignee, age_days facts). Previously triage items only surfaced if a
     notification happened to fire; now the whole queue is scanned every run. Watch-only:
     these items never enter notif_map, so nothing gets marked read. Dedup: if a
     notification already covers the issue, the existing item is annotated instead.

  2. SKILL.md Phase 3 — removed "Linear ENT team triage items" from ACTIONABLE; added
     explicit ACTIONABLE bullet for `kind=new_comment` (reply on my ticket or a thread
     I commented in); mentions/assigned unchanged. Added AWARE rules: `ent_triage` is
     NEVER an inbox action regardless of severity; ENT issueCreated/subscribed
     notifications with nothing addressed to me personally get the same treatment.

  3. SKILL.md Phase 4 — removed the "Triage <ID>" item template; replaced with a
     "Reply on <ID>" template for new_comment replies.

  4. SKILL.md Phase 6 — new "ENT triage watch" awareness section: only genuinely
     serious items are numbered (Urgent/High priority, prod-down, security, key
     account, many hotels); the rest collapse to an unnumbered count; severe items get
     named in the TL;DR; promotion defaults to "Look at", never "Triage". Also added a
     Phase 2 rule so dive budget isn't spent triaging the queue.

  Verified: live read-only run of the new queue fetch returned 28 ENT triage items
  with no errors (top of queue: ENT-7031, ENT-7029 (Medium), ENT-7030, ENT-7014,
  ENT-7007). Queue view: https://linear.app/canary-technologies/team/ENT/triage
  No Linear state was modified.
project: null
source_id: null
tags: []
time_minutes: 5
title: adjust hte gtd task to not pull out triage items
updated: 2026-07-30 14:39:51.637290
waiting_on: null
waiting_since: null
working_on: false
---

Modify the /gtd skill. 

I am no longer responsible for triaging ENT Linear issues

Keep the Linear check, but it should pull out issues where I have been mentioned, or where there's a reply to one of my tickets or comments. 

It SHOULD still analyze ENT triage queue and flag serious or high priority issues for my attention (not to triage)