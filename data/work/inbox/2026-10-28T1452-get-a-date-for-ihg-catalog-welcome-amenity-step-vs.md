---
area: null
completed_at: null
contexts:
- react
created: 2026-10-28 14:52:21.559382
defer_until: null
due: null
energy: medium
id: 2026-10-28T1452-get-a-date-for-ihg-catalog-welcome-amenity-step-vs
order: null
output: |-
  ## Agent run 2026-10-28T16:40
  **Answer: nobody has committed to a date.** No ticket exists for the catalog / welcome-amenity-step work, so there is nothing to date yet. Nothing was posted.

  **What exists**
  - Caitlyn, 10-23 (https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1792720325077329?thread_ts=1792692313.584389&cid=C03V5P4B48P): "by mid-November all IHG's should be on check-in v3 because they are expecting the separate Welcome Amenity step."
  - Taylor, 10-23, same thread: paused all IHG v3 migration until Andrea and Connor are back. Taylor won't ship the separate step until the Q4 copy, image and renaming changes are done.
  - Andrea, 10-26 (https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1793019778323619?thread_ts=1792692313.584389&cid=C03V5P4B48P): the step needs direct catalog writes, upsell-script changes so new IHGs don't get welcome-amenity upsells, and removal of those upsells from IHGs already configured. She called it "a medium sized effort". She gave no date.
  - Andrea, 10-27, same thread: "v3 as default" is not the same as "v3catalog as default". ENT will switch the scripts to v3 as the default once Connor gives the greenlight, "expected in the next week or so". That covers plain v3 only, not the catalog or welcome-amenity work.
  - Connor is at the BW conference through Wed 10-28.
  - Linear:
    - Project IHG Scripting - Q4A 2026 (https://linear.app/canary-technologies/project/ihg-scripting-q4a-2026-bca67c82a9ea): lead Andrea, target date 2026-11-30 (month resolution). Its summary names "separation of welcome amenity in the check-in flow" as in scope. No milestone or issue covers the catalog writes or the upsell removal.
    - ENT-7807 Welcome Amenity copy changes (https://linear.app/canary-technologies/issue/ENT-7807/ihg-q4-scripting-welcome-amenity-copy-changes): Connor, Todo, no due date.
    - Mobile SDK side: MOB-1364 iOS (https://linear.app/canary-technologies/issue/MOB-1364) and MOB-1365 Android (https://linear.app/canary-technologies/issue/MOB-1365) are both due 2026-11-03, unassigned. MOB-1426 Monaco (https://linear.app/canary-technologies/issue/MOB-1426) is Eric, Todo.

  **The gap:** Mobile expects mid-November (~11-15). The ENT project's only date is end of November. The work has no ticket or estimate, and it is gated on Connor's v3-default greenlight, so it can't start before ~11-04. A medium effort starting then probably misses 11-15.

  **Draft reply for the #ihg thread** (https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1792692313584389). NOT SENT; needs your OK:
  > @Andrea @Connor quick timing check. Caitlyn's note is that IHG expects the separate Welcome Amenity step by mid-Nov. The ENT side (catalog writes, stop adding WA upsells, remove existing WA upsells, plus ENT-7807 copy) has no ticket or date yet, and the Q4A project targets end of Nov. Can we get a ticket and a realistic ship date this week? If it's later than ~11-15, @Caitlyn Levine needs to reset IHG's expectation now, not mid-Nov.

  **Other options:** DM Andrea instead, or raise it in your next sync with her. If you want it tracked, I can draft an ENT ticket for the catalog + upsell-removal work under P-ENT-2357. Not created.
project: null
source_id: null
tags: []
time_minutes: 15
title: Get a date for IHG catalog + Welcome Amenity step vs Caitlyn's mid-November
  expectation
updated: 2026-10-28 16:24:40.891320
waiting_on: null
waiting_since: null
working_on: false
---

From: check-in v3 rollout research, 2026-10-28 (#ihg thread, #best-western thread, TOOL 'Automate Check-in V3 Onboarding' design)
Caitlyn (Mobile, #ihg 10-23): SDK hotels must be on v3; "by mid-November all IHGs should be on check-in v3" for the separate Welcome Amenity step.
Andrea wants the catalog / welcome-amenity work grouped with the quarterly IHG changes. It needs direct catalog writes plus upsell script changes to remove existing welcome-amenity upsells.
These timelines need to line up.