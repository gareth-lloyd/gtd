---
area: null
contexts:
- react
created: 2026-05-20 10:18:45.071965
defer_until: null
due: null
energy: medium
id: 2026-05-20T1018-review-pr-43431-laura-dewald-dm-ask
order: null
output: "## Agent run 2026-05-20T10:25:00\n\n**Already resolved — no action needed.**\n\nPR
  #43431 ([TOOL-104] Explicit definitions on product statuses, author Ramiro Nieto)
  was\n**merged on 2026-05-19** with `APPROVED` review decision. Laura's DM ask has
  been satisfied.\n\nTimeline:\n- 2026-05-01: Laura DeWald left two rounds of questions,
  asked for Gareth's input.\n- 2026-05-14: Laura DM'd Gareth to take a look.\n- 2026-05-15:
  Gareth reviewed — \"Looks fine from my point of view. One minor\n  comment worth
  thinking about but non-blocking.\"\n- 2026-05-18 / 2026-05-19: Laura responded and
  approved.\n- 2026-05-19 16:21 UTC: Merged to master by Ramiro.\n\n### Post-hoc read
  of the change (for awareness only)\n\nRefactor + new endpoint + tooltip. ~687 /
  -85 across 11 files.\n\n- `canary/canary_products.py`: replaces the inline dict
  in `get_available_products` with a\n  declarative `PRODUCT_ACTIVATION_RULES` list
  of `ProductActivationRule(product, is_active,\n  active_description)`. Clean equivalence
  with the prior dict; behavior preserved.\n- `onboarding/services/property_list.py`:
  same pattern applied to sub-products via\n  `SUB_PRODUCT_RULES` keyed by frontend
  product name; also introduces a `SubProductName`\n  enum (good — strings were stringly-typed
  before).\n- `onboarding/views/properties.py`: new `PropertyProductDefinitionsView`
  at\n  `/onboarding/api/properties/product-definitions`, gated by\n  `onboarding.view_salesforcehotelaccount`.
  Builds response by iterating\n  `CANARY_PRODUCT_TO_FRONTEND_NAME` and looking up
  rule + sub-rules, plus a hardcoded\n  `KIOSK` entry tacked on at the end.\n- Frontend:
  Vue tooltip on the Product Status card, using a new `useProductDefinitionsQuery`.\n\n###
  Quibbles I would have raised pre-merge\n\n1. **PR description overstates the tests.**
  It says \"Drift-guard tests ensure\n   `active_description` text stays in sync with
  the `is_active` callable.\" The tests\n   actually lock the *set* of products/sub-products
  and check name uniqueness — they do\n   **not** verify that the description matches
  what the callable does. If someone tweaks a\n   predicate, the description can drift
  silently. (Mostly cosmetic — the descriptions are\n   human-written anyway.)\n2.
  **Description style inconsistency.** Most rules read \"has X is enabled on the hotel\"\n
  \  (grammatically awkward — flag name embedded as a phrase). KIOSK reads\n   \"The
  `has_kiosk` flag is enabled on the hotel.\" (backticked, cleaner). Worth a\n   follow-up
  cleanup if anyone ends up here.\n3. **KIOSK is a special case in `_build_product_definitions`.**
  Hardcoded outside\n   `PRODUCT_ACTIVATION_RULES` because KIOSK isn't a `CanaryProducts`
  member. Asymmetric\n   but defensible — it's not actually a \"Canary product\" in
  the enum sense.\n4. **Silent partial degradation path.** `_build_product_definitions`
  logs a warning and\n   skips if a frontend product has no matching activation rule.
  The view still returns 200\n   with a partial list. The view tests assert the full
  set is present, which catches it in\n   CI, but in prod a future addition to `CANARY_PRODUCT_TO_FRONTEND_NAME`
  without a\n   matching rule would quietly drop that product from the tooltip. Low
  blast radius (it's\n   just a tooltip), but a strict assert/raise inside the dev/test
  path would be safer.\n\nNone of this is worth a follow-up comment on a merged PR.
  Logging here for awareness.\n"
project: null
source_id: https://canarytechnologies.slack.com/archives/D07U6KK5W1G/p1778772840907859
tags:
- morning-gtd
- slack
time_minutes: 20
title: 'Review PR #43431 (Laura DeWald DM ask)'
updated: 2026-05-20 14:35:03.876783
waiting_on: null
waiting_since: null
working_on: false
---

DM May 14: 'Can you take a look at this PR when you have some time? PR 43431'. https://canarytechnologies.slack.com/archives/D07U6KK5W1G/p1778772840907859