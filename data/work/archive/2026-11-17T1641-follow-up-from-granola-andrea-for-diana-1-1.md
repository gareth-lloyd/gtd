---
area: null
completed_at: 2026-11-19 16:28:56.528369
contexts: []
created: 2026-11-17 16:41:06.023653
defer_until: null
due: null
energy: low
id: 2026-11-17T1641-follow-up-from-granola-andrea-for-diana-1-1
order: null
output: |
  ## Agent run 2026-11-18T12:31

  **Status: the follow-up did not happen. The IHG topic was not raised in today's Diana 1-1, and Andrea's talking points never arrived.**

  ### What the follow-up was
  From the Andrea 1-1 on 2026-11-17 (https://notes.granola.ai/d/bd917df5-ed58-42be-bae1-88dc74777eb0, transcript ~16:32-16:41):
  - IHG V3 catalog + amenity-in-check-in rollout, hard deadline **3 Dec**, Tincho building.
  - Loyalty upsells cannot be removed from the upsell list as planned: guests on older SDK builds have no forced update, and IHG is slow to take new SDK versions.
  - Andrea's proposed solution: leave the IHG upsell provider as is (keep creating loyalty upsells), add the loyalty amenity in the check-in flow via a new provider, and have an API endpoint filter by SDK version (old SDK gets loyalty amenities in the upsell list, new SDK has them filtered out).
  - Open question: who owns the filtering endpoint. You suggested the mobile team (they have done backend work for app functions and have the context with AD). Andrea: it depends on whether it is too late to change what the new SDK calls for this release; if it is, the logic lives in In-Stay as a version branch.
  - Agreed: Andrea asked whether you wanted to give Diana a heads up; you said you were meeting Diana the next morning and asked Andrea to ping talking points before her end of day. Andrea was also going to catch up with Connor and Taylor, then talk to Leah and Diana herself.

  ### What actually happened
  - **No talking points from Andrea.** Her DM with you has nothing after 16:14 EET on 17 Nov (last messages are the block-planning exchange). Nothing in the group DM with Connor either. Slack search for the topic (amenity / loyalty upsell / SDK version, since 15 Nov) found no thread on it involving Diana.
  - **Not raised with Diana.** Diana 1-1 today 11:01 (https://notes.granola.ai/d/a36bce8b-be1d-4ad9-bc54-fdeb927987b8): full transcript read; no mention of IHG, amenity, loyalty upsells, or SDK version filtering. Your two items were the shadowing sessions and nothing else; the call ended at ~11:16.
  - I found no evidence that Andrea has spoken to Diana directly yet (no Slack trace; a call would not show up).

  ### Related context worth knowing
  - Same class of problem is live right now in A/D: Leandro's PR #65312 (https://github.com/canary-technologies-corp/canary/pull/65312) fixes additional-guest steps being seeded into every flow regardless of manifest version, which breaks all current SDK clients. Thread: https://canarytechnologies.slack.com/archives/C029BPP02H0/p1794863517999539 . Leandro's position there is "version whole flows, don't filter steps", which is relevant to how the IHG amenity filtering should be framed.
  - Diana said today the block is now full (tipping funnel ~1 wk, additional-guests screen for the Australia activation ~1 wk, Best Western migration docs, possibly Team Chat). Any 3 Dec ask on mobile lands on a loaded team, so the "is it too late for the release" answer matters soon.
  - Diana also said she wants to meet Andrea (triage rotation, how projects get planned) and has questions prepared for Andrea and Martijn but has not sent them. One Andrea-Diana conversation could cover both.

  ### Suggested next step (drafts only, nothing sent)
  Draft DM to Diana:
  > Hi Diana, one thing I meant to raise this morning. For the IHG V3 + amenity rollout (hard date 3 Dec), enterprise found we can't remove loyalty upsells from the upsell list, because guests on older SDK builds never get the amenity step in check-in. Andrea's plan is to keep the loyalty upsells, add the amenity in the check-in flow, and have the API filter the upsell list by SDK version (old SDK sees them, new SDK doesn't). Two questions for you: (1) is it too late to change what the next SDK release calls / sends for this, and (2) does it make sense for mobile to own that version-filtering endpoint, or should it live in In-Stay? Andrea will reach out with details. It might be worth combining with the triage/planning chat you wanted with her.

  Draft DM to Andrea:
  > I didn't get to the IHG amenity / SDK version filtering with Diana this morning, sorry. I'm giving her a heads up now. Can you go to her directly with the details? The key question for her is whether it's too late for the next SDK release. She also wants time with you on triage rotation and planning process, so one call could cover both.

  ### Not covered
  - I did not check Linear for a ticket tracking the IHG amenity filtering work, or Diana's calendar for an existing Andrea meeting.
  ## Agent run 2026-11-18 (second pass: Andrea's assumptions checked against master)

  Supersedes the draft DM to Diana above: its question "is it too late to change what the next SDK release calls" is the wrong question.

  - No shipped SDK can receive the amenity step. `membership_gift` is only in the V3 manifest and `MANIFEST_MIN_VERSIONS` has no V3 row for iOS or Android, so mobile caps at V2 (`backend/canary/guest_experience/versioning.py`). Web gets V3 at once.
  - So for 3 Dec every app guest keeps the loyalty upsell whatever mobile does. The 3 Dec risk is web: web guests would see both the gift step and the welcome-amenity upsells unless the upsell list is filtered.
  - The filter key should be "does this client's flow contain the gift step" (manifest version), not raw SDK version. Flows are already selected per manifest, so an exclusion on the V3 flow's upsell step config needs no new endpoint and no SDK call change.
  - The upsell step handler cannot see the request or SDK version today (`StepHandler(configuration, session)`), so a header-based filter there needs plumbing.
  - Mobile's real work is later: render the gift step and add V3 minimums. V3 also bundles guest profiles, so declaring V3 opts the SDK into those too.
  - Not checked: Tincho's branch, the SDK repos, any upsell listing the app uses outside the check-in flow, the "300 hotels" figure, forced-update capability.
  ## Agent run 2026-11-18 (third pass: other factors; corrects the second pass)

  Correction: the second pass read a local master from 2026-10-30. Two of its points are wrong: mobile has already built the gift step, and the manifest split is being reworked so V3 no longer drags in guest profiles.

  - Mobile work is done: MOB-1364 (https://linear.app/canary-technologies/issue/MOB-1364), MOB-1365, MOB-1366 are Done. iOS 1.6.3 and Android 1.11.2 render `membership_gift`.
  - Backend switch-on is not live. PR #63584 (https://github.com/canary-technologies-corp/canary/pull/63584) was merged into the stack branch of PR #64335 (https://github.com/canary-technologies-corp/canary/pull/64335), not master. #64335 is approved, open, self-rated High risk, and needs a re-seed of v3 hotels after deploy. It asks mobile to confirm the deposit minimums before merge.
  - The IHG app is far behind. Groundcover, last 3h, SDK requests mentioning ihg- hotels: iOS 1.3.12 and 1.2.4, Android 1.7.1 and 1.5.7. None reach 1.6.3 / 1.11.2. Small sample, log lines not guests.
  - Hotel scope for the v3 move is small: PR #64702 (https://github.com/canary-technologies-corp/canary/pull/64702, ENT-8163, draft) moves only not-live IHG GMS Core hotels, about 125 (93 US, 32 EU). Live hotels go through A/D's AD-10588.
  - ENT-8166 "Update Welcome Amenity Flow" (https://linear.app/canary-technologies/issue/ENT-8166) is Todo, unstarted, Tincho, no due date. It gates #64702. Nothing in onboarding on master creates MembershipGift rows yet.
  - Nothing dedupes gift step vs loyalty upsells on master. A web guest would see both and could pick both.
  - A guest who finishes check-in in the app and later opens the web link does not get web-only steps (#64335 notes), so old-app guests only ever get the amenity through the upsell.
  - Possible kiosk coupling, unverified: PR #64837 says kiosk finds a gift's PMS package by upsell code.
  - Revised ask for Diana: confirm the deposit minimums on #64335, and what it takes to get IHG onto iOS 1.6.3 / Android 1.11.2. No new mobile build work for 3 Dec.
project: null
source_id: null
tags: []
time_minutes: 5
title: follow up from granola andrea for Diana 1-1
updated: 2026-11-19 16:28:56.528350
waiting_on: null
waiting_since: null
working_on: true
---