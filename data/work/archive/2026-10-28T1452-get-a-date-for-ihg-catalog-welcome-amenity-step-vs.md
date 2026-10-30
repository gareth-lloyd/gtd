---
area: null
completed_at: 2026-10-29 15:59:29.403372
contexts:
- react
created: 2026-10-28 14:52:21.559382
defer_until: null
due: null
energy: medium
id: 2026-10-28T1452-get-a-date-for-ihg-catalog-welcome-amenity-step-vs
order: null
output: |-
  ## Agent run 2026-10-28T16:40
  **Answer: nobody has committed to a date.** No ticket exists for the catalog / welcome-amenity-step work, so there is nothing to date yet. Nothing was posted.

  **What exists**
  - Caitlyn, 10-23 (https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1792720325077329?thread_ts=1792692313.584389&cid=C03V5P4B48P): "by mid-November all IHG's should be on check-in v3 because they are expecting the separate Welcome Amenity step."
  - Taylor, 10-23, same thread: paused all IHG v3 migration until Andrea and Connor are back. Taylor won't ship the separate step until the Q4 copy, image and renaming changes are done.
  - Andrea, 10-26 (https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1793019778323619?thread_ts=1792692313.584389&cid=C03V5P4B48P): the step needs direct catalog writes, upsell-script changes so new IHGs don't get welcome-amenity upsells, and removal of those upsells from IHGs already configured. She called it "a medium sized effort". She gave no date.
  - Andrea, 10-27, same thread: "v3 as default" is not the same as "v3catalog as default". ENT will switch the scripts to v3 as the default once Connor gives the greenlight, "expected in the next week or so". That covers plain v3 only, not the catalog or welcome-amenity work.
  - Connor is at the BW conference through Wed 10-28.
  - Linear:
    - Project IHG Scripting - Q4A 2026 (https://linear.app/canary-technologies/project/ihg-scripting-q4a-2026-bca67c82a9ea): lead Andrea, target date 2026-11-30 (month resolution). Its summary names "separation of welcome amenity in the check-in flow" as in scope. No milestone or issue covers the catalog writes or the upsell removal.
    - ENT-7807 Welcome Amenity copy changes (https://linear.app/canary-technologies/issue/ENT-7807/ihg-q4-scripting-welcome-amenity-copy-changes): Connor, Todo, no due date.
    - Mobile SDK side: MOB-1364 iOS (https://linear.app/canary-technologies/issue/MOB-1364) and MOB-1365 Android (https://linear.app/canary-technologies/issue/MOB-1365) are both due 2026-11-03, unassigned. MOB-1426 Monaco (https://linear.app/canary-technologies/issue/MOB-1426) is Eric, Todo.

  **The gap:** Mobile expects mid-November (~11-15). The ENT project's only date is end of November. The work has no ticket or estimate, and it is gated on Connor's v3-default greenlight, so it can't start before ~11-04. A medium effort starting then probably misses 11-15.

  **Draft reply for the #ihg thread** (https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1792692313584389). NOT SENT; needs your OK:
  > @Andrea @Connor quick timing check. Caitlyn's note is that IHG expects the separate Welcome Amenity step by mid-Nov. The ENT side (catalog writes, stop adding WA upsells, remove existing WA upsells, plus ENT-7807 copy) has no ticket or date yet, and the Q4A project targets end of Nov. Can we get a ticket and a realistic ship date this week? If it's later than ~11-15, @Caitlyn Levine needs to reset IHG's expectation now, not mid-Nov.

  **Other options:** DM Andrea instead, or raise it in your next sync with her. If you want it tracked, I can draft an ENT ticket for the catalog + upsell-removal work under P-ENT-2357. Not created.

  ## Agent run 2026-10-29T15:40
  Nothing posted. Sources: the #ihg v3 thread (https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1792692313584389), your mobile check-in thread, and the code on master.

  ### Q1: What does IHG actually need? Do all hotels have to be on the v3 catalog?
  **No, the catalog isn't needed.** IHG wants the separate Welcome Amenity step in check-in. That requires each hotel to be on check-in **v3**. The field catalog is a separate switch.
  - The code has two flags. `checkin_version = v3` routes guests to the step flow. `uses_field_catalog` points the reg-card form at the field catalog. `V3MigrationService.migrate_hotel_to_v3` sets the first flag. `migrate_hotel_to_v3_and_catalog` sets both. See `backend/canary/guest_experience/services/v3_migration.py`.
  - The step is `MembershipGiftStepHandler` in `backend/canary/guest_experience/check_in/steps/membership_gift_step/handler.py`. It never reads the catalog. It shows when `hotel.has_membership_gifts` is on and the guest's tier has eligible `MembershipGift` rows.
  - Keeping IHG off the catalog is also the safer path. Tincho said non-US GMS Core reg-card scripts break on catalog hotels (https://linear.app/canary-technologies/issue/ENT-7720). Andrea separated "v3 as default" from "v3catalog as default" for the same reason.

  **Per-hotel work (my reading of the code):**
  1. Move the hotel to v3. ENT already plans to make v3 the script default once Connor gives the greenlight.
  2. Add a `MEMBERSHIP_GIFT` step to the hotel's flow. `CheckInFlowGenerationService` doesn't add this step on its own; I grepped and nothing in `guest_experience/services` creates it. So a script has to add it.
  3. Turn on `has_membership_gifts` and create `MembershipGift` rows with IHG's Platinum and Diamond options, plus the new copy and images (ENT-7807, and the images Loyalty sends by Nov 3).
  4. Remove the existing welcome-amenity upsell so guests don't get the offer twice. Today it comes from `WELCOME_AMENITY_BY_BRAND_US` in `onboarding/configuration_providers/ihg/ihg_upsells_provider.py`. Change the provider for new hotels and write a cleanup for hotels already configured.
  - Andrea's "directly writing to catalog" most likely means steps 2–3, which are v3 config and gift records, not the guest-field catalog. **I haven't confirmed that with her.** It's worth one question, because the answer decides whether catalog risk is in scope at all.

  **Mobile catch, verified in `guest_experience/versioning.py`:** `MEMBERSHIP_GIFT` only ships in manifest V3. `MANIFEST_MIN_VERSIONS` caps both iOS and Android at V2 because no released SDK supports V3. The new SDK (MOB-1364 / MOB-1365) has to add a V3 minimum, or app users will never see the step. Manifest V3 also includes the guest-profile steps (`MATCH_GUEST_PROFILE`, `SAVE_GUEST_PROFILE`), so that SDK has to render those too, or the manifest needs splitting. Worth checking that Mobile knows this.

  ### Q2: What's the timescale?
  **Mid-November is no longer the date. The real deadline is Dec 3 (Dec ~20 at worst).**
  - Caitlyn's "by mid-November all IHGs on v3" (10-23) came before the app plan settled. On 10-28 in your mobile check-in thread (https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1793210520419289?thread_ts=1791457530.248069&cid=C03V5P4B48P), she said IHG "decided they wanted to wait until the separate Welcome Amenity step is built to roll out at scale. The target for this to be in app is Dec 3 (or Dec ~20 if IHG's testing overflows past the planned sprint)".
  - Same thread: Taylor and Caitlyn agreed on about 5 pilot properties until full rollout.
  - Backward from the IHG app timeline:
    - **~Nov 10–11:** steps 1–3 done on the pilot and test hotels, with final copy and images, so joint testing (~Nov 12–24) runs on real config.
    - **By Dec 3:** steps 1–4 done on every IHG hotel in the app rollout, and the ENT scripts make it the default for new IHGs.
    - **Watch:** the step appears in web check-in as soon as a hotel is configured, so web goes live when the config does. Taylor won't ship it until the Q4 copy, image and renaming changes are done.
  - That fits the Q4A project's Nov 30 target (https://linear.app/canary-technologies/project/ihg-scripting-q4a-2026-bca67c82a9ea) far better than the mid-Nov gap from the last run suggested. The ~Nov 10 pilot config is the tight date. There's still no ticket for it.

  **Open questions:**
  - For Andrea: does "catalog" mean the gift config or the field catalog?
  - For Caitlyn or Mobile: does the Nov 10 SDK raise the V3 minimum, guest-profile steps included?
  - For ENT: who configures the ~5 pilot hotels by ~Nov 10?
project: null
source_id: null
tags: []
time_minutes: 15
title: Understand schedule and reason of V3 migration for IHG catalog + Welcome Amenity
  step
updated: 2026-10-29 15:59:29.403360
waiting_on: null
waiting_since: null
working_on: false
---

CONTEXT:
From: check-in v3 rollout research, 2026-10-28 (#ihg thread, #best-western thread, TOOL 'Automate Check-in V3 Onboarding' design)
Caitlyn (Mobile, #ihg 10-23): SDK hotels must be on v3; "by mid-November all IHGs should be on check-in v3" for the separate Welcome Amenity step.

Andrea wants the catalog / welcome-amenity work grouped with the quarterly IHG changes. It needs direct catalog writes plus upsell script changes to remove existing welcome-amenity upsells.

IHG APP timeline:
Thanks for the screenshot. I've added the timeline to the item's output. You'd already archived it, so I edited it where it is in archive and didn't move it.

  IHG app timeline:

  ┌──────────────────────────┬─────────────────────────────────────────────────────────────────────────────────────────────────────┬───────────────┐
  │           Date           │                                              Milestone                                              │     Owner     │
  ├──────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┼───────────────┤
  │ Tue Nov 3                │ iOS and Android dev complete (MOB-1364, MOB-1365); Loyalty sends the welcome amenity images by then │ Canary Mobile │
  ├──────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┼───────────────┤
  │ Wed Nov 4 – Mon Nov 9    │ Internal QA (4 days), including IHG flavor regression                                               │ Canary QA     │
  ├──────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┼───────────────┤
  │ Tue Nov 10               │ SDK version handed to IHG                                                                           │ Canary Mobile │
  ├──────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┼───────────────┤
  │ Wed Nov 11 – Thu Nov 12  │ IHG sprint starts and they create a branch with the new version                                     │ IHG app team  │
  ├──────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┼───────────────┤
  │ ~Fri Nov 12 – Fri Nov 24 │ Joint testing (1 week); IHG's analytics work may delay our access                                   │ Canary + IHG  │
  ├──────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┼───────────────┤
  │ Nov 25 – Dec 2           │ IHG release prep (includes Thanksgiving)                                                            │ IHG           │
  ├──────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┼───────────────┤
  │ Thu Dec 3                │ Release                                                                                             │ IHG           │
  └──────────────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────┴───────────────┘

  Points worth noting:
  - The joint-testing dates don't add up. In 2026, Nov 12 is a Thursday and Nov 24 is a Tuesday, not Fridays. The range is also about 12 days, though the table says 1 week.
    Testing is the step that decides whether release stays on Dec 3 or slips to Caitlyn's fallback of about Dec 20, so it may be worth asking her which end of the range is right.
  - There's no backend work for Canary on the chart. It's all Mobile and QA. The one outside dependency is Loyalty's images by Nov 3.
  - Dec 3 is the same date Caitlyn gave as the in-app target in your mobile check-in thread.

ASK:
* What is actually required for IHG? All hotels migrated to V3 catalog?
* On What timescale is it needed?