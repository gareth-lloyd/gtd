---
area: null
contexts:
- react
created: 2026-07-24 09:26:13.749559
defer_until: null
due: null
energy: medium
id: 2026-07-24T0926-reply-to-laura-re-investigator-expansion-cost-valu
order: null
output: |
  ## Agent run 2026-07-24T09:45

  Read Laura's full DM (https://canarytechnologies.slack.com/archives/D07U6KK5W1G/p1784836250809019)
  and sanity-checked her numbers — they hold up:
  - Cost: 23 routed/day x $11 avg x 30d = ~$7.6k/mo (matches her $7.5k). Sept standard
    pricing ~1.47x = ~$11k/mo, plausible if runs are on Sonnet 5 intro rates.
  - Value: 60% x 23/day = ~14 correct diagnoses/day; at 15-30 min saved each that is
    3.5-7 h/day = 0.44-0.88 FTE (matches her 0.5-0.9).
  - Weak point: accuracy sample is only ~30 resolved tickets, so 60% has a 95% CI of
    roughly +/-18pts (~42-75%) — and it was measured mostly on PMS/SDM, which have
    dedicated context gatherers.

  Bear notes context: expansion thesis from Stephanie Barry 1-1 (Jul 23) is to take the
  investigator from unscaled internal tool to a proper product path, with routing
  accuracy as a named workstream (Bear: "Stephanie Barry 1-1", "Triage agent"). Andres
  Figueira has an overlapping triage skill (KB + Datadog context + similar tickets/PRs)
  worth folding in as a context gatherer for teams that lack one (Bear: "Andres Figueira").

  DRAFT REPLY (NOT SENT — needs your approval; say "send it" or edit first):

  ---
  Thanks for pulling this together — the numbers hold up (I re-ran the math) and the
  value case clears the bar even at the Sept price. My call: yes to the staged per-team
  rollout, gated on two things first:

  1. Productionize your accuracy dashboard — per-team accuracy vs eventual resolution is
  the go/no-go signal for each stage, so it needs to be off your laptop and visible
  before we expand.
  2. Spend guardrails — a per-investigation cap (your range hit $30) and a monthly budget
  alert, so a bad loop can't quietly multiply the bill.

  Then stage it: pick the next 1-2 teams by ticket volume, preferring ones where a
  context gatherer already exists or is cheap to build (worth looking at whether Andres's
  triage skill covers some of that). Run each team ~2 weeks; keep it on if accuracy holds
  (I'd say >=50% given the value math still clears at that level), pause and build
  gatherers if it doesn't.

  Two things to firm up as we go: (a) the 60% is on ~30 resolved tickets so the true
  range is wide (+/-~18pts) — the dashboard will tighten that as volume grows; (b) can
  you confirm whether our runs are actually billing at intro rates, so the ~$11k Sept
  number is real? If it is, we can also look at dropping simpler ticket classes to a
  cheaper model before September.

  Can you sketch the proposed team order + gatherer gaps and we'll lock the first stage?
  ---

  Nothing was sent to Slack or any external service.
project: null
source_id: https://canarytechnologies.slack.com/archives/D07U6KK5W1G/p1784836250809019
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Reply to Laura re: investigator expansion cost/value numbers'
updated: 2026-07-24 10:06:00.505957
waiting_on: null
waiting_since: null
working_on: false
---

DM Jul 23: expanding investigator to all eng-routed tickets ≈ $7.5k/mo now (~$11k/mo from Sept at standard pricing) vs ~$950 today; ~60% root-cause accuracy ≈ 0.5–0.9 FTE of triage saved. She suggests staged per-team rollout + per-team accuracy dashboard. Needs your call on next step.
https://canarytechnologies.slack.com/archives/D07U6KK5W1G/p1784836250809019