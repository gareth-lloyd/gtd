---
area: null
contexts:
- react
created: 2026-05-27 01:38:03.204879
defer_until: null
due: null
energy: medium
id: 2026-05-27T0138-review-pr-46289-ent-6076-programmatically-set-wynd
order: null
output: |
  ## Agent run 2026-05-27T10:30Z

  **PR #46289** — ENT-6076 Programmatically set Wyndham OHIP guarantee_codes during onboarding (Martin Rodriguez, +480/-6, 15 files)

  ### Verdict
  Ship it. Solid PR — pattern-conforming, well-tested, narrowly scoped. Two trivial nits and one non-blocking CI concern below.

  ### What it does
  - **Gateway**: new `PATCH /api/accounts/me/oracle_ohip/guarantee_codes` (msgspec-validated, transactional + `select_for_update`, 404 when no OHIP config, 422 on bad payload).
  - **Service**: new `OracleOHIPConfigurationService.update_guarantee_codes` using the existing `copy()` helper → `save(update_fields=["guarantee_codes"])`.
  - **Canary**: new client + service wrappers; service clears `_GatewayAccountCache`.
  - **Onboarding**: new `ConfigureOhipGuaranteeCodesPlan` + new `UPDATE_PMS_CONFIGURATION` stage inserted between `BASE_CONFIGURATION_NEW` and `GOLIVE` for `WYNDHAM_CONNECT_PLUS`.

  ### Correctness
  - View flow verified: `get_and_lock_configuration` raises `PMSConfigurationNotFound` → caught → re-raised as `NotFound` (404). Tests cover.
  - `copy()` mutates in-place and returns the same instance, so `save(update_fields=["guarantee_codes"])` is right.
  - `_GatewayAccountCache.clear(hotel)` matches the pattern used by `disable_configuration`. Skipping `PMSIntegrationStatsService.sync/refresh` is correct — those care about vendor/`is_enabled`, not `guarantee_codes`.
  - URL ordering is fine; `me/oracle_ohip/guarantee_codes` does not collide with `me/<str:vendor>/{cleanup,disable,validate}` (suffix differs).
  - msgspec `GuaranteeCodesBody` enforces non-empty strings + `min_length=1` on the lists, mirroring the legacy marshmallow `GuaranteeCodeMapSchema`. Good.
  - Stage flow test updated to reflect the new chain. Plan registered in `KNOWN_PLANS`. ✅

  ### Concerns / nits

  1. **CI: "Check code coverage" failing on pms-gateway.** Per the coverage comment, PR-added lines are 96% covered and project coverage went up. The failure is from unrelated master-level files dropping below threshold. Either `coverage:skip` label or rebase; not a code issue but it does block merge gatekeeper.

  2. **Unused logger in plan** (`onboarding/plans/configure_ohip_guarantee_codes_plan.py:8`) — `logger = structlog.stdlib.get_logger(__name__)` declared but never used. Trivial; drop the import.

  3. **Bare event log in canary service** (`pms_gateway/services/pms_gateway.py:260`) — `logger.info("update_oracle_ohip_guarantee_codes")` has no context. Compare `disable_configuration` which logs `hotel=hotel, vendor=vendor.value`. Add at least `hotel=hotel` for parity / debuggability. Trivial.

  4. **Redundant `{**updates}`** in view's diff log (`accounts/views/update_oracle_ohip_guarantee_codes.py:46`) — `updates` is already a dict. Stylistic; matches what's elsewhere in the file though.

  5. **Plan does not convert gateway errors to `raise_expected_error`** (onboarding CLAUDE.md flags this as a pattern). In practice the WCP stage chain guarantees the OHIP account exists by the time this runs, and existing PMS-integration plans don't catch either, so this is a "consistent with neighbors" rather than a bug. Skip unless the team wants it tightened.

  6. **`next()` picks the first OhipConfiguration with codes** and silently ignores any siblings. WCP provider only emits one, so this is fine today, but worth a one-line comment if more provider shapes might appear later.

  ### Bot reviews
  - Copilot: "Ok to merge".
  - review-bot: failed (separate workflow infra issue, not content).
  - All other CI green: pyright, migrations, security, e2e, Tusk Drift.

  ### Recommendation
  Approve. Optional: ask Martin for the logger context + unused-import cleanup before merge, and apply `coverage:skip` (or get unrelated files green) to unblock the merge gatekeeper.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/46289
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #46289: ENT-6076 Programmatically set Wyndham OHIP guarantee_codes
  during onboarding'
updated: 2026-05-27 13:34:06.981019
waiting_on: null
waiting_since: null
working_on: false
---

Author Martin Rodriguez — personally requested. Gateway PATCH endpoint + onboarding script. https://github.com/canary-technologies-corp/canary/pull/46289