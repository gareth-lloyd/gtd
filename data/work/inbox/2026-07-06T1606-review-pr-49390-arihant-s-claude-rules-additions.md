---
area: null
contexts:
- react
created: 2026-07-06 16:06:16.903517
defer_until: null
due: null
energy: medium
id: 2026-07-06T1606-review-pr-49390-arihant-s-claude-rules-additions
order: null
output: |
  ## Agent run 2026-07-07T11:40 — Review of PR #49390

  PR: https://github.com/canary-technologies-corp/canary/pull/49390
  "Add path-scoped Claude rules and tighten CLAUDE.md guidance" — arihantdaga.
  Status: **already MERGED** (2026-07-02, commit 91dcb744d47). +1186/-33 across ~40
  new `.claude/rules/` files + CLAUDE.md/makefile edits. So this is post-merge
  feedback, not a gate.

  ### Verdict: strong, high-accuracy PR. Ship-quality. Nothing merge-blocking; a few
  minor corrections worth a follow-up commit.

  The real risk in a rules PR is factual drift — a wrong API/path in a rule silently
  misdirects every future coding agent. The PR claims "every cited API was verified
  against source." I spot-checked a broad, high-leverage sample (~40 concrete
  symbol/path/API/linter/make-target claims) against the live codebase via 3 parallel
  verification agents (backend canary+shared, pms-gateway, frontend). **Accuracy held
  up remarkably well — the large majority verified exactly.**

  Confirmed correct (representative):
  - The `globs:` → `paths:` frontmatter conversion is CORRECT — Canary's own
    factory:improve skill (references/gotchas.md:41) documents `paths:` as the supported
    key and that rules load lazily on matching-file access. So the 4 legacy rules were
    indeed mis-keyed before; this fixes them.
  - Stale-fact fixes are all genuinely right: `BaseModel`→`SoftDeleteModel` (no
    `BaseModel` class exists anymore), `packages/shared/src/`→`packages/shared/` path
    alias (matches vite.config.mts:289 + tsconfig.json:34), `waitFor`→`vi.waitFor`.
  - Backend symbols all exist as cited: isolate(on_error_factory=, remove_after=),
    get_canary_object_or_404, readonly_database/no_readonly_database, CanaryException
    (+ pms-gateway common.exceptions re-export), lock/lock_instance, PermissiveTypedSchema,
    Statsd.metrics.*, safe_backfill_iterator, ConfigurableStringsMixin, default_i18n/
    validate_i18n, CanaryBaseCommand/GatewayBaseCommand, FeaturesService.get_feature_rollout
    (+ FeatureRollout.rollout_percentage), the deprecate_field example migration file,
    structlog.stdlib.get_logger.
  - pms-gateway symbols all exist: AbstractAPI.get_provider, FetchService.get_service,
    CardKind, XMLDict.get_list, Rollout.is_object_in_dynamic_rollout, DeltaCapableModel
    (delta_identifiers / DELTA_INCAPABLE_FIELDS), MembershipInformation example,
    vendors/integrations/oracle_ohip.
  - Frontend symbols all exist: createQuery/createQueryList/createMutation from
    shared/bridge, MutationEffectKind (NO_ACTION/INSERT_OR_REORDER/REMOVE/REFRESH),
    useDayjs():ComputedRef<typeof dayjs>, Deferred, useTimeFormatter/useDateFormatter,
    getLocalizedDayjs, I18nString/LanguageCode, CanaryButton onClick loading-guard
    (line 311 swallows click while loading), the 3 eslint rules (vue3-no-dollar-i18n,
    vue3-no-legacy-v-model, vue3-no-ref-of-collection), setupFile.ts vi.useFakeTimers().
  - Repo facts all correct: migration_files_only linter rule + the <20-added-line
    exemption (linter tests confirm 19 passes / 20+ fails), generate-openapi / check-fix /
    translate / test-app / typecheck-changes / test-backend make targets all exist.

  ### Findings (all minor; the PR is merged so these are follow-up nits)

  1. **[LOW] `bridge-api.md` — the only fabricated example.** The rule illustrates with a
     `salesAgent/PatchRfpThread.ts` module, a `"sales_agent.RFPThread"` resourceKind, a
     `/sales-agent/config` endpoint, and a `<!-- source -->` pointer to
     `frontend/packages/shared/api/salesAgent/`. None of these exist — no `sales_agent`
     app, no `RFPThread`, no `salesAgent/` folder (the real app is `sales_booking`; a real
     resourceKind is `"booking.GuestBooking"`). Harm is low (it's illustrative, not a
     convention an agent copies verbatim), but it directly contradicts the "every cited API
     verified" claim and the source pointer is dead. Worth swapping to a real endpoint.

  2. **[NIT] `django-data-queries.md` — pms-gateway replica-routing shorthand.** Written as
     "pms-gateway: `common.db.read_only`". `common.db.read_only` is the *module*; the
     decorator is `readonly_database` (import: `from common.db.read_only import
     readonly_database`). As written it reads like `read_only` is the symbol. Suggest
     `common.db.read_only.readonly_database`.

  3. **[NIT] Inconsistent import style for `IgnoreMigrationLintRules`.** `django-migrations.md`
     uses `from shared.canary_migrations.ignore_migration_lint_rules import ...` while
     deprecate_field.md uses `from shared.canary_migrations import ...`. Both work (the
     package __init__ re-exports it); the package-level import is canonical. Pick one.

  4. **[NIT] `FetchService.get_service` first param is `config`, not `configuration`** as the
     rule's inline example spells it. Positional, so harmless to callers.

  ### Coverage caveat
  I verified a representative sample of the most falsifiable claims, not literally every
  bullet across all ~40 files. Given the sample was ~40 claims and only 1 substantive
  inaccuracy surfaced (finding #1), overall factual quality is high.

  ### Suggested next step (NOT done — needs your go-ahead)
  PR is merged, so no approval to give. If you want, I can draft either (a) a short Slack
  reply to Arihant in the thread summarizing the verdict + the 4 nits, or (b) a follow-up
  one-commit fix for findings #1–#3. I did NOT post anything to Slack or GitHub. Say the
  word and I'll draft the exact text/diff for your approval first.
project: null
source_id: https://canarytechnologies.slack.com/archives/C019TQLQDJP/p1783009825526599?thread_ts=1783009825.526599&cid=C019TQLQDJP
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 20
title: 'Review PR #49390: Arihant''s Claude rules additions'
updated: 2026-07-07 11:40:59.189412
waiting_on: null
waiting_since: null
working_on: false
---

Arihant Daga asked in #eng-general for a review of PR #49390 (adds Claude rules for a lot of things).
https://github.com/canary-technologies-corp/canary/pull/49390
Slack: https://canarytechnologies.slack.com/archives/C019TQLQDJP/p1783009825526599?thread_ts=1783009825.526599&cid=C019TQLQDJP