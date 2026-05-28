---
area: null
contexts: []
created: 2026-05-28 21:18:53.287373
defer_until: null
due: null
energy: low
id: 2026-05-28T2118-investigate-scheduled-campaigns-do-they-have-enter
order: -2
output: |
  ## Agent run 2026-05-28T22:10 (supersedes & corrects the 21:36 run)

  **Question (Ricardo, PR #46545 / CC-2569):** Drop the enterprise-portfolio exclusion
  (IHG / Wyndham / Best Western) from `migrate_scheduled_campaigns_to_variants`? His
  premise: the exclusion was copied from the GJ-message migration where it guards an
  IHG-specific segmentation path; scheduled campaigns have no enterprise-specific flow,
  so it's "dead weight."

  ### Conclusions (plain)
  1. **Keep the exclusion.** It is cheap and reversible: it only filters the *default
     batch run*, and enterprise can still be migrated deliberately via
     `--portfolio-identifier` / `--hotel-ids`.
  2. **Excluding enterprise does NOT disrupt their campaign sends.** This is the safe
     direction. (Verified for today's code; relies on stated intent for the
     not-yet-merged campaign path — see caveats.)
  3. **The risk lives on the *include* side, not the exclude side.** Removing the
     exclusion sweeps enterprise hotels into an untargeted backfill that creates
     hotel-scoped V2 `Segment`s + `MessageVariant`s on them via auto-naming — the same
     machinery that produced the ENT-5765 cleanup on the GJ side — and does so outside
     the controlled enterprise rollout process.
  4. **Ricardo's premise is true but doesn't prove "dead weight."** There is no
     enterprise scheduled-campaign provisioning flow, but the exclusion's value for
     campaigns is blast-radius + rollout coordination, not duplicate-provisioning.
  5. **Timing:** today campaign variants are not even consulted when sending (the
     campaign send path doesn't exist in master yet), so any impact only begins once
     CC-2568 ships. This is fundamentally a *sequenced-rollout* decision (CC-2198).

  ### Evidence & reasoning

  **(a) The exclusion is batch-only — verified.**
  In the PR's `_get_hotels()`, `--hotel-ids` returns `Hotel.objects.filter(id__in=...)`
  with no exclusion; `--portfolio-identifier` resolves to hotel-ids and behaves the
  same. Only the no-args batch path applies `ENTERPRISE_PORTFOLIO_IDENTIFIERS`. So
  "keep it" does not block enterprise migration — it defers it to a deliberate run.

  **(b) Send safety — what I actually verified in master.**
  The live send path is `GuestJourneyMessageService._registered_send_reservation_message`
  (`guest_journey/services/guest_journey_message.py:1390`). Findings:
  - It is gated by `reservation.hotel.rollout_message_variants` (line 1436). (My prior
    run wrongly attributed this gate to a debug view — it is genuine production logic.)
  - Variants are resolved **via `guest_journey_message`** (line 1439-1448). Scheduled
    campaigns have a `MessageScheduleSpec` but **no GuestJourneyMessage**, so campaign
    variants are not consulted by this path at all today. Confirmed there is no
    campaign send path in master: grep for `get_best_variant_for_campaign_reservation`
    returns nothing and `git log` shows no CC-2568 commit.
  - Fallback is NOT uniformly clean: when the flag is on, a GJM exists, and variant
    eval returns `NO_MATCH`, the path **suppresses the send** —
    `return SenderResult(sent=False, failure_reason="variant_no_match")` (line 1461-73).
    Only the "no variant at all" case falls through to spec templates (line 1509+).
  - `rollout_message_variants` defaults to **True** (hotels migration 0732), so the
    gate is effectively on for most hotels.

  **(c) Send safety — what I could NOT verify (caveat on conclusion 2).**
  CC-2568 ("Resolve V2 variants in scheduled campaign send path", Linear status *Ready
  for Deploy*) states the campaign path will "use V2 variants when present, fall back
  to V1 otherwise, flag-free." That is the source for "excluding is safe after CC-2568
  ships" — it is **ticket intent, not verified code** (not merged). Caution: the ticket
  says it will "extract logic identical to `get_best_variant_for_reservation`," and
  that sibling logic contains the NO_MATCH *suppression* branch above. So I cannot rule
  out that a campaign which *has* variants but matches none could be suppressed — which
  is an argument for migrating campaigns carefully, and a further reason not to fold
  enterprise into an untargeted batch.

  **(d) The include-side risk (ENT-5765), stated at its true strength.**
  ENT-5765 remediated ~2241 IHG `Segment`s whose auto-generated names ("Loyalty:
  NON_MEMBER" …) diverged from IHG onboarding's proper names
  (`tmp/onetime/ihg/20260401_ent_5765_segment_name_fix.py`). The campaign command
  reuses the same `convert_segments_to_v2` / `build_segment_name` /
  `_SEGMENT_NAME_OVERRIDES` helpers, and `Segment`s are hotel-scoped and reused by
  `(hotel, name)` — i.e. shared with the GJ side. The ENT-5709 overrides now produce
  correct names for **known IHG loyalty** patterns, so for those the migration would
  *reuse* the existing segment rather than create a dupe. Honest residual risk: (i)
  non-loyalty segments and Wyndham/BW are not covered by overrides and could create
  net-new/oddly-named hotel-scoped segments visible in segmentation; (ii) this happens
  outside the coordinated enterprise process. This is weaker than "this is exactly
  ENT-5765 again" (my prior phrasing overstated it) but is a real, asymmetric downside
  that the exclude side does not carry.

  **(e) Ricardo's premise — verified true.**
  `grep` of `onboarding/configuration_providers/{ihg,wyndham,best_western}` shows zero
  `ScheduledCampaign` references; campaigns are created via the hotelier API/service
  (`guest_journey/views|services/scheduled_campaign.py`), unlike GJ messages which
  enterprise onboarding re-provisions. So the *literal* GJ rationale (PR #41631:
  "these portfolios have their own onboarding flows that handle message variants
  separately") does not transfer to campaigns. It does not follow that the exclusion is
  dead weight — see (d) and (a).

  ### Corrections to the 21:36 run (self-critique)
  - "Sends are safe either way" was sourced from the CC-2568 ticket, not code; now
    scoped to verified-today vs. intent-for-CC-2568, and the NO_MATCH suppression
    branch is surfaced as a caveat.
  - Prior run cited the gate at `reservation_scheduled_messages.py:135` (a debug/preview
    view). The real production gate is `guest_journey_message.py:1436`.
  - ENT-5765 parallel was overstated; re-stated at true strength given the name
    overrides now in place.
  - CC-2119 was presented as proof enterprise hotels have *scheduled campaigns*. It is
    labelled "GMS: Guest Journey Messages" and may be a GJ-message issue, not a
    ScheduledCampaign. Downgraded to *suggestive, not confirmed*; enterprise
    scheduled-campaign existence is not independently verified (I did not query prod —
    safety rule).

  ### Open items for Gareth
  - Read the CC-2568 branch and confirm the campaign path's fallback is truly "no
    variants → V1" and whether a NO_MATCH suppression can apply to campaigns.
  - If you want hard numbers on enterprise scheduled-campaign counts, that needs a
    read-only prod/staging query (not done here per safety rules).
  - Decision is reversible and low-cost either way; the asymmetry favours keeping it.

  ### Refs
  - PR #46545 (CC-2569) · CC-2568 (send path, Ready for Deploy, unmerged) · CC-2198
    (rollout) · CC-2119 (IHG — possibly GJ-message, not campaign)
  - Original GJ exclusion: PR #41631
  - ENT-5765: tmp/onetime/ihg/20260401_ent_5765_segment_name_fix.py (names fixed by
    ENT-5709 / PR #41896)
  - Production send path + gate: guest_journey/services/guest_journey_message.py:1436
    (variant resolve 1439-1448; NO_MATCH suppression 1461-1473; spec fallback 1509+)
  - rollout flag default=True: hotels migration 0732_hotel_rollout_message_variants_default_true
project: null
source_id: null
tags: []
time_minutes: 5
title: INVESTIGATE scheduled campaigns - do they have enterprise impact?
updated: 2026-05-28 22:10:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1779982889863049