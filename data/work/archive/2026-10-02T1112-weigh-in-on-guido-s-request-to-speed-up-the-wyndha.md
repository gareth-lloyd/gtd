---
area: null
completed_at: 2026-10-02 13:01:46.299973
contexts:
- react
created: 2026-10-02 11:12:13.860716
defer_until: null
due: null
energy: medium
id: 2026-10-02T1112-weigh-in-on-guido-s-request-to-speed-up-the-wyndha
order: null
output: |-
  ## Agent run 2026-10-02T09:31:06Z

  Nothing was sent or posted. A draft reply is at the bottom for you to send or discard.

  ### Recommendation
  Don't block Guido, but don't agree to "all Wyndhams on v3 by Oct 7" either. Three points are worth making in his thread:
  1. "All of Wave 1" will not get mobile what it asked for. About 5,200 Wyndhams are still on v2, and nearly all of them tokenise through the hotel payment gateway, which the migration code classes as Wave 2, not Wave 1.
  2. Non-US/CA Wyndhams are an untested cohort on v3. I found none on v3 yet, so they should go as a small pilot batch with a day of monitoring, not all at once.
  3. The mobile requirement is still unconfirmed. Diana has not replied (checked 12:30 EEST), Caitlyn said on Sep 30 the date is "likely getting pushed", and Connor says Wyndham starts with a small percentage of users.

  ### What the data says
  Source is the Snowflake mirror of prod (CANARY_RAW.CANARY, US region only), filtered to active, non-demo hotels with check-in and a `wyndham-` slug. CDC rows ran up to 2026-10-02 04:37 UTC.

  | | Hotels |
  | --- | --- |
  | Wyndhams on v3 | 428 |
  | Wyndhams on v2 | 5,207 |
  | v2, same config shape as the migrated ones (hotel PG with config, no deposits, ID step required, US/CA) | 5,006 |
  | v2, not tokenising via hotel PG ("Stripe direct", the code's Wave 1) | 163, of which 110 are outside US/CA |
  | v2, outside US/CA in total | 128 |
  | v2, Canary processes deposits (Wave 3) | 11 |
  | v2, card upload policy "always" (a v3 compatibility blocker) | 5 |
  | v2, ID step with OCR (Wave 4) | 2 |

  - All 428 v3 Wyndhams tokenise via the hotel gateway, so by the code's taxonomy they are Wave 2, not the "stripe direct" Wave 1 that Guido describes. Either the plan page defines a Wyndham-specific Wave 1 or his description is loose. I could not read the plan page (https://pages.cnry.cloud/v3-migration-and-test-plan/ is behind Cloudflare login), so this is an open question for him.
  - My count of 428 does not match Guido's figures (~600 before the Oct 1 batch, ~850 after). 428 is almost exactly your 177 from Sep 23 plus his 250. The gap could be other regions, mirror lag, or my filters. I did not query EU or AP. Worth asking him for the dashboard number.
  - The homogeneity cuts in Guido's favour: 5,006 of the remaining hotels look exactly like the 427 already migrated, so bulk migration of that group is lower risk than the raw number suggests.
  - Caitlyn's example (v2 mobile shows the ID screen even when it is disabled) barely applies to Wyndham, because about 99% of Wyndhams have the ID step required anyway. The useful question for Diana is which screens v2 mobile shows that the standard Wyndham config has switched off.

  ### Where people already stand
  - Connor, Sep 23 group DM (https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1790165191647799): "we're going to need to migrate in bulk soon", comfortable with A/D using Wyndhams, but would "prefer not to roll out v3 broadly until it's stable and verified for the variety of check-in configs". He will enable v3 in the ENT scripts once A/D is confident.
  - Connor, Oct 1 in #epd-enterprise (https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1790880548683779): surprised that v3 is a mobile dependency, it had not been flagged. Dana says both v2 and v3 were tested on mobile and should work.
  - Guido, Sep 10 (https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1789059484362059): thought end of September was "a bit early and risky" and preferred spreading to end of October.
  - Ani, Sep 11, same thread: avoid sites with a clear pathway to the Wyndham team or that come up often in conversation. Nobody has turned that into a hold-out list.
  - Connor and Ani have not answered Guido's Oct 2 request yet (https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1790889390967789?thread_ts=1789059484.362059&cid=C04STT7UPRQ).

  ### ENT-side costs of a full-estate move
  - Onboarding scripts still default new Wyndhams to v2 (Andrea, Oct 1). "Every Wyndham on v3" will not hold for new hotels until that changes.
  - The reg card plan now fails on v3 hotels: ENT-7607, PR #57957 (https://github.com/canary-technologies-corp/canary/pull/57957), verified at `backend/canary/onboarding/plans/registration_card_plans.py:69`. That is the guard you proposed, and it means any scripted Wyndham reg card change is blocked for every migrated hotel until the scripts are v3-aware.
  - The QR poster routed guests to v2 on migrated hotels when you checked on Sep 23. I did not verify whether that has been fixed.
  - v3 is still producing fixes: Lea's PR #58735 (https://github.com/canary-technologies-corp/canary/pull/58735) fixes a bug "now surfacing due to V3 schemaform validation", and Fede shipped several bug-bash fixes on Oct 1.
  - Rollback exists (`revert_hotel_from_v3` management command) and A/D has a fleet monitoring skill (`watch-v3-fleet`).

  ### Draft reply for Guido's #wyndham thread (not sent)
  > Weighing in from ENT, since I raised the rollout question in #epd-enterprise. Three things before the rest of Wave 1 goes:
  > 1. Scope. How many hotels is "all of Wave 1"? By my count around 5,200 Wyndhams are still on v2 and nearly all of them tokenise through the hotel gateway, which the dashboard calls Wave 2. Wave 1 alone won't get mobile to "every Wyndham on v3".
  > 2. Non-US/CA. I can't see any non-US/CA Wyndham on v3 yet. Can we do 10-20 of those first and watch them for a day before the rest?
  > 3. The mobile requirement isn't confirmed. Diana hasn't replied, the Oct 7 date may move, and Wyndham starts with a small share of users. I'd hold the "all by next week" target until she does.
  >
  > On our side: ENT onboarding scripts still default new Wyndhams to v2, and the reg card plan now refuses v3 hotels (ENT-7607). We need both v3-aware before the whole estate moves.

  ### Not done
  - Plan page not read (login wall), so Guido's Wave 1 size and hold-out list are unknown to me.
  - EU and AP regions not counted.
  - No check of v3 error rates on the migrated hotels. The canary MCP and Teleport sessions were down.
project: null
source_id: https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1790889390967789?thread_ts=1789059484.362059&cid=C04STT7UPRQ
tags:
- morning-gtd
- slack
time_minutes: 15
title: Weigh in on Guido's request to speed up the Wyndham check-in v3 migration
updated: 2026-10-02 13:01:46.299967
waiting_on: null
waiting_since: null
working_on: false
---

Guido migrated 250 more Wyndhams on Oct 1 (~850 on v3) and wants to do all of Wave 1 now, incl. non-US/CA and larger hotels, because mobile wants every Wyndham on v3 before the ~Oct 7 mobile launch (date may slip). He asked Connor and Ani, not you by name, but you told #epd-enterprise that Connor wants all Wyndham capabilities supported in v3 before wide rollout. Your question 'why is v3 needed for mobile?' got a provisional answer from Caitlyn (v2 mobile shows every check-in screen regardless of config); Diana still to confirm.
https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1790889390967789?thread_ts=1789059484.362059&cid=C04STT7UPRQ
https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1790880548683779