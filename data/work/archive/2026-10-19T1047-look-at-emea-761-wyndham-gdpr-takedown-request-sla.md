---
area: null
completed_at: 2026-10-19 12:56:12.481593
contexts:
- react
created: 2026-10-19 10:47:41.974500
defer_until: null
due: null
energy: medium
id: 2026-10-19T1047-look-at-emea-761-wyndham-gdpr-takedown-request-sla
order: null
output: |
  ## Agent run 2026-10-19T13:05
  **SLA breach is moot now: EMEA-761 was closed Done at 07:49 UTC today. But it looks like the wrong action was taken.** This is an ACCESS / Right-to-Know request, not an erasure.

  - Ticket: EMEA-761 (https://linear.app/canary-technologies/issue/EMEA-761/wyndham-gdpr-takedown-request), Zendesk #211379 (https://canarysupport.zendesk.com/tickets/211379), Slack SLA alert (https://canarytechnologies.slack.com/archives/C0A83PDRP3P/p1792330315847099)
  - Why it breached: created Thu Oct 15 13:31 UTC and sat in Triage until Mon Oct 19 07:22 UTC. That covered the weekend, and the Oct 18 13:31 breach time passed. The Canary Agent triage asked for "hotel information" and nobody picked it up. Marta Ochowicz Malarz then took it from In Progress to Done in about 27 minutes.
  - **Request type mismatch:**
    - This one's attachment is `WHR ACCESS_Data Privacy Requests_Canary_20261015.csv` (138 bytes, 1 row). The Zendesk subject is "CANARY Data Elements for ACCESS/RIGHT TO KNOW Requests".
    - The normal monthly batches are `WHR ERASURE_...csv` (~11KB, ~240 rows) with the subject "MONTHLY GDPR TAKEDOWN/ ERASURE Request". See EMEA-703 (https://linear.app/canary-technologies/issue/EMEA-703/wyndham-gdpr-takedown-request) on 09-24 and EMEA-645 (https://linear.app/canary-technologies/issue/EMEA-645/wyndham-gdpr-takedown-request) on 08-27.
    - The Zendesk-to-Linear template titled it "GDPR Takedown Request" anyway.
  - What was done: Marta ran the obfuscation and found no records. Martijn Dekker then compared the count to last month's 240, which mixes up two different request streams. Nobody in the thread noticed it was an access request.
  - Consequences:
    - (a) The data subject's access request has probably not been answered. Wyndham wants a report of the data Canary holds on this person, not a deletion. GDPR gives one month from Oct 15.
    - (b) If obfuscation had matched, we would have deleted data the subject only asked to see.
    - (c) The next monthly ERASURE batch should still arrive around late October, so don't treat 1 row as "volume dropped".
  - Not checked: I didn't open the CSV (PII) or run any lookup for the subject.

  **Suggested next step (not sent, needs your OK):** post a Linear comment on EMEA-761 to reopen it:
  > @Marta Ochowicz Malarz @Martijn Dekker heads-up: this one isn't a takedown. The file is `WHR ACCESS_...` and Zendesk #211379 says "Data Elements for ACCESS/RIGHT TO KNOW Requests". Wyndham wants a report of what Canary holds on this person, not deletion, and the monthly ERASURE batch (~240 rows) is a separate ticket. Can we reopen and either produce the access export or confirm back to Wyndham via Zendesk that we hold no data? It might also be worth having the intake template stop labelling ACCESS requests "GDPR Takedown".

  Possible follow-up: ask the privacy/EMEA owners whether the Zendesk→Linear intake should branch on ACCESS vs ERASURE, and whether Wyndham requests skip the Canary Agent "missing hotel info" stall. That stall is what blew the SLA.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0A83PDRP3P/p1792330315847099
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 15
title: 'Look at EMEA-761 Wyndham GDPR Takedown Request: SLA breached Oct 18'
updated: 2026-10-19 12:56:12.481586
waiting_on: null
waiting_since: null
working_on: false
---

From morning awareness (Slack highlights).
https://canarytechnologies.slack.com/archives/C0A83PDRP3P/p1792330315847099