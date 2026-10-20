---
area: null
completed_at: 2026-10-19 12:46:38.897174
contexts:
- react
created: 2026-10-19 10:37:05.481479
defer_until: null
due: null
energy: medium
id: 2026-10-19T1037-add-context-and-acceptance-criteria-for-script-cha
order: null
output: |
  ## Agent run 2026-10-19T12:45
  Nothing owed. The ask is superseded and the work was done by someone else.

  - Andrea withdrew the ask 8 minutes after posting it: "oh nvm, I see the other ticket. Will combine" (https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1792077493597039?thread_ts=1790006579.628339&cid=C09M5GRJPL2). The GTD fetcher missed that follow-up.
  - ENT-7905 (https://linear.app/canary-technologies/issue/ENT-7905) is Done (2026-10-16), assigned to Ryan Rogers. His spike comment covers the context: test mode only gates Canary pages, not the Wyndham app (has_check_in_mobile) or Guest Journey links, and each brand script set a different subset of gates. Andrea approved the shared-rule approach.
  - The acceptance criteria now live in ENT-7916 (https://linear.app/canary-technologies/issue/ENT-7916), which is In Review with draft PR #60466 (https://github.com/canary-technologies-corp/canary/pull/60466). EnableMsaProductsPlan puts not-yet-live hotels into check-in/out test mode with an empty whitelist and sets has_check_in_mobile=False. GoLivePlan restores all three gates. A live hotel is unchanged by a rebuild.
  - Follow-ups: ENT-7917 (https://linear.app/canary-technologies/issue/ENT-7917) covers the census and backfill for BW, IHG Core and IHG Pilot. AD-10380 (https://linear.app/canary-technologies/issue/AD-10380) covers legacy direct URLs that ignore test mode.

  Suggested: no Slack reply needed. Optionally review #60466, since it touches Wyndham onboarding you built.
project: null
source_id: https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1792076987260609?thread_ts=1790006579.628339&cid=C09M5GRJPL2
tags:
- morning-gtd
- slack
time_minutes: 30
title: Add context and acceptance criteria for script changes to ENT-7905 (check-in
  test mode spike)
updated: 2026-10-19 12:46:38.897168
waiting_on: null
waiting_since: null
working_on: false
---

Andrea asked me in the Wyndham has_check_in_mobile thread. Open 3 days, no reply from me.
https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1792076987260609?thread_ts=1790006579.628339&cid=C09M5GRJPL2
https://linear.app/canary-technologies/issue/ENT-7905