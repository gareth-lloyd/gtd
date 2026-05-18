---
area: null
contexts: []
created: 2026-05-05 16:08:07.890178
defer_until: null
due: null
energy: low
id: 2026-05-05T1608-capture-queries-and-tmp-and-useful-stuff-for-andre
order: 1
output: |
  ## Agent run 2026-05-15T16:10

  Reviewed `backend/canary/tmp/` with focus on `repeatable/` (and `useful/`),
  weighting recent items. Below are the curated candidates to refine and
  hand to a new Enterprise team manager, grouped by what they'd actually
  reach for. Each "repeatable" script is a parameterised, re-runnable
  shell-plus snippet — the closest thing we have to an Enterprise ops
  runbook in code.

  ### TIER 1 — share first (high reuse, generic, low blast radius)

  - `repeatable/create_and_run_onboarding_batch.py` (Jan 21) — the single
    most reusable one. Parameterised `create_custom(identifiers,
    onboarding_type, plan_names, ...)` that builds + runs an
    OnboardingScriptBatch via the service layer. This is the canonical
    "push a config change to N Wyndham/BW hotels" tool. Refine: drop
    hardcoded `username` fallback, add a dry-run print of resolved hotels
    before running.
  - `repeatable/debug_onboarding_scripts.py` (Jan 16) — `onb_problems(hotel)`
    returns a set of human-readable onboarding gaps (no PMS plan, no go-live,
    etc.). Excellent triage helper for "why isn't this hotel live". Refine:
    fix stray `from unittest import result` import and hardcoded "March 1st".
  - `useful/create_user.py` (Apr 28) — clean `create_at_hotel(...)` using
    PortfolioUserManagementService / PropertyRoleGrant. Frequent ask from
    Enterprise. Already well-structured; just needs a docstring + commit flag.
  - `useful/deactivated_hotels_by_script_type.py` (Apr 17) — queryset of
    hotels with a completed run for a given script type (default
    REMOVE_HOTEL_FROM_PARENT_BRAND). Good audit primitive.
  - `repeatable/debug_payment_gateway_config.py` (Dec 5) — GatewayConfig
    inspection w/ admin LogEntry history. Generically useful for payment
    onboarding escalations. Refine: the big FIXED/FIXED_NON_US hardcoded
    site-id blocks should be function args.

  ### TIER 2 — useful but brand/event-specific (share as examples/patterns)

  - `repeatable/remove_hotel_from_sso_organization_and_users.py` (Feb 17) —
    transactional removal of SSO users from hotels, with a safety guard that
    refuses if the hotel is still attached to the org. Good template for the
    "decouple a hotel from a parent brand" runbook; HOTEL_IDS hardcoded.
  - `repeatable/20260213_analyze_addon_purchase_rate.py` &
    `20260213_analyze_upsell_purchas_rate.py` (Feb 13) — ASCII-bar
    purchase/upsell rate reports (per-hotel ORM, all-hotel raw SQL). Nice
    self-serve analytics the manager can rerun by changing a slug. Light
    refine + rename the typo'd "purchas".
  - `repeatable/wyn/correct_wyndham_portfolio_membership.py` (May 3) &
    `bw/correct_best_western_portfolio_memberships.py` — portfolio
    reconciliation. Note: per saved feedback, portfolio changes MUST go
    through PortfolioService — verify these do before promoting.
  - `repeatable/wyn/setup_wyndham_connect_plus.py` (Apr 30) &
    `20260506_update_use_cases_on_guest_journey_messages.py` (May 6) — most
    recent, large, Wyndham-Connect-Plus specific. Document as the current
    WC+ setup playbook rather than refactor.

  ### NOTE / hygiene

  - `repeatable/20260211_audit_user_credit_card_views.py` is 0 bytes — drop.
  - `repeatable/ihg/` (Feb) is mostly dated one-off migrations
    (`20260212_ihg_upsell_use_cases*`, REVERT script) — keep as history, not
    runbook material, except `find_membership_program_levels.py`.
  - Lots of `find_non_standard_registration_cards.py` duplicated across
    wyn/ and bw/ — consolidate into one parameterised version.

  Suggested next step (for user, not done): pick Tier 1, move into a proper
  `enterprise/ops_scripts/` package with docstrings + dry-run flags, and
  walk the new manager through `create_and_run_onboarding_batch` +
  `debug_onboarding_scripts` as the core loop.
project: 2026-04-10T0840-ent-handover
source_id: null
tags: []
time_minutes: 5
title: Go through the backend/canary/tmp folder, looking in particular at "repeatable"
  code. Pick out candidates for refinement and sharing with a new Enterprise team
  manager.
updated: 2026-05-15 16:10:30.000000
waiting_on: null
waiting_since: null
working_on: false
---

Emphasize more recent items. 
Look for things that seem relevant and useful