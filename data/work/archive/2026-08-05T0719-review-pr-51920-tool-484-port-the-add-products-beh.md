---
area: null
completed_at: 2026-08-05 14:58:26.089153
contexts:
- react
created: 2026-08-05 07:19:55.390606
defer_until: null
due: null
energy: medium
id: 2026-08-05T0719-review-pr-51920-tool-484-port-the-add-products-beh
order: null
output: |
  ## Agent run 2026-08-05T11:05:38Z

  Reviewed the stacked delta of PR #51920 (https://github.com/canary-technologies-corp/canary/pull/51920)
  against its base #51493 (https://github.com/canary-technologies-corp/canary/pull/51493): 3 commits,
  +227/-4 across hotel_products_plan.py, demo_hotel_products_provider.py, test_hotel_plans.py.
  Deep-compared against the source of truth OnboardingService.activate_hotel_products, plus two
  specialist agent passes (code review + test coverage). NOT posted to GitHub — findings are local only.

  VERDICT: Approve-quality port. No blocking bugs; behavior-preserving for every existing caller
  (verified: all demo configs had has_authorizations_tier_basic=False, so authorization_tier=None is a
  no-op there; the removed inline BASIC derivation is reproduced verbatim in DefaultHotelProductsProvider;
  demo provider clones via **__dict__ so new fields propagate; test stub builds fields generically).
  CI green except advisory review-bot fail. Worth raising with Ramiro before merge:

  1. (best catch) Empty-list test-emails case untested. _resolve_test_emails returns [] when the
     opportunity has no implementation_lead_email, and add products still enables test mode with [].
     The port's guard is `is not None`, so [] must flow through as distinct from None — the subtlest
     part of the port, zero coverage (all tests use ["lead@example.com"]). The milestone-5 provider is
     one `or None` away from silently dropping test-mode enablement for lead-less hotels.
     Ask: add a test with check_in_test_emails=[] asserting has_check_in_test flips True.
  2. Missing asymmetric check-in/check-out test. The happy-path test flips both products with identical
     email lists; a copy-paste cross-wiring mutant in the check_out branch (e.g. was_check_IN_enabled)
     would pass every test. One test with has_check_in=True/has_check_out=False and distinct lists
     kills the whole mutant class.
  3. has_authorizations_tier_basic is now write-only dead surface — this PR moved its only reader into
     the provider's local variable; grep confirms zero consumers of the config field. The stack's own
     last commit did exactly this cleanup for the tipping fields, so dropping it belongs here too.
  4. `if config.enable_form_template_generic_links:` uses truthiness while the dataclass docstring says
     "None means do not touch" and all three sibling fields use `is not None` — False and None are
     indistinguishable. No bug today (all providers emit None), but it collapses the tri-state.
  5. Cheap test add: assert the FormTemplate generic-links update is hotel-scoped (second hotel's
     template stays inactive) — a dropped hotel= filter would flip templates fleet-wide.
  6. PR description stale: says "all six fields" / lists tipping fields dropped by the final commit
     (macroscope bot flagged this too), says the tier is "applied after the derived basic tier
     assignment" (derivation now lives in the provider, nothing to be after), and says existing
     providers emit None for all fields (default provider derives BASIC for authorization_tier).

  Minor/no-action: config email lists are aliased onto model fields (list(...) copy would be cheap
  insurance); has_check_in_test-already-True guard untested (unusual state).

  Verified correct (pre-empting reviewer nits): was_check_in/out captured before _update_fields, matching
  add products' had_check_in comment; `hotel.has_check_in and not was_check_in_enabled` is exactly
  equivalent to the source's products_to_add test because only_set_true means live hotels only flip
  False→True; TABLET_REGISTRATION/TABLET_EFOLIO fold into has_check_in/out in the provider; AUTH_ONLY/
  PAYMENT_ONLY rules deliberately deferred to the milestone-5 provider per PR body; FormTemplate.update()
  after hotel.save() is safe (plan runs inside transaction.atomic, FormTemplate is a plain Model);
  idempotent on re-run; imports/test-style comply with CLAUDE.md.

  Suggested next action: comment on the PR with items 1-4 + 6 (drafts above are ready to adapt), or
  approve with nits. Nothing here blocks merge.
project: 2026-04-16T1210-unblock-team
source_id: https://github.com/canary-technologies-corp/canary/pull/51920
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #51920: [TOOL-484] Port the add products behaviors into the plan'
updated: 2026-08-05 14:58:26.089141
waiting_on: null
waiting_since: null
working_on: false
---

Ramiro Nieto, personally requested. Stacked on #51493 (skippable HotelProductsPlan writes).
https://github.com/canary-technologies-corp/canary/pull/51920