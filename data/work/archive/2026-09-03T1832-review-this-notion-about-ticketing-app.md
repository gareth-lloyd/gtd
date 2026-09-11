---
area: null
completed_at: 2026-09-11 14:39:13.975038
contexts:
- consume
created: 2026-09-03 18:32:41.265484
defer_until: null
due: null
energy: low
id: 2026-09-03T1832-review-this-notion-about-ticketing-app
order: null
output: |
  ## Agent run 2026-09-04T15:40:00

  Reviewed: [Ticketing Escalation System](https://app.notion.com/p/canarytechnologies/Ticketing-Escalation-System-39d814686151802b8bb2c9e3ffab2335?source=copy_link)

  **Overall**: Strong, well-scoped spec. Reviewed 16 competitor products (Shiji,
  Snapfix, HotSOS, ALICE, Quore, Unifocus, Optii, Flexkeeping, hub OS, Sweeply,
  Breezeway, Jira SM, Zendesk, MaintainX, UpKeep, Limble). Core design principles are
  sound and well-justified: escalation only surfaces (never reassigns/reprioritizes),
  priority (not deadline) gates timer-chasing since every ticket gets an auto-deadline,
  permission-based routing instead of stale name lists, flood-protection batching
  above 10 simultaneous escalations, and a documented "what it deliberately doesn't do
  yet" section (shift awareness, digest, dismiss button, repeat reminders, SMS,
  Android push) that shows the scope cuts were conscious, not oversights. The 10
  worked examples are genuinely useful — they preempt most "what about X" questions.

  **Gaps / questions worth raising before build:**

  1. **Overlapping escalation reasons while already red is undefined.** All examples
     show one reason firing after the prior one cleared (e.g. unassigned → assigned →
     not-started). No example covers a ticket already red for one reason (e.g.
     unassigned) that then also trips a second reason (e.g. missed deadline) while
     still red — this is a real case, e.g. Example 4's Broken key card (10 min stall
     window, 30 min deadline): if still unassigned at 9:30pm it would hit both stall
     and deadline. Does the label/notification update, stack, or get suppressed until
     cleared?

  2. **Priority/department changed mid-flight isn't addressed.** If a ticket's
     priority is bumped from Low to Medium after it's already sat unstarted past what
     would have been the stall window, does it escalate immediately on the change, or
     does the clock start fresh from the edit? Worth an explicit rule so it doesn't
     surprise hotels.

  3. **"Other" + Low priority combination isn't demonstrated.** The doc states
     department-less tickets get stall timers "whatever their priority," but the only
     worked example (Example 7) uses Medium. A Low-priority "Other" ticket would be a
     good add to confirm the override actually beats the golden rule as stated.

  4. **Amber warning on edited deadlines.** "Created with ≤15 min to go" skips the
     amber warning. Unclear whether a deadline *edited* down to ≤15 min remaining after
     creation also skips it, or fires immediately since the window's already inside 15
     min.

  5. **Manual escalate cooldown is silent.** Pressing Escalate again within 10 minutes
     is blocked — doc doesn't say whether the presser gets any feedback (toast/error)
     or it just silently no-ops.

  6. **Minor: "within the same minute or two" (flood cap trigger)** is imprecise for
     what reads like an implementation-ready spec — worth tightening to an exact
     window before eng picks it up.

  7. **Minor: numbering restarts at 1 for both the "timers" and "human actions" lists**
     under "When tickets escalate" — likely a Notion→Markdown export artifact, not a
     content issue, but worth a glance in the source doc.

  None of these are blocking — they're the kind of edge cases that surface in the
  first week of a beta and are cheap to nail down in the doc now. The doc's own
  "known gaps" section already shows this team closes such gaps deliberately rather
  than by accident, so raising these is in that spirit.
project: 2026-09-08-mobile
source_id: null
tags: []
time_minutes: 30
title: Review this notion about ticketing app
updated: 2026-09-11 14:39:13.975033
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/Ticketing-Escalation-System-39d814686151802b8bb2c9e3ffab2335?source=copy_link