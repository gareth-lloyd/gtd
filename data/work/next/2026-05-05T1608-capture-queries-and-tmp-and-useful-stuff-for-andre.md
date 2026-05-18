---
area: null
contexts: []
created: 2026-05-05 16:08:07.890178
defer_until: null
due: null
energy: low
id: 2026-05-05T1608-capture-queries-and-tmp-and-useful-stuff-for-andre
order: 1
output: "## Agent run 2026-05-15T16:10\n\nReviewed `backend/canary/tmp/` with focus
  on `repeatable/` (and `useful/`),\nweighting recent items. Below are the curated
  candidates to refine and\nhand to a new Enterprise team manager, grouped by what
  they'd actually\nreach for. Each \"repeatable\" script is a parameterised, re-runnable\nshell-plus
  snippet — the closest thing we have to an Enterprise ops\nrunbook in code.\n\n###
  TIER 1 — share first (high reuse, generic, low blast radius)\n\n- `repeatable/create_and_run_onboarding_batch.py`
  (Jan 21) — the single\n  most reusable one. Parameterised `create_custom(identifiers,\n
  \ onboarding_type, plan_names, ...)` that builds + runs an\n  OnboardingScriptBatch
  via the service layer. This is the canonical\n  \"push a config change to N Wyndham/BW
  hotels\" tool. Refine: drop\n  hardcoded `username` fallback, add a dry-run print
  of resolved hotels\n  before running.\n- `repeatable/debug_onboarding_scripts.py`
  (Jan 16) — `onb_problems(hotel)`\n  returns a set of human-readable onboarding gaps
  (no PMS plan, no go-live,\n  etc.). Excellent triage helper for \"why isn't this
  hotel live\". Refine:\n  fix stray `from unittest import result` import and hardcoded
  \"March 1st\".\n- `useful/create_user.py` (Apr 28) — clean `create_at_hotel(...)`
  using\n  PortfolioUserManagementService / PropertyRoleGrant. Frequent ask from\n
  \ Enterprise. Already well-structured; just needs a docstring + commit flag.\n-
  `useful/deactivated_hotels_by_script_type.py` (Apr 17) — queryset of\n  hotels with
  a completed run for a given script type (default\n  REMOVE_HOTEL_FROM_PARENT_BRAND).
  Good audit primitive.\n- `repeatable/debug_payment_gateway_config.py` (Dec 5) —
  GatewayConfig\n  inspection w/ admin LogEntry history. Generically useful for payment\n
  \ onboarding escalations. Refine: the big FIXED/FIXED_NON_US hardcoded\n  site-id
  blocks should be function args.\n\n### TIER 2 — useful but brand/event-specific
  (share as examples/patterns)\n\n- `repeatable/remove_hotel_from_sso_organization_and_users.py`
  (Feb 17) —\n  transactional removal of SSO users from hotels, with a safety guard
  that\n  refuses if the hotel is still attached to the org. Good template for the\n
  \ \"decouple a hotel from a parent brand\" runbook; HOTEL_IDS hardcoded.\n- `repeatable/20260213_analyze_addon_purchase_rate.py`
  &\n  `20260213_analyze_upsell_purchas_rate.py` (Feb 13) — ASCII-bar\n  purchase/upsell
  rate reports (per-hotel ORM, all-hotel raw SQL). Nice\n  self-serve analytics the
  manager can rerun by changing a slug. Light\n  refine + rename the typo'd \"purchas\".\n-
  `repeatable/wyn/correct_wyndham_portfolio_membership.py` (May 3) &\n  `bw/correct_best_western_portfolio_memberships.py`
  — portfolio\n  reconciliation. Note: per saved feedback, portfolio changes MUST
  go\n  through PortfolioService — verify these do before promoting.\n- `repeatable/wyn/setup_wyndham_connect_plus.py`
  (Apr 30) &\n  `20260506_update_use_cases_on_guest_journey_messages.py` (May 6) —
  most\n  recent, large, Wyndham-Connect-Plus specific. Document as the current\n
  \ WC+ setup playbook rather than refactor.\n\n### NOTE / hygiene\n\n- `repeatable/20260211_audit_user_credit_card_views.py`
  is 0 bytes — drop.\n- `repeatable/ihg/` (Feb) is mostly dated one-off migrations\n
  \ (`20260212_ihg_upsell_use_cases*`, REVERT script) — keep as history, not\n  runbook
  material, except `find_membership_program_levels.py`.\n- Lots of `find_non_standard_registration_cards.py`
  duplicated across\n  wyn/ and bw/ — consolidate into one parameterised version.\n\nSuggested
  next step (for user, not done): pick Tier 1, move into a proper\n`enterprise/ops_scripts/`
  package with docstrings + dry-run flags, and\nwalk the new manager through `create_and_run_onboarding_batch`
  +\n`debug_onboarding_scripts` as the core loop.\n"
project: 2026-04-10T0840-ent-handover
source_id: null
tags: []
time_minutes: 5
title: Go through the backend/canary/tmp folder, looking in particular at "repeatable"
  code. Pick out candidates for refinement and sharing with a new Enterprise team
  manager.
updated: 2026-05-18 13:39:30.000111
waiting_on: null
waiting_since: null
working_on: true
---

Emphasize more recent items. 
Look for things that seem relevant and useful