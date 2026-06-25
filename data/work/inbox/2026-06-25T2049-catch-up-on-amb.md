---
area: null
contexts: []
created: 2026-06-25 20:49:58.828921
defer_until: null
due: null
energy: low
id: 2026-06-25T2049-catch-up-on-amb
order: null
output: |
  ## Agent run 2026-06-25T20:07:21Z

  Caught up on Martin Rodriguez's (Linear: "Tincho Martin Rodriguez"; GitHub:
  @martinrodriguezcanary) work on the Wyndham AMB (Apple Messages for Business)
  rollout.

  ### The work lives in one Linear project
  "Define AMB Configuration Plan and Roll Out for Wyndham" (Enterprise team),
  owned by Martin. It's a phased plan: Eng design → Phase A (onboarding wiring) →
  Phase B (existing-site backfill) → Phase C (Apple inbound) → Phase E (EU). All
  ENT-65xx tickets below are his.

  ### SHIPPED (merged to master)
  - ENT-6422 Eng design — Done. Notion doc "Eng Design: AMB Rollout for Wyndham — V2".
    https://linear.app/canary-technologies/issue/ENT-6422
  - ENT-6561 A1: AMBSettings DTO + AMBConfigService.provision_amb_config — Done.
    PR #48355 MERGED 2026-06-22.
    https://github.com/canary-technologies-corp/canary/pull/48355
    https://linear.app/canary-technologies/issue/ENT-6561
  - ENT-6562 A2: AMBSettingsPlan + WyndhamAMBConfigProvider (+KNOWN_PLANS) — Done.
    PR #48360 MERGED 2026-06-23.
    https://github.com/canary-technologies-corp/canary/pull/48360
    https://linear.app/canary-technologies/issue/ENT-6562

  ### IN FLIGHT (open PRs, awaiting review — not yet shipped)
  - ENT-6563 A3: Wire AMB plan into WYNDHAM_MSA and WYNDHAM_CONNECT_PLUS onboarding —
    In Review. PR #48818 OPEN (created 6/25, +36 lines). CI green; blocked only on
    REVIEW_REQUIRED (needs a human approval).
    https://github.com/canary-technologies-corp/canary/pull/48818
    https://linear.app/canary-technologies/issue/ENT-6563
  - ENT-6564 A4: Disable AMB on deactivation / re-enable on reactivation —
    In Review. PR #48826 OPEN (created 6/25, +181/-12). Real CI checks pass; the one
    "FAILURE" is the non-blocking `review-bot` automated reviewer, not a test. Blocked
    on REVIEW_REQUIRED (needs a human approval).
    https://github.com/canary-technologies-corp/canary/pull/48826
    https://linear.app/canary-technologies/issue/ENT-6564

  ### NOT STARTED (no code yet)
  Phase B — Existing-site rollout (all status Todo, no PRs):
  - ENT-6565 B1: TargetedRollout enum + ROLLOUTS entry + recipe (one CI-atomic PR).
    Backfill recipe `enable_wyndham_amb_20260611` over ~4,761 live US Wyndham hotels.
  - ENT-6566 B2: Deactivation/rollback path (kill-switch + DISABLE recipe) — prereq to B3.
  - ENT-6567 B3: Run US backfill (staged) + monitoring.
  - ENT-6568 B4: GrowthBook default-serve true for Wyndham (dashboard change, no code).
  - ENT-6569 B5: Catch the 9 Connect-Plus-only hotels the B1 recipe misses.
  Phase C — Apple inbound (Backlog, blocked on Apple coordination):
  - ENT-6570 C1, ENT-6571 C2, ENT-6572 C3.
  Phase E — EU rollout (Backlog, deferred; E1 blocked on Apple EU business_id approval):
  - ENT-6573 E1, ENT-6574 E2.

  ### Bottom line
  Foundation (A1+A2) is merged. The two onboarding-wiring PRs (A3 #48818, A4 #48826)
  are done and just sitting in review — the only thing blocking them is a human
  reviewer. Nothing in Phase B (the actual portfolio backfill) has been written yet,
  and Phases C/E are externally blocked on Apple. So: build phase is essentially
  complete and ready to enable new onboardings once the two PRs merge; the existing-
  fleet backfill is the next chunk of real eng work and hasn't begun.

  Note: not strictly part of AMB, Martin also has unrelated open PRs in flight
  (#48621 ENT-6558 booking-gateway admin scoping, #48462 ENT-6587 Wyndham Calls UI
  gating, #47094 ENT-5449 IHG segment-flag removal) — flagging only so "his open PRs"
  aren't confused with the AMB set.

  Did not post or modify anything in Linear/GitHub (read-only).
project: null
source_id: null
tags: []
time_minutes: 5
title: Catch up on martin rodriguez's shipped and unshipped work on the wyndham amb
  rollout check linear tickets and github prs
updated: 2026-06-25 23:18:10.568151
waiting_on: null
waiting_since: null
working_on: true
---