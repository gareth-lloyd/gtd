---
area: null
contexts:
- consume
created: 2026-05-25 04:18:16.620643
defer_until: null
due: null
energy: low
id: 2026-05-25T0418-read-rachel-kim-s-whatsapp-fallback-report-wyndham
order: null
output: |
  ## Agent run 2026-05-25T12:00:00Z

  Read Rachel Kim's reply (2026-05-21) in the #wyndham thread Ani started about WhatsApp delivery failures on Wyndham US/Canada properties.

  ### Two distinct patterns Rachel identified

  1. **Low-volume hotels (top of Ani's list — e.g. Super 8 Corvallis, Baymont Anderson).** Front-desk staff are sending manual messages with *both* SMS and WhatsApp selected as channels. SMS delivers; WhatsApp fails because the guest doesn't have WhatsApp. The UI exposes the WhatsApp option because the hotel has `allow send whatsapp = true`. **This is essentially expected behavior / a UX setting question, not a bug.**

  2. **High-volume hotels — Puerto Varas, Casa Marina Sosua, Merida, Moose Jaw, Palacio Azteca.** These are sending **automated Guest Journey (GJ) WhatsApp messages** to guests without WhatsApp, and **we are NOT falling back to a different channel as we should**. This is the real bug — the WhatsApp→SMS (or other) fallback path is broken or missing for these 5 properties.

  ### Open / next-action implications for me

  - The 5 high-volume properties match the GTD title exactly (Casa Marina Sosua, Merida, Moose Jaw, Puerto Varas, Palacio Azteca). Rachel surfaced the fallback gap but did not (in this thread) propose a fix or owner.
  - No Linear ticket referenced in-thread. Worth checking if there's already a ticket for the GJ WhatsApp fallback failure before filing one.
  - Ani had to chase Rachel after 3 days for the answer — thread is now resolved on her side.

  ### Links
  - Thread: https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1779389756947469?thread_ts=1779119627.606199&cid=C04STT7UPRQ
  - Omni dash Ani shared: https://canarytechnologies.omniapp.co/e/10:114Bb6bs/10

  No actions taken on external services. Recommend: (a) search Linear for an existing GJ WhatsApp fallback ticket, (b) if none, file one against the messaging team scoped to the 5 hotels above.
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1779389756947469?thread_ts=1779119627.606199&cid=C04STT7UPRQ
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 10
title: 'Read: Rachel Kim''s whatsapp-fallback report (#wyndham)'
updated: 2026-05-25 12:06:01.223084
waiting_on: null
waiting_since: null
working_on: false
---

GJ message whatsapp fallback issue across Casa Marina Sosua, Merida, Moose Jaw, Puerto Varas, Palacio Azteca. https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1779389756947469?thread_ts=1779119627.606199&cid=C04STT7UPRQ