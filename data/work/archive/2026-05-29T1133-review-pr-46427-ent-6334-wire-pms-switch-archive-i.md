---
area: null
contexts:
- react
created: 2026-05-29 11:33:52.490046
defer_until: null
due: null
energy: medium
id: 2026-05-29T1133-review-pr-46427-ent-6334-wire-pms-switch-archive-i
order: null
output: |
  ## Agent run 2026-05-29T12:55 (review only — nothing posted to GitHub)

  PR #46427 "ENT-6334 Wire PMS switch archive into Best Western onboarding" by martinrodriguezcanary.
  +282/-5, 8 files. State: OPEN, REVIEW_REQUIRED, not a draft. CI: E2E passed, coverage 100% on
  added lines. Only bot reviews so far (Copilot x2, both now clean); no human review yet. My personal
  review was requested.

  ### Verdict: LGTM — approve. Solid, well-documented, well-tested. No blocking issues found.

  ### What it does
  - Wires `PMS_SWITCH_ARCHIVE` as an archive-only ad-hoc stage into `BEST_WESTERN_MSA`
    (`property_configuration_processes.py`). FE allowlist has offered it since #36643 but backend
    wiring was missing, so the app showed the option then rejected with "Invalid script type" (the
    ENT-6334 bug). Confirmed the FE allowlist (frontend/manage/.../Cohort/constants.ts:549) does list
    PMS_SWITCH_ARCHIVE under BEST_WESTERN_MSA — premise is accurate.
  - Adds two pre-run checks (checks/pms_switch_checks.py):
    - `pms_switch_has_enabled_vendor` (brand-agnostic, NON-skippable): account must have an enabled
      outbound vendor to archive.
    - `best_western_pms_switch_archive_targets_old_pms` (BW-specific, skippable): refuses when HotelKey
      (the new PMS) is already the outbound vendor, so the archive can't hit the new PMS.
  - Adds `stub_hotelkey_configuration` + `hotelkey` kwarg on `stub_account` (pms_gateway/testing.py).
  - Rewors the archive plan success instruction so it no longer hard-references a CLEANUP stage that
    BW doesn't wire (next_stages=[]).

  ### Both Copilot comments are already resolved (verified against the current diff)
  1. "[Important] Mews PMS switch would always be blocked." RESOLVED. The current code guards with
     `if hasattr(account, gateway_vendor.value):` before reading is_enabled. Account DTO has no `mews`
     field (confirmed in pms_gateway/schemas/account.py — only opera/hotelkey/etc.), so Mews falls
     through to `return None` (trusts account.type). There's a dedicated regression test
     `test_passes_for_vendor_not_modeled_in_account_dto`. The 2nd Copilot pass found no new comments.
  2. "[Consider] success instruction tells operator to run CLEANUP which BW doesn't have." RESOLVED.
     Instruction reworded to "If a PMS switch cleanup stage follows, wait ..." (plan + test updated).

  ### Correctness checks I ran
  - Vendor enum values verified (backend/shared/shared/pms/core/vendor.py): HOTEL_KEY="hotelkey"
    (matches Account.hotelkey field → generic check's is_enabled path works), MEWS="mews" (no DTO
    field → hasattr False → trusted), OPERA="opera". All consistent.
  - Both checks catch broad `except Exception` on get_account and return an error string (fails loud,
    blocks the run) — matches the existing `_resolve_wyndham_pms_switch_vendors` pattern. No silent
    failure.
  - "disabled config => nothing to archive" semantics match the existing wyndham check convention.
  - Pre-run checks return error strings (not plan errors), so no exceptions.py error-code entries are
    needed — correct.
  - Both checks are registered for the BW stage; ordering is fine (generic accepts enabled HotelKey,
    BW guard then blocks it).

  ### Non-blocking observations (optional, worth a mention to author — NOT posted)
  - The BW HotelKey guard is `skippable=True`. That means an operator CAN skip the one guard that
    prevents accidentally archiving the new PMS (HotelKey). The rationale (future migration *away*
    from HotelKey) is documented in code, and the non-skippable has-enabled-vendor check still runs,
    so this is an acceptable judgment call — just flagging the protective intent is bypassable by
    design.
  - Minor: `pms_switch_has_enabled_vendor` is named/documented as brand-agnostic but is only wired
    into BW. Fine as a reusable building block; no action needed.

  ### Suggested next step
  Approve. If you want, I can post an approving review or a short comment noting the skippable-guard
  observation — say the word and I'll draft the exact text first (I have NOT posted anything).
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/46427
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #46427: ENT-6334 Wire PMS switch archive into BW onboarding'
updated: 2026-05-29 13:05:00.701476
waiting_on: null
waiting_since: null
working_on: false
---

Personal review requested (martinrodriguezcanary), not yet reviewed. https://github.com/canary-technologies-corp/canary/pull/46427