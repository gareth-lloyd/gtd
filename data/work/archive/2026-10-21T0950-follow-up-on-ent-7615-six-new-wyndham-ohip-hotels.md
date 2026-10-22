---
area: null
completed_at: 2026-10-21 14:47:03.012480
contexts:
- react
created: 2026-10-21 09:50:09.708635
defer_until: null
due: 2026-10-21
energy: medium
id: 2026-10-21T0950-follow-up-on-ent-7615-six-new-wyndham-ohip-hotels
order: null
output: |-
  ## Agent run 2026-10-21T11:05

  **Ryan is right.** None of the Wyndham OHIP configs created since Sept 14 received a single streamed business event in the last 24h (Groundcover, `event:consume.event_payload`). The 5 polling configs log `business_events.no_events` every 15 minutes. The canary2 sockets for chains WHRMID3 and WHRLT3 are healthy and stream events for neighbouring hotels, so the gap is per hotel: Oracle has no publisher bound for these hotel codes.

  **Why.** A publisher is a per-hotel Oracle binding: subscriber OHIP16680 (canary2) or OHIP588 (canary1), plus hotelId and the reservation source. Kim bound the existing fleet when she moved it to canary2 (Connor's plan, Sept 14: https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1789397041634739). Nothing in our onboarding creates a publisher. `wyndham_pms_config_provider.py:145-183` sets `supports_business_events` only for US/CA hotels. It sets no `business_events_fetch_method`, so the default POLL applies. It sets no `streaming_*` creds, and `client_id` falls back to canary1. So new hotels get no publisher.

  **Config state.** Gateway `oracle_ohip_oracleohip`, deduplicated:
  | id | chain | hotel | created | fetch env | stream env | method |
  |---|---|---|---|---|---|---|
  | 24360 | WHRMID3 | 61445 | 09-14 | c1 | c2 | STREAM |
  | 24689 | WHRLT3 | 55173 | 09-22 | c1 | c2 | STREAM |
  | 24722 | WHRMID3 | 61562 | 09-23 | c1 | - | POLL |
  | 24723 | WHRMP41 | 592590 | 09-23 | **c2** | - | POLL |
  | 24724 | WHRFUL3 | 61495 | 09-23 | c1 | - | POLL |
  | 24854 | WHRMP79 | 58929 | 09-25 | **c2** | - | POLL |
  | 24855 | WHRMP79 | 58930 | 09-25 | **c2** | - | POLL |
  | 25647 | WHREX04 | 60348 | 10-19 | **c2** | - | POLL (disabled) |
  - Ryan's "six" is probably the six configs before WHREX04, which is new and disabled. I count 7 enabled.
  - Only 24360 and 24689 match the ENT-7615 target setup (fetch on c1, stream on c2). Someone set those by hand.
  - Ryan's "three chains on billed canary2" are WHRMP41, WHRMP79 and WHREX04. The canary2 client_id comes from their OHIP Credentials By Chain Code onboarding values.
  - 61562 is POLL on c1 with no streaming creds, even though 61445 in the same chain streams.

  **Can the gateway push publishers? Not today.**
  - The cockpit's "Push publisher" (`admin.py:676`, `services/migration_status.py:280`) does call createPublishers, one hotel at a time.
  - Bug: `subscriber_interface_code` (`migration_status.py:69-88`) keys on `client_id`, not `streaming_client_id`. For split configs like 24360 and 24689, the sweep reads publishers from canary1 (OHIP588), and a push would bind to canary1 while the socket listens on canary2. The success message would still say "Pushed to Canary 2". The cockpit also labels these configs as canary1.
  - The push needs a reservation source captured by the sweep or confirmed by the customer. A brand-new hotel has neither, so the button is refused ("No reservation source to push").

  **Recommendation.**
  1. Short term: ask Kim to add the canary2 (OHIP16680) publisher for each new hotel as part of setup, as she did for the fleet. Start with these 7.
  2. In ENT-7615 (Ryan), make onboarding:
     - set c1 fetch plus c2 `streaming_*` creds and STREAM, as on 24360;
     - stop using canary2 client_ids for API calls on WHRMP41, WHRMP79 and WHREX04;
     - fix the existing 5 configs.
  3. Gateway: if we want to self-serve publishers, fix `subscriber_interface_code` to use the streaming client_id when one is set, and allow an explicit source code on push. Tag Khush, per Andrea's comment on the ticket.

  **Draft reply on ENT-7615 (NOT posted; needs your OK):**
  > Covering for Connor. Confirmed: none of the post-Sept-14 configs (61445, 55173, 61562, 592590, 61495, 58929, 58930) got a streamed event in the last 24h, while the WHRMID3/WHRLT3 canary2 sockets stream fine for neighbouring hotels. So it's per-hotel publishers. Nothing on our side creates them for new hotels, and the cockpit's Push publisher can't do it yet: it needs a captured source, and it picks the interface code from client_id, so on split c1-fetch/c2-stream configs it would bind to canary1. Proposal: short term, ask Kim to add the OHIP16680 publisher for each new hotel at setup (I can draft the ask). In this ticket, onboarding should set c1 fetch plus c2 streaming creds and STREAM, as on 24360/24689, and switch WHRMP41/WHRMP79/WHREX04 back to c1 for API calls. 61562 and 61495 also need streaming creds. cc @khushatcanary if we want the gateway to push publishers itself.

  **Not done.** I posted nothing anywhere. I couldn't find where Connor named you as cover. I didn't check the publisher source codes, because the migration-status table isn't mirrored to Snowflake.
project: 2026-08-31-ihg
source_id: https://linear.app/canary-technologies/issue/ENT-7615/wyndham-scripting-change-to-support-ohip-migration#comment-5317a340
tags:
- morning-gtd
- linear
time_minutes: 20
title: 'Follow up on ENT-7615: six new Wyndham OHIP hotels get no business events
  (Connor OOO)'
updated: 2026-10-21 14:47:03.012474
waiting_on: null
waiting_since: null
working_on: false
---

Ryan Rogers asked Connor (OOO this week) about Kim moving publishers to Canary 2: the six Wyndham OHIP hotels onboarded since Sept 14 receive no business events, so new hotels seem to get no publisher. Connor named me as cover.
https://linear.app/canary-technologies/issue/ENT-7615/wyndham-scripting-change-to-support-ohip-migration