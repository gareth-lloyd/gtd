---
area: null
contexts:
- react
created: 2026-06-04 13:13:31.944753
defer_until: null
due: null
energy: low
id: 2026-06-04T1313-follow-up-on-demo-filter-decision-filter-on-hotels
order: null
output: |
  ## Agent run 2026-06-04T10:26:30Z

  TL;DR: The decision is ALREADY IMPLEMENTED in PR #46622 (TOOL-187), which was
  reworked on 2026-06-03 *after* Asher's call. No new code needed — the follow-up
  is to review/merge that PR and sanity-check one definitional nuance.

  ### The decision (from the thread)
  The Manage Properties page is a SalesforceHotelAccount (SFHA)-centric view; it
  shows SF accounts even when no Hotel exists yet, so the base query must stay on
  SFHA. New demos created via the demo-onboarding flow have NO SFHA row, so they
  weren't appearing. The original fix (PR #47001 / TOOL-256) created blank/nullable
  SFHA rows for demos. Asher's final call: model changes are overkill —
    - demo filter ON  → change the query to filter on Hotel, not SFHA
    - demo filter OFF → don't show demo hotels at all

  ### Fallout already actioned
  - PR #47001 ("[TOOL-259] nullable salesforce_account_id") → CLOSED
  - TOOL-256 (backfill SFHA rows for existing demos) → Canceled 2026-06-03
  - TOOL-265 (disable sync button for demos) → Canceled

  ### Current state of the work — PR #46622, "[TOOL-187] Add demo-hotel filter",
  Ramiro Nieto, OPEN / In Review, last pushed 2026-06-03 20:32Z (after the 15:07Z
  decision). It now matches the decision:
  - View `PropertiesView.get` branches on `is_demo`
    (backend/canary/onboarding/views/properties.py):
      • ON  → `PropertyListService.list_demo_hotels()` queries
        `Hotel.objects.filter(portfolio__identifier=USER_CREATED_DEMOS)` (filters on
        Hotel, not SFHA), paginates Hotels, and mocks an unsaved SFHA per row via
        `build_demo_account()` so the existing serializer still works.
      • OFF → unchanged `list_properties()` SFHA query. Demo hotels have no SFHA
        row, so they're naturally absent → "hidden when off" satisfied for free
        (which is exactly why the backfill approach was dropped).
  - Serializer flags `is_demo = account.pk is None` (in-memory mock = demo).
  - Tests added for both list + detail demo paths; detail resolves via
    `get_property_account_or_404` (uuid → SFHA, else fall back to demo Hotel).

  ### One nuance worth confirming with Asher/Ramiro before merge
  "Demo" in the PR == membership of the `USER_CREATED_DEMOS` portfolio, NOT the
  `Hotel.is_demo` boolean. Consequence: a hotel with `is_demo=True` that ALSO has a
  real SFHA row still shows in the default (OFF) list. That's almost certainly the
  intended scope (the goal is surfacing accountless new-flow demos), but the thread
  said "demo hotels" generically — worth a one-line confirmation that portfolio-
  scoping (not is_demo) is the agreed predicate.

  ### Recommended next action for Gareth
  No code to write. Decide whether your review is needed on PR #46622 (it's the
  epd-enterprise team's review queue; Asher's review request in the thread was on the
  now-closed #47001). If reviewing, confirm the portfolio-vs-is_demo nuance above.
  Did NOT post anything to Slack/GitHub/Linear.
project: null
source_id: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1780499230405699?thread_ts=1780493979.663979&cid=C047K6WSUJY
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 10
title: 'Follow up on demo-filter decision: filter on hotels, not SalesforceHotelAccount'
updated: 2026-06-04 15:48:16.915558
waiting_on: null
waiting_since: null
working_on: false
---

#epd-enterprise — Asher: decided model changes are overkill; change the query to filter on hotels (not SalesforceHotelAccount) when demo filter is on, and hide demo hotels entirely when it's off. https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1780499230405699?thread_ts=1780493979.663979&cid=C047K6WSUJY