---
area: null
contexts:
- react
created: 2026-05-15 07:23:46.016383
defer_until: null
due: 2026-05-15
energy: low
id: 2026-05-15T0723-advise-rachel-re-wyndham-whatsapp-number-190291804
order: 1
output: |
  ## Agent run 2026-05-20T15:40Z

  ### Who owns +19029180410?
  Per ENT-5878 (the WCP offline-WhatsApp cohort I worked on in April), this number maps to:
  - **Hotel:** Microtel Summerside (id 7029)
  - **WABA:** 690171786901502 (shared with Microtel Kitimat / +17786553494, which was successfully reonboarded on Apr 24)
  - **Twilio subaccount:** ACe69bf43d4db3b97ef1a7c4d29e1209e3
  - **Original block reason:** Twilio error 63120 / Meta Business Account locked (Category 1 in ENT-5878). Meta finally lifted the block; only this sender is still pending registration.

  ### Is Microtel Summerside still on WCP / still active?
  Yes. Datadog shows hotel_id:7029 producing ~9.9k logs over the last 14 days across canary, event-batch-processor, celery-segmentation, and message-scheduler services. It is a live WCP hotel, not churned.

  ### Why is the number on the WhatsApp Business **App** version?
  Someone with possession of the SIM/eSIM downloaded the WhatsApp Business *consumer app* (not the API) and verified +19029180410 on it. That happens when a franchise staff member or owner thinks WhatsApp is broken, installs the app to keep using the number, and unwittingly claims it on Meta's app track. While the number is registered to the app, Twilio cannot reonboard it to the WA Business API — the two registrations are mutually exclusive.

  ### Recommendation for Rachel
  Default position: **yes, we want it back on WCP** — the hotel is live and the rest of the WCP fleet is being reonboarded after this exact Meta unblock cycle. But because someone at the property has actively claimed it on the WhatsApp app, do NOT just tell Mindy to proceed silently. Steps:

  1. **Reply to Mindy:** "Please hold — we want to reonboard but need to confirm with the property first, since someone there has claimed the number on the WhatsApp Business app and forcibly migrating it back will log them out mid-conversation."
  2. **Escalate to Wyndham corporate (or whoever owns the WCP relationship for franchise outreach)** to ask Microtel Summerside:
     - Are they actively using +19029180410 for guest comms via the WhatsApp Business app today?
     - Do they want to return to managed/Canary WhatsApp (i.e. the WCP experience), or have they deliberately moved off?
     - If yes to returning: they need to delete the WhatsApp Business app account on this number first (Settings → Account → Delete my account). Then Twilio can proceed.
  3. **If hotel confirms "we moved on / keep us on the app":** Mark this sender as decommissioned on our side (set `twilio_whatsapp_sender_status` accordingly, clear `whatsapp_phone_number` / disable `allow_send_whatsapp`). Tell Mindy to close the ticket — we no longer need this number on WA Business API.
  4. **If hotel confirms "yes please reonboard" + has removed the app:** Tell Mindy to proceed with API registration.

  ### Suggested Slack reply to Rachel (draft — not sent)
  > Rachel — that number (+19029180410) is Microtel Summerside (hotel id 7029). They're still a live WCP hotel in our system, so by default we do want WhatsApp back online for them. But because someone at the property has taken the number onto the WA Business *app*, forcibly migrating it back to the API will log them out of whatever conversations they're having right now.
  >
  > Before Mindy proceeds, can we get someone on the Wyndham side to reach out to the property and confirm (a) whether they're actively using the app, and (b) whether they want us to put it back on Canary/WCP? If yes, they'll need to delete the WhatsApp Business app account on that number first. If they say they're happy on the app, we'll decommission the sender on our end instead and Mindy can close the ticket.
  >
  > Happy to send any details to whoever picks up the franchise outreach.

  ### Open follow-ups (not blockers for replying to Rachel)
  - +17802642966 (Days Inn Conference Centre Camrose Norsemen, hotel 129666) is the other remaining WCP number still pending after Meta unblock — worth checking with Rachel whether Mindy has any update on it too.
project: 2026-04-16T1351-ship
source_id: https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1778707537462869?thread_ts=1775646924.310129&cid=C04STT7UPRQ
tags:
- morning-gtd
- slack
time_minutes: 10
title: 'Advise Rachel re: Wyndham WhatsApp number +19029180410'
updated: 2026-06-16 15:53:03.050349
waiting_on: null
waiting_since: null
working_on: false
---

Meta lifted block but number is on WhatsApp App version; Mindy needs to know whether to proceed / is Wyndham still using it. https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1778707537462869?thread_ts=1775646924.310129&cid=C04STT7UPRQ