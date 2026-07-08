---
area: null
contexts:
- react
created: 2026-07-07 10:35:47.130648
defer_until: null
due: null
energy: low
id: 2026-07-07T1035-respond-on-ent-6711-reshare-your-rca-hunch-for-dis
order: null
output: |
  ## Agent run 2026-07-07T11:45 (draft — NOT yet posted)

  Grounded the hunch against the code so Tincho has concrete pointers. Note the
  full mechanism write-up already lives in PMS-9191 (https://linear.app/canary-technologies/issue/PMS-9191),
  which Gareth authored (branch glloyd/pms-9191) and which is now Done. ENT-6711
  is Andrea's parallel "run the RCA" ticket; the open question is *why validation
  never completed*. Tincho's ask: reshare the hunch to ground his research.
  Andrea already relayed a one-liner ("validation failed but was expected, so we
  set them live anyway — look at the pms_validation steps").

  ### Draft comment to post on ENT-6711 (reply in Tincho's thread) — AWAITING APPROVAL

  Resharing my hunch, now grounded against the code. (Full mechanism write-up is in
  PMS-9191 — this ticket is the "why were they live with validation never completed"
  follow-up.)

  **How enable is *supposed* to work:**
  - Every config upsert disables the config and seeds the vendor's required validation
    steps as `INCOMPLETE` (`AccountService.__upsert_configuration` → `disable_configuration`
    + `__ensure_validations_exist`, `accounts/services/account.py:424,427,449-465`).
  - The only path to `is_enabled=True` is `AccountValidationService.validate()` driving
    every seeded step to `COMPLETE`. `_enable_account`
    (`accounts/services/account_validation.py:195-207`) enables the config **only when
    zero `AccountValidation` rows remain `INCOMPLETE`** — if any step is missing/incomplete
    it early-returns and enable never fires.
  - Each step in `validate()` (`account_validation.py:70-101` — `FETCH_RESERVATION`,
    `FETCH_RESERVATIONS`, `IP_WHITELIST`, `AUTHENTICATE`, `FETCH_EVENTS`,
    `FETCH_RUN_EXISTS`) raises `ValidationFailed` on failure, which skips
    `_update_validation`/`_enable_account` and leaves that step `INCOMPLETE`.

  **Why they were "live anyway" despite is_enabled=False — the crux:** go-live is
  decoupled from `is_enabled`.
  - `GoLivePlan.execute()` (`canary/onboarding/plans/go_live_plan.py:40`) sets
    `hotel.is_live=True` with no check that the gateway config reached `is_enabled=True`.
  - The go-live gate `checks/configuration_completed.py` (`_check_script_type_completed`
    + the BW/Wyndham MSA variants) only checks that the `VALIDATE_PMS_CONFIGURATION`
    onboarding batch reached `COMPLETED` — **not** that validation passed or is_enabled
    flipped.
  - So a hotel could be fully live and receiving webhooks while its gateway config sat
    `is_enabled=False` with steps stuck `INCOMPLETE`. It only *worked* because the old
    webhook handlers ignored `is_enabled` — the bypass #48448/#48465 removed on Jun 22.

  **The hunch in one line:** these ~189 configs went live through onboarding + the
  webhook bypass without ever completing `AccountValidationService.validate()`. The
  go-live check verifies the *script batch ran*, not that validation *succeeded*, so a
  failed/incomplete validation was tolerated and they were set live anyway. PMS-9191's
  samples back this: config written once (`updated_at==created_at`), empty
  `admin_history`, zero fetch_runs.

  **Where I'd start:**
  1. Pull `AccountValidation` rows for the affected accounts — which `validation` kinds
     are stuck `INCOMPLETE`? Clustering names the failing step. (Fastest discriminator:
     validation ran-and-failed vs never-invoked.)
  2. Read `ConfigurePMSIntegrationValidatePlan.execute()`
     (`canary/onboarding/plans/configure_pms_integration_validate_plan.py:52-91`) and
     the go-live gate `checks/configuration_completed.py` — confirm the batch can reach
     COMPLETED without every validation passing.
  3. Vendor scope: Wyndham/OHIP was *excluded* from the Jun 22 gate (`oracle_ohip`), so
     the 189 are mostly the push vendors in PMS-9191 (autoclerk, synxis, jonas_chorum,
     cloudbeds). Check each one's `get_validations()` for a step that structurally can't
     pass for a webhook-only property (e.g. `FETCH_RUN_EXISTS`).

  Aside: OHIP has an explicit manual override that special-cases Wyndham —
  `oracle_ohip/admin.py enable()` sets `is_enabled=True` directly for non-WHR chains but
  leaves WHR ("must be enabled via the script"), so Wyndham has its own is_enabled path
  (`reports/providers/wyndham_onboarding_ohip.py`) — worth a separate look if any of the
  affected are OHIP.

  (Branch note: the gate PRs are filed under PMS-9050; PMS-9191 is the RCA that traced
  the blast radius.)

  ### Status
  Draft only — NOT posted to Linear (posting needs explicit approval). Waiting on
  Gareth to confirm before commenting on ENT-6711.

  ### Key links
  - ENT-6711: https://linear.app/canary-technologies/issue/ENT-6711
  - PMS-9191 (the RCA, Done): https://linear.app/canary-technologies/issue/PMS-9191
  - Gate PRs (under PMS-9050): canary#48448, canary#48465
  - Code map: accounts/services/account_validation.py:70-101,195-207;
    accounts/services/account.py:424,427,449-465;
    canary/onboarding/plans/go_live_plan.py:40;
    canary/onboarding/plans/configure_pms_integration_validate_plan.py:52-91;
    canary/onboarding/checks/configuration_completed.py;
    vendors/integrations/oracle_ohip/admin.py enable()
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-6711/run-root-cause-analysis-for-disabled-integrations
tags:
- morning-gtd
- linear
time_minutes: 10
title: 'Respond on ENT-6711: reshare your RCA hunch for disabled integrations'
updated: 2026-07-07 13:49:19.679126
waiting_on: null
waiting_since: null
working_on: false
---

Tincho @-mentioned you: reshare your hunch on where to begin looking. Hunch so far: validation step failed but was expected, so integrations were set live anyway.
https://linear.app/canary-technologies/issue/ENT-6711/run-root-cause-analysis-for-disabled-integrations