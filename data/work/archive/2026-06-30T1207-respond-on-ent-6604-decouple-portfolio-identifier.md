---
area: null
contexts:
- react
created: 2026-06-30 12:07:19.489264
defer_until: null
due: null
energy: medium
id: 2026-06-30T1207-respond-on-ent-6604-decouple-portfolio-identifier
order: null
output: |
  ## Agent run 2026-06-30T12:50 — analysis + draft reply (NOT yet posted to Linear)

  ### My view: yes, split it. The region-local slice is genuinely separable.

  rrogers is right. The gate (ENT-6687) exists solely to supply a global-uniqueness
  mechanism — and global uniqueness only matters for identifiers that cross regions.
  Region-local / above-property identifiers never cross regions, so the shared enum's
  accidental global-uniqueness guarantee was never doing anything for them. Holding
  staff-minted single-region identifiers hostage to the global spike is over-gating.

  ### Code verification (fresh read of master, /Users/garethlloyd/projects/canary)

  - `hotels/models/portfolio.py`: `identifier = CharField(max_length=64, null=True)` —
    NO `choices=`, NO regex/validators. Partial unique index `Q(identifier__isnull=False)`
    is per-regional-Postgres only. `clean()` is the ONLY valid-value gate (enum-membership
    check). Confirms rrogers: half-done already (choices= dropped in d155a4ec, "Stop using
    choices on Portfolio identifier field" #33879, Nov 2025).
  - `Portfolio.save()` never calls `full_clean()`; `clean()` fires only via
    PortfolioService.create_portfolio, the admin ModelForm, and test stubs. The admin
    **create-from-scratch** path writes via `get_or_create()` and already bypasses
    validation today — so free-form is already reachable on one in-region path (current
    silent footgun, independent of this ticket).
  - Unguarded `Portfolio.Identifier(value)` coercion sites: a fresh read finds only TWO
    genuinely unguarded — `onboarding/plans/populate_demo_data_plan.py:90` and
    `onboarding/schemas/rollout_recipe.py:47`. The others ENT-6687's audit listed
    (portfolio_hotels, apply_portfolio_settings, user_assignment_operation,
    onetime_ihg_fix) are already try/except-guarded. The load-bearing one —
    `api_gateway/request_framework/authorize.py` (AuthorizeHotelByApplicationPortfolio) —
    is already guarded. So the hardening surface is SMALLER than ENT-6687 implies, all in
    onboarding/demo/management-command code, not hot paths.
  - identifier is NOT purely a passive tag: branched on in voice find_reservation
    (WYNDHAM channel code) and gates analytics exclusions / SDK discovery / public
    visibility via frozensets (PUBLIC/STAGING/DISCOVERABLE_PORTFOLIO_IDENTIFIERS). But
    those are enum-value-keyed frozensets — new free-form region-local tags simply won't
    be members, which is the safe default. Reinforces: harden the coercion sites, the
    membership checks fail safe on their own.

  ### Two conditions I want baked into the slice

  1. NAMESPACE/COLLISION (the one real coupling to ENT-6687's Decision F Q4). If we mint
     free-form identifiers now and the spike later enables cross-region free-form, a
     region-local value could collide with a cross-region value or an existing enum value.
     The new format-check `clean()` should at minimum reject any value equal to an existing
     `Portfolio.Identifier`, and we should settle the reserved-namespace convention (or an
     explicit "region-local identifiers are migratable, here's how") inside this slice so
     interim minting doesn't paint the spike into a corner. Keep it lightweight — staff-
     minted, mostly passive tags.
  2. HARDEN-THEN-RELAX ORDERING + re-confirm inventory. Relaxing `clean()` without
     hardening the unguarded sites lets a free-form value reach them and crash. Land them
     together (or harden first), and re-confirm the unguarded inventory during impl rather
     than trusting either count.
  Plus: fold in closing the admin get_or_create validation gap so both create paths run the
  same format-check clean().

  ### Links
  - ENT-6604: https://linear.app/canary-technologies/issue/ENT-6604/decouple-portfolioidentifier-from-the-hard-coded-enum-table-backed
  - ENT-6687 (the gating spike, Decision F): https://linear.app/canary-technologies/issue/ENT-6687/spike-global-portfolio-identifier-resolution-uniqueness-mechanism

  ### DRAFT reply to rrogers (awaiting Gareth's approval before posting — NOT sent)
  ---
  Yes, let's split it. Agreed the region-local slice is separable — the gate (ENT-6687) is
  really only about cross-region uniqueness, and region-local identifiers never cross
  regions, so the accidental-enum-uniqueness guarantee was never doing anything for them.
  No reason to hold staff-minted single-region identifiers hostage to the global spike.

  Scope the new ticket to the region-local slice as you described: relax `clean()` to a
  format check, harden the unguarded `Portfolio.Identifier(value)` sites, keep the enum as
  source of truth for cross-region brands. Cross-region free-form stays gated on ENT-6687.

  Two things I want baked into the slice before we start minting:

  1. Don't let region-local minting constrain the spike. The one real coupling is
     namespace/collision (your Decision F Q4). If we mint free-form identifiers now and
     ENT-6687 later turns on cross-region free-form, a region-local value could collide
     with a cross-region one — or with an existing enum value. So the format check should
     at minimum reject anything equal to an existing `Portfolio.Identifier`, and I'd like
     us to settle the reserved-namespace convention (or an explicit "these are migratable,
     here's how" note) as part of this slice rather than after. Keep it lightweight —
     these are staff-minted, mostly passive tags.
  2. Harden before (or with) the relax, and re-confirm the inventory. Relaxing `clean()`
     without the call-site hardening lets a free-form value reach the unguarded coercion
     sites and crash. Heads up: the surface is smaller than ENT-6687's audit suggests — a
     fresh read has populate_demo_data_plan and rollout_recipe as the only genuinely
     unguarded sites; portfolio_hotels / apply_portfolio_settings / user_assignment_operation
     / onetime_ihg already try/except, and authorize.py (the load-bearing one) is guarded.
     Worth re-confirming during impl rather than trusting either count.

  While we're in there: the admin create-from-scratch path already writes unvalidated
  identifiers via `get_or_create` (skips `full_clean`), so today one path is validated and
  one isn't. Route it through the same format-check clean() to close that gap in the same
  pass.

  Go for it.
  ---

  NEXT STEP FOR GARETH: approve/edit the draft above, then I (or you) post it as a comment
  on ENT-6604. I did not post anything — external writes need explicit approval.
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-6604/decouple-portfolioidentifier-from-the-hard-coded-enum-table-backed
tags:
- morning-gtd
- linear
time_minutes: 15
title: 'Respond on ENT-6604: decouple Portfolio.identifier — rrogers proposes splitting'
updated: 2026-06-30 15:43:42.256224
waiting_on: null
waiting_since: null
working_on: false
---

rrogers: region-local slice is low risk + separable; near-term need is staff-minted identifiers. Wants your view on splitting. https://linear.app/canary-technologies/issue/ENT-6604/decouple-portfolioidentifier-from-the-hard-coded-enum-table-backed