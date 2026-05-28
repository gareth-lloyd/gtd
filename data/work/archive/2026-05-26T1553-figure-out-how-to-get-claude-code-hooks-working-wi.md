---
area: engineering
contexts:
- craft
created: 2026-05-26 15:53:38.292563
defer_until: null
due: null
energy: medium
id: 2026-05-26T1553-figure-out-how-to-get-claude-code-hooks-working-wi
order: null
output: |
  ## Agent run 2026-05-28T09:03Z

  Research only — no code written, no hooks wired. Findings + a prioritized
  proposal below. Happy to implement Tier 1 on request.

  ### 1. How Claude Code hooks work (the useful subset)

  Hooks are shell/HTTP/MCP commands the harness fires on lifecycle events. They
  receive JSON on stdin (tool_name, tool_input, cwd, prompt, session_id, etc.)
  and influence behavior via exit code + JSON on stdout. Key levers for us:
  - PreToolUse  — fires BEFORE a tool runs. Can deny/allow/ask or rewrite input.
    Exit 2 = hard block (bypasses allow rules; deny rules still win). This is
    the enforcement event.
  - PostToolUse — fires AFTER a tool succeeds. Can't block, but can inject
    `additionalContext` back to the model. This is the feedback/lint event.
  - Stop / SubagentStop — fires when a turn ends. `decision:"block"` forces the
    model to keep working. Good for "don't finish until checks pass".
  - SessionStart / UserPromptSubmit — inject context (dynamic reminders, current
    enum values, registries) at session/prompt time.
  Config lives in settings.json under `hooks`, keyed by event, with a `matcher`
  (tool name, exact or regex). Precedence: managed > CLI > project-local >
  project > user. **Managed settings** (macOS: /Library/Application Support/
  ClaudeCode/managed-settings.json, deployable via MDM) can enforce hooks that
  users cannot override — the real "enterprise" lever.

  ### 2. What already exists in this repo

  - `.claude/hooks/block-production-access.py` — a PreToolUse(Bash) guardrail
    that blocks shell-plus/ssh/kubectl/psql/aws/deploy against prod/staging.
    NOTE: it is committed but NOT referenced in any repo settings.json `hooks`
    block, and no readable managed-settings.json exists locally — so it's either
    wired via MDM-deployed managed settings (not visible to the agent, matching
    its "cannot be bypassed" docstring) or not yet active. Worth confirming.
  - Many `.claude/settings.json` files (root + per-service) but they only set
    `permissions.deny` (secrets/env files) + plugins. No `hooks` blocks anywhere.
  So: the org has the governance-hook PATTERN established, but zero app-quality
  hooks. That's the gap and the opportunity.

  ### 3. Mapping to Enterprise-domain apps (onboarding + rules_based_configuration)

  I read both apps. "Enterprise concerns" interpreted as the enterprise hotel-
  deployment domain (Wyndham/IHG/BW/Marriott onboarding + config rules). The
  apps' documented footguns map almost 1:1 onto hookable checks:

  onboarding/ (from its CLAUDE.md):
  - New OnboardingPlan must be registered in KNOWN_PLANS (services/plan.py) AND
    wired into ONBOARDING_TYPE_CONFIG (models/property_configuration_processes.py).
    Easy to forget → silent no-op. Hookable: detect new `class X(OnboardingPlan`
    in an edited plan file, grep it isn't in both registries, warn.
  - Plans must call `self.raise_expected_error(CODE, ...)` with CODE present in
    BOTH exceptions.py WHAT_HAPPENED and WHAT_TO_DO dicts — not generic raises.
    Hookable: grep edited plan for raise_expected_error codes, verify they exist
    in both dicts.
  - OnboardingValue creation with SF account IDs must call add_sf_id_checksum().
    Hookable: flag edits that build OnboardingValue with a raw account_id.

  rules_based_configuration/ :
  - Ships a Django system check `check_configuration_consistency` (id E001) that
    walks every config tree and rejects contradictory rule combinations
    ("tokenize cards" + "no payment gateway"). This is THE enterprise-specific
    invariant in that app. Today it only fires at `manage.py check`/CI time.
    Hookable: run `manage.py check` automatically whenever an rbc file changes
    so contradictions surface the instant they're written, not in CI.

  ### 4. Proposed opportunities (prioritized)

  TIER 1 — high value, low effort:
  - PostToolUse(Edit|Write) scoped to onboarding/**.py & rules_based_configuration/
    **.py: run `ruff check --fix` + `pyright` on just the edited file, feed
    errors back as additionalContext. (Matches the lint commands already in the
    onboarding CLAUDE.md; gives the model instant typecheck feedback.)
  - PostToolUse(Edit|Write) on rules_based_configuration/**: run `manage.py check`
    and surface any E001 consistency errors. Single biggest domain-specific win.

  TIER 2 — custom onboarding validators (small Python hook script, PostToolUse on
  onboarding/plans/**):
  - Warn on unregistered new plans (not in KNOWN_PLANS / ONBOARDING_TYPE_CONFIG).
  - Warn on raise_expected_error codes missing from exceptions.py dicts.
  - Stop hook: if onboarding tests/source changed, run the relevant pytest subset
    before letting the turn finish ("verify and fail loud" from CLAUDE.md).

  TIER 3 — governance / managed settings:
  - Extend block-production-access.py (Bash matcher) to also block onboarding mgmt
    commands (cron_run_onboarding_script_batches, dev_onboard_*) and Salesforce
    PRODUCTION API writes from agent sessions.
  - Formalize the whole set via MDM-deployed managed-settings.json so Tier 1-3
    can't be bypassed org-wide — this is the actual "enterprise enforcement" move
    vs. per-repo opt-in.

  ### 5. Caveats / open questions for you
  - Confirm whether block-production-access.py is actually wired (via managed
    settings) — if not, that's a latent governance gap worth closing first.
  - Tier 1 PostToolUse hooks fire on EVERY edit in those trees; pyright on the
    whole app is slow, so scope to the single changed file and cache. Worth a
    quick perf check before rolling out.
  - Decide scope: per-developer (project settings.json, opt-in) vs org-enforced
    (managed settings). Drives where these live.

  ## Agent run 2026-05-28T09:12Z — creative hook exploration

  Went a layer deeper into both apps to find non-obvious hook plays. Each is
  grounded in code that already exists. Ranked by signal.

  STANDOUTS:

  B1. rbc "blast-radius" behavioral-diff hook  ★ most novel
    A rules engine's danger is that a one-line rule edit silently changes
    resolved config for whole cohorts. ConformityService already exposes
    `get_all_possible_setting_combinations()`, `hotel_conforms()`,
    `get_setting_value_for_hotel_attributes()` — and these operate on the
    in-memory rule trees + HotelAttributes, NOT hotel DB rows, so a hook can
    run them safely with zero prod access. PostToolUse on conformity/consistency
    edits: snapshot resolved settings across representative (MSA × brand ×
    country) combos before and after the edit, inject the DIFF as context —
    "your change flipped tokenize_cards true→false for Wyndham/US + IHG/CA."
    Turns an opaque edit into an observable behavioral diff at edit-time. This
    is basically `detect_drift` logic minus the prod hotel loop.

  A1. rbc codegen-staleness hook  ★ cheap + high value
    `generate_setting_types` produces conformity.pyi and ALREADY has a `--check`
    mode that fails if the stub is stale (used in CI). PostToolUse on the setting
    definitions: run `generate_setting_types --check`; if stale, either warn or
    auto-regenerate so the model never leaves a stale type stub for CI to reject.

  C1. onboarding registry-coherence Stop hook
    There's already a `check_config_provider_required_fields` mgmt command. Pair
    it with a tiny assertion that every OnboardingPlan subclass is present in BOTH
    KNOWN_PLANS and ONBOARDING_TYPE_CONFIG, and run on Stop when onboarding/ was
    touched — block turn-end on failure. Kills the "new plan silently never runs"
    class of bug.

  D1. dynamic brand-context injection (UserPromptSubmit / SessionStart)
    CLAUDE.md is static; enums drift. When a prompt mentions a brand or
    OnboardingType, a hook can shell to a small introspection command and inject
    LIVE data: ConfigProviders registered for that brand, their
    REQUIRED_SALESFORCE_FIELDS, current OnboardingType/ScriptType members,
    KIND_ID_TYPES. The model then writes against today's wiring, not a snapshot.

  E1. real-account-ID / PII leak guard (PreToolUse Edit|Write)
    Enterprise onboarding handles real customer Salesforce account IDs (15/18-char
    SF IDs). salesforce_ids.py is full of real ones LEGITIMATELY (e.g.
    "0015w000025qeYnAAI"). Risk: a real hotel account ID hardcoded into a test
    fixture or plan elsewhere. Hook: scan written content for SF-ID patterns (and
    real hotel slugs) outside the allowlisted homes (salesforce_ids.py, fixtures
    dir) and block. Enterprise data-hygiene guard with a precise allowlist.

  SECOND TIER:

  G1. mirror-test Stop hook — onboarding convention is "tests mirror source"
    (tests/plans/test_X.py). If a plan/service was edited but its mirror test
    wasn't touched, nudge on Stop. Enforces a documented convention for free.

  F1. onetime_/migration safety — onboarding has ~25 throwaway `onetime_*`
    commands + 145 migrations. PreToolUse(Bash): warn when a `onetime_*` command
    runs locally against non-local. PostToolUse(migrations/): flag irreversible
    ops or multiple leaf migrations (ties to existing fix-migration-conflicts /
    split-migration skills).

  I1. audit/compliance HTTP hook — PostToolUse `http` hook streaming every
    onboarding/rbc edit to an internal audit trail (SOC2/compliance angle); pairs
    with the managed-settings governance theme so it can't be turned off.

  EXPERIMENTAL / FLAG THE TRADEOFF:

  H1. idempotency LLM-judge (prompt-type PreToolUse) — single-turn model guard on
    plan edits: "does this preserve idempotency / keep transactional work out of
    post_success_hook?" Powerful but CLAUDE.md says don't overuse the model for
    routing/judgment — use sparingly, only where static analysis can't reach.

  J1. MCP-tool hook via canary-local — the canary-local MCP server exposes
    get_hotel_settings / get_feature_flags. A PreToolUse `mcp_tool` hook could
    validate a proposed config change against live feature-flag gating. Niche.

  K1. SubagentStart(Explore) hint injection — inject onboarding/rbc structure
    hints (registry file locations, key services) so Explore subagents skip
    re-discovering the layout every run.

  My pick if we build ONE: B1 (blast-radius diff) — it's the most unique to a
  rules engine and impossible to get from CLAUDE.md or CI feedback alone. A1 is
  the cheapest first win. Both are pure-local, no prod access.
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: 15
title: Look for opportunities to get claude code hooks into use for Enterprise concerns
updated: 2026-05-28 12:19:51.414022
waiting_on: null
waiting_since: null
working_on: false
---

* explore how hooks work - what's possible?
* Explore how to map this to Enterprise concerns: /onboarding app, /rules_based_configuration app, etc