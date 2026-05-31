---
area: null
contexts:
- react
created: 2026-05-29 11:43:03.691705
defer_until: null
due: null
energy: medium
id: 2026-05-29T1143-review-pr-46618-ent-6171-staging-portfolio-identif
order: null
output: |
  ## Agent run 2026-05-29T12:10 — Review of PR #46618 (ENT-6171)

  Verdict: APPROVE. Clean, well-tested, low-LOC foundational PR. No blocking
  defects. One awareness note (the shim's intentional breadth) worth a sentence
  in the PR description; not a blocker.

  NOTE ON METHOD: working tree is on master, so this review is from `gh pr diff`
  plus reading the (unchanged-by-PR) call sites on master. I did NOT post anything
  to GitHub.

  ### What it does
  - Adds IHG_STAGING / WYNDHAM_STAGING / BEST_WESTERN_STAGING to
    Portfolio.Identifier and to PUBLIC_PORTFOLIO_IDENTIFIERS.
  - Adds PRODUCTION_TO_STAGING map + modifies
    PortfolioService.hotel_belongs_to_portfolio_by_identifier so a production
    identifier query ALSO matches the corresponding staging portfolio
    (one-directional shim).
  - Maps each staging identifier to its production LoyaltyProgramIdentifier
    (same priority) in membership_level_new.
  - Adds a separate staging exclusive-portfolio frozenset in add_to_portfolio_plan
    (staging brands mutually exclusive among themselves; do NOT conflict with
    production brand exclusivity).
  - No data migration (dropped intentionally; existing IHG Staging row id 3764 set
    by hand per-environment).

  ### Correctness checks that PASS
  - NO migration needed and none is missing: Portfolio.identifier is
    `models.CharField(max_length=64, ...)` with NO `choices=` kwarg, so adding
    TextChoices members does not alter the field — `makemigrations --check` in CI
    stays green. (Also correct to drop the data migration.)
  - New values ("ihg_staging"=11, "wyndham_staging"=15, "best_western_staging"=20)
    all fit max_length=64.
  - Shim is correctly one-directional: querying production matches staging;
    querying staging does NOT expand to other production brands. Tested
    (production_match_staging, staging_does_not_match_other_production, list form).
  - Exclusivity: the separate frozenset is consistent with the existing per-set
    loop; staging<->production non-conflict is behaviourally tested
    (staging_does_not_block_production_brand, staging_brands_are_mutually_exclusive).
  - Loyalty priority mirrors production exactly (IHG=0, WYNDHAM/BW=1); even if a
    hotel were in both prod+staging of one brand, same identifier+priority -> no
    conflict.

  ### Awareness note — shim breadth (NOT a bug; by design)
  The shim lives in the SHARED helper hotel_belongs_to_portfolio_by_identifier,
  which has ~50 call sites. So "production query now also matches staging" applies
  transparently everywhere — which is exactly the intended mechanism (one shim so
  every production-brand check includes the matching staging hotel). I read the
  call-site categories to confirm none is a landmine:
    - booking flows, voice booking agents, check-in (incl. check_in_payment.py),
      guest journey segmentation, messaging templates, guest reservation
      renderables, enterprise_ihg reservation data, IHG greener-stay segmentation,
      payment_verification view — all feature-shaping "is this a Wyndham/IHG
      hotel?" checks where staging SHOULD mirror production. Intended.
    - onboarding config providers (wyndham/ihg/bw deactivate + remove-from-parent-
      brand guards, MSA, group_use_case, onboarding_batch) — guard checks like
      `if not belongs_to(WYNDHAM): error`. A *_STAGING hotel now passes these
      guards; benign/edge-case, consistent with staging≈production.
  Correction to an earlier draft of this note: there is NO billing_service.py or
  integrations/wyndham/payment_service.py caller (those files don't exist; an
  earlier tool-output glitch produced a bogus "billing" snippet). The real
  payment-adjacent callers are guest_booking_payment_view, payment_verification,
  and check_in_payment — all feature-shaping, not money-movement gating. So there
  is no billing/charge landmine. Suggest the author just add one line to the PR
  body noting the shim transparently widens all ~50 production-brand checks to
  include staging, for future archaeology.

  ### Minor / nits
  - PUBLIC_PORTFOLIO_IDENTIFIERS has DUAL semantics per its docstring: GrowthBook
    targeting (hotel_public_portfolio_identifiers, the intent here) AND "membership
    should be visible to end users." The visibility side effect is low risk for
    internal staging hotels. Good: staging was NOT added to
    DISCOVERABLE_PORTFOLIO_IDENTIFIERS, so guest-SDK hotel listing is unaffected.
  - Shim is environment-agnostic (no is_production gate). Fine given the staging-env
    premise; means the mapping is unconditional (only matters if a *_STAGING
    portfolio ever holds hotels in the PROD db).
  - test_add_to_portfolio_plan__staging_brands_are_mutually_exclusive uses inline
    imports + an inline ConfigProvider subclass; repo prefers top-level imports,
    but acceptable as test-local scaffolding.

  ### Test coverage: GOOD
  Behavioral, not shape-only (author deliberately dropped frozenset/dict structure
  tests in commit 2 — good). Covers the shim both directions + list form, plan
  exclusivity both ways, and membership canonical-level mapping via parametrize.
  PR claims 69+83+31 passing, pyright/ruff clean (not re-run by me).

  Recommendation: approve. Optional: one PR-description sentence on the shim's
  breadth. No GitHub review/comment was posted by me.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/46618
tags:
- morning-gtd
- github
- from-awareness
time_minutes: 20
title: 'Review PR #46618: ENT-6171 staging portfolio identifiers + brand-mapping shim'
updated: 2026-05-29 12:33:11.298038
waiting_on: null
waiting_since: null
working_on: false
---

Bottom of rrgrs's pre-production-hotels stack (review first). Adds IHG_STAGING/WYNDHAM_STAGING portfolio identifiers, mappings, brand-mapping shim. https://github.com/canary-technologies-corp/canary/pull/46618