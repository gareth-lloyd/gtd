---
area: null
completed_at: null
contexts: []
created: &id001 2026-11-24 15:35:27.769802
defer_until: null
due: null
energy: null
id: 2026-11-24T1535-workup-accuracy-next-steps-from-the-confidence-che
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: null
title: 'Workup accuracy: next steps from the confidence check'
updated: *id001
waiting_on: null
waiting_since: null
working_on: false
---

Finding (24 Nov, local mirror snapshot workup-20261123-080952Z, 711 graded declarations, 21 Sep to 22 Nov):
Workup's stated confidence predicts being wrong. High: next step right 230 of 439 (52%). Medium: 81 of 249 (33%). Evidence-gap signals (tool gaps, budget exhaustions) predict nothing.
Hand off is the de facto "not sure" box: 35% of medium-confidence tickets go there and are right 22 of 87.
"Ask for more info" was the right answer on 13 of 711 (2%); Workup's asks were right 0 of 33.

Next steps:
1. Cost a second investigation pass on medium-confidence runs. Being unsure is mostly about the cause.
2. Report medium-confidence hand-offs separately on the dashboard, so they stop dragging the Hand off number.
3. Propose gating auto-actions on high confidence (config 66%, no-action 70%; still short of the 90% bar).
4. Re-run the confidence cut on blind-graded rows only, to confirm it holds.
5. Fix the talking points: remove item 5 (request-info as note) and item 8 (name an owner). Add the confidence finding.
6. Orbital feedback: reword the grader bullet. Jason's agents#473 and #474 reuse today's judges, are unreviewed since 22 Oct, and test only the last two stages. Find a reviewer.
7. Raise on the Workup Improvement Plan (Notion): the unlock bar (15 actions at 90%) passes by luck about 1 time in 6; audit closes that stayed closed; reconcile "don't widen" with Actioning for Messaging.
8. TOOL-838 steps 1 and 3 as a precondition for Orbital parallel validation.

Scripts: scratchpad conf.py (session c4f4563f). Notes: backend/canary/tmp/data/workup_accuracy/NOTES.md