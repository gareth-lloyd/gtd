---
area: null
completed_at: null
contexts: []
created: 2026-10-14 16:46:54.605594
defer_until: null
due: null
energy: low
id: 2026-10-14T1646-review-this-thread
order: null
output: |
  ## Agent run 2026-10-14T17:05
  Thread (https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1791922645177919): Andrea and Tincho on IHG PMS issues, Oct 13-14. 17 replies. Nobody asks you for anything and you are not tagged.

  The thread separates two problems:
  1. HotelKey 2-way config (GRRPE plus 25 more live IHG GMS Core/Core Plus hotels). These are old hand-made configs with a blank brand_identifier or the legacy env, so the Gateway refuses 2-way calls. In a 3h window, 12 of the 25 hit "missing fields that allow this operation". Details: ENT-7812 comment (https://linear.app/canary-technologies/issue/ENT-7812/investigate-why-hk-wasnt-configured-for-2-way#comment-d5b112d7).
     - Owner: Yauheni (fixed GRRPE, owns PMS-6643 https://linear.app/canary-technologies/issue/PMS-6643). Tincho said he'd post the script Yauheni ran into the ticket.
     - Guard: PR #59996 / ENT-7814 (https://github.com/canary-technologies-corp/canary/pull/59996) makes VALIDATE fail when the gateway's brand/env don't match the onboarding values. After huddling with Taylor, Tincho changed it so the Validate step runs; Taylor needs that to fix the hotels and wants to retry a few once it merges.
     - Andrea flagged a probable missing step in a configuration KB doc. Nobody has picked that up.
  2. FreedomPay gateway missing (ENT-7708 https://linear.app/canary-technologies/issue/ENT-7708, Andrea). Card pushes fail. 15 of the 25 hotels are affected. Andrea had a PR due EOD Oct 13 but was still deciding the backfill strategy for creating the FP gateway.

  PR #59996 status: Andrea APPROVED it at 13:45Z today after several rounds, mergeState CLEAN, still OPEN. Tincho's last message (16:14 EEST) asked how it looked, and the approval answers that. It is ready for Tincho to merge.

  For you:
  - Nothing is blocking on you. It is relevant to ENT-6032 (IHG HotelKey+FreedomPay pilot) and to the onboarding validation work.
  - Possible follow-ups (none done): (a) check that ENT-7708's backfill approach lands; (b) ask who owns the KB/onboarding doc gap so new hotels don't repeat it; (c) watch Taylor's retry after #59996 merges.
project: null
source_id: null
tags: []
time_minutes: 5
title: review this thread
updated: 2026-10-14 17:05:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1791922645177919