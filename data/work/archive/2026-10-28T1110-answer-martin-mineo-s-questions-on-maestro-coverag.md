---
area: null
completed_at: 2026-10-28 14:04:46.486923
contexts:
- react
created: 2026-10-28 11:10:01.001596
defer_until: null
due: null
energy: medium
id: 2026-10-28T1110-answer-martin-mineo-s-questions-on-maestro-coverag
order: null
output: |
  ## Agent run 2026-10-28T13:55
  Already answered; no reply from you is needed.

  Thread (https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1793114645344669?thread_ts=1793114645.344669&cid=C09M5GRJPL2):
  - Martin (2026-10-27 17:24) asked the mobile group: (1) do BW and Wyndham integrate through the React Native SDK or the native ones, and (2) may he add `<screen>_<element>` test ids to RN Demo's screens (only 4 today, on the config screen) and send the PR for review.
  - Diana Perez Afanador replied 8 minutes later (https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1793115153015059?thread_ts=1793114645.344669&cid=C09M5GRJPL2): (1) Wyndham and BW both integrate through RN, and RN calls the native flows internally, but some bridging bugs only show up when you test RN directly; (2) the internal flows already have the native test ids, so only the RN Demo app's own screens need new ones.
  - Martin replied "thanks" at 18:55, so the thread is closed.

  Nothing to add unless you want to endorse the plan. Optional one-liner, not sent:
  > +1 to Diana. Since BW and Wyndham both ship through RN, a few smoke flows on RN Demo (launch SDK → one check-in path → return to host) catch bridging regressions the native-sample flows can't. Happy to review the test-id PR.
project: null
source_id: https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1793114645344669?thread_ts=1793114645.344669&cid=C09M5GRJPL2
tags:
- morning-gtd
- slack
time_minutes: 15
title: Answer Martin Mineo's questions on Maestro coverage for the RN demo (#epd-mobile)
updated: 2026-10-28 14:04:46.486908
waiting_on: null
waiting_since: null
working_on: false
---

Martin is asking the mobile group whether Maestro flows should also cover the React Native demo, and which SDK to target. You read it but haven't replied.
https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1793114645344669?thread_ts=1793114645.344669&cid=C09M5GRJPL2