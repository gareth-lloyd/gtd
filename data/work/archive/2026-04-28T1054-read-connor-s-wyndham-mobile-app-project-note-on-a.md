---
area: null
contexts:
- computer
created: 2026-04-28 10:54:36.124473
defer_until: null
due: null
energy: low
id: 2026-04-28T1054-read-connor-s-wyndham-mobile-app-project-note-on-a
order: null
project: null
source_id: https://canarytechnologies.slack.com/archives/C0A4EN8SJLA/p1776809892683889
tags:
- morning-gtd
- slack
time_minutes: 10
title: 'Read Connor''s #wyndham-mobile-app-project note on API key setup'
updated: 2026-04-29 09:02:36.182371
waiting_on: null
waiting_since: null
---

Connor agreed with Jason to set Wyndham up similarly to IHG (separate test env / API key) before mobile testing resumes. Caitlyn driving changes with Wyndham. Worth understanding the new setup before next Wyndham mobile work lands.

Deep-dive findings (full thread):
- Concrete change: Diana opened Wyndham repo PR https://github.com/WyndhamDigital/whr_frontend_reactnative/pull/1087 so the Canary SDK uses different appId/secretKey per env. Wyndham must populate `EXPO_PUBLIC_CANARY_STG_APP_ID` and `EXPO_PUBLIC_CANARY_STG_SECRET_KEY`.
- Key trail (per Jason / Diana / Caitlyn):
  - Wyndham: keys Luiza sent via Sendsafely were *staging*. Production keys still need to be issued for Wyndham.
  - IHG: keys Luiza generated were *prod*; staging keys were a follow-up.
  - Naming hint: staging keys contain "staging" between underscores in the value.
- Owner: Caitlyn Levine driving comms with Wyndham; Diana / Jason owning SDK side. Not blocking me unless I touch Wyndham mobile flow.

Thread: https://canarytechnologies.slack.com/archives/C0A4EN8SJLA/p1776778205375569
SDK PR (Wyndham repo): https://github.com/WyndhamDigital/whr_frontend_reactnative/pull/1087