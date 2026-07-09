---
area: null
contexts:
- react
created: 2026-07-09 07:57:31.259626
defer_until: null
due: 2026-07-09
energy: medium
id: 2026-07-09T0757-review-pr-48478-for-leandro-canary-products-produc
order: null
output: |
  ## Agent run 2026-07-09T14:05 — Review of canary_products.py change in PR #48478

  PR: [#48478 [AD-7836] Add config library and buckets with per-audience permissions](https://github.com/canary-technologies-corp/canary/pull/48478)
  Scope reviewed (per Leandro's ask): the `is_active_for_hotel` helper he added to
  `backend/canary/canary/canary_products.py`, grounded on your `PRODUCT_ACTIVATION_RULES`.
  I did NOT review the rest of the PR (config_library buckets, OCR fix) beyond the one caller.

  ### The change
  ```python
  @classmethod
  def is_active_for_hotel(cls, product: "CanaryProducts", hotel: "Hotel") -> bool:
      return any(rule.is_active(hotel) for rule in PRODUCT_ACTIVATION_RULES if rule.product == product)
  ```
  Sole caller today: `ConfigurationBucket.is_available_for` in
  `guest_experience/configuration_library/buckets/base.py` — passes `cls.PRODUCT`. All three
  current buckets declare `PRODUCT = CanaryProducts.CHECK_IN`.

  ### Verdict: correct and well-designed. Approve with two minor notes — no blockers.

  **Positives**
  - Correct given the `test_every_rule_has_a_unique_product` invariant: at most one rule matches,
    so `any()` evaluates a single predicate. Cleanly reuses `rule.is_active` so single-product
    checks can't drift from `get_available_products` / the union method. Good instinct.
  - Test is genuinely discriminating: `stub_hotel(has_check_in=True, has_chat=False)` asserting
    CHECK_IN True + CHAT False actually guards cross-product leakage — if the impl OR'd across all
    rules, CHAT would falsely return True. Docstring is accurate.

  **1. (Minor, latent silent-failure) Product with no rule -> silent False, not loud.**
  I verified `TABLET_EFOLIO` is the *only* one of the 19 `CanaryProducts` members with no entry in
  `PRODUCT_ACTIVATION_RULES`. For it (or any future unruled product), `is_active_for_hotel` returns
  `False` — indistinguishable from "genuinely inactive." Because the caller is
  `ConfigurationBucket.is_available_for(cls.PRODUCT)`, a bucket that ever declares
  `PRODUCT = TABLET_EFOLIO` (or a newly-added product before its rule lands) would be silently
  never-offered rather than failing at test time. No live bug — all current buckets use CHECK_IN.
  Suggestion (fits the existing drift-guard philosophy): add a test asserting every `CanaryProducts`
  member has exactly one rule, OR have the helper raise when no rule matches instead of returning
  a definitive False. Either closes the gap cheaply.

  **2. (Optional, style) Could be an instance method on the enum.**
  `CanaryProducts.CHECK_IN.is_active_for_hotel(hotel)` reads more naturally than
  `CanaryProducts.is_active_for_hotel(CanaryProducts.CHECK_IN, hotel)`. The classmethod form is fine
  and explicit — call it a taste note, not a request.

  **Note (not a change request): repeated-call DB cost.** For CHECK_IN the predicate is pure
  attribute access (no query). But `rule.is_active` for AUTHORIZATIONS / PAYMENT_LINKS /
  DIGITAL_COMPENDIUM issues a DB query per call. Fine today (buckets are all CHECK_IN); worth
  keeping in mind if `is_available_for` ends up called in a loop over many product-typed buckets.

  ### Suggested reply to Leandro (NOT sent — draft only)
  > The helper looks good — correct given the unique-product invariant, and nice reuse of
  > `rule.is_active` so it can't drift from `get_available_products`. Two small things: (1)
  > `TABLET_EFOLIO` is the one product with no rule, so `is_active_for_hotel` returns False for it
  > silently — if a bucket ever uses an unruled product it'd just never be offered. Worth a test
  > asserting every product has a rule, or raising when none matches. (2) Purely optional: could be
  > an instance method (`CanaryProducts.CHECK_IN.is_active_for_hotel(hotel)`). Neither blocks.
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1783537789743849
tags:
- morning-gtd
- slack
time_minutes: 20
title: 'Review PR #48478 for Leandro: canary_products product-enabled helper'
updated: 2026-07-09 13:38:57.172293
waiting_on: null
waiting_since: null
working_on: false
---

Leandro added a method to canary_products.py returning whether a hotel has a product enabled, grounded on my PRODUCT_ACTIVATION_RULES; asked me to review that part. https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1783537789743849 (PR #48478)