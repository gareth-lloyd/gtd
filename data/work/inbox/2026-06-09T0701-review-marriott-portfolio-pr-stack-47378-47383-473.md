---
area: null
contexts:
- react
created: 2026-06-09 07:01:12.557049
defer_until: null
due: null
energy: medium
id: 2026-06-09T0701-review-marriott-portfolio-pr-stack-47378-47383-473
order: null
output: |
  ## Agent run 2026-06-09T11:45

  Reviewed the ENT-6293 stack (all by abrad, stacked on andrea/ent-6293-marriott-portfolio-identifier).
  Read each diff plus the touched source: portfolio.py model, membership_level_new.py
  (PORTFOLIO_TO_LOYALTY_PROGRAM_IDENTIFIER_MAP + get_program_identifier_for_hotel),
  PortfolioService.add_hotels, and CanaryBaseCommand.

  VERDICT: All three are sound and well-scoped. No blockers. Safe to approve once a human
  approval is added (the "review-bot fail" check is just the review-approvals gate — REVIEW_REQUIRED,
  not a code defect; the underlying job shows success). CI checks otherwise show "skipping"
  (merge-queue style — they run on enqueue). Author flagged DB tests weren't run locally (no
  Docker); rely on CI.

  --- PR #47378 (add MARRIOTT identifier) — APPROVE ---
  - One-line enum add `MARRIOTT = "marriott"`. Correct that no migration is needed: the `identifier`
    CharField declares no `choices=`, so the enum member doesn't alter the schema (verified in
    portfolio.py:108-113). Unique partial constraint on identifier means only one portfolio can
    hold "marriott".
  - Value "marriott" is distinct from existing MVW ("MVW", Marriott Vacation Worldwide) and the
    marriott_* members. Good.

  --- PR #47383 (map generic MARRIOTT → Marriott loyalty) — APPROVE ---
  - Adds map entry priority=1, matching the existing marriott_upsells/kiosk/demo entries (all → MARRIOTT, prio 1).
  - Confirmed resolution logic (get_program_identifier_for_hotel, membership_level_new.py:979) reads
    DIRECTLY-attached portfolios with no parent walk and takes max priority — so PR2 is what activates
    loyalty for hotels placed directly in the generic portfolio. PR body's claim is accurate.
  - If a hotel is in both the generic MARRIOTT and a marriott_* portfolio, both resolve to MARRIOTT
    (prio tie) — no behaviour change. Tests cover both the resolver case and the map entry.
  - Minor (non-blocking): generic MARRIOTT is not added to PUBLIC_PORTFOLIO_IDENTIFIERS (only
    MARRIOTT_DEMO is). If the canonical Marriott portfolio should expose membership to end users /
    Growthbook targeting, that's a follow-up — likely intentionally out of scope here.

  --- PR #47384 (wire_marriott_portfolio command) — APPROVE with notes ---
  Logic is correct and idempotent: dry-run default, --commit gates writes, atomic transaction,
  re-parents only when needed, backfills only missing hotels via PortfolioService.add_hotels
  (preserves role/SSO side effects — matches the repo rule to never touch PortfolioHotel directly).
  Parent-is-root guard is good. Tests cover wiring, idempotency, no-write-without-commit, missing-id no-op.

  Notes worth raising with the author (none blocking):
  1. WEAK TARGET GUARD: the command only checks the target is a root (parent_id is None). It does NOT
     check the target's identifier is blank or already "marriott". Running with a wrong --portfolio_id
     pointing at some other root portfolio would re-parent all three marriott_* portfolios under it and
     backfill their hotels — with `will_assign_identifier=False` in the plan. Dry-run output would
     reveal this (operator must read the plan), but a defensive guard (`assert parent.identifier in
     (None, MARRIOTT)` else error) would make the wrong-id case fail loud. Recommend adding it.
  2. PARTIAL STATE on the skip-child-with-children guard: if a marriott_* child has its own children
     it is skipped for re-parenting (good, avoids 3-level hierarchy), BUT its hotels are still
     backfilled into the parent (missing_hotel_ids is computed over ALL children up front). Result:
     that child stays a root while its hotels also land in the parent — not a true parent/child link.
     Harmless in practice (marriott_* portfolios are unlikely to have children) but inconsistent;
     worth a one-line comment or excluding such children from the hotel union too.
  3. add_arguments() override does not call super(), so the base --uptime-heartbeat-id/-token args are
     dropped and handle() doesn't report_heartbeat. --commit still works (added in create_parser).
     Fine for a one-shot manual command, but diverges from the CanaryBaseCommand convention.
  4. SSO-mismatch is a real run-time failure mode: add_hotels calls validate_hotel_sso_compatibility
     per hotel; if any marriott_* hotel's SSO org differs from the parent's linked org it raises and
     the whole atomic block rolls back. Dry-run won't surface this (add_hotels isn't called). Operator
     should be ready for it. Loyalty resolution itself is unaffected by the backfill (every union hotel
     already resolves to MARRIOTT via its marriott_* membership), and the 1-day in-proc
     HOTEL_PROGRAM_IDENTIFIER_CACHE staleness is therefore benign.

  CONTEXT FLAG (not a code issue): ENT-6293 originated from ONE hotel (San Francisco Proper, InforHMS)
  asking to embed Marriott Bonvoy — the ticket says "This is one hotel asking, not the whole group."
  This stack builds generic Marriott-portfolio infrastructure (canonical loyalty parent + wiring
  command). Worth confirming with abrad that the broader infra is the intended scope vs. the
  single-hotel ask, so the ticket/scope stay aligned.

  No external writes made. No PR comments posted (drafted findings above for your call on whether to
  relay to abrad).
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/47378
tags:
- morning-gtd
- github
- from-awareness
time_minutes: 40
title: 'Review Marriott portfolio PR stack: #47378 → #47383 → #47384 (abrad)'
updated: 2026-06-09 11:45:36.058618
waiting_on: null
waiting_since: null
working_on: false
---

Stacked series — generic Marriott portfolio identifier (47378), map to Marriott loyalty program (47383), wire_marriott_portfolio command (47384). https://github.com/canary-technologies-corp/canary/pull/47378