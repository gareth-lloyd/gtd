---
area: null
completed_at: null
contexts: []
created: 2026-10-08 21:25:55.236996
defer_until: null
due: null
energy: low
id: 2026-10-08T2125-review-ent-sprint-planning-particularly-for-the-ad
order: null
output: |
  ## Agent run 2026-10-09 (rewritten 12:30 after testing the V3 blocker claim)
  Sources:
  - Oct 8 ENT standup/sprint planning, full transcript: https://notes.granola.ai/d/f464554a-0071-4566-af32-bb953f27ca76
  - PR #59425 and its review thread: https://github.com/canary-technologies-corp/canary/pull/59425#discussion_r4210411435
  - Code on origin/master d57b9aeabb9
  - Snowflake CANARY_RAW mirror, read-only, all 3 regions (lags about 25 min)
  - Earlier handoffs: Lea regcard reply, Lea call/binding tree, ad-research V3 rules

  ### ELI10
  A hotel's check-in form used to come from one big document, the "reg card". Our IHG scripts set hotels up by rewriting that document.
  AD (the Arrivals & Departures team) is moving hotels to a new check-in system, V3. V3 still reads the reg card: change the card and V3 picks up the change. So V3 is fine for us.
  The only thing stopping our scripts on V3 hotels is a safety lock we added ourselves. Andrea's PR #59425 removes it.
  Later, AD will move hotels to a second new thing, the "catalog". There the form is built from separate pieces instead of the reg card. Our scripts only write the card, so on a catalog hotel nothing they write would reach guests. AD's planned "upsert" fixes that by rebuilding the pieces from the card.
  Today no real hotel is on the catalog, so the upsert blocks nothing yet. It matters once AD starts moving hotels onto the catalog.

  ### The AD check-in rollout claim, corrected
  What the meeting said:
  - Connor (via Babur on the AD side): every hotel will be on V3 by end of October.
  - Andrea: that doesn't unblock us; all our scripts stay blocked until AD writes an upsert that pushes reg card updates into their catalog, and AD's answers have been inconsistent.

  What the code and data say:
  1. V3 by itself doesn't block the scripts.
     - Our own ENT-7607 guard (`ERROR_HOTEL_ON_CHECK_IN_V3` in `AddRegistrationCardPlan`) blocks them.
     - PR #59425 (ENT-7720) removes it. Saving a reg card already rebuilds the V3 flow (`sync_v3_flow_on_registration_card_save`).
     - Dana and Guido confirmed this on the ticket.
  2. The upsert only matters for hotels on the field catalog (`uses_field_catalog=True`).
     - On a catalog hotel the guest form comes from catalog rows, so reg card writes don't reach guests.
     - Leandro's proposal (2026-10-08): make the regcard-to-catalog conversion re-runnable on a hotel that already has a catalog, overwriting its fields. Today `move_to_catalog` returns ALREADY_ON_CATALOG.
     - Flipping back to the card and re-converting fails too, because the old rows no longer reproduce the new card.
     - Lea said "We can prioritize that" and Andrea accepted. That is a commitment without a date. The thread shows no inconsistent answers.
  3. Data:
     - 9 IHG hotels are on V3, all in the US: atlcp, atlmu, bhmbe, bhmbm, ewrsp, slfms, snsrw, srtvl, syrdw. This includes the 3 ENT-7720 Core Plus pilots (slfms, snsrw, srtvl).
     - 0 IHG hotels are on the catalog. Only 2 hotels in the estate are, both test hotels (anvil-hotel52, vibhors-test-hotel). EU and AP have no IHG V3 hotels and no catalog hotels.
     - Andrea's "some hotels on V3 and on the catalog" doesn't match the data.
  4. So #59425 alone unblocks all 9 IHG V3 hotels.
     - Moving a hotel to the catalog is a separate step from the V3 migration. The upsert's real deadline is when AD starts moving production hotels onto the catalog, not end of October.
     - Dana's open PR #59709 (https://github.com/canary-technologies-corp/canary/pull/59709, "keep tablet v3 hotels on check-in v3 and the catalog") suggests that is coming.

  Other IHG scripting work: Andrea's auth config script PR (handles V2, and V2 existing in upserts). Joshua and Louisa are tagged, and ENT review comes after.

  ### Other main work pieces from the meeting
  - Priorities (Connor):
    1. Ryan gets Wyndham Barclays into implementation. The design call on Oct 9 is Ryan, Andrea and Connor only, recorded for Andres and Lotta.
    2. Reactive work on the Expo to Omni launch.
    3. IHG scripting as requests come in.
    Best Western SSO is still a major focus. Andreas picks SCIM back up when he returns.
  - Skimm: going ahead, but not shipping for the conference. The mobile workaround unblocks the app.
  - Tincho: drift-detection acknowledgment PRs are about half done. He has 28 points, so nothing new gets pulled in. He is point person while Lotta and Andreas are out.
  - Ryan:
    - Content Gateway is wrapping up: 1 PR, then the AEM meeting next week, Show & Tell in 1-2 weeks.
    - Barclays eng design comments are still open.
    - ENT-7615 design goes to Kush, followed by an implementation sub-ticket.
    - He is on triage.
  - Guest URL check-in link ticket (Ryan): tools-team flags (Sam) put check-in into test mode when it is added to a live hotel. The likely fix is to force them false in go-live scripts, plus a small backfill. The tools team needs to confirm.
  - IHG Core/Core Plus from Salesforce (Andrea): this is now 3-4 tickets. The first PR would mark about 160 of 165 hotels unhealthy. Your steer: don't let the alerts block it, validate the opportunity structure with Taylor, and tell the Salesforce side we depend on it.
  - Andrea's cross-region header design moves to next week. EU AMB sits with Wyndham, and Connor is bumping it. HotelKey/LinkIt is blocked externally.

  ### Main unanswered questions
  1. What is holding #59425? It needs a human decision on the overwrite risk. With the guard gone, every reg card provider can overwrite live V3 cards, and the only backup is `legacy_schema`, restored by hand. A bot reviewer, Macroscope, marked it HUMAN_REQUIRED.
  2. When do production hotels start moving to the catalog, and is IHG in that? This is the real deadline for Lea's upsert. Ask Lea or Guido.
  3. Is the upsert the right long-term design, or should onboarding write catalog fields directly? Sam's design came up in the thread. Andrea and Lea both say neither team is ready for direct writes yet.
  4. Is it safe to always force the check-in test-mode flags off at go-live, and how many live hotels need a backfill? Ask the tools team (Sam).
  5. Is there still a reliable Salesforce signal for IHG Core/Core Plus now that the Salesforce structure has changed again? "Loop in Taylor" has no owner.
  6. Who on ENT reviews the IHG script PRs after AD's review? No owner was named.
  7. These are still open from earlier meetings, via Granola search: GDPR reg card anonymization before the Turkey/Thailand/France rollouts, and an SDK vs non-SDK flag for scripting at 50-150+ properties. See the Enterprise clients sync, Oct 7: https://notes.granola.ai/d/59de57f7-c736-4d19-a35c-321aa616b73f

  Nothing was posted anywhere.
project: null
source_id: null
tags: []
time_minutes: 5
title: Review ent sprint planning transcript, particularly for the AD check-in rollout
  stuff.
updated: 2026-10-09 12:30:00
waiting_on: null
waiting_since: null
working_on: false
---

Main work pieces. Main unanswered questions