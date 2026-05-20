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
output: |
  ## Agent run 2026-05-20T10:25:00

  **Already resolved — no action needed.**

  PR #43431 ([TOOL-104] Explicit definitions on product statuses, author Ramiro Nieto) was
  **merged on 2026-05-19** with `APPROVED` review decision. Laura's DM ask has been satisfied.

  Timeline:
  - 2026-05-01: Laura DeWald left two rounds of questions, asked for Gareth's input.
  - 2026-05-14: Laura DM'd Gareth to take a look.
  - 2026-05-15: Gareth reviewed — "Looks fine from my point of view. One minor
    comment worth thinking about but non-blocking."
  - 2026-05-18 / 2026-05-19: Laura responded and approved.
  - 2026-05-19 16:21 UTC: Merged to master by Ramiro.

  ### Post-hoc read of the change (for awareness only)

  Refactor + new endpoint + tooltip. ~687 / -85 across 11 files.

  - `canary/canary_products.py`: replaces the inline dict in `get_available_products` with a
    declarative `PRODUCT_ACTIVATION_RULES` list of `ProductActivationRule(product, is_active,
    active_description)`. Clean equivalence with the prior dict; behavior preserved.
  - `onboarding/services/property_list.py`: same pattern applied to sub-products via
    `SUB_PRODUCT_RULES` keyed by frontend product name; also introduces a `SubProductName`
    enum (good — strings were stringly-typed before).
  - `onboarding/views/properties.py`: new `PropertyProductDefinitionsView` at
    `/onboarding/api/properties/product-definitions`, gated by
    `onboarding.view_salesforcehotelaccount`. Builds response by iterating
    `CANARY_PRODUCT_TO_FRONTEND_NAME` and looking up rule + sub-rules, plus a hardcoded
    `KIOSK` entry tacked on at the end.
  - Frontend: Vue tooltip on the Product Status card, using a new `useProductDefinitionsQuery`.

  ### Quibbles I would have raised pre-merge

  1. **PR description overstates the tests.** It says "Drift-guard tests ensure
     `active_description` text stays in sync with the `is_active` callable." The tests
     actually lock the *set* of products/sub-products and check name uniqueness — they do
     **not** verify that the description matches what the callable does. If someone tweaks a
     predicate, the description can drift silently. (Mostly cosmetic — the descriptions are
     human-written anyway.)
  2. **Description style inconsistency.** Most rules read "has X is enabled on the hotel"
     (grammatically awkward — flag name embedded as a phrase). KIOSK reads
     "The `has_kiosk` flag is enabled on the hotel." (backticked, cleaner). Worth a
     follow-up cleanup if anyone ends up here.
  3. **KIOSK is a special case in `_build_product_definitions`.** Hardcoded outside
     `PRODUCT_ACTIVATION_RULES` because KIOSK isn't a `CanaryProducts` member. Asymmetric
     but defensible — it's not actually a "Canary product" in the enum sense.
  4. **Silent partial degradation path.** `_build_product_definitions` logs a warning and
     skips if a frontend product has no matching activation rule. The view still returns 200
     with a partial list. The view tests assert the full set is present, which catches it in
     CI, but in prod a future addition to `CANARY_PRODUCT_TO_FRONTEND_NAME` without a
     matching rule would quietly drop that product from the tooltip. Low blast radius (it's
     just a tooltip), but a strict assert/raise inside the dev/test path would be safer.

  None of this is worth a follow-up comment on a merged PR. Logging here for awareness.
source_id: https://canarytechnologies.slack.com/archives/D07U6KK5W1G/p1778772840907859
tags:
- morning-gtd
- slack
time_minutes: 20
title: 'Review PR #43431 (Laura DeWald DM ask)'
updated: 2026-05-20 10:25:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

DM May 14: 'Can you take a look at this PR when you have some time? PR 43431'. https://canarytechnologies.slack.com/archives/D07U6KK5W1G/p1778772840907859
