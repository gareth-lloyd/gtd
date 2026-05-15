---
area: null
contexts: []
created: 2026-05-15 06:28:58.036798
defer_until: null
due: null
energy: low
id: 2026-05-15T0628-review-rami-s-product-status-pr
order: -19
output: |
  ## Agent run 2026-05-15T07:05

  Reviewed PR #43431 "[TOOL-104] Explicit definitions on product statuses"
  (Ramiro Nieto, +602/-74, 11 files, base master, MERGEABLE, not draft).
  ldewald explicitly tagged you for domain feedback ("not super familiar
  with this code") and left 4 questions. NOTHING posted to GitHub — review
  drafted below for you to post/adapt.

  ### What the PR does
  Refactors `CanaryProducts.get_available_products` and onboarding
  `_get_sub_products` from imperative blocks into declarative
  `PRODUCT_ACTIVATION_RULES` / `SUB_PRODUCT_RULES`, each rule pairing the
  activation predicate with a human-readable `active_description`. Adds
  `/onboarding/api/properties/product-definitions` endpoint + a Vue tooltip
  ("Active when: …") on the Product Status card.

  ### Verdict: solid refactor, but DO NOT approve as-is. It oversells.

  **1. (BLOCKER) The headline "drift-guard test" does not exist.**
  PR description claims "Drift-guard tests ensure active_description stays
  in sync with the is_active callable". Both `ProductActivationRule` and
  `SubProductActivationRule` docstrings claim a test "inspects the
  is_active source to assert every hotel attribute referenced in
  active_description also appears in the callable." It doesn't. The two new
  test files (`test_product_activation_rules.py`,
  `test_sub_product_rules.py`) only assert (a) product/name uniqueness and
  (b) the rule set equals a hardcoded expected set. Zero source inspection,
  zero description-vs-callable comparison. ldewald flagged exactly this on
  canary_products.py:209. The docstrings AND the PR description are false.
  This matters because the descriptions are the whole point — they're shown
  to users — and several are free prose over private logic that WILL rot.

  **2. (CONCRETE PROOF point 1 matters) COMPENDIUM description is already
  wrong, day one.** `DIGITAL_COMPENDIUM.active_description` =
  "The hotel has a Compendium Configuration row whose product tier is
  anything other than DISABLED." But `_get_compendium_product_availability`
  (single-hotel path, the one this rule uses) delegates to
  `CompendiumSelector.get_has_compendium(hotel)` — NOT the
  exclude(product_tier=DISABLED) query. That prose was copied from the
  `_many` bulk variant. So a user-facing tooltip is already inaccurate
  before any drift, with no test to catch it. This is the single strongest
  argument that the prose-without-enforcement approach is fragile.

  I verified the other 4 helper-backed descriptions and they ARE accurate:
  AUTHORIZATIONS ✓, SALES_BOOKINGS ✓, TABLET_REGISTRATION ✓
  (has_tablet_reg_v1 and (has_check_in or has_check_out)), PAYMENT_LINKS ✓.
  The ~13 simple `lambda hotel: hotel.has_x` ones are self-evidently fine.

  **3. (Minor) KIOSK bypasses the "single source of truth."** It's appended
  manually in `_build_product_definitions` with a hardcoded description, not
  in PRODUCT_ACTIVATION_RULES, not drift-guarded at all. `hotel.has_kiosk`
  is the right flag so the text is accurate, but it contradicts the
  docstring's "single source of truth" framing. Either route it through a
  rule or note the exception.

  **4. Behavioral parity — verified safe.** I checked the old dict
  insertion order vs the new PRODUCT_ACTIVATION_RULES list order: identical,
  so `get_available_products` output (incl. ordering) is preserved 1:1.
  ldewald's "no test exercises the lambdas" concern (test file line 5) is
  valid as defense-in-depth but the refactor is faithful by inspection — a
  2-3 rule behavioral test is cheap insurance, not a blocker. His suggested
  `stub_hotel(...)` test is reasonable if `stub_hotel` supports those kwargs.

  ### On ldewald's other 2 questions (you can endorse these)
  - properties.py:44 "silent drop if rule is None": agree it's ugly, but
    note it IS test-guarded — `test_get__returns_definitions_for_every_
    frontend_product` locks the exact name set, so a missing rule fails CI.
    A `logger.warning`/assert is still cleaner. Low priority.
  - property_list.py:355 plain-string sub-product names vs enum: valid, but
    NOT a regression — pre-refactor `_sub("MOBILE_KEY", …)` also used raw
    strings, and SUB_PRODUCT_RULES keys ("AUTHORIZATION" vs enum
    AUTHORIZATIONS, "CHECKOUT" vs CHECK_OUT) already mismatch the enum.
    Enum would help; reasonable as a follow-up, scope creep here.

  ### Recommended response to Rami (draft — not posted)
  "Nice refactor, the declarative pattern reads well and parity is
  preserved. Two things before approval: (1) the drift-guard test described
  in the docstrings and PR body doesn't exist — either implement the
  source-inspection check as written, or remove that claim from both
  docstrings and the PR description so we're not relying on a safety net
  that isn't there. (2) Concretely showing why (1) matters: the COMPENDIUM
  description describes the `_many` bulk query, but the rule uses
  `_get_compendium_product_availability` → `CompendiumSelector.
  get_has_compendium`, so the tooltip is already inaccurate. Please fix that
  description and consider whether descriptions should be derived from a
  structured form rather than hand-written prose. KIOSK also bypasses the
  rules list — worth a comment. ldewald's logger.warning and behavioral-test
  suggestions are good to fold in."

  ### Next step for you
  Decide whether to post the above on GitHub (I did not). The COMPENDIUM
  inaccuracy + nonexistent drift-guard are the two points only you can
  authoritatively call given the domain-knowledge ask.
project: null
source_id: null
tags: []
time_minutes: 5
title: REview Rami's product status PR
updated: 2026-05-15 07:05:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://github.com/canary-technologies-corp/canary/pull/43431