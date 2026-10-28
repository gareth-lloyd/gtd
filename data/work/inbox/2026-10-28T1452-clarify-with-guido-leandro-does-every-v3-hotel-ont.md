---
area: null
completed_at: null
contexts:
- react
created: 2026-10-28 14:52:21.595826
defer_until: null
due: null
energy: low
id: 2026-10-28T1452-clarify-with-guido-leandro-does-every-v3-hotel-ont
order: null
output: |-
  ## Agent run 2026-10-28T16:40

  ### Short answer: mostly settled already. The "end of Oct" line is stale.
  - The TOOL design (https://app.notion.com/p/canarytechnologies/Eng-Design-Automate-Check-in-V3-Onboarding-3df8146861518182b3b7ee941e476814), Risk 5, says: "every v3 hotel is due to move onto it by the end of October 2026". Nothing else in the doc backs this up, and no source is cited. The doc was last edited 2026-10-27.
  - A&D decided the opposite on 2026-10-20. Guido, in the #epd-arrivals-departures thread "Discussion about migration to v3, catalog and step configurator" (https://canarytechnologies.slack.com/archives/C029BPP02H0/p1792167805759819?thread_ts=1792167805.759819&cid=C029BPP02H0):
    > Decisions: 1- Continue to do the v3 migration (without Catalog) 2- Once Catalog/Step Configurator is ready, migrate the v3 hotels to use Catalog 3- Onboarding hotels should already use Catalog/Step Config
    Dana then explained that the question had been whether to pause v3 until the configurator reached GA. The answer was no: keep migrating to v3, because moving hotels to the catalog later is easy. The reason for waiting: once a hotel is on the catalog, CS cannot edit its configuration the way they do today, so either A&D make the edits or Step Configurator ships for those hotels at the same time. Guido and Lea (Leandro, U08ARJSSP71) both took part.
  - So Andrea is right about existing hotels, Wyndham included. They go to v3 now and to the catalog later, once Step Configurator is ready. Nobody has given a date for that, and nothing says end of October.

  ### What is still open (the actual question for Guido/Lea)
  1. Decision 3 ("onboarding hotels should already use Catalog") is so far built only for non-enterprise DEFAULT onboarding. TOOL-871 (https://linear.app/canary-technologies/issue/TOOL-871), PR #60865 (https://github.com/canary-technologies-corp/canary/pull/60865), merged 10-23, routes those hotels to v3 plus the catalog. The design lists Wyndham MSA, BW MSA, IHG Pilot and IHG GMS Core as out of scope. Does decision 3 also cover Enterprise onboarding scripts? Or should Enterprise scripts flip to v3 only, with no catalog, and join the later catalog migration with everyone else?
  2. Is there a target date, or a Step Configurator GA milestone, for moving existing v3 hotels onto the catalog? Does that batch include Enterprise brands?
  3. IHG-specific: Tincho flagged that non-US GMS Core reg-card processes fail on hotels already on the catalog (#ihg, 10-22). Taylor and Guido paused IHG v3 migration. Any Enterprise catalog move depends on fixing that first.

  Related: AD-10463 (https://linear.app/canary-technologies/issue/AD-10463), Done 10-23, added a single V3MigrationService entry point that does v3 plus catalog in one transaction. If the answer to Q1 is "catalog too", Enterprise would call that method. That links to the sibling item "Ask AD whether Enterprise onboarding providers can reuse TOOL-871's path".

  ### Draft Slack reply. NOT SENT
  Suggested destination: reply in Guido's 10-16 thread in #epd-arrivals-departures (link above), so the decision and its clarification stay together. Alternative: a group DM with Guido and Lea.

  > Hey <@U09CRG0LWP8> <@U08ARJSSP71>, a follow-up on the decisions above, for the Enterprise onboarding scripts (Wyndham / BW / IHG). We're about to change them from v2=STABLE to v3, and want to land them in the right state:
  > 1. Does decision 3 ("onboarding hotels should already use Catalog") cover Enterprise onboarding too, or only the DEFAULT path that TOOL-871 just did? Our plan is v3 only, no catalog, and those hotels join the later catalog migration with everyone else.
  > 2. Is there a target date or Step Configurator milestone for moving existing v3 hotels onto the catalog, and does it include Enterprise brands? The Automate Check-in V3 Onboarding design says "every v3 hotel by end of October 2026". I think that predates your 10-20 decision, but want to check.
  > 3. For IHG specifically, non-US GMS Core reg-card scripts currently break on catalog hotels, so they'd need fixing before any IHG catalog move.

  ### Side note
  If Guido confirms, Risk 5 in Sam's design should be corrected (it currently says end of October). That would be a Notion comment for Sam. It is not drafted or posted.

  Nothing was sent or posted anywhere.
project: null
source_id: null
tags: []
time_minutes: 10
title: 'Clarify with Guido/Leandro: does ''every v3 hotel onto the field catalog by
  end of Oct 2026'' include Enterprise?'
updated: 2026-10-28 16:24:54.928862
waiting_on: null
waiting_since: null
working_on: false
---

From: check-in v3 rollout research, 2026-10-28 (#ihg thread, #best-western thread, TOOL 'Automate Check-in V3 Onboarding' design)
The TOOL design's Risks section says every v3 hotel is due to move onto the catalog by end of October 2026.
Andrea believes Wyndhams are only moving to v3, not the catalog. Contradiction to settle before committing script changes.