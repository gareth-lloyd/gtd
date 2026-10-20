---
area: null
completed_at: null
contexts: []
created: 2026-10-19 13:57:25.153198
defer_until: null
due: null
energy: low
id: 2026-10-19T1357-check-on-mobile-analytics-sdk-source-in-snowflake
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: 10
title: Check on mobile analytics / SDK source in Snowflake (covering for Connor)
updated: 2026-10-19 13:59:38.733050
waiting_on: null
waiting_since: null
working_on: false
---

Connor's bar: "the first step of the full solution, not a hack". Snowflake can't tell SDK activity from web. Caitlyn is the point person, and Carmela is involved. Groundcover is good enough for Wyndham for now.

Check:
- Has anyone started a short eng design for a source identifier (iOS/Android, mobile/web) that scales across products? Diana suggested writing one.
- MOB-1325: Connor says ENT isn't the right team and it should go to Data Platform. Has it been raised?
- Status of the check-in/checkout count dashboard.

Links:
- Connor's SDK-source thread: https://canarytechnologies.slack.com/archives/C0A4EN8SJLA/p1792076912655559
- Connor agreeing Groundcover is OK for Wyndham for now: https://canarytechnologies.slack.com/archives/C0A4EN8SJLA/p1792084745016179?thread_ts=1792076912.655559&cid=C0A4EN8SJLA
- MOB-1325: https://linear.app/canary-technologies/issue/MOB-1325/add-sdk-as-a-check-in-source-and-pass-it-through-to-snowflake-omni-and
Connor's coverage post (#epd-enterprise, Oct 15): https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1792086541978799
Connor <> Gareth 1:1 notes (Oct 15): https://app.notion.com/p/canarytechnologies/Connor-Gareth-1ae8146861518002b563c3fc97fca9f3