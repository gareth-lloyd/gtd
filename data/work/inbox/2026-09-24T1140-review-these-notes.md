---
area: null
completed_at: null
contexts: []
created: 2026-09-24 11:40:54.858912
defer_until: null
due: null
energy: low
id: 2026-09-24T1140-review-these-notes
order: null
output: |
  ## Agent run 2026-09-24

  Reviewed the Gemini notes from the Sep 23 "Workup Agent Sync" (https://mail.google.com/mail/?authuser=glloyd@canarytechnologies.com#all/thread-f:1877139508035322169), read against the Sep 16 sync notes (https://mail.google.com/mail/?authuser=glloyd@canarytechnologies.com#all/thread-f:1876506203721821586), your Slack DM thread with Laura and Stephanie from last night (https://canarytechnologies.slack.com/archives/C0A4BS2AREH/p1790169107627089), TOOL-733 (https://linear.app/canary-technologies/issue/TOOL-733), and the local Workup/Jev backtest notes in backend/canary/tmp/data/workup_typesafe/NOTES.md. The Gmail link's opaque ID cannot be resolved by the API, so the Sep 23 notes are the assumed target (newest match on "workup", unstarred, not yet reviewed).

  ### What the Sep 23 notes say

  1. MCP SQL tool: reverted to Teleport auth, 5 tickets cancelled, block-list module and Postgres grant manifest merged to prod, Sallyport migration planned after first release. Asher owns an internal explainer message and end-to-end staging test by next week.
  2. Engram evaluation: Jason (simulated) and Stephanie (historical Workup tickets). Claimed lift "up to 21%" on Workup cases, "100%" on simulated. Agentic recall with Haiku +22%, GLM +17%. Cost per ticket: $18 baseline, $20 deterministic recall, $15 GLM agentic. Next: Haiku vs self-hosted GLM cost analysis, then productionize agentic recall (Stephanie, Jason). Plan to turn the test suite into a reusable agent lab.
  3. Nothing is assigned to you.

  ### Review: questions worth raising before "productionize agentic recall"

  - Leakage check on the historical eval. Engram recalls past tickets. If the memory store was built from the full window and then scored on tickets in that same window, a recalled duplicate or the ticket's own resolution trivially "solves" it. Ask whether the memory was built with a per-ticket temporal cutoff (only tickets resolved before the eval ticket was filed). Without that, the 21% is not a production estimate.
  - "100% on simulated scenarios" is a red flag, not a result. Simulated cases built around what the memory contains will always be found. It should be reported as a smoke test, not a lift.
  - Relative or absolute? Workup's human-label baseline on the Aug 20 to Sep 18 window was 52.7% next-step match (91 labels, our backtest) and 41.5% by LLM judge. A 21-point absolute lift takes it to ~74%, a 21% relative lift to ~64%. The notes do not say which, nor n, nor whether grading was human or judge. Human labels are anchored on Workup's own declaration (only 6 of 91 predate it), so judge-vs-human matters.
  - Break-out by next-step bucket is the missing number. The dominant miss is a confident code fix on a ticket that closes as duplicate or no action: TOOL-733 gives 48 code-fix declarations with 8 right, 12 closed duplicate, 9 no action; Laura's Slack numbers on thin tickets are 11 of 20 diagnoses wrong, 7 of 19 next steps right, 1 of 99 declarations Request Info (Sep 15-23). Our backtest found the same blind spot (no-action 4 of 21 for Workup). Memory of past tickets is exactly the mechanism that should fix duplicate and no-action, so if Engram's lift is not concentrated there it is probably measuring something else. Ask for the per-bucket confusion.
  - GLM cheaper than baseline ($15 vs $18) means recall shortens the run. Worth confirming it shortens by resolving earlier rather than by terminating on a recalled-but-wrong answer. The correctness lift claim covers this only if the eval set is clean (see leakage point).
  - Haiku cost is not in the notes, so the "cost analysis" action item is currently missing half its inputs.
  - Ordering vs TOOL-733. Laura's plan in Slack is declaration fixes first (TOOL-733 execution-read bar plus a Request Info exit when the hypothesis can't be verified), then the nudge. TOOL-733 is In Review with PR #57629 (https://github.com/canary-technologies-corp/canary/pull/57629). Engram productionization should be re-baselined after that lands, or the two changes confound each other on the dashboard's next-step card.
  - Reusable agent lab: our extract/compile/judge harness (179 tickets, read-only pull from the overlord DB, Jev as a $0.00008/ticket blind judge at 69.5% human agreement) already does most of this and is gitignored under backend/canary/tmp/data/workup_typesafe. Worth offering to Jason and Stephanie before they build a second one.

  ### Follow-through gaps from Sep 16

  The Sep 16 action items are not mentioned on Sep 23 and their status is unknown: Asher sharing the SQL design with Jason; Laura on Twilio log access, duplicate detection before code-fix suggestions (TOOL-706 / TOOL-709 exist, and Laura's Notion "Workup duplicate retrieval check (2026-09-16)" page was shared Sep 21), agent decomposition discussion with Jason, and messaging status in the hotel context object. The Sep 23 direction reversal on auth (Django-based on Sep 16, back to Teleport on Sep 23) is not explained in the notes.

  ### Suggested actions for you

  - Reply on the Workup sync thread or DM Stephanie/Jason with the leakage and per-bucket questions above before the cost analysis starts.
  - Point them at the workup_typesafe harness as the "reusable lab" starting point.
  - Ask Laura whether the Sep 16 items (Twilio, duplicates, hotel context) are still hers or folded into TOOL-706/709.

  No external writes were made. Nothing sent, commented, or changed in Slack, Linear, Notion, or Gmail.
project: null
source_id: null
tags: []
time_minutes: 5
title: review these notes
updated: 2026-09-24 11:48:41.116716
waiting_on: null
waiting_since: null
working_on: true
---

https://mail.google.com/mail/u/0/#search/workup/FMfcgzQhWfMTlJgfTQncvNvkCzBBclrW
workup