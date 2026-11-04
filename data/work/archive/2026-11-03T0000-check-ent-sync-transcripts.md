---
area: null
completed_at: 2026-11-04 13:54:13.374205
contexts:
- consume
created: 2026-11-03 00:00:00
defer_until: null
due: null
energy: low
id: 2026-11-03T0000-check-ent-sync-transcripts
order: null
output: |
  ## Agent run 2026-11-03T09:30

  Latest row in the Transcripts DB is the 2026-11-02 ENT Sync (https://app.notion.com/p/40c8146861518016ace6e8f4d7ace8e7). The row's Attendees/Topics/Action Items/Decisions properties are all empty; everything below comes from the embedded meeting-notes summary + transcript. Speakers: Connor, Andrea, Ryan, Tincho, Andrés. Gareth not present.

  ### Things that touch Gareth
  - Tincho is kicking off the drift-detection engine design "on top of Garrett's [=Gareth's] draft work" and added spec notes in Notion; also adding a milestone to expand drift rules from Wyndham to Best Western + IHG (expects more IHG drift alerts as properties onboard). Worth checking his notes line up with the ENT-7726 binding-rules plan.
  - Tincho has 2 PRs making country_code required on hotel save in Django admin + a backfill (GDPR compliance). Andrea flagged that breaking admin save has bitten other teams; they'll discuss alternatives in the ticket before merging. Relevant to the country_code/get_country() convention.
  - Cross-org SSO/portfolio modelling: Connor wants someone to review Lautaro's existing Notion page on user/SSO merging and to pull the list of portfolios containing hotels from multiple organizations (expected to be mgmt/ownership groups). No owner named.
  - Nathan (new hire on Connor's side) starts this week (summary says "today", transcript says "tomorrow"). Team asked to share past-work context in 1:1s and add him as optional to show-and-tells. Projects: Wyndham Barclays (Ryan), BW branding (Andrés, tentative), Welcome amenity rollout, IHG scripting changes.

  ### Decisions
  - SCIM deactivation scope stays narrow: do NOT scope-creep SCIM to fix cross-org portfolio modelling. Aimbridge-type portfolios (130 hotels: 122 non-IHG + 9 IHG) are exceptions to fix separately.
  - Heuristic agreed: an org that manages permissions via SSO may only grant/remove access to hotels in that org. Users needing cross-brand access must use username/password. Connor: this is both a security and UX concern, and "almost certain" we don't enforce it today; also need to revisit when SSO users get merged with password users.
  - QR vs. voice booking-gateway-per-channel fix (Andrea's eng design, reviewed by Stephen Reddekopp) is prioritised above Skim/SCIM for Andrés, below any remaining Omni work. QR bookings are failing across all Wyndham hotels because they're configured CRS-only, likely for months unnoticed.
  - IHG corporate-user permission requests (Connor Swords ticket) stay white-glove/ENT-owned; not self-serve. Won't build against IHG's SSO side while it's still in flux. CSMs sat on the request ~7 weeks (Priyanka).
  - Tincho's country-code PRs go in this sprint, pending the admin-save discussion.

  ### Action items (owner)
  - Ryan: root-cause the Wyndham "no reservations from PMS" issue (scheduling a fetch + PMS validate plan fixed it; KB article written); Chinese country-code breakdown for Ani; chase Barclays early this week ahead of Thursday's meeting; PRs needing review incoming.
  - Tincho: get enterprise sign-off on the GDPR retention-variable backfill command (Andrea to approve), run it, post in IHG channel; comment on the IHG corporate-user permissions ticket; discuss country-code admin requirement with Andrea in the ticket.
  - Andrés: message Natalia about Manage Portfolios UI beta (others set up, no feature feedback yet); fix QR/voice booking gateway, loop in Ani + Marta.
  - Connor/Andrea: make sure Marta (voice pod) knows about and is monitoring the QR booking failures.
  - Unassigned: pull multi-org portfolio list; review Lautaro's SSO-merging Notion page.

  ### Other status
  - Andrea: IHG membership tally (pass real tier, not hotel default); IHG core typing; hotel health checks to only run near go-live; non-SLA triage.
  - Andrés: Omni idle, waiting on Daniel; Wyndham segmentation paused pending Wyndham green light; Skim actively in development.
  - Martijn Dekker (EMEA) owns the cron validating the GDPR retention variable.

  ## Agent run 2026-11-03T14:54

  No newer row than the 2026-11-02 sync exists in the Transcripts DB (queried today; next-newest is 2026-10-05). Re-read the 2026-11-02 transcript in full: the 09:30 summary above is accurate. This run chased the three open threads that touch Gareth.

  ### 1. Drift detection: Tincho's spec is blocked on Gareth's draft PRs
  - Tincho's "spec notes" = GJM drift detection spike (ENT-7906), Notion https://app.notion.com/p/40c81468615181799174d3e25255f790 (created 2026-11-02 13:51). Status line: "Spike complete... Build is blocked on Gareth's rules-engine foundation landing." Eng design continues in ENT-8066 (https://linear.app/canary-technologies/issue/ENT-8066/eng-design, In Progress, milestone "Guest Journey Messages", project Configuration Drift Detection).
  - Approach: brand rules tree says which GJM use-cases a hotel must have; a value reader returns what it has; drift reports the gap. Report-only, one Wyndham slice first (loyalty brand, non-SEAPR, v1 config, AMER). Needs a new NoneOf predicate (GJM-specific, Tincho will add). Cites Gareth's GJM proposal (https://app.notion.com/p/3f9814686151813da661eb802029d0eb) and foundation doc (https://app.notion.com/p/3e58146861518147b489e3fa8e8aef09) as inputs.
  - Dependencies he lists: #59047 (https://github.com/canary-technologies-corp/canary/pull/59047), #59059 (https://github.com/canary-technologies-corp/canary/pull/59059), #61724 (https://github.com/canary-technologies-corp/canary/pull/61724), #61725 (https://github.com/canary-technologies-corp/canary/pull/61725). Verified today: all four are still DRAFT, last touched 2026-10-27, stacked (59059 on 59047; 61724 and 61725 both on 59059). Confirmed by diff: ValueReaderRegistry/register_value_reader live in #61725, SupersetOf in #61724, so his mapping is right even though the PR titles ("First binding rules", "Country conventions engine") don't say so.
  - Implication: Tincho now has a concrete downstream consumer waiting on the ENT-7726 stack. Worth deciding whether to land #59047+#59059 ahead of the conventions/value-reader PRs, or at least tell Tincho the expected order and timing. (Plan: ~/.claude/plans/zippy-soaring-metcalfe.md.)

  ### 2. country_code PRs: the "breaks admin save" worry is already moot
  - The two PRs are #62669 "[ENT-7346] Rewrite the country_code backfill safely" (https://github.com/canary-technologies-corp/canary/pull/62669) and #62676 "[ENT-8078] Fill country_code from country in admin and API" (https://github.com/canary-technologies-corp/canary/pull/62676). Both open, non-draft, no reviews yet, reviewers requested = pod-enterprise + Pod: Arrivals/Departures (per memory, Gareth's approval won't clear the pod-enterprise CODEOWNERS gate).
  - #62676 does NOT make country_code required in admin. The form's clean() keeps an explicit code, else derives it from free-text `country` via resolve_hotel_country_code; unresolvable leaves it unchanged. Profile PATCH derives only when `country` actually changes. "na"/"n/a" guarded against Namibia. Second commit at 19:23 on 2026-11-02 (after the sync) skips derivation for non-string country. So Andrea's concern from the meeting is addressed by design; nothing in the diff adds a required field or a ValidationError.
  - #62669: dry-run-by-default backfill via get_country + legacy map; description says 424 active hotels (387 US / 31 EU / 6 AP) have blank country_code, ~140 in GDPR-retention-default countries; resolves 321 of 424.
  - ENT-8078 has zero Linear comments, so the "discuss in the ticket" action hasn't happened. Uses `get_country()` on `country_code`, consistent with the convention in ~/.claude/CLAUDE.md. Caveat in PR: CompendiumPropertyInfoView still writes country/country_code independently (left to STAY-3589, which plans to make country_code the source of truth).

  ### 3. Lautaro's SSO/user-merging page (unowned review)
  - Most likely candidate: "Global User Profile / Global SSO" design doc, https://app.notion.com/p/3f381468615180939704fd689cd53eb0 (edited 2026-10-23, Design Doc Database). Older related: "Merge non-SSO Wyndham users after first sign-in" (2024, https://app.notion.com/p/8a65500cf2de4899ab36900e0dda34ce), "Typed Portfolios" design doc (https://app.notion.com/p/37481468615181b6b94bd569ba782491), "Portfolio-wide property role assignment" (https://app.notion.com/p/15ef3fa424fc43b2a6568036268fa7f6). Authorship not verified; nobody has picked this up as far as Notion/Linear show.

  ### Suggested next actions for Gareth (not taken)
  - Reply to Tincho on ENT-8066 or in the ENT channel with the landing order/ETA for #59047/#59059/#61724/#61725, or ask him to review them so they move out of draft.
  - Optionally review #62676 for the get_country convention and the compendium gap; the pod-enterprise approval still has to come from someone in that team.
  - Nothing external was written. No Salesforce, Linear, Notion, GitHub or Slack writes.
project: null
source_id: null
tags: []
time_minutes: 10
title: Check ENT sync transcripts
updated: 2026-11-04 13:54:13.374186
waiting_on: null
waiting_since: null
working_on: false
---

Review the latest ENT sync meeting transcript — action items, decisions, and topics.

https://app.notion.com/p/canarytechnologies/13c93352d06c4e88bb69af559237645c?v=5f62f3dba7234433870e5cfeb927403f&source=copy_link