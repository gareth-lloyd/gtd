---
area: null
completed_at: null
contexts: []
created: 2026-09-16 14:54:38.205014
defer_until: 2026-09-21 09:00:00
due: null
energy: low
id: 2026-09-16T1454-ping-joshua-to-ask-if-he-needs-input-on-rules-base
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: 5
title: ping joshua to ask if he needs input on rules based
updated: 2026-09-18 15:18:38.872750
waiting_on: null
waiting_since: null
working_on: false
---

1. Review PR #56000 (https://github.com/canary-technologies-corp/canary/pull/56000). This is SDM-5039, the ticket you filed about rules reading nonexistent keys. Luiza
     implemented it as a Django system check because pyrefly silently stops enforcing large Literal unions, so the static-typing design in your ticket did not work. Joshua
     approved. abrad only left comments, and jordan-canary is also requested. Linear marks the umbrella SDM-4862 as blocked by this ticket, so it is the last gate on their
     milestone due 2026-09-17.
  2. Triage ENT-7488 (https://linear.app/canary-technologies/issue/ENT-7488). Luiza filed it in Enterprise Triage on 2026-09-09 asking for gateway and PMS capabilities as settings
     keys. It is your ENT-6097 Part 2 proposal plus gateway capabilities, and needs a derived-key mechanism the vocabulary does not have yet. It does not block them, but the
     engine-side half of SDM-4991 waits on it. Their PR #55833 ships the check on the admin checker surface as a stopgap.
  3. Confirm or refute the two deposit-slot rules they dropped from your ENT-5030 draft in PR #55352. Luiza's review found no code coupling between the deposit slot and the
     auto-post CC flag, and replaced it with a rule keyed on the seven PMS adapters that raise without a slot. Her note invites you to bring the rules back with a code citation if
     your incident evidence says otherwise.
  4. Workstream E co-build. Your team offered on 8/5 to co-build Four Seasons and ESA brand profiles plus template and named-config packages. That milestone sits at 6% with a
     target date of 2026-09-03 already passed. Expect them to ask what your side can commit.
  5. Review turnaround. SDM-4862 notes they expected slow Enterprise review while the drift project was paused. A named reviewer for SDM PRs touching the rules engine would remove
     that friction.

  Two items from my earlier overview are no longer asks. ENT-7103 (explanation messages on rules) is Done since 2026-09-10 and ENT-7113 (scope US-centric rules by region) is
  Deployed since 2026-09-14. Worth confirming whether the new explanation field reaches consistency errors, not just drift specs, since their rule messages currently carry the
  full remediation text as a workaround.

✻ Baked for 1m 19s · done 14:53