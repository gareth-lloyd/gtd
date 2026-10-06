---
area: null
completed_at: 2026-10-06 13:48:15.255558
contexts:
- react
created: 2026-10-06 07:15:43.059794
defer_until: null
due: 2026-10-06
energy: medium
id: 2026-10-06T0715-answer-diana-in-epd-enterprise-can-wyndham-mobile
order: null
output: |-
  ## Agent run 2026-10-06T13:41

  Nothing was posted. A draft reply is at the bottom for you to send.

  ### Where it stands

  - Nobody has replied to Diana's 10-05 message. It is the last message in the thread (https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1791186249199629?thread_ts=1790880548.683779&cid=C047K6WSUJY).
  - Guido's 10-01 ask to Connor/Ani is still unanswered. It is the last message in that thread (https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1790889390967789?thread_ts=1789059484.362059&cid=C04STT7UPRQ).
  - Your direct question ("Wyndham can proceed on a mix of V2 and V3?", https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1790934353953989?thread_ts=1790880548.683779&cid=C047K6WSUJY) never got a yes or no. Diana's reply explains the IHG/Wyndham difference in SDK update speed, and adds that Wyndham SDK changes get harder once the app is in production.
  - Caitlyn was onsite at Marriott on 10-05 and said she would be slow to respond (https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1791222330712999).
  - I could not find the "date is likely slipping" statement in Slack, so the current launch date is unconfirmed from what I can see.

  ### What the answer looks like

  A mix is technically fine, and it is also unavoidable. The open question is whether the v2 experience in the app is good enough to ship.

  - Both paths work. Dana: "we tested both. V2 and V3 should both work properly" (https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1790888097576389?thread_ts=1790880548.683779&cid=C047K6WSUJY).
  - The v2 gap is on the mobile side. Diana (https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1790934278871299?thread_ts=1790880548.683779&cid=C047K6WSUJY): on v2 the app shows every screen in a hardcoded order and uses the config only to show or hide buttons such as skip. Only the credit card step is skipped, and only on iOS (via `cc_step_status`); Android does not. She can add step skipping for v2 if the backend exposes a flag, as long as the Wyndham SDK can still be updated.
  - Wyndham Connect defaults are ID step disabled and additional guests disabled (`backend/canary/enterprise_wyndham/configs/wyndham.py:229`). So on a v2 Wyndham the app presumably shows screens the hotel has turned off. That is my inference from Diana's description; nobody has stated what a Wyndham guest sees on v2.
  - Not every Wyndham can be on v3 by launch whatever Connor/Ani decide. `get_compatibility_blockers` (`backend/canary/guest_experience/services/v3_migration.py:64`) blocks card upload policy always/high-risk, surcharge manual correction, and Canary-managed payments without hotel-wide deposits. Guido's Wave 1 is narrower still: Stripe direct, no ID verification, no deposits, no surcharges. Hotels outside Wave 1 stay on v2 at launch.
  - Guido's numbers on 10-01: about 600 Wyndhams on v3, about 1000 planned by Oct 7, and he can go faster if Connor/Ani agree (https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1790882392340139?thread_ts=1790880548.683779&cid=C047K6WSUJY). I did not get a current count.
  - Launch-day exposure is small. Connor says Wyndham is enabling for a small percentage of guests first, not per property (https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1790866004790319?thread_ts=1790006579.628339&cid=C09M5GRJPL2).

  ### A possible third route, unconfirmed

  `migrate_hotel_to_v3 --sync-only` seeds a hotel's v3 flow without flipping web traffic (`sync_v3_flow`, `v3_migration.py:91`). A docstring in `backend/canary/guest_experience/services/migration_stats.py:301` says the mobile team's test hotels are already in this state: "the SDK is served v3 and the flip is deliberately withheld". If the Wyndham SDK can be pointed at v3 for a hotel whose web guests are still on v2, the app could launch all-v3 without accelerating the web rollout. The SDK is not in this repo, so I could not check how it picks v2 or v3. Only Diana can say. The same Wave 2-4 blockers apply unless `--force` is used.

  ### The decision to force

  1. Launch on the mix and accept v2 behaviour for the hotels not yet migrated.
  2. Fix v2 step skipping in the SDK before the production build goes out. Diana's point is that this window closes at launch.
  3. Move all of Wave 1 to v3 now. This needs Connor/Ani's go-ahead for Guido and still leaves the non-Wave-1 hotels on v2.

  My recommendation: 3 plus a decision on 2. Wave 1 hotels are the ones with ID and deposits off, which is where v2's show-every-screen behaviour is most wrong, so moving them removes most of the mismatch. The remainder needs either the SDK fix or an explicit "v2 is acceptable" from Caitlyn.

  ### Draft reply for the #epd-enterprise thread (not sent)

  > Thanks @Diana. So v3 isn't a hard requirement for Wyndham, but anything we want to change in how the app handles v2 has to go in before the production launch.
  >
  > We will launch on a mix either way. Guido has about 600 Wyndhams on v3 and plans about 1000 by the 7th, and hotels with card upload, surcharge correction or Canary-managed payments can't move to v3 yet.
  >
  > So the question is whether v2 in the app is good enough to ship. Most Wyndhams have ID and additional guests turned off. On a v2 hotel, does the guest still see those screens?
  >
  > If yes, I see two things to decide this week:
  > 1. @Connor @Ani can Guido migrate the rest of Wave 1 now? He has been waiting on a go-ahead since last Thursday: https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1790889390967789?thread_ts=1789059484.362059&cid=C04STT7UPRQ
  > 2. @Caitlyn for the hotels that stay on v2, do we fix step skipping in the SDK before launch, or accept it? What is the launch date now?
  >
  > @Diana one more: can the SDK use v3 for a hotel whose web check-in is still on v2? We can seed the v3 flow without flipping web traffic, and I think that's how your test hotels are set up.

  ### Not done

  - No Slack messages sent, and no reply to Guido in #wyndham.
  - No live count of Wyndhams on v2 vs v3. The canary MCP servers failed to connect and the Teleport session has expired.
project: 2026-09-08-mobile
source_id: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1791186249199629?thread_ts=1790880548.683779&cid=C047K6WSUJY
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Answer Diana in #epd-enterprise: can Wyndham mobile launch on a mix of check-in
  v2 and v3?'
updated: 2026-10-06 13:48:15.255534
waiting_on: null
waiting_since: null
working_on: false
---

Diana answered my question on 10-05: IHG needed v3 because their SDK updates are slow; Wyndham's SDK is still updatable, but harder once in production. Nobody has yet confirmed whether all Wyndhams must be on v3 before the mobile launch (~Oct 7; Caitlyn said the date is likely slipping). Guido has been waiting since 10-01 in #wyndham for a go-ahead from Connor/Ani to migrate all of Wave 1 faster.
https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1791186249199629?thread_ts=1790880548.683779&cid=C047K6WSUJY
Guido's ask: https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1790889390967789?thread_ts=1789059484.362059&cid=C04STT7UPRQ