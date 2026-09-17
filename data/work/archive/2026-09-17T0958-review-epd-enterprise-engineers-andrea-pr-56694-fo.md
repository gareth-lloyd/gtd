---
area: null
completed_at: 2026-09-17 12:26:13.851027
contexts:
- react
created: 2026-09-17 09:58:14.609201
defer_until: null
due: null
energy: medium
id: 2026-09-17T0958-review-epd-enterprise-engineers-andrea-pr-56694-fo
order: null
output: |
  ## Agent run 2026-09-17T07:54:57Z

  Read-only review of both PRs (diffs read in full, callers checked on local master). Nothing posted to
  GitHub, Slack or Linear. No tests run locally; CI state taken from `gh pr checks`.

  Slack source: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1789588483508029
  Andrea's message mentions only #56694 ("IHG might have this same issue, so created a shared helper").
  No thread replies. Nobody has reviewed either PR yet (both REVIEW_REQUIRED).

  ### PR #56694 - HotelKey tokenization in PMS config stages
  https://github.com/canary-technologies-corp/canary/pull/56694
  Ticket: ENT-7537 (https://linear.app/canary-technologies/issue/ENT-7537/payment-information-not-syncing-to-pms-best-western-auburndale-inn-and)
  +229/-19, 7 files, author abrad. CI: only non-blocking Playwright shards 3/4 + 4/4 and `review-bot` fail
  (same three fail on #55507, so likely not PR-specific; not investigated).

  What it does: new `configure_hotel_key_tokenization(hotel)` in
  `onboarding/configuration_providers/hotel_key_tokenization.py` sets auth `pms_payment_method_strategy` and
  `pms_deposit_strategy` to TOKENIZE, copies the check-in gateway onto the auth config if auth has none,
  sets `is_tokenizing_with_hotel_payment_gateway` when a check-in gateway exists, warns (non-fatal) when
  there is no gateway. Called from a new `Vendor.HOTEL_KEY` branch in the BW provider and from both IHG
  HotelKey providers (replacing their check-in-only block).

  Verdict: code is small, clean and well tested. Approvable on code; two things worth raising first.

  1. IHG behaviour change is bigger than "shared helper" suggests (main point for you, given ENT-6032).
     Before: IHG HotelKey stages only flipped the check-in tokenization flag when a gateway existed.
     After: every run of `IHGPmsConfigProvider` / `IHGGmsCorePmsConfigProvider` unconditionally sets both
     auth strategies to TOKENIZE, gateway or not, including re-runs on already-live pilot hotels. That is
     probably right if HotelKey is token-only, but the PR's own caveat says no HotelKey token post has ever
     succeeded in production, and nothing was verified against a real HotelKey run. Worth asking Andrea:
     has anyone confirmed with PMS/INT that TOKENIZE actually works for IHG HotelKey + FreedomPay, and is
     it OK for a re-run to flip live Wave 1 hotels? I did NOT verify the "HotelKey only accepts tokens"
     claim: a quick grep of `backend/pms-gateway/hotelkey` found no payment-method capability declarations,
     so treat it as the ticket's assertion.
  2. No-gateway path writes a known-broken config. With no gateway the helper still sets TOKENIZE and only
     warns. Cards fail either way (raw_cc is rejected too), so this is defensible, and the warning text is
     clear. But it relies on an operator reading run warnings; Auburndale got into this state because
     nobody noticed. Optional ask: should this be a pre-run check instead of a post-hoc warning?

  Smaller notes:
  - Warning clobber: callers do `results.update(helper(...))`, which would overwrite an existing
    `non_fatal_warnings` string. Not a live bug: base `perform_hotel_configuration` returns only
    `config_provider`, and the BW `results` dict has no warning before the HotelKey branch. Other IHG
    providers append to the key instead; fine to leave.
  - Gateway copy mirrors `wyndham_go_live_provider.py:78-85` exactly (only when auth has none). Good.
  - Wyndham's version also sets `integration_auto_post_cc_to_pms`; this helper does not. Probably
    intentional (BW sets it elsewhere?) - not checked.
  - `AuthorizationConfiguration.clean()` is not called (`save(update_fields=...)`), but moving to TOKENIZE
    can only satisfy that hosted-redirect rule, never violate it.
  - IHG result key rename (`is_tokenizing_with_hotel_payment_gateway` ->
    `check_in_configuration.is_tokenizing_with_hotel_payment_gateway`): PR says only tests read it; I did
    not grep for other readers.
  - Does not fix bw-10352 itself (PR says so). That hotel still needs a HotelKey-accepted tokenizing
    gateway plus both strategies flipped by hand. Linter side is PR #56690
    (https://github.com/canary-technologies-corp/canary/pull/56690, open, by megolem).

  ### PR #55507 - Core Plus HR gateway check + tip-config drift monitor
  https://github.com/canary-technologies-corp/canary/pull/55507
  Ticket: ENT-7446 (https://linear.app/canary-technologies/issue/ENT-7446/deactivated-tip-departments-still-appear-on-the-staff-side)
  +122/-44, 7 files, author abrad, open since ~2026-09-09, only a macroscope bot review + Andrea's own
  replies. Same three CI failures as above.

  Note: Andrea's Slack message does not mention this PR; the pairing came from the awareness capture.
  The PR title/description also partly describe things already merged in #55475 ("add drift detection",
  "skip if hr gateway is assigned" are in the What list but not in this diff). The actual diff is a
  follow-up: live hotels report drift as `metric_only`, resolve failure reports `errored`,
  `_serialize` removed, `_resolve_tip_config` takes the partial config, test renames, and the frontend
  enum member + label + help text for `TIP_CONFIG_MATCHES_ONBOARDING`.

  Verdict: looks correct and low risk; reasoning in the description is sound. Points to raise:
  1. `_drift_outcome` returns METRIC_ONLY for a live hotel even with zero drift, so live hotels never
     show HEALTHY for this check. Intentional per the test
     (`...no_drift_after_go_live_flips_can_be_tipped`), but confirm the cohort UI renders metric_only
     with value 0 sensibly.
  2. `except (ValueError, KeyError)` is narrow. `OnboardedPropertyHealthService` swallows anything else
     into an empty result that rolls up healthy - which is the exact failure the PR says it is closing.
     Any other exception type from `apply_variant_to_partial_config` / `to_tip_config` still goes silent.
  3. Dropping `_serialize` means raw UUID / enum / Decimal values go into `results`; relies on
     `MonitoredCheckResult.results` using `DjangoJSONEncoder` (claimed in the PR, not verified by me).
  4. Frontend eslint and vue-tsc were not run by the author (no node_modules). The change is one enum
     member plus entries in two total maps, so CI typecheck is the real gate; I did not see a failing
     frontend check.
  5. The docstring trimmed in `checks/ihg.py` removed the "why" (gateway attached by hand keeps syncing
     staff into disabled departments). Minor; that context is useful.
  6. PR description could be tightened so the What list matches the diff.

  ### Suggested next step (your call)
  - #56694: approve with a question about the IHG re-run / unverified TOKENIZE path, or hold until
    PMS/INT answers the open gateway question on ENT-7537.
  - #55507: approve with the narrow-except note, or ask for a description cleanup first.
  No review comments drafted or posted. If you want them posted, tell me which points and I'll draft
  the exact text for approval.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1789588483508029
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 20
title: 'Review: #epd-enterprise-engineers - Andrea: PR #56694 for HotelKey migrations
  (started from a Best Western issue); also #55507 tip-config drift detection'
updated: 2026-09-17 12:26:13.851022
waiting_on: null
waiting_since: null
working_on: false
---

Andrea: PR #56694 for HotelKey migrations (started from a Best Western issue); also #55507 tip-config drift detection
https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1789588483508029