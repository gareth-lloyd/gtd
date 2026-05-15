---
area: null
contexts: []
created: 2026-05-15 06:28:58.036798
defer_until: null
due: null
energy: low
id: 2026-05-15T0628-review-rami-s-product-status-pr
order: -19
output: "## Agent run 2026-05-15T07:05\n\nReviewed PR #43431 \"[TOOL-104] Explicit
  definitions on product statuses\"\n(Ramiro Nieto, +602/-74, 11 files, base master,
  MERGEABLE, not draft).\nldewald explicitly tagged you for domain feedback (\"not
  super familiar\nwith this code\") and left 4 questions. NOTHING posted to GitHub
  — review\ndrafted below for you to post/adapt.\n\n### What the PR does\nRefactors
  `CanaryProducts.get_available_products` and onboarding\n`_get_sub_products` from
  imperative blocks into declarative\n`PRODUCT_ACTIVATION_RULES` / `SUB_PRODUCT_RULES`,
  each rule pairing the\nactivation predicate with a human-readable `active_description`.
  Adds\n`/onboarding/api/properties/product-definitions` endpoint + a Vue tooltip\n(\"Active
  when: …\") on the Product Status card.\n\n### Verdict: solid refactor, but DO NOT
  approve as-is. It oversells.\n\n**1. (BLOCKER) The headline \"drift-guard test\"
  does not exist.**\nPR description claims \"Drift-guard tests ensure active_description
  stays\nin sync with the is_active callable\". Both `ProductActivationRule` and\n`SubProductActivationRule`
  docstrings claim a test \"inspects the\nis_active source to assert every hotel attribute
  referenced in\nactive_description also appears in the callable.\" It doesn't. The
  two new\ntest files (`test_product_activation_rules.py`,\n`test_sub_product_rules.py`)
  only assert (a) product/name uniqueness and\n(b) the rule set equals a hardcoded
  expected set. Zero source inspection,\nzero description-vs-callable comparison.
  ldewald flagged exactly this on\ncanary_products.py:209. The docstrings AND the
  PR description are false.\nThis matters because the descriptions are the whole point
  — they're shown\nto users — and several are free prose over private logic that WILL
  rot.\n\n**2. (CONCRETE PROOF point 1 matters) COMPENDIUM description is already\nwrong,
  day one.** `DIGITAL_COMPENDIUM.active_description` =\n\"The hotel has a Compendium
  Configuration row whose product tier is\nanything other than DISABLED.\" But `_get_compendium_product_availability`\n(single-hotel
  path, the one this rule uses) delegates to\n`CompendiumSelector.get_has_compendium(hotel)`
  — NOT the\nexclude(product_tier=DISABLED) query. That prose was copied from the\n`_many`
  bulk variant. So a user-facing tooltip is already inaccurate\nbefore any drift,
  with no test to catch it. This is the single strongest\nargument that the prose-without-enforcement
  approach is fragile.\n\nI verified the other 4 helper-backed descriptions and they
  ARE accurate:\nAUTHORIZATIONS ✓, SALES_BOOKINGS ✓, TABLET_REGISTRATION ✓\n(has_tablet_reg_v1
  and (has_check_in or has_check_out)), PAYMENT_LINKS ✓.\nThe ~13 simple `lambda hotel:
  hotel.has_x` ones are self-evidently fine.\n\n**3. (Minor) KIOSK bypasses the \"single
  source of truth.\"** It's appended\nmanually in `_build_product_definitions` with
  a hardcoded description, not\nin PRODUCT_ACTIVATION_RULES, not drift-guarded at
  all. `hotel.has_kiosk`\nis the right flag so the text is accurate, but it contradicts
  the\ndocstring's \"single source of truth\" framing. Either route it through a\nrule
  or note the exception.\n\n**4. Behavioral parity — verified safe.** I checked the
  old dict\ninsertion order vs the new PRODUCT_ACTIVATION_RULES list order: identical,\nso
  `get_available_products` output (incl. ordering) is preserved 1:1.\nldewald's \"no
  test exercises the lambdas\" concern (test file line 5) is\nvalid as defense-in-depth
  but the refactor is faithful by inspection — a\n2-3 rule behavioral test is cheap
  insurance, not a blocker. His suggested\n`stub_hotel(...)` test is reasonable if
  `stub_hotel` supports those kwargs.\n\n### On ldewald's other 2 questions (you can
  endorse these)\n- properties.py:44 \"silent drop if rule is None\": agree it's ugly,
  but\n  note it IS test-guarded — `test_get__returns_definitions_for_every_\n  frontend_product`
  locks the exact name set, so a missing rule fails CI.\n  A `logger.warning`/assert
  is still cleaner. Low priority.\n- property_list.py:355 plain-string sub-product
  names vs enum: valid, but\n  NOT a regression — pre-refactor `_sub(\"MOBILE_KEY\",
  …)` also used raw\n  strings, and SUB_PRODUCT_RULES keys (\"AUTHORIZATION\" vs enum\n
  \ AUTHORIZATIONS, \"CHECKOUT\" vs CHECK_OUT) already mismatch the enum.\n  Enum
  would help; reasonable as a follow-up, scope creep here.\n\n### Recommended response
  to Rami (draft — not posted)\n\"Nice refactor, the declarative pattern reads well
  and parity is\npreserved. Two things before approval: (1) the drift-guard test described\nin
  the docstrings and PR body doesn't exist — either implement the\nsource-inspection
  check as written, or remove that claim from both\ndocstrings and the PR description
  so we're not relying on a safety net\nthat isn't there. (2) Concretely showing why
  (1) matters: the COMPENDIUM\ndescription describes the `_many` bulk query, but the
  rule uses\n`_get_compendium_product_availability` → `CompendiumSelector.\nget_has_compendium`,
  so the tooltip is already inaccurate. Please fix that\ndescription and consider
  whether descriptions should be derived from a\nstructured form rather than hand-written
  prose. KIOSK also bypasses the\nrules list — worth a comment. ldewald's logger.warning
  and behavioral-test\nsuggestions are good to fold in.\"\n\n### Next step for you\nDecide
  whether to post the above on GitHub (I did not). The COMPENDIUM\ninaccuracy + nonexistent
  drift-guard are the two points only you can\nauthoritatively call given the domain-knowledge
  ask.\n"
project: null
source_id: null
tags: []
time_minutes: 5
title: REview Rami's product status PR
updated: 2026-05-15 12:58:11.800315
waiting_on: null
waiting_since: null
working_on: false
---

https://github.com/canary-technologies-corp/canary/pull/43431