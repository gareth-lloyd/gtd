---
area: null
completed_at: 2026-11-10 15:21:13.638933
contexts: []
created: 2026-11-09 16:32:48.078862
defer_until: null
due: null
energy: low
id: 2026-11-09T1632-linear-working-on
order: null
output: |-
  ## Agent run 2026-11-10T14:25 (read-only; nothing changed in Linear, Slack, Notion or GitHub)

  You have 5 open issues assigned (4 started, 1 backlog; nothing in Todo, Triage or a Blocked status). One can be closed now, one is a 20-minute review, three are stalled and need a decision rather than work.

  ### Close now
  - ENT-7898 Duplicate card authorization from OTA check-in (https://linear.app/canary-technologies/issue/ENT-7898) - In Progress.
    You set the check-in credit card step to Disabled for ihg-lancp on 2026-10-19 (Option A, the Rooms Manager's choice). Dan Logan said on 2026-10-21 the client had reported no issues since and he was confirming. Nothing since, in Linear or in the Slack thread (https://canarytechnologies.slack.com/archives/C0BJPFZKQ9W/p1792011114211459).
    Suggested closing comment: "Closing: card step has been disabled at ihg-lancp since 19 Oct and no further double authorizations have been reported. @dlogan reopen if the property comes back."
    Loose end: the product gap (online check-in has no OTA / virtual-card handling) was dropped from the summary and has no ticket. Golem also suggested a KB article (/enterprise:add-to-kb ENT-7898).

  ### Do (new, small)
  - ENT-8222 Review eng design: GJM Drift Detection (https://linear.app/canary-technologies/issue/ENT-8222) - Backlog, created 2026-11-09 by Tincho.
    Doc: https://app.notion.com/p/41381468615181089aa2d0e08023625a (status REVIEW ME!, no comments from anyone yet). Sibling review tickets: ENT-8221 Andrea, ENT-8223 Ryan, ENT-8224 Andres.
    What it wants from you specifically:
    - Iteration 1 rollout step 1 is "Gareth's stack lands". All four PRs it lists are still your drafts: #59047 (https://github.com/canary-technologies-corp/canary/pull/59047), #59059 (https://github.com/canary-technologies-corp/canary/pull/59059), #61724 (https://github.com/canary-technologies-corp/canary/pull/61724), #61725 (https://github.com/canary-technologies-corp/canary/pull/61725). So you are the project's critical path.
    - Check the dependency table: it calls #61724 the "SupersetOf predicate" and #61725 the "Value reader interface", but the PR titles are "Country conventions engine" and "First binding rule: EU ID collection". I did not open the diffs, so this may just be naming.
    - Two calls it defers to you for iteration 2: is edited message copy drift at all, and does the drift-contributor seam live on ConformityService or in the drift layer.
    - It says ENT-7726 settled that the column-less reader key is theirs to build by extending #61725.

  ### Stalled - status is misleading, needs a decision
  - ENT-5987 Upsell item not syncing, La Quinta Dallas North Central (https://linear.app/canary-technologies/issue/ENT-5987) - In Progress, labelled "Blocked: Other".
    Still broken: wyndham-53270 had 2 charges_failed "Cannot find charge code" in the last 7 days (latest 2026-11-08). Your diagnosis from May stands - the property's SynXis chart of accounts lacks the addon codes; no Canary change needed.
    Waiting on Wyndham HCS since Marta Ziaei's comment of 2026-07-14 (the property had made all its PMS codes inactive). Four months, no update, no Slack mention since June.
    Not yours to unblock. Options: ping Marta for a status and reassign to her, since the remaining work is CS/Wyndham; or close as "no Canary change, waiting on property" and let the Zendesk ticket (https://canarysupport.zendesk.com/tickets/173444) carry it.
    Draft ping: "@Marta - any word from Wyndham HCS on the La Quinta Dallas North Central upsell codes? Charges were still failing with 'Cannot find charge code' as of 8 Nov. If this is with the property now I'd like to hand the ticket to you or close it on the eng side."

  - ENT-5697 Addon charge posting broken for Wyndham hotels missing cashier_id (https://linear.app/canary-technologies/issue/ENT-5697) - In Review since 2026-07-09, but there is no PR or branch.
    Still firing: 33 "Cannot post billing charge without cashier_id" failures across 29 hotels in the last 24h (was ~47/day in March). Your April finding: 125 of 153 OHIP chain-code credential sets have no cashier_id, ~937 Wyndham hotels exposed. The fix needs cashier_id values from Wyndham per chain code; nobody appears to be chasing that.
    New since you last looked: PMS-9353 (https://linear.app/canary-technologies/issue/PMS-9353), a "Create New Cashier ID" helper on the OHIP admin form, shipped 2026-07-29. That may let us create cashier IDs without waiting on Wyndham - worth asking Lei Ferretti whether it works at chain-code level.
    Cannot be closed as done. Either move it to Todo with that question as the next step, or hand it to PMS.

  - ENT-5695 Addon charge posting fails for missing vendor_id (https://linear.app/canary-technologies/issue/ENT-5695) - In Review since 2026-07-09, no PR or branch.
    Still firing, and not shrinking: at least 65 vendor_id failures in the last 24h, of which about 46 are the blank-code kind this ticket describes (was ~29/day in March). The rest are a newer variant where a non-blank code is rejected ("vendor_id 'Parking' is not a valid UUID and no addon with that code was found").
    The investigation is finished (your 2026-07-16 comment: 133 hotels, 457 paid blank-code rows). What is left is the work nobody has picked up: save-time validation of addon codes, surfacing failed posts to staff, and a per-hotel config cleanup that has to go through BW.
    Cannot be closed as done. Suggest moving it back to Todo, or splitting it: one eng ticket for validation + surfacing failures (which would also cover ENT-5697 and ENT-5987's silent failures), and a CS ticket for the config cleanup.

  ### Caveats
  - Error counts are one 24h window (to 2026-11-10 ~12:20 UTC) of event __pushto_pms_purchase_order.charges_failed in production; the grouped result was truncated at 30 rows, so the vendor_id total is a floor.
  - "No PR" is from a GitHub search on the ticket IDs plus local branch names; a PR that never mentioned the ticket would be missed.
  - The first 250 of your assigned issues by last update were all closed apart from these; I listed open ones by state type rather than paging the full history.
project: null
source_id: null
tags: []
time_minutes: 5
title: My issues in linear. What can be unblocked, closed, done?
updated: 2026-11-10 15:21:13.638928
waiting_on: null
waiting_since: null
working_on: false
---