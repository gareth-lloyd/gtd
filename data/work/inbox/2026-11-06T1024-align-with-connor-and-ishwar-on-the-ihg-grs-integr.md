---
area: null
completed_at: null
contexts:
- react
created: 2026-11-06 10:24:22.246386
defer_until: null
due: null
energy: medium
id: 2026-11-06T1024-align-with-connor-and-ishwar-on-the-ihg-grs-integr
order: null
output: |
  ## Agent run 2026-11-06T13:05+02:00

  **TL;DR:** The IHG dynamic room-upgrade provider is mostly on master already, dormant behind the per-hotel `dynamic_addon_provider = ihg` gate. Six of Ishwar's PRs were closed unmerged in Sep 2026 and need rebasing. The real blockers for an end-of-year pilot are IHG-side: unanswered API questions, a production API key, and content-API provisioning. Mobile is unverified, and Caitlyn has not replied to Connor. One wrinkle to raise: Chanda's written ask says "reprioritized for Q1", while Connor reports IHG wants it live by end of year.

  ### Sources
  - Slack thread (Connor/Ishwar, Nov 5-6): https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1793915756730589?thread_ts=1793915756.730589&cid=C03V5P4B48P
  - Chanda's ask (Connor's DM, not readable by me): https://canarytechnologies.slack.com/archives/D091CKPC07K/p1793632668267539
  - Connor's Notion brief: NOT accessible via the Notion integration (404, probably a private page). Open it in the browser: https://app.notion.com/p/canarytechnologies/IHG-GRS-Integration-Status-Re-start-Brief-Nov-5-2026-40f814686151811ca41de8233d54508f
  - Tech design "IHG Room Upgrade API Integration" (Ishwar, status IN REVIEW, edited Nov 5): https://app.notion.com/p/38b814686151817382e1d03a47bfed54
  - Linear project "[Upsells] IHG Enterprise Upsells API": https://linear.app/canary-technologies/project/upsells-ihg-enterprise-upsells-api-25e4ed39bba3
  - IHG Pilot Weekly [Internal], Nov 2 notes: https://app.notion.com/p/2b58146861518092bbe4c551fb29f9ba

  ### What IHG says (Nov 2 weekly + Slack)
  - Nov 2 weekly: "GRS integration (no IHG dev needed; Canary confirming level of effort). GRS docs and staging credentials are already in place." IHG LT will say "go" once Connor reverts with the lift required. Connor flagged he does not know the IHG guest-data ecosystem and wants a crash course from Chanda.
  - Chanda (Nov 1 DM to Connor): pushing to get GRS "reprioritized for Q1", wants a gut check on the Development section (DV1-DV4) she drafted, not a full estimate.
  - Connor (Nov 5 thread): IHG asking for capacity/timeline estimates "tomorrow" and "set up by end of the year". Connor and Ishwar talked ~01:00 EET Nov 6 and Connor planned to send the grid plus questions. Nico was tagged and has not replied.
  - Ishwar's grid feedback: DV1/DV2 fine; DV3 (fetching offers for a specific reservation) arguably IHG-owned; DV4 should read "suppress" the room upsells configured in Canary.

  ### What is already on master (dormant behind the gate)
  Merged, Jul-Sep 2026, all Ishwar (in15):
  - #50396 STAY-4114 DynamicAddonProvider.IHG enum + migration; #50395 STAY-4115 Nor1 freeze / provider semantics
  - #54385 STAY-4121 IHGUpsellClient (read offers); #54386 STAY-4123 offer -> GuestUpsell mapper
  - #54645 STAY-4122 DynamicAddonsService dispatch by provider
  - #54955 STAY-4125 write-back PUT; #54956 STAY-4126 post-commit write-back lifecycle (PENDING -> APPROVED/DENIED)
  - #54716 STAY-4802 provider room-upgrade offers on v1/v2 + v3 guest surfaces
  - STAY-4112 confirmation-number resolver (HOLIDEX / EXTERNAL_REFERENCE_ID / EXTERNAL:CRS_*) marked Merged
  - Onboarding config providers for IHG upsells exist under backend/canary/onboarding/configuration_providers/ihg/
  Design doc's deployment model: every PR ships inert; activation is a single reversible per-hotel switch, no deploy.

  ### Closed unmerged PRs (the "stale" work Ishwar means)
  - #54650 STAY-4114 portfolio guard on admin edit (+124/-4) https://github.com/canary-technologies-corp/canary/pull/54650
  - #55527 ENT-7359 onboarding-time enable + rollout backfill (+387/-2); ticket Canceled Sep 18 https://github.com/canary-technologies-corp/canary/pull/55527
  - #56485 STAY-4126 show write-back outcome instead of generic failure toast (+132/-6) https://github.com/canary-technologies-corp/canary/pull/56485
  - #56486 STAY-4123 per-night pricing on IHG upgrades (+94/-5) https://github.com/canary-technologies-corp/canary/pull/56486
  - #56484 STAY-4888 reconciliation sweep (+373/-3); deliberately dropped in favour of an inline verify-read (STAY-5052, Backlog, unassigned) https://github.com/canary-technologies-corp/canary/pull/56484
  - #54741 STAY-4802 e2e spec for dynamic room upgrades (+565/-15) https://github.com/canary-technologies-corp/canary/pull/54741
  - #54387 PREVIEW branch, superseded, ignore
  Total ~1,100 lines to rebase onto ~2 months of master drift. "A few days + testing" (Ishwar) is plausible for the code; the schedule risk is elsewhere.

  ### Linear: still open in the project
  Todo/Backlog, all unassigned: STAY-4113 API access / prod key plan, STAY-4116 email ownership (IHG sendEmail vs Canary), STAY-4117 Hotel Content API (blocked on IHG provisioning), STAY-4119 monitoring, STAY-4120 verify mobile renders dynamic upsells, STAY-4803 hide room-type selector, STAY-4892 cache offers per reservation, STAY-5052 verify read after ambiguous write-back, STAY-4118 durable impressions (optional). Canceled: STAY-4124, STAY-4127 analytics POST back to IHG, STAY-5043 currency guard.

  ### Open questions IHG has not answered (from the tech design)
  1. Is the modify PUT idempotent (same inventoryTypeCode twice = no-op)? Does IHG-TransactionId dedupe a retry? Does a repeated PUT re-send the guest email? Is there a reservation read for reconciliation?
  2. Email ownership: IHG sendEmail=true vs Canary's email vs both (duplicate-email risk).
  3. Production API key for vendor CANRY, and whether offers and reservations use different keys (key scoping).
  4. Content API provisioning for room descriptions/images (staging sample returned HCM/HCS warnings; inventoryTypeName is the fallback).
  5. Product, not IHG: when to submit the write-back (on selection vs on check-in completion). PRD still says "falls back to static tier pricing"; design says empty set. Needs amending.

  ### Mobile
  - Design: dynamic upsells render through the guest-experience step framework, which the SDK consumes via OpenAPI, and #54716 also covers v1/v2. So mobile should get it for free IF the hotel is on the v3 check-in flow. Nobody has verified this (STAY-4120 untouched since Aug 28).
  - Caitlyn has not replied to Connor's question. Her Nov 6 "vaguely 2027" message in #staff-ops-pilots is about Wyndham staff messaging, not this.
  - From your Oct 28 1-1 with Caitlyn: web and mobile IHG config assumed identical; Eric paused the upsells custom view to do the IHG welcome-amenity screen; IHG mobile rollout wants every hotel on V3 first (~20-30 on the app today). https://notes.granola.ai/d/464b6712-3e50-4752-924b-87d51c3f7fe3

  ### Suggested alignment points for Connor and Ishwar
  1. Resolve the date: Chanda wrote Q1, Connor heard end of year. Which is it, and is "by end of year" code-complete-on-staging or live on pilot hotels?
  2. Define the pilot slice. Must-have to activate on a few hotels: reopen #54650, #56485, #56486, pick #55527 or a manual admin flip, and do STAY-5052. Nice-to-have: #54741 e2e, monitoring (STAY-4119), hide room-type selector (STAY-4803).
  3. Capacity: Ishwar is the only person with context and is on In-Stay priorities; who owns this through December, and does Nico need to be in the loop (he was tagged, silent)?
  4. IHG dependencies Connor should put on the grid as IHG-owned with dates: answers to the write-back questions, prod key, content-API access, test reservations at staging POC hotels (the sampled ones in the design doc are stale).
  5. Mobile: get Caitlyn to confirm whether IHG wants upgrades in the app, then a half-day STAY-4120 verification on a live branch before anyone promises it.
  6. Calendar risk: December lockdowns (weekend lockdowns already block merges; holiday freeze likely). Anything targeting EOY needs to merge by early-to-mid December.

  ### Draft Slack reply (NOT sent; for the #ihg thread)
  > Catching up on this. Quick read from the eng side: most of the IHG provider is already on master behind the per-hotel gate (offers client, mapper, dispatch, write-back lifecycle, guest surfaces). What's stale is ~6 closed PRs (portfolio guard, rollout enable, failure UX, per-night pricing, verify-read) that need a rebase, so Ishwar's "few days + testing" matches what I see. The schedule risk is IHG-side: the write-back questions from the design doc (PUT idempotency, TransactionId dedupe, repeat emails, a reconcile read), a prod key for CANRY, and content-API access. Suggest those go on the grid as IHG-owned with dates. Two things to pin down before we commit to a date: Chanda's note says Q1 reprioritisation, not EOY; and mobile is unverified (STAY-4120), Caitlyn can you confirm whether IHG wants upgrades in the app? Happy to do a 20-min sync with Connor/Ishwar/Nico to lock the pilot slice.

  ### Not done / limits
  - Could not read Connor's Notion brief or Chanda's DM (private). Could not confirm whether Connor actually sent the grid after the 01:00 call.
  - No Gmail trail on GRS in your inbox; Ishwar's open-questions email went to Connor.
  - Nothing was posted or changed anywhere; all external systems read-only.
project: null
source_id: https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1793915756730589?thread_ts=1793915756.730589&cid=C03V5P4B48P
tags:
- morning-gtd
- slack
time_minutes: 20
title: Align with Connor and Ishwar on the IHG GRS integration restart (end-of-year
  ask)
updated: 2026-11-06 11:45:09.913826
waiting_on: null
waiting_since: null
working_on: false
---

IHG abruptly restarted the GRS room-upgrade integration and wants it by end of year. Connor sent IHG a capacity/timeline grid yesterday. Ishwar: implementation was code-complete but PRs closed and stale; a few more days plus testing, open questions with IHG unanswered. Mobile piece unknown (Caitlyn asked).
https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1793915756730589?thread_ts=1793915756.730589&cid=C03V5P4B48P
Brief: https://app.notion.com/p/canarytechnologies/IHG-GRS-Integration-Status-Re-start-Brief-Nov-5-2026-40f814686151811ca41de8233d54508f