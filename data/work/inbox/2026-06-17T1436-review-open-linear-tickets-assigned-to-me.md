---
area: null
contexts: []
created: 2026-06-17 14:36:25.149335
defer_until: null
due: null
energy: low
id: 2026-06-17T1436-review-open-linear-tickets-assigned-to-me
order: 7
output: |
  ## Agent run 2026-06-17T12:52Z

  Reviewed all open (non-archived) Linear issues assigned to you. 9 open + 3 that
  are archived but still showed in lists. Read-only review — nothing was changed in
  Linear or GitHub.

  ### Most urgent / needs a decision

  - **ENT-5508 (Medium) — SSO migration leaves orphaned role grants** — status is
    "In Review" but its only PR (#40585) is **CLOSED / blocked**, last touched
    2026-04-02 (~2.5 months stale). Status is misleading: there's nothing actually
    in review. Decide: re-open/rebuild the PR, or move the ticket out of In Review.
    Security + Authentication labels, so worth not letting it rot.
    https://linear.app/canary-technologies/issue/ENT-5508
    PR: https://github.com/canary-technologies-corp/canary/pull/40585

  - **ENT-5227 (Medium, Oncall) — Account without portfolio roles can make dashboard
    changes** — In Review, delegated to Golem, untouched since 2026-04-16 (~2 months).
    Permissions-escalation bug (user without portfolio roles could assign property
    roles). Stale; confirm whether Golem's work landed or needs you to take it back.
    https://linear.app/canary-technologies/issue/ENT-5227

  ### In Review — likely just need a merge nudge or status cleanup

  - **ENT-5974 (High) — Drive IHG portfolio membership from SF Associated_Enterprise_
    Deployments__c + Opportunity segment** — In Review, updated 2026-05-21 (~4 wks).
    No matching open PR diff surfaced in Linear — check if the PR merged and this can
    be closed, or if it's waiting on review.
    https://linear.app/canary-technologies/issue/ENT-5974
  - **ENT-5610 (High) — Hotels failing OHIP payment posting "Payment Method is not
    valid"** — In Review, updated 2026-05-12 (~5 wks). ~27 Wyndham errors/day, card
    silently not recorded in PMS. Chase to merge — this is live customer impact.
    (Matches your memory note project_ent5610.)
    https://linear.app/canary-technologies/issue/ENT-5610
  - **ENT-5310 (Low) — Wyndham check-in message use-case overlap with migration step**
    — In Review, delegated to GitHub Copilot, updated 2026-05-11. Low priority; let
    Copilot finish or close out.
    https://linear.app/canary-technologies/issue/ENT-5310

  ### In Progress

  - **ENT-6022 (Medium) — Wyndham/OHIP silent CC-post drop at Zermatt (ENT-5898
    follow-up)** — updated 2026-04-30 (~7 wks). Investigation ticket, no movement in
    a while. Decide whether to resume or park it.
    https://linear.app/canary-technologies/issue/ENT-6022

  ### Todo (not started) — note the cluster

  ENT-5697, ENT-5695, and ENT-5987 are all the same failure family (addon/upsell
  charges silently not posting to the PMS due to missing per-hotel config). Worth
  considering as one batch of work rather than three separate fixes.

  - **ENT-5987 (Medium) — Upsell item not syncing to PMS (La Quinta Dallas North
    Central)** — labelled "Blocked: Other"; updated 2026-06-05 (most recently active).
    Confirm what it's blocked on. https://linear.app/canary-technologies/issue/ENT-5987
  - **ENT-5697 (Medium) — Addon charge posting 100% broken for ~45 Wyndham hotels
    missing cashier_id** — ~332 errors/7d, silent. Updated 2026-04-09.
    https://linear.app/canary-technologies/issue/ENT-5697
  - **ENT-5695 (Medium) — Addon charge posting fails for hotels missing vendor_id PMS
    config** — sibling of ENT-5697. Updated 2026-04-09.
    https://linear.app/canary-technologies/issue/ENT-5695

  ### Archived but still showing as "assigned + open"

  These came back in the assignee query but are archived — likely safe to ignore,
  flagging in case any should be un-archived:
  - EMEA-281 (Medium) — Sketch regional/country configs in rules-based config system
  - ENT-6130 (High) — PRD for view portfolio templates
  - ENT-3097 (Medium) — Settings/Property Info Preferred Language UI bug

  ### Suggested next actions for you
  1. ENT-5508: fix the misleading In-Review status (PR is closed) — re-open or re-bucket.
  2. ENT-5610 + ENT-5974: nudge reviewers to merge (both High, both live impact).
  3. ENT-5227: reclaim from Golem or confirm it's done.
  4. Decide whether to batch ENT-5695/5697/5987 as one PMS-config-sync workstream.
project: null
source_id: null
tags: []
time_minutes: 5
title: review open linear tickets assigned to me
updated: 2026-06-17 15:52:52.219488
waiting_on: null
waiting_since: null
working_on: false
---