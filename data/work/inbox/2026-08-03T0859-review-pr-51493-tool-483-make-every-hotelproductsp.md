---
area: null
completed_at: null
contexts:
- react
created: 2026-08-03 08:59:34.528584
defer_until: null
due: null
energy: medium
id: 2026-08-03T0859-review-pr-51493-tool-483-make-every-hotelproductsp
order: null
output: |
  ## Agent run 2026-08-03T13:35:00

  Reviewed PR #51493 (https://github.com/canary-technologies-corp/canary/pull/51493)
  — [TOOL-483] Make every HotelProductsPlan write skippable, by Ramiro Nieto
  (https://linear.app/canary-technologies/issue/TOOL-483/make-every-hotelproductsplan-write-skippable).
  Milestone 3 of "Unify Onboarding & Add Products Code"
  (https://app.notion.com/p/39e8146861518017bae7e1b8144beb1c).

  **Nothing posted to GitHub.** This is a local review only — draft comments below are
  yours to send or drop.

  ### Verdict: approve with comments

  The refactor is correct and does what it says. All 3 files reviewed
  (`hotel_products_plan.py`, `demo_hotel_products_provider.py`, `test_hotel_plans.py`).
  No blocking defect found. Creation behaviour is genuinely unchanged: both providers fill
  every new field with the previously-hardcoded values. I checked every `ProductsConfig`
  construction site — the 3 the diff doesn't show (`demo_hotel_products_provider.py:158`,
  `:172`, `:174`) are all `**base.__dict__` splats off already-populated configs, so they're
  safe. `EnableMsaProductsConfig` is a separate class and unaffected.

  The one thing I verified that the two Macroscope bot reviews did not: the new
  `test_execute__all_none_config_touches_nothing` really does exercise the new `None`-skip
  in `_update_fields`, because `stub_hotel_with_role_based_permissions` defaults
  `is_live=False` → `only_set_true=False` → without the skip it would `setattr(hotel,
  "has_check_out", None)` and blow up on save. So the test has teeth.

  ### Comments worth raising (none blocking)

  **1. "Touches nothing" is field-level, not row-level.** An all-`None` run still executes 7
  unconditional saves — `hotel.save()` plus `authorization_configuration`, `chat_configuration`,
  `check_in_configuration`, `check_out_configuration`, `payment_links_configuration`,
  `compendium_configuration`. Values don't change, but the rows are written: `modified` bumps
  (`Hotel` is `BackwardsCompatibleTimeStampedModel`) and a bare `save()` writes every column,
  clobbering any concurrent write. Harmless today (fresh hotel at creation, nobody else writing);
  materially riskier once this plan runs against a **live** hotel, which is the whole point of
  the milestone. Not a blocker for a pure refactor, but worth a follow-up ticket to make the
  saves conditional or move to `save(update_fields=[...])` before Add Products ships. The repo's
  own `.claude/rules/backend/django-data-queries.md` calls out the bare-`save()` clobber risk.
  I confirmed `EventableModelMixin` does *not* hook `save()`, so there's no audit-event storm —
  just the row write.

  **2. On a live hotel the plan still cannot turn anything off.** `_update_fields` with
  `only_set_true=True` skips every `False`, so for live hotels `None` and `False` are already
  indistinguishable — the new `None`-skip is dead code on that path. Since Add Products targets
  live hotels, the "skippable writes" framing may mislead whoever builds on this: you can skip
  a write, but you still can't clear a flag. Worth stating explicitly in the `ProductsConfig`
  docstring, which currently just says "None means do not touch".

  **3. Truthiness-guarded blocks collapse `None` and `False`.** The blocks gated on
  `if config.has_authorizations:` / `has_contracts` / `has_advanced_fraud_v2` / `has_e_folio` /
  `has_tipping` / `has_tablet_reg_v1` / `has_chat and has_chat_ai` / `compendium_product_tier`
  skip correctly on `None`, so the acceptance criterion holds. But the coupling has a trap: to
  set `authorization_tier = BASIC` you must also pass `has_authorizations` truthy
  (`if config.has_authorizations and config.has_authorizations_tier_basic:`), and likewise
  `has_chat` truthy to set chat AI. An Add Products run that passes `has_authorizations=None`
  ("don't touch, already on") will silently skip the tier write. Same shape for chat. This is
  the exact "miss one and it silently does the wrong thing" failure the ticket warns about, just
  inverted. Suggest a comment on those two conditionals, or splitting them in the follow-up PR.

  **4. `has_dispute_generation` is an order-dependent conditional write, not a plain skippable
  one.** The guard reads `hotel.authorization_configuration.has_formweaver_auth_or_contract_flow`
  *after* the block that may have just written it from config, and `hotel.has_check_in` after
  `_update_fields` may have just written that. So passing
  `has_formweaver_auth_or_contract_flow=None` + `has_dispute_generation=True` against a live
  hotel with the flow off silently skips. The field comment documents the intent, which is good.
  There's no test for the "config says True but hotel has check-in" branch — cheap to add.

  **5. Nit — 5× copy-paste in the demo provider.** The same 5 lines
  (`has_formweaver_auth_or_contract_flow` / `has_formweaver_autosend_messages` /
  `id_verification_provider` / `has_dispute_generation` / `user_running_plan=None`) are repeated
  across `DEFAULT_DEMO_PRODUCTS_CONFIG` and the 4 onboarding-type configs. A shared
  `DEMO_AUTHORIZATION_DEFAULTS` dict splatted into each would remove the "add a field, miss one
  config" hazard that the no-defaults rule is specifically trying to prevent. Also
  `user_running_plan=None` is dead in all 5 — `DemoHotelProductsProvider.__init__:176`
  unconditionally overwrites it. Required by the no-defaults invariant, so fine, just noise.

  **6. Nit — `_StaticProductsProvider` test helper breaks the ABC contract.**
  `ConfigProvider.__init__` is abstract with signature `(self, data: OnboardingPlanData)`; the
  helper takes `config` and never sets `self.data`, so `execute_rollout` would `AttributeError`.
  Works because Python doesn't check signatures, and it's underscore-prefixed test-only, so
  low stakes.

  ### Things I liked

  - `_stub_all_none_products_config()` via `dict.fromkeys(dataclasses.fields(...))` auto-adapts
    when fields are added — the test can't rot.
  - `test_products_config__no_field_has_a_default` enforces the no-defaults invariant mechanically
    rather than by convention. Good call.
  - Nesting the `SupportUser` lookup inside `if config.all_products is not None:` avoids a
    pointless DB query on skip runs.

  ### CI status

  Green now. The earlier red on 2026-07-30 (14 Blacksmith failures — addons post-checkin, F&B,
  membership loyalty, digital tipping) was marked **outdated** and the follow-up E2E run passed
  (https://github.com/canary-technologies-corp/canary/actions/runs/30640063418). Those were
  guest-hub E2E tests with no plausible connection to this diff — flake/infra, not this PR.
  Macroscope blocks auto-approval only because the files are pod-enterprise-owned and the author
  isn't in that pod, i.e. it needs a human — you.

  ### Suggested next step

  Approve with the comments above as non-blocking. Items 1–3 are really "before Add Products
  ships on top of this", not "before this merges" — consider asking Rami to log them on the
  milestone rather than expanding this PR, since the whole point is that the refactor ships
  clean and separate from behaviour fixes.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/51493
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #51493: [TOOL-483] Make every HotelProductsPlan write skippable'
updated: 2026-08-03 13:35:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

Personally requested (rami + ldewald + pod-enterprise). +192/-51, REVIEW_REQUIRED, mergeable.
https://github.com/canary-technologies-corp/canary/pull/51493