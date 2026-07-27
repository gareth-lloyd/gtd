---
area: null
contexts:
- react
created: 2026-07-24 09:26:13.816288
defer_until: null
due: null
energy: medium
id: 2026-07-24T0926-review-ramiro-s-eng-design-unify-onboarding-add-pr
order: null
output: |
  ## Agent run 2026-07-24T10:12
  Read the full design doc (https://app.notion.com/p/canarytechnologies/Unify-Onboarding-Add-Products-Code-39e8146861518017bae7e1b8144beb1c), the divergence spreadsheet (https://docs.google.com/spreadsheets/d/17Qcm_5aNFVSO37053fhSpXEai_xs-a1pZw4OyaZpOk8/edit), and verified the claims against the actual code in backend/canary/onboarding (HotelProductsPlan in plans/hotel_products_plan.py, activate_hotel_products in services/onboarding.py, the Add Products view in views/onboarding_hotel_products.py).

  VERDICT: approve with comments. The design is sound, the staged rollout (flag on Add Products only, creation fixes as individually revertable PRs, characterization tests as flip criterion) is careful, and the divergence catalogue held up to code verification — all 16 rows match the code, including subtle ones (basic-tier case omitting has_consolidated_cc_payments_widget is in the spreadsheet; per-ProductType callback duplication up to 4x for auths; the is_dev() gate on callback attribution exists exactly as the ticket describes). Also verified: ProductsConfig fields are all required-at-construction except user_running_plan (supports Risk 3), no framework-level None-skip exists today (milestone 3 is genuinely new work), and the ONLY non-test caller of activate_hotel_products(_from_salesforce) is the Add Products view — so the milestone-7 deletion is safe.

  Suggested feedback (drafted, NOT posted anywhere):
  1. Catalogue gap — Compendium: the plan writes compendium product_tier LITE or FULL from config (hotel_products_plan.py:202-206, LITE reachable e.g. via Wyndham MSA config); activate hard-codes FULL (onboarding.py:983-985). Not in the spreadsheet or the doc table — add a row.
  2. Possible catalogue gap — fallback-to-SMS: the creation provider derives it from hotel_country (hotel_products_plan.py:82-84); activate computes it from hotel.country_code region at activation time (onboarding.py:880-884). Different data sources; can diverge for hotels with inconsistent country data.
  3. Unknown-product handling at creation: milestone 5's fail-loud parsing covers only the new opportunity provider. The creation path still silently drops unmapped ProductTypes (PRODUCT_TYPE_TO_CANARY_PRODUCT.get(...) is None -> skip, hotel_products_plan.py:231-232) while activate raises on unexpected types. That silent skip is exactly the "product paid for but never activated" hole the AC quote in the problem statement describes — suggest a follow-up ticket to fail loud (or alert) at creation too.
  4. Risk 3's mitigation is weaker than stated: required-fields-no-defaults catches an OMITTED field at construction, but the opportunity provider deliberately sets most fields to None — mapping a purchased product to the wrong None still constructs fine. Characterization tests catch it only while the legacy path exists to diff against; after deletion there is no net. Suggest per-product provider unit tests (each opportunity product => its expected non-None write set).
  5. Milestone 3 underspecified: after the refactor the plan has two overlapping skip mechanisms — the new None-skip and the existing _update_fields(only_set_true=is_live_hotel) gate (never writes falsy values on live hotels; does not apply to the unconditional block at lines 166-206). The doc should spell out the None / False / only_set_true interaction, otherwise "pure refactor, behavior preserving" is hard to review.
  6. Characterization tests: the ticket lists a non-live hotel fixture, but the only_set_true gate and the check-in/check-out test-mode email behavior manifest ONLY on live hotels — add a live-hotel-with-prior-state fixture, and assert callback counts (to pin the dedup fix).
  7. Transaction boundary for milestone 5: today activate_hotel_products_from_salesforce is one @transaction.atomic covering activation + MSA exclusion + admin roles (onboarding.py:781-825); the plan framework wraps plan runs in its own atomic (onboarding.py:655) while roles/MSA/support-user stay in the view. Decide and state whether the new path keeps a single transaction across plan run + view responsibilities. (Related pre-existing gap, not a regression: the view creates OnboardingScriptBatch/Run history records outside the atomic block, so activation can succeed with no script record.)

  Notable confirmed-today bug the doc catalogues but is worth amplifying with product: an opportunity selling ONLY Digital Authorizations Basic Plan gets no auths product at all from the creation path (config requires has_authorizations AND basic tier; spreadsheet calls it "biggest functional gap").

  Links: Slack request https://canarytechnologies.slack.com/archives/C0BJX0SD4RM/p1784819540484079 (no thread replies). Doc has 2 open inline comments (one from Andrea's org about other teams not knowing both paths need updating; one on flip semantics).

  Next step (yours): I can post findings 1-7 as inline Notion comments on the doc and/or reply to Ramiro in the DM — needs your go-ahead; nothing has been posted.
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C0BJX0SD4RM/p1784819540484079
tags:
- morning-gtd
- slack
time_minutes: 30
title: 'Review Ramiro''s eng design: Unify Onboarding & Add Products code paths'
updated: 2026-07-24 10:51:27.290325
waiting_on: null
waiting_since: null
working_on: false
---

Ramiro (group DM with Andrea, Jul 23): "I've made an eng design to unify the hotel creation and adding products paths. Can you take a look when you have some time?"
Doc: https://app.notion.com/p/canarytechnologies/Unify-Onboarding-Add-Products-Code-39e8146861518017bae7e1b8144beb1c
https://canarytechnologies.slack.com/archives/C0BJX0SD4RM/p1784819540484079