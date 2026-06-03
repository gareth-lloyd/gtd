---
area: null
contexts:
- react
created: 2026-06-03 10:32:43.193491
defer_until: null
due: null
energy: medium
id: 2026-06-03T1032-review-pr-46584-tool-193-update-salesforce-product
order: null
output: |
  ## Agent run 2026-06-03T12:39:18

  Reviewed PR #46584 [TOOL-193] — Salesforce product name alias mappings. Read all 4
  changed files in full plus the surrounding call sites (onboarding write path,
  property-list read path, salesforce_opportunity sync path). Did NOT post anything to
  GitHub — review is recorded here only.

  ### Verdict: LGTM / approve, with one question worth confirming + a few minor nits.

  Well-scoped, well-tested, reversible (follow-up ticket TOOL-260 already filed to remove
  the aliases post-migration). CI is green (E2E passed, 100% coverage on added lines,
  threshold check passed). I could not re-run the unit tests locally (the PR branch's
  worktree resolved system pytest instead of the project venv, and per my time-box rule I
  didn't fight the env) — but the tests are simple deterministic assertions I read in full,
  and CI already exercises them.

  ### What the PR does (all correct)
  - `PRODUCT_TYPE_ALIASES` + `_missing_` fallback: casefolded keys, looked up AFTER the
    existing case-insensitive pass. Renamed SF labels resolve to existing canonical members
    without flipping canonical values. Good temporary-shim design.
  - Observability: unknown non-blank values now log `salesforce.unknown_product` — directly
    addresses the ticket's "silent drop" concern.
  - `_MOBILE_KEY = "Mobile Keys - Wallet"` added to IGNORED_PRODUCT_TYPES. Correctly stays
    out of the `PRODUCT_TYPE_TO_CANARY_PRODUCT` assert (it's ignored). The new
    `_activate_product` case is defensive/unreachable in normal flow — it's stripped at
    onboarding.py:642 (`- IGNORED_PRODUCT_TYPES`) before activation — but consistent with the
    existing _KIOSK/_PMS_INTEGRATION/_SET_UP_FEE cases. Fine.
  - property_list filter: alias icontains matching. The Smart Checkout->Check-Out case
    genuinely needs it (`icontains "Check-Out"` won't match "Smart Checkout"). The Upsells /
    Mobile Ordering aliases are redundant (canonical value is already a substring of the new
    label) but harmless. Guest-messaging consolidation handled correctly: base MESSAGING
    stays, "AI Guest Messaging" aliases to MESSAGING_WITH_AI.

  ### One question worth confirming (not a blocker)
  - CHECKOUT label mismatch: the Linear ticket's rename table lists the OLD checkout label as
    "Contactless Checkout", but the enum's canonical CHECK_OUT value is "Check-Out", and the
    PR only adds the NEW label "Smart Checkout" as an alias. So the PR resolves "Check-Out"
    (canonical) and "Smart Checkout" (new). If SF's current/old value is literally
    "Contactless Checkout", that string matches neither and would already be dropping today
    (and during the flip window). Almost certainly the ticket table is just loose wording and
    the real SF field is "Check-Out" — but worth a one-line confirm with Stacy/Sales Ops,
    since checkout is the one row where old label != canonical enum value. (Upsells, Mobile
    Ordering, Guest Messaging - AI Module all match their canonical enum values exactly, so
    those are unambiguous.)

  ### Minor nits (non-blocking)
  - Observability gap: the warning fires on the `ProductType()` constructor path (onboarding
    + `get_products_for_opportunity`) but NOT on property_list's `_PRODUCT_TYPE_BY_LOWER.get()`
    dict-lookup read path, which silently skips unknowns. Drift is still observable via the
    other paths, so OK, but not uniform.
  - Pre-existing adjacent bug (out of scope): `get_products_to_activate` (onboarding.py:636)
    catches `except KeyError`, but `ProductType(unknown)` raises `ValueError` — so a truly
    unknown product in the onboarding write path hard-crashes instead of raising the graceful
    OnboardingServiceError. Not this PR's job, but with the new warning it'll now log then
    still crash. Worth a heads-up to the author.
  - Canary linter flagged missing autospec on the new `patch("onboarding.salesforce.logger")`.
    The file already has 36 bare `patch(...)` calls, so this just follows existing convention;
    adding `autospec=True` would silence the bot but isn't important for a logger patch.

  ### Suggested reply to ramiro (DRAFT — not posted; needs your approval before sending)
  "LGTM — clean shim and good call adding the unknown_product warning + the TOOL-260 cleanup
  follow-up. One thing to sanity-check: the ticket lists the old checkout label as
  'Contactless Checkout' but the enum canonical is 'Check-Out' and the alias only covers the
  new 'Smart Checkout'. Can you confirm SF's current value is actually 'Check-Out'? If it's
  literally 'Contactless Checkout' we'd be dropping it both now and during the flip window.
  Other three renames match their canonical enum values so they're unambiguous. Non-blocking."

  No action taken on GitHub/Linear/Slack. Let me know if you want me to post the comment.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/46584
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #46584: [TOOL-193] Update Salesforce product name mappings for SF
  rename'
updated: 2026-06-03 12:56:35.551086
waiting_on: null
waiting_since: null
working_on: false
---

ramironieto requested me personally + DM'd: touches core onboarding concepts. https://github.com/canary-technologies-corp/canary/pull/46584