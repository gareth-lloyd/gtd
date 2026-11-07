---
area: null
completed_at: 2026-11-06 16:26:55.139776
contexts:
- react
created: 2026-11-06 10:24:21.906358
defer_until: null
due: null
energy: low
id: 2026-11-06T1024-reply-to-laura-dewald-re-mobile-pod-triage-coachin
order: null
output: |-
  ## Agent run 2026-11-06 16:21:33

  **Verdict: Laura is right, and the data says it is a queue-ownership problem more than a judgment problem. Mobile has no triage rotation; AD does.**

  ### What the two tickets show
  - MOB-1334 (https://linear.app/canary-technologies/issue/MOB-1334/no-notifications-get-sent-through-the-staff-app): in Mobile Triage since 2026-10-08 (29 days), SLA breached 2026-10-11, unassigned. Workup posted a high-confidence root cause 11 minutes after creation (Hotel.enable_push_notifications rollout flag off for the 4 hotels; a config change, label "Next Step: Config Change"). Nobody actioned it. Cristina chased 10-14 and 10-16; Diana replied 10-19 that a project would ship "by end of week" and asked how to update the ticket. Nothing since.
  - AD-10713 (https://linear.app/canary-technologies/issue/AD-10713/keyboard-not-appearing-in-canary-app-on-ipads-hotel-arts): Workup routed to Mobile (high confidence) 2026-10-22. Sat in Mobile Triage 14 days with zero engineer comments, SLA breached 10-25, Boybit chased 10-28 and 11-05. Moved to AD on 11-05; Federico (AD triage on-call this week) engaged within hours and flagged the app in the screenshots is not even our kiosk app. Mobile never looked.

  ### It is a pattern
  Mobile Oncall-labelled tickets created in the last 60 days: 9. Left Triage: 1 (MOB-1321, same day). SLA tickets already breached: MOB-1334, MOB-1372 (https://linear.app/canary-technologies/issue/MOB-1372), MOB-1174 (assigned to Caitlyn but still in Triage since August). MOB-1473 (https://linear.app/canary-technologies/issue/MOB-1473), a Groundcover Staff Ops push-failure alert, breaches 2026-11-07. Three more carry Workup Next Step labels (Config Change, Duplicate, Feature Request) nobody has closed out.

  ### Structural cause
  Linear triage responsibility: AD has a weekly rotation (Federico, Pat, Matthew, Bruno, Elena) with action "notify". Mobile has triage enabled, no rotation, no responsible user. Nothing pings anyone when a ticket lands in MOB.

  ### Ownership wrinkle (from Bear notes)
  - Jason handed the Mobile pod's people side to me in Sep 2026, so this is mine to fix, not something to coach from the outside.
  - Per Blake, the Staff App is owned by James Lovatt's staff ops team now; Mobile core keeps Lattice. MOB-1334 and MOB-1473 are both staff-app push tickets routed to MOB (TOOL-831 "Route Staff App issues to the Mobile team"). Worth deciding with James whether staff-app oncall belongs in MOB or a staff-ops team before adding a rotation.
  - Eric (21 Oct): many mobile bug reports are already-fixed issues IHG has not pulled, so the pod has learned to discount inbound reports. That is the judgment part Laura is sensing.

  ### Draft reply to Laura (DM D07U6KK5W1G, not sent)
  Agree, and it's broader than those two. I pulled the Mobile triage queue: of 9 oncall tickets routed to MOB in the last 60 days, one left Triage. Three SLA tickets have breached (MOB-1334, MOB-1372, MOB-1174) and MOB-1473 breaches tomorrow. MOB-1334 had a Workup config-change diagnosis 11 minutes in and nobody actioned it; AD-10713 sat 14 days with no comment until it moved to AD and Federico picked it up within hours.

  Root cause is structural before it's coaching: AD has a Linear triage rotation with notify, Mobile has none, so nothing pings anyone. Mobile reports to me now, so this one's mine. Plan: (1) set a MOB triage rotation this week, (2) sort out with James whether staff-app oncall (MOB-1334, MOB-1473, TOOL-831 routing) should live in MOB or staff ops, (3) run the queue down with Diana and Francisco, starting with the Workup next-step labels that are minutes of work. Will loop you in on the staff-app routing question since it touches Workup.

  ### Suggested follow-ups (not captured)
  - Set Mobile triage rotation in Linear (needs team admin).
  - Talk to James Lovatt re staff-app oncall ownership and TOOL-831 routing.
  - Queue-clear session with Diana and Francisco; MOB-1473 breaches 2026-11-07.
project: null
source_id: https://canarytechnologies.slack.com/archives/D07U6KK5W1G/p1793919294278489
tags:
- morning-gtd
- slack
time_minutes: 10
title: 'Reply to Laura DeWald re: Mobile pod triage coaching for SLA tickets'
updated: 2026-11-06 16:26:55.139756
waiting_on: null
waiting_since: null
working_on: false
---

Laura: Mobile pod may need coaching on Triage, especially SLA tickets. Examples: AD-10713 (keyboard not appearing on iPads, Hotel Arts) and MOB-1334 (no notifications through staff app).
https://canarytechnologies.slack.com/archives/D07U6KK5W1G/p1793919294278489