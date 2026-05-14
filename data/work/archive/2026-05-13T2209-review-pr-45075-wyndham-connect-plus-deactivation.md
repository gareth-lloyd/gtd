---
area: null
contexts:
- react
created: 2026-05-13 22:09:18.928038
defer_until: null
due: null
energy: medium
id: 2026-05-13T2209-review-pr-45075-wyndham-connect-plus-deactivation
order: null
output: '## Agent run 2026-05-14T12:35


  Reviewed PR #45075 (ENT-5951 — Martin). 5 files, +298/-0. Adds `WyndhamConnectPlusDeactivateHotelProvider`
  and wires `DEACTIVATE_MSA_HOTEL` into the WYNDHAM_CONNECT_PLUS process; also patches
  `WyndhamRemoveHotelFromParentBrandProvider` to flip three WCP-specific switches
  it was missing.


  ### Verdict

  **Approve with minor comments.** Follows existing patterns (mirrors `IHGPilotDeactivateHotelProvider`
  and the WYNDHAM_MSA `DEACTIVATE_MSA_HOTEL` wiring almost exactly). Scoping is correct,
  tests are sensible, no security concerns. Worth posting a couple of nits before
  merge.


  ### What''s good

  - Reverses only what WCP-specific providers enable: `has_authorizations` + `has_formweaver_auth_or_contract_flow`
  (from `WyndhamConnectPlusGoLiveProvider`), `has_ai`/`is_ai_responding_enabled`/`booking_url_prefix`
  (from `WyndhamConnectPlusChatConfigProvider`), `has_voice` (from `ConfigureVoicePlan`),
  `has_onsite_booking` (from WCP go-live config). Verified by reading each enabling
  provider.

  - Correctly removes `MSA_WYNDHAM_CONNECT_PLUS` portfolio while preserving `WYNDHAM`
  portfolio + SSO + association IDs (WCP shares Wyndham SSO org; opt-out shouldn''t
  strip it).

  - Pre-run checks (`WYNDHAM_HOTEL_BELONGS_TO_BRAND` + `SALESFORCE_OPPORTUNITY_OPTED_OUT`)
  match the WYNDHAM_MSA `DEACTIVATE_MSA_HOTEL` setup at property_configuration_processes.py:1340-1343.
  Consistency is good.

  - Reuses existing `ScriptType.DEACTIVATE_MSA_HOTEL` + `DeactivateHotelPlan` — no
  new ScriptType, no plan-name migration. Clean.

  - Uses `PortfolioService.hotel_belongs_to_portfolio_by_identifier` (matches the
  canonical convention in memory).

  - Idempotent: all flag flips are `= False`; `PortfolioService.remove_hotel` is idempotent.

  - Skip-gate at `onboarding_batch.py:659` already covers `DEACTIVATE_MSA_HOTEL`,
  so a deactivated hotel can still re-run this script. No change needed there.


  ### Comments to leave on PR


  1. **Scope creep in `WyndhamRemoveHotelFromParentBrandProvider` patch (worth calling
  out, not blocking).** The PR also adds `has_authorizations`, `has_onsite_booking`,
  `has_formweaver_auth_or_contract_flow` flips to the existing parent-brand-removal
  provider. These were missed because the original was written before WCP existed.
  The fix is correct and safe (strictly more aggressive cleanup on a path that already
  torches everything), but it''s a separable bug fix. Consider calling it out explicitly
  in the PR body as "also fixes" so reviewers don''t miss it — the diff buries it.


  2. **`disabled_features` key inconsistency.** New provider returns `"ai_chat": True`;
  the parent-brand provider returns `"chat": True`. The distinction (deactivate-only-AI
  vs disable-chat-entirely) is reasonable, but if anything downstream parses these
  dicts for telemetry/audit, the key drift will bite. Probably fine to leave — worth
  a glance.


  3. **No integration test for the wiring.** Tests cover the provider in isolation.
  A small assertion that `ONBOARDING_TYPE_CONFIG[WYNDHAM_CONNECT_PLUS].ad_hoc_stages[DEACTIVATE_MSA_HOTEL]`
  resolves to `(DeactivateHotelPlan, WyndhamConnectPlusDeactivateHotelProvider)` would
  catch future wiring regressions. Martin says he sanity-checked at runtime — a one-liner
  test pins it permanently.


  4. **Docstring nit.** "For complete removal from the Wyndham brand, use `WyndhamRemoveHotelFromParentBrandProvider`"
  — there''s also `WyndhamDeactivateHotelProvider` (full MSA suspend, still part of
  brand). Mentioning both alternatives helps the next reader.


  5. **No reactivate path.** Out of scope per ticket. Likely needed soon — if a hotel
  opts back in, the only path today is re-running WCP onboarding from scratch, which
  may re-trigger Twilio/WhatsApp work. Worth a follow-up ticket.


  6. **Out of scope per PR body:** Twilio number release, WhatsApp sender deactivation,
  refunds. Fine for a phase-1 script — the operator running this still has manual
  cleanup. Make sure that''s documented somewhere ops can find (runbook? Notion?).


  ### Could not verify locally

  Tried to run the tests but pytest blew up on `shared.pytest_test_imports` import
  — local env issue unrelated to this PR. CI will confirm.

  '
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/45075
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #45075: Wyndham Connect Plus deactivation script (Martin)'
updated: 2026-05-14 12:29:19.763819
waiting_on: null
waiting_since: null
working_on: false
---

WCP deactivation/opt-out script. Personally requested.
https://github.com/canary-technologies-corp/canary/pull/45075