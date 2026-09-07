---
area: null
completed_at: null
contexts: []
created: 2026-09-03 22:08:29.476854
defer_until: null
due: null
energy: low
id: 2026-09-03T2208-investigate-workup-metrics
order: null
output: |
  ## Agent run 2026-09-04T12:19:23Z

  Both linked pages require interactive login I couldn't complete on your behalf:
  - https://agents.cnry.land/workup — Google SSO sign-in screen only ("Sign in with your Canary Google account"); the OAuth flow needs your account, not something I can drive headlessly.
  - https://linear.app/canary-technologies/view/next-step-tickets-69f507a962f4 — the Playwright browser session isn't logged into Linear either (hit the Linear login screen).

  Fell back to the Linear MCP (separately authenticated) to pull the same underlying data the "next-step-tickets" view is presumably built on: issues carrying the `Workup` label (applied when the Workup agent has a session on a ticket), further tagged `Workup: Investigated` and `Next Step: <category>` once the agent declares a next step (see TOOL-551 and TOOL-552, both Done).

  **Sample: 100 most-recently-created `Workup`-labeled issues** (2026-08-24 to 2026-09-04, not the full backlog — `hasNextPage: true` on this query):
  - 96/100 carry `Workup: Investigated` (agent completed an investigation)
  - Of those, 62/96 have a `Next Step: <category>` label; the other 34 were investigated but not (yet) categorized
  - Next Step breakdown (n=62): Code Fix 18, Config Change 13, Ops Action 12, Escalate 7, Duplicate 5, Feature Request 5, Request Info 1, No Action 1
  - Spans teams: PMS Engineering, Messaging, Communications Core, SDM, Integrations, CustOps, EMEA, Security, In-Stay, Arrivals/Departures, Agent Knowledge, Frontend Enablement

  Related in-flight Internal Tools work (from a title search on "workup"): TOOL-639 (SQL tool skill guidance), TOOL-620/621/635 (Teleport/MCP run_sql infra), TOOL-598 (handoff failures should fall back to a comment), TOOL-609 (Groundcover links in response), TOOL-562 (SQL tool design sign-off, In Review) — https://linear.app/canary-technologies/team/TOOL

  **Not done:** couldn't get the actual dashboard numbers from agents.cnry.land/workup (accuracy/judge scores, run volume, latency — see TOOL-473 "Workup investigation quality tracking (judge, schema, dashboard)") or the precise Linear view contents, since both need a login only you can complete. If you want the real dashboard metrics, sign in to https://agents.cnry.land/workup once (e.g. via `! `-prefixed browser command or just opening it yourself) and I can pull from there next time, or point me at an API/token for it.

  ## Agent run 2026-09-04T12:32:11Z

  You signed into https://agents.cnry.land/workup in the Playwright-controlled browser (Google session was already cached, so it landed straight on the dashboard). Full "Workup Quality" metrics, All-time view:

  **Next-step correctness** (uncalibrated — no eval run against hand grades yet, treat as directional): 26% right bucket + right object on 57 scored (+7pts vs last week). 25/57 right bucket alone. 54 of 182 resolved tickets eligible for grading (30%); 0 awaiting judgment, 1 ungradable from evidence, 9% decided mechanically. Flagged follow-up: SDM-5000 (https://linear.app/canary-technologies/issue/SDM-5000) — no bucket supportable from the evidence.

  **Accuracy confusion matrix** (declared next step vs actual; diagonal = correct): Config Change 6, Ops Action 5, Code Fix 4, Feature Request 3, Escalate 2, Request Info 0/1(!), Duplicate 4, No Action 1. Dashboard's own read: "a miss inside a confusable pair: Config/Ops, Escalate/Feature Request, or the close cluster (Feature Request/Request Info/Duplicate/No Action)."

  **Sharpness** (right object, given right bucket): Config Change 2/6, Ops Action 4/5, Code Fix 3/4, Feature Request 1/3, Escalate 1/2, Duplicate 3/4, No Action 1/1. Duplicate/No Action grade mechanically so they read artificially high.

  **Declared cause × declared next step** cross-tab surfaces two systemic patterns the dashboard calls out explicitly: cause=code bug but step=Config Change ("papering over a bug"), and cause=configuration but step=Escalate ("a self-serve tooling gap"). Dominant cell: cause=code bug → step=Code Fix, 18.

  **Human labor**: 0% of tickets resolved end-to-end by the Workup actor itself (0 of 54 — status never moved to terminal by Workup). 1.0 activations/ticket average; 0% needed a second activation.

  **Cause diagnosis (secondary axis)**: judge agreement 77% (n=62 labels) — correct 95, partial 52, incorrect 54, unassessable 22. Button on page: "10 human vs judge disagreements" (not opened).

  **Operations**: 340 runs · $11.78 avg/run · $739.97 spent this week · 84 runs posted nothing · 1% declined by design.

  **Grading queue** (backlog of tickets needing human grading): Needs a grade 3 · Unjudged 36 · All 340 · Disagreements 10 · Gaps 245 · No diag 89. Calibration progress: "52 of ~50 calibration grades."

  Sample grading-queue rows visible on load: PMS-10352 (correct, gap 1, $5.79) — https://linear.app/canary-technologies/issue/PMS-10352; PMS-10349 (partially correct, gap 2, $12.22) — https://linear.app/canary-technologies/issue/PMS-10349; PMS-10321 (incorrect, gap 2, $6.16) — https://linear.app/canary-technologies/issue/PMS-10321.

  Not explored this run: the `/users`, `/teams`, `/bots`, `/tickets`, `/sandboxes`, `/usage`, `/metrics`, `/settings` sub-pages linked in the sidebar, or the disagreements/grading-queue drill-downs — this pass only covered the dashboard landing page. Also still haven't loaded the Linear "next-step-tickets" saved view itself (linear.app session in the same browser is separate from the Google session and still logged out).
project: null
source_id: null
tags: []
time_minutes: 5
title: investigate workup metrics
updated: 2026-09-04T12:32:11Z
waiting_on: null
waiting_since: null
working_on: false
---

https://agents.cnry.land/workup
https://linear.app/canary-technologies/view/next-step-tickets-69f507a962f4?layout=list&ordering=dateCreated&orderingDirection=desc&grouping=none&subGrouping=none&showCompletedIssues=all&showSubIssues=true&showTriageIssues=true