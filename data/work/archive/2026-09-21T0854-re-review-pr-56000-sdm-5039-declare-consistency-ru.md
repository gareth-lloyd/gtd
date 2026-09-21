---
area: null
completed_at: 2026-09-21 13:49:22.725951
contexts:
- react
created: 2026-09-21 08:54:01.490881
defer_until: null
due: null
energy: medium
id: 2026-09-21T0854-re-review-pr-56000-sdm-5039-declare-consistency-ru
order: null
output: |
  ## Agent run 2026-09-21T10:45:18Z

  **Recommendation: APPROVE** PR #56000 (https://github.com/canary-technologies-corp/canary/pull/56000)
  at head `bb95338369`. Both of my CHANGES_REQUESTED points are resolved. Two non-blocking
  observations below. Nothing was posted to GitHub; the draft review text is at the bottom.

  ### State
  - Head `bb95338369` (2026-09-18 14:14Z). CI: 70 checks pass, none failing. `mergeable: MERGEABLE`,
    `mergeStateStatus: BLOCKED` only because my CHANGES_REQUESTED still stands.
  - Parent PR #55498 (https://github.com/canary-technologies-corp/canary/pull/55498) merged 09-14,
    so the diff against master is clean (11 files, +396/-139).
  - Linear: SDM-5039 (https://linear.app/canary-technologies/issue/SDM-5039/consistency-rules-validate-declared-keys-statically-and)
  - Reviewed by reading the full diff and the PR-head versions of `consistency.py`, `checks.py`,
    `testing.py`, `apps.py`, `setting_type_generator.py`. I did NOT run the tests locally; relying on green CI.

  ### My two comments: both addressed
  1. Rule-skip dropped concrete contradictions
     (https://github.com/canary-technologies-corp/canary/pull/56000#discussion_r4046782676).
     `ConsistencyService.validate_settings` now runs every rule and drops only errors whose `keys`
     intersect the sentinel-valued keys, exactly the suggested shape. New test
     `test_finalize__still_raises_on_a_contradiction_between_a_rules_concrete_keys` pins my example
     (integration_enabled=False, push_to_charges=True, push_to_notes=ANY_NON_NULL) against the real
     addon rule and asserts the notes key is absent from the raised error.
  2. W001 would fire permanently on the Wyndham tree
     (https://github.com/canary-technologies-corp/canary/pull/56000#discussion_r4046791303).
     W001 and the exercised/skipped tally are gone; `check_configuration_consistency` is back to a
     plain E001 comprehension.

  ### Luiza's follow-up change (the one she pinged me about)
  https://github.com/canary-technologies-corp/canary/pull/56000#discussion_r4047550332
  `advanced_fraud_gate_covers_verification` now names its two gating keys (`has_authorization_ui_v2`,
  `has_contract_v3_rollout`) in the error, and the decorator docstring states the contract: an error
  must list every key the rule read to reach it. I walked all 9 rules against that contract and they
  all comply. The failure direction when a future rule forgets a gating key is safe: the error is
  kept, so `finalize()` raises loudly (false positive), never a silent pass.

  ### Non-blocking observations
  - **OR-gates over-drop under the "name every key read" contract.** In the advanced-fraud rule the
    error now names all five keys, so `has_id_verification=True, has_advanced_fraud_v2=False,
    has_authorization_ui_v2=True, has_contract_v3_rollout=ANY_NON_NULL` is dropped, although
    ui_v2=True alone makes it a real contradiction whatever contracts_v3 turns out to be. Same for
    `has_amount_verification=ANY_NON_NULL` beside a concrete `has_id_verification=True`. This is the
    silent direction. It is theoretical today: the only ANY_NON_NULL definitions in production trees
    are `hotel.has_check_out`, one key at `wyndham.py:236`, and the two `payment_gateway_config_id`
    keys (`wyndham.py:471`, `:480`), none of them on an OR-gate. Fine to land; worth a follow-up
    note or ticket if trees start promising authorization flags.
  - **The contract is convention only, and `keys=` now feeds E002 alone.** After the switch from
    skipping to filtering, the declared keys no longer gate anything; filtering uses
    `error.keys`. The hoisted module constants make a body typo unlikely, but nothing checks that a
    rule's `error.keys` are a subset of its declared keys. A one-line assertion in
    `validate_settings` (or a test over the real registry) would make the declaration load-bearing
    again. Optional.
  - Nits: PR title still says "skip rules on ANY_NON_NULL" while the body and code say filter
    errors. `checks.py` imports the private `_RULES` (tests already do; consistent with the existing
    `ConformityService._ROOTS` access). `test_check__passes_for_registered_rules_with_real_keys`
    relies on autodiscovery having populated `_RULES`; it does (the `test_checks.py` autouse fixture
    does not clear `_RULES`), but an `assert _RULES` would stop it passing vacuously.

  ### Other reviewers' threads (abrad, 09-14): all handled
  Sentinel moved to `services/sentinels.py` (removes the duplicated scan and the import cycle),
  `SettingTypeGeneratorService.get_all_setting_keys()` imported directly, test registers through the
  decorator inside `reset_consistency_service_context()`, rule keys hoisted to module constants.
  Still true from abrad's nit: `get_all_setting_keys()` re-introspects all `CONFIGURABLE_MODELS` on
  every `manage.py` run that executes checks, unmemoized. Small cost, not blocking.

  ### Draft review to post (NOT posted; needs your explicit go-ahead)
  Destination: `gh pr review 56000 --approve --body ...`

  > Both points addressed, thanks. Filtering by error keys is the right shape and the finalize test
  > pins the case exactly. Good catch on the advanced-fraud gating keys.
  >
  > Two non-blocking thoughts, fine as follow-ups:
  > 1. Naming every key read over-drops on OR-gates. In `advanced_fraud_gate_covers_verification`,
  >    `has_authorization_ui_v2=True` with `has_contract_v3_rollout=ANY_NON_NULL` is a real
  >    contradiction whatever contracts_v3 resolves to, but the error names contracts_v3 so it is
  >    dropped. No production tree promises those keys today, so nothing is hidden right now.
  > 2. `keys=` now only feeds E002; the filter uses `error.keys`. Asserting
  >    `set(error.keys) <= declared_keys` in `validate_settings` would keep the declaration
  >    load-bearing and catch an error naming an undeclared key.
  >
  > Nit: the PR title still says "skip rules"; the code filters errors.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/56000
tags:
- morning-gtd
- github
time_minutes: 15
title: 'Re-review PR #56000: SDM-5039 declare consistency-rule keys, skip rules on
  ANY_NON_NULL'
updated: 2026-09-21 13:49:22.725946
waiting_on: null
waiting_since: null
working_on: false
---

https://github.com/canary-technologies-corp/canary/pull/56000
Luiza (lmanhaes1) addressed my CHANGES_REQUESTED and re-requested review on 09-18.