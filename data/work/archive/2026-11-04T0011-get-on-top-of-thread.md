---
area: null
completed_at: 2026-11-04 15:52:32.147281
contexts: []
created: 2026-11-04 00:11:12.658105
defer_until: null
due: null
energy: low
id: 2026-11-04T0011-get-on-top-of-thread
order: null
output: |
  ## Agent run 2026-11-04T13:56 (Europe/Athens)

  Thread: https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1790006579628339 (163 replies, Sep 21 to Nov 3). Last message is Ani at Nov 3 23:25 EET asking Caitlyn to clarify "and web".

  ### Where it stands
  - Phase 1 (Oct 15-19, closed): not-live Wyndham hotels got app check-ins. You turned has_check_in_mobile off for ~700 hotels, go-live scripts were fixed (ENT-7908, ENT-7916 shared rule, both Done, Ryan), Ani's limbo list of 21 was disabled on Oct 19.
  - Phase 2 (Nov 3, open): site 47150 (has_check_in_mobile=false) got a checkout via the app on Nov 2. Diana confirmed the SDK gates checkout/messaging/tipping only on the product flags has_checkout / has_messaging / has_tipping, and ignores has_check_out_test. Only check-in has a second SDK-specific flag.
  - Ani's requirement: no guest interactivity of any kind with a site before go-live, every module, every enterprise SDK partner. Connor: "a miss on our side", fast-track. Diana: BE + SDK work, "nothing too complicated", but old app builds will not honor new flags.
  - Caitlyn confirmed with Wyndham (Nov 3 21:37): they do NOT force app updates and will not until stable. So any flag-only fix leaves old builds exposed indefinitely.
  - Caitlyn then proposed shutting off all checkout "across app and web" for the affected properties until the fix. Ani pushed back ("I don't know if we should shut off anything") and asked what "and web" means. That is the unresolved exchange at the end of the thread.
  - A ticket already exists: MOB-1470 "SDK: Add guest-facing activation flag so not-live sites can't be used" (https://linear.app/canary-technologies/issue/MOB-1470/sdk-add-guest-facing-activation-flag-so-not-live-sites-cant-be-used). Urgent, Todo, assignee Francisco Prieto, created by Caitlyn Nov 3, project "Feature Flagging SDK Flows". The description already names your "short engineering design first" suggestion, the old-SDK-version problem, go-live script update and backfill. No comments on it yet.
  - Related, all Done: ENT-7905 spike (Ryan's finding: test mode gates only Canary pages, not the app; https://linear.app/canary-technologies/issue/ENT-7905), ENT-7808, ENT-7862.

  ### Questions aimed at you or unanswered
  1. Ani (Nov 3 14:56): "What is the timeline on this type of work?" Nobody answered. You proposed the design; Francisco owns MOB-1470.
  2. Caitlyn vs Ani on the interim shutoff. Caitlyn's "app and web" almost certainly means turning has_checkout off for not-live hotels, which also hides checkout on the hotel dashboard. Ani's objection is that sites need products enabled for the hotel before go-live. Someone needs to make the call; you have the lever (same script as Oct 15, different flags).
  3. Caitlyn (Nov 3 21:37) asked Diana for workarounds for inactive hotels given no force update. Unanswered.

  ### Backend-only fallback worth putting in the design (code check, not verified end to end)
  - Diana said on Sep 23 that the app hides every Canary button unless both the hotel and the reservation resolve from the API. That behaviour exists in every shipped build.
  - The SDK reads backend/canary/guest/views/guest_reservations_view.py (GuestReservationView / GuestReservationsView, public API). Its hotel payload (GuestHotelSchema) carries has_check_in, has_tipping, tip_configuration, check_in_configuration.has_check_in_mobile and check_out_configuration.has_check_out_test. So a server-side gate that returns the product flags as off, or no reservation, for SDK callers at hotels that are "enabled for hotel, not for guests" would be honored by old builds with no app release.
  - Caveat: that endpoint is shared with web guest flows, so the gate must be SDK-only. The view already reads a `source` query param (Source enum); whether the SDK sends it needs confirming with Diana/Eric before relying on it.
  - The reservation payload already serialises is_check_in_test_whitelisted / is_check_out_test_whitelisted, so test-mode plumbing to the app exists server-side; the app just does not read the checkout one.

  ### Not done
  - No prod query run. Quantifying app-sourced checkouts / messages / tips at not-live Wyndham hotels since Oct 8 (same shape as your Oct 15 check-in query) would settle whether the interim shutoff is worth the hotel-side cost. Snowflake MCP or Sallyport read-only can do it on request.
  - Nothing posted anywhere.

  ### Draft reply for the thread (not sent)
  > Catching up. Where I think we are:
  > - MOB-1470 (Urgent, Francisco) captures the real fix: SDK-specific per-module flags, BE + SDK. I will write the short design this week so it works for every enterprise SDK partner, and answer Ani's timeline question from that.
  > - Since Wyndham will not force updates, the design needs a backend fallback old builds already honour. Diana's Sep 23 note gives one: the app hides every Canary button when the hotel or reservation does not resolve. Returning the product flags as off (or no reservation) to SDK callers for not-live hotels covers every shipped version.
  > - Interim: Caitlyn, I read "app and web" as turning has_checkout off for the not-live hotels, which also hides checkout on their dashboard. Ani, is that acceptable until the fix lands, or do those hotels need checkout visible pre-go-live? If acceptable I can run the same script as Oct 15 for has_checkout, has_messaging and has_tipping against the not-live list.
  ## Agent run 2026-11-04T15:41 (Europe/Athens), second pass: settings landscape and impact

  Briefing page for the next-step conversation (private until shared): https://claude.ai/artifact/XarM3aQZjPebF4fMNcr8ps

  Headline numbers (analytics mirror, 8 Oct to 4 Nov):
  - 722 not-live Wyndham hotels have check-out on with messages off (active, non-demo). 153 of them got 271 uninvited check-outs since 8 Oct, up to 15 at one hotel.
  - Weekly uninvited check-outs at not-live Wyndham hotels: 27, 23, 18 (pre-launch baseline from QR/direct links), then 35, 60, 75, 116, and 45 in the first three days of this week. SDK attribution only started 3 Nov; 11 not-live hotels logged an SDK check-out in two days.
  - Uninvited check-ins at not-live hotels fell from 28 (week of 5 Oct) to roughly 0 after the 15 Oct has_check_in_mobile fix.
  - Tips cannot be attributed (the 'app' tip source predates the SDK at ~5k/month); Diana's SDK source fix for tips and upsells merged 3 Nov.
  - Estate (US/CA): 4,824 live with products and messages on; ~700 not live with products on and messages off (the exposed set); ~78 live with messages off; 13 not live with messages on.

  Code facts that change the design (from the mapping agent, file refs in the page):
  - The SDK already receives has_check_out_test, has_check_in_test and the per-guest whitelist booleans on every reservation payload and ignores them.
  - The backend already distinguishes SDK traffic via the X-SDK-Platform header (canary/client_source.py), so a server-side SDK-only gate needs no new header or app release. The app hides buttons for fields it does not receive (Diana 23 Sep, Eric 3 Nov on checkOut null).
  - Only v3 session create enforces test mode server-side. Legacy check-in and all check-out direct URLs bypass it (AD-10380, unassigned in A/D triage).
  - Messaging flag is has_chat (not has_messaging); check-out is has_check_out. Web step 2 is has_check_in_messages / has_check_out_messages plus per-message schedule enable.
  - The rules registry has no rule for has_check_in_mobile.

  Conversations since the first pass:
  - Side thread Eric/Caitlyn 3 Nov (https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1793732365091069): turning has_check_out off at a hotel hides the app button on every build (MOB-1253); Eric: fine short term, but we still need SDK-specific flags.
  - Caitlyn pinged Francisco on MOB-1470 at 23:37 (https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1793741860506959); he has not started (IHG focus) and asked what her additional thoughts are. No reply yet.
  - Your Diana 1-1 today (https://notes.granola.ai/d/5d99c53d-e0ec-4052-87c4-0765ae8b619d): new gates default open and are closed selectively; Francisco to post a draft proposal fast, enterprise case first; IHG flags land in the release after next (1-2 months). Diana said Wyndham has force update; Caitlyn says they do not. Needs clearing up.

  Options laid out in the page: A) has_check_out off at the ~720 (hotel dashboard loses check-out, Ani's objection); B) backend SDK-only gate on X-SDK-Platform for pre-go-live hotels, every build honours it, no app release; C) MOB-1470 per-module SDK flags, durable but new builds only; D) SDK honours the test fields it already gets; E) AD-10380. Suggested sequence: B now, C as the design with B as the fallback, A only if B cannot ship in days.

  Seven questions to settle are listed in section 7 of the page.

  Not done / blocked:
  - Production reader query for has_check_in_mobile and test-mode counts: the auto-mode classifier denied Bash prod-db reads of hotel data (information_schema reads were allowed). The ready-to-run SQL is at the end of the page; run it with `! canary prod-db query canary "..."` if you want the numbers.
  - Snowflake CANARY_RAW is still unauthorized for your role; ANALYTICS.ANALYTICS_PUBLIC works via the direct server._run_query bypass (the MCP process hung).
  - Nothing posted anywhere. Artifact is private until you share it.
project: null
source_id: null
tags: []
time_minutes: 5
title: get on top of thread
updated: 2026-11-04 15:52:32.147273
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1793741159482929?thread_ts=1790006579.628339&cid=C09M5GRJPL2