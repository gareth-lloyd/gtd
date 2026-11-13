---
area: null
completed_at: 2026-11-12 13:04:35.823313
contexts: []
created: 2026-11-12 12:11:49.812476
defer_until: null
due: null
energy: low
id: 2026-11-12T1211-bw-mobile-app-sitch
order: null
output: |
  ## Agent run 2026-11-12T12:22

  Read-only research in #best-western-mobile-app-project. Nothing was posted or changed.

  ### Why you were pulled in
  Diana tagged you with no text at 11:13 GMT today, at the end of Connor's thread
  (https://canarytechnologies.slack.com/archives/C0AQLLSLGH0/p1794257012596689), and you were added to the channel.
  She did not say what she wants. Nothing in your DM with her explains it either.
  My read (inference, not stated): she wants your view on the open engineering question in that thread, which is
  whether Canary mobile should work inside BWH's app codebase, and what that would cost in Q4B.

  ### The situation
  - BWH (app is being rebranded WorldHotels) had Telus build its app rebuild, embedding the Canary RN SDK with custom views. Scope for Canary is check-in only.
  - Telus has left one developer behind. BWH says much of the app is in a bad place and is negotiating for Telus to supply more developers at Telus's cost or a steep discount.
  - On the 11-09 testing call the Canary team concluded Telus probably built the integration wrong, including suspected hard-codes for the reg card. BWH floated an 11/24 date that Caitlyn laughed at, and on 11-03 she said she "would be shocked if Jan 5 happened".
    Thread: https://canarytechnologies.slack.com/archives/C0AQLLSLGH0/p1794253103546139
  - Canary QA (Martin) still has no test builds and no PMS access (AutoClerk test lab), which he first asked for on 10-20.

  ### What Connor asked (11-09)
  1. Priority 1: get Martin test builds (iOS and Android) and AutoClerk PMS access.
  2. Priority 2: get codebase access so Canary removes the Telus hard-codes itself. He asked what Q4B work this would displace.

  ### Where the thread landed
  - Caitlyn: it would delay BLE in the Wyndham app and the Guest App. Q4B list is Apple/Google Pay for Wyndham, BLE in the Wyndham SDK, BLE offline support, deep links (IHG commitment by EOY), accessibility certification, Guest App.
  - Caitlyn set out three models: (1) Wyndham model, Canary integrates in their code; (2) IHG model, Canary sits beside their devs; (3) Telus owns it. She prefers 2. Her worry about 1 is that with no Telus resource Canary ends up fixing things indefinitely.
  - Diana: sees the risk and wants explicit ownership boundaries, but notes Wyndham-model velocity is much better than IHG. She flags that BWH uses custom views, so UI ownership is an extra question. She suggested a meeting.
  - Martin is on vacation 11-30 to 12-08.
  - A call (with BWH's Dave and Monte, per Connor) was rescheduled to Thursday, which is today, 11-12.

  ### What changed after that thread (11-10 and 11-11)
  - Leopoldo, after talking to Ron Stenger: no agreement exists to develop BWH's app; pause any code work until a lightweight SOW and contract terms are signed (incident liability, support ownership, security exposure). Connor agreed.
    https://canarytechnologies.slack.com/archives/C0AQLLSLGH0/p1794349692962069
  - Connor in the same thread: Monte (BWH) does not want to give Canary codebase access. BWH is bringing Telus back for the unfinished work, and the Canary cleanup is part of that. So option 1 is off the table for now.
  - Test builds are coming, with limited seats and probably shared logins: Martin, Caitlyn, Connor, then Lorena, who asked for Luan Silva to be added. Diana asked for access too. PMS access is requested but not confirmed.
    https://canarytechnologies.slack.com/archives/C0AQLLSLGH0/p1794345467052599
  - Martin's WorldHotels MVP test cases have been waiting on Caitlyn's review since 11-04; he chased on 11-11 twice.
    https://app.notion.com/p/canarytechnologies/WorldHotels-Mobile-App-Canary-MVP-Test-Cases-draft-for-review-40e814686151813d8db1d4ce23b8f3aa

  ### Open items that could want your input
  - Diana's meeting on the engagement model has not been set up, and the codebase question is half-closed by BWH's refusal. Worth asking Diana what she wants from you.
  - If codebase access comes back, it needs the SOW first and it competes with BLE for Wyndham and the Guest App.
  - Not checked: today's rescheduled call, the BWH Teams channel, and anything outside this Slack channel.

  ### Other references
  - Test plan: https://app.notion.com/p/canarytechnologies/Test-plan-Mobile-App-SDK-Best-Western-3ff8146861518064b4e1dfc7567ebcab
  - BWH Check-In Demo (QA requests and open questions): https://app.notion.com/p/canarytechnologies/BWH-Check-In-Demo-3f281468615180f186cbfcb2130c4f91
project: null
source_id: null
tags: []
time_minutes: 5
title: BW mobile app sitch
updated: 2026-11-12 13:04:35.823295
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C0AQLLSLGH0/p1794257012596689