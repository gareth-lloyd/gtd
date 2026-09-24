---
area: null
completed_at: 2026-09-24 10:33:56.230577
contexts:
- react
created: 2026-09-24 10:00:56.978724
defer_until: null
due: 2026-09-24
energy: medium
id: 2026-09-24T1000-look-at-ent-7594-wyndham-jennifer-williams-unable
order: null
output: |
  ## Agent run 2026-09-24T10:30+03:00

  **Status: diagnosed and blocked on Marta's decision for ~42h. SLA breaches ~20:30 UTC tonight. Nothing is technically unresolved; it is a stalled hand-off.**

  **What Ryan found (Linear comment, 2026-09-22 15:56 UTC, https://linear.app/canary-technologies/issue/ENT-7594):**
  - Nothing changed on Jennifer's account. Canary only lets an admin assign a portfolio role if they hold every permission on it.
  - The role she was assigning to Dawn MacBurnie, WHR Support, picked up `portfolio_has_agent_assist_access` for the Voice team's Agent Assist pilot. Jennifer's roles lack it, so Save fails. Every other Wyndham role still works for her.
  - I verified the permission landed 2026-07-30 in PR #51461 (EV-251), consistent with Ryan's timeline.
  - Dropdown does not hide unassignable roles, so it only fails on Save. Tracked as ENT-7400 (Backlog, no priority): https://linear.app/canary-technologies/issue/ENT-7400
  - The two "AP Calls" portfolio roles are Canary test roles from June (one held by 16 Canary staff, one by nobody). Wyndham does not need them; Ryan said "we'll clean them up".
  - Side finding: WHR Support has 218 holders, far more than the Agent Assist pilot planned for. Ryan said he'd check with the Voice team. No evidence that check happened.

  **Ryan's options to Marta (he recommends 1):**
  1. Give Jennifer a small new role with only the agent-assist permission so she can assign WHR Support herself. Affects only her.
  2. We add WHR Support to Dawn ourselves. Quick, but Jennifer stays blocked and it recurs.
  3. Add the permission to Jennifer's WHR Internal role. Avoid: 40 holders would all get agent-assist access.

  **Where it stalled:**
  - Marta has not replied on Linear since Ryan's comment. Ticket now carries `Blocked: Other` (last update 2026-09-23 20:40 UTC).
  - No Slack discussion anywhere since 2026-09-22 beyond the SLA bot (https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1790195415243139) and Ryan's Sep 22 EOD listing the ticket.
  - Jennifer emailed Marta directly (no Zendesk ticket), so Jennifer likely has had no answer for two days either.

  **Recommendation:**
  - Unblock today by doing options 1 AND 2 together: grant Dawn WHR Support now so the customer ask is met before the SLA, and create Jennifer's agent-assist role so it does not recur. Both are small admin changes; Ryan can do them in minutes once Marta says go (or you say go on her behalf, since Jennifer is a key contact).
  - Separately: chase the 218-holder question with the Voice team before handing out more agent-assist access. If the pilot was meant to be small, option 1 may be the wrong default and Voice may want WHR Support trimmed instead.
  - Ask Ryan to close out the AP Calls role cleanup on the same ticket so Marta can reply to Jennifer's second question.

  **Draft nudge to Marta (NOT sent; Slack DM or Linear reply, your call):**
  > Hi Marta, ENT-7594 (Jennifer Williams / portfolio role) hits its SLA tonight and it's been waiting on your pick since Ryan's comment on Monday. Suggest we do both: Ryan adds WHR Support to Dawn today so Jennifer's request is done, and gives Jennifer a tiny agent-assist role so she can do it herself next time. OK to proceed? Ryan also needs a word with Voice about the 218 WHR Support holders before we hand out more agent-assist access. https://linear.app/canary-technologies/issue/ENT-7594

  **Not done / caveats:**
  - I did not read the code path for the "must hold every permission" guard; I trust Ryan's test. The permission's existence and date are verified.
  - No writes made to Linear, Slack, or prod. No Salesforce touched.
project: null
source_id: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1790195415243139
tags:
- morning-gtd
- linear
- from-awareness
time_minutes: 20
title: 'Look at ENT-7594: Wyndham — Jennifer Williams unable to add a Portfolio Role
  (SLA runs out tonight)'
updated: 2026-09-24 10:33:56.230572
waiting_on: null
waiting_since: null
working_on: false
---

High priority, In Progress with Ryan Rogers. SLA-at-risk bot fired 20:30 UTC on Sep 23 with ~24h left. Jennifer Williams is a key Wyndham contact.
https://linear.app/canary-technologies/issue/ENT-7594
Bot post: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1790195415243139