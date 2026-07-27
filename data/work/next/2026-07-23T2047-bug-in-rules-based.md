---
area: null
contexts: []
created: 2026-07-23 20:47:56.803924
defer_until: null
due: 2026-07-27
energy: low
id: 2026-07-23T2047-bug-in-rules-based
order: null
output: |
  ## Agent run 2026-07-24T10:13

  **Verdict: the reviewer's claim is CONFIRMED — real, unguarded, untested. But no production corruption has occurred (checked prod DB).**

  ### Mechanism (verified in code)
  - `enterprise_wyndham/configs/wyndham.py:222` defines `hotel.integration_secret_key` = `ANY_NON_NULL` (FINAL) for all WYNDHAM_CONNECT_GMS hotels.
  - The validation path is safe: `ConformityService._compare_settings` (rules_based_configuration/services/conformity.py:768) has an explicit `isinstance(expected_value, AnyNonNullType)` guard.
  - The write path is NOT: `apply_portfolio_settings.process_hotel` (rules_based_configuration/management/commands/apply_portfolio_settings.py:121-136) compares `actual_value == expected_value`. `AnyNonNullType` defines no `__eq__`, so a real secret string never equals the sentinel — every hotel is always treated as drifted. The command writes by default (`--dry-run` is opt-in), so a bare `manage.py apply_portfolio_settings wyndham` calls `apply_setting`, which does `setattr(hotel, "integration_secret_key", <sentinel>)` then `hotel.save()`. CharField coerces via `str()` → repr fallback → the literal string `"ANY_NON_NULL"` overwrites the real secret. Confirmed `str(sentinel) == 'ANY_NON_NULL'` in a REPL.
  - Blast radius of a bare run: every Wyndham Connect GMS hotel loses its integration secret (breaks PMS sync / reservation-widget auth), and `Hotel.save()` (hotels/models/hotel.py:1626) flags `gateway_account_needs_sync` when the key changes, so the corrupted value propagates to the gateway.
  - Second instance, same bug: `hotel.check_in_configuration.payment_gateway_config_id` = ANY_NON_NULL (wyndham.py:362). That one is an int FK, so `save()` would crash on int-coercion — loud, and since all saves for a hotel share one `transaction.atomic()` block it would incidentally roll back the secret-key corruption for NORTH_AMERICA_LIVE hotels. Hotels matching CONNECT_GMS but not NA_LIVE get silent corruption with no such accidental protection.
  - Bonus symptom: even `--dry-run` logs a bogus perpetual "change" for these keys on every run.
  - `drift.py` and the on-save signal are read/warn-only — `apply_portfolio_settings` is the only write path. Command added in PR #35897 / ENT-5033 (https://github.com/canary-technologies-corp/canary/pull/35897).

  ### Has it already fired in prod?
  No. Queried the prod mirror (US region): `SELECT id, name FROM canary_raw.canary.hotels_hotel WHERE integration_secret_key = 'ANY_NON_NULL'` → 0 rows. (EU/AP not checked — the query was permission-blocked mid-session — but Wyndham Connect GMS hotels are US-region, so exposure there is nil-to-negligible.)

  ### No test covers it — confirmed
  `rules_based_configuration/tests/management/commands/test_apply_portfolio_settings.py` has 15 tests, zero mentions of ANY_NON_NULL / AnyNonNullType.

  ### Proposed fix (not applied — working tree left clean on the ENT-6664 migrations branch)
  In `process_hotel`, skip validation-only sentinels before the equality check, mirroring `_compare_settings`:

      from rules_based_configuration.services.conformity import AnyNonNullType

      for setting_key, expected_value in expected_settings.items():
          # ANY_NON_NULL is a validation-only sentinel; it has no concrete
          # value to apply and must never reach setattr/save.
          if isinstance(expected_value, AnyNonNullType):
              continue
          ...

  Plus a regression test: register a spec with `ANY_NON_NULL` on `hotel.integration_secret_key`, run the command without `--dry-run`, assert the secret is unchanged and no change is logged. Worth also considering a belt-and-braces guard in `apply_setting` (raise on AnyNonNullType) so future write paths can't repeat this.

  Nothing was committed, pushed, or posted anywhere; repo untouched.

  ## Agent run 2026-07-24T10:31 — fix design (planned, not implemented)

  Scope confirmed with Gareth: **guard only** (no defensive raise in `apply_setting`). No Linear ticket exists yet.

  ### Code change
  `rules_based_configuration/management/commands/apply_portfolio_settings.py` — extend the conformity import with `AnyNonNullType`, and skip sentinels at the top of the `process_hotel` settings loop, mirroring the existing `_compare_settings` guard:

      for setting_key, expected_value in expected_settings.items():
          # ANY_NON_NULL is a validation-only sentinel: there is no concrete
          # value to apply, so it must never reach setattr/save.
          if isinstance(expected_value, AnyNonNullType):
              continue

  Side benefit: kills the perpetual bogus "change" log these keys emit on every --dry-run.

  ### Regression test
  `rules_based_configuration/tests/management/commands/test_apply_portfolio_settings.py`, in the existing `TestProcessHotel` class (existing mock-ConformityService pattern, but with autospec=True):
  `test_process_hotel__skips_any_non_null_sentinel_without_writing` — hotel with a real `integration_secret_key`; mock expected settings = `{"hotel.integration_secret_key": ANY_NON_NULL}`; run `process_hotel(hotel, None, dry_run=False)` (the dangerous bare-run path); assert returns 0 and `refresh_from_db()` shows the secret unchanged (persisted-state assertion).

  ### Mechanics
  - Branch off `origin/master` (NOT the current ENT-6664 migrations branch; tree is clean, restore checkout after): `glloyd/fix-apply-portfolio-settings-any-non-null`. No migration → single normal PR, no split.
  - Before opening the PR: draft a Linear ticket (bug + blast radius + "no prod corruption yet"), get explicit approval to create it, then reference it in the PR. Push, open draft PR, report CI; never merge.

  ### Verification
  1. `direnv exec . pytest rules_based_configuration/tests/management/commands/test_apply_portfolio_settings.py --nomigrations -v` — new test + existing 15 pass.
  2. Revert the guard locally → confirm the new test fails, then re-apply (proves it catches the regression).
  3. `direnv exec . make check-fix` from backend/canary; commit linter fixes as `lint`.

  Full plan file: /Users/garethlloyd/.claude/plans/plan-the-fix-kind-backus.md
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: 5
title: bug in rules-based
updated: 2026-07-27 14:05:21.235536
waiting_on: null
waiting_since: null
working_on: false
---

## 2 · "`ANY_NON_NULL` has no equality guard, so a bare run writes the literal string over `integration_secret_key`"

**His point:** unguarded bug in the write path; no test covers it.