---
area: null
contexts:
- react
created: 2026-06-09 07:01:12.616907
defer_until: null
due: null
energy: medium
id: 2026-06-09T0701-review-pr-47321-ent-6177-portfolio-scoped-staging
order: null
output: |
  ## Agent run 2026-06-09T12:05 (review of PR #47321)

  Reviewed locally against the PR head (origin/rrogers/ent-6177-...). Diff is 9 files,
  +422/-28: bootstrap command, ApplicationService.provision_with_credentials +
  list_active_staging_credentials_for_portfolio, GSI selector, create_application refactor,
  portfolio admin read-only field, and tests. Verdict: clean, well-tested, ready to merge —
  with ONE merge-order gate (below).

  ### IMPORTANT — merge-order dependency (confirmed in git history, not a code defect)
  The latest commit on the branch (b75eddab852 "Drop ENT-6171 changes ... now owned by that
  PR") REMOVES the staging-identifier symbols this PR consumes. At the current branch head these
  do NOT exist anywhere in the tree:
    - portfolios.services.portfolio.PRODUCTION_TO_STAGING  (imported by bootstrap command)
    - Portfolio.STAGING_PORTFOLIO_IDENTIFIERS              (used by admin staging_credentials)
    - Portfolio.Identifier.WYNDHAM_STAGING                 (used in tests)
  They are expected to arrive via the base branch once ENT-6171 lands. So `manage.py check`,
  the imports, and the test suite will only pass after ENT-6171 is in the base
  (rrogers/ent-6372-...). This matches the PR's stated merge order (ENT-6371 + ENT-6171 →
  ENT-6372 → this) and `gh pr diff` is clean against the base — but it MUST be enforced:
  do not merge this ahead of ENT-6171/ENT-6372, or master breaks on import.

  ### Correctness — looks good
  - provision_with_credentials is a faithful, line-for-line extraction of the
    Application+Identity+AuthToken flow out of create_application; create_application now just
    delegates. No behavior change; the dropped `credential_pair` assertions in the
    create_application test reflect that the secret is no longer logged (good).
  - Secret handling is right: secret_key is printed to stdout for the operator and never written
    to structured logs. Docstring on the service method spells this contract out.
  - Idempotency is portfolio-level (skip mint if an active staging credential already exists),
    and intentionally tolerates >1 during rotation overlap. Dry-run/commit/missing-portfolio
    paths are all handled; assert-not-None before the mint is sound (only reached under --commit
    after creation).
  - list_active_staging_credentials_for_portfolio filters is_staging AND status==ACTIVE AND
    deleted_at is None — tests cover production/revoked/soft-deleted exclusion.
  - _resolve_operator uses email__iexact and handles DoesNotExist / MultipleObjectsReturned with
    CommandError. Brand is restricted to WYNDHAM via _BRAND_CHOICES.
  - Admin field guards on STAGING_PORTFOLIO_IDENTIFIERS before hitting DynamoDB, so non-staging
    portfolios return "-" with no query. No circular-import risk (application_service does not
    import portfolios).

  ### Minor / non-blocking
  1. list_applications_by_portfolio_uuid does a single table.query with no LastEvaluatedKey
     pagination, so it only returns the first ~1MB page. The docstring says "returns every
     application row" which slightly overclaims. This is consistent with most sibling query
     methods in the selector and fine at staging scale (a handful of rows), but if a staging
     portfolio ever accumulated many application rows the idempotency check / admin display could
     silently undercount. Cheap to add a paginate loop or soften the docstring; not required now.
  2. The provision flow (Application → Identity → AuthToken) isn't wrapped in a transaction, so a
     mid-flow failure leaves a half-provisioned application. These are DynamoDB writes (not
     transactional anyway) and this matches the pre-existing create_application behavior, so it's
     not a regression — just noting the failure mode.
  3. create_portfolio runs ExploService.get_or_create when is_production(); a staging portfolio
     bootstrapped in a prod env would mint an Explo customer. Almost certainly harmless, just
     flagging the side effect.

  Did NOT run the test suite locally (would need ENT-6171 symbols present). Relied on reading the
  diff + the four touched test files; the author reports 123 passing and ruff/check clean.

  No external writes made (no PR comment posted). If you want the merge-order gate or the
  pagination/docstring nit raised on the PR, say the word and I'll draft a comment for approval.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/47321
tags:
- morning-gtd
- github
- from-awareness
time_minutes: 20
title: 'Review PR #47321: ENT-6177 Portfolio-scoped staging credentials (rrgrs)'
updated: 2026-06-10 15:03:37.561263
waiting_on: null
waiting_since: null
working_on: false
---

Bootstrap command + selector + admin (Part A). https://github.com/canary-technologies-corp/canary/pull/47321