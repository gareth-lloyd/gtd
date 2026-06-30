---
area: null
contexts:
- react
created: 2026-06-30 12:07:19.419584
defer_until: null
due: null
energy: medium
id: 2026-06-30T1207-fix-ci-on-pr-48994-ent-6664-wyndham-call-center-bo
order: null
output: |
  ## Agent run 2026-06-30T12:45 (approx)

  **Root cause:** CI on PR #48994 (https://github.com/canary-technologies-corp/canary/pull/48994)
  had exactly one real failure — the `make check-fix-lint check-fix-format` job in
  "9.CAN.AUTO Check Canary". `ruff format --check` flagged one file:
  `backend/canary/onboarding/tests/rollouts/test_rollout_service.py` (a single over-long
  `patch.dict(...)` call at ~line 470 that needed wrapping/unwrapping per ruff format).

  The "OpenAPI specs" FAILURE was NOT a real problem with the diff — it was a cascade: its
  upstream changed-files/discover jobs were CANCELLED (superseded run), and the gate script
  exits 1 when those are cancelled. The large pile of other CANCELLED checks were all from the
  superseded run, not genuine failures.

  **Fix applied:** ran `uv run ruff format` on the file (1 insertion, 3 deletions — collapsed
  the wrapped `patch.dict` onto one line). Verified `ruff format --check` and `ruff check`
  both pass on the file.

  **Pushed:** commit `63dc182854b` ("ENT-6664: ruff format test_rollout_service.py") to
  branch `glloyd/ent-6664-wyndham-call-center-booking-onboarding-design`. New CI run kicked
  off automatically (head 63dc182, 32 jobs in progress, no failures at time of writing).

  **Next:** watch the new run complete — the format job should now pass. Nothing else in the
  diff was touched. Did NOT merge (per your manual-merge preference).

  ## Agent run 2026-06-30T10:00 (follow-up: "check ci")

  After the push, the format job passed but "OpenAPI specs" failed again — this time NOT a
  superseded cascade. Root cause was **CI infra flakiness**: the "Discover OpenAPI services"
  job hung on its initial `git fetch` of the PR merge ref (started 09:35:22, killed by the
  10-minute job timeout at 09:45:17 — "The operation was canceled"). That cancellation
  cascaded into the OpenAPI specs gate (gate exits 1 when discover is cancelled). Nothing to
  do with the diff.

  **Action:** re-ran the failed jobs (`gh run rerun 28434722479 --failed`). On re-run all four
  OpenAPI jobs passed (Discover / Check changed files / staleness+stability / specs gate).

  **Final state:** PR #48994 head `63dc182854b` — all checks green, 0 running, 0 failures,
  mergeable=MERGEABLE. Still NOT merged (your call).
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/48994
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Fix CI on PR #48994: ENT-6664 Wyndham call-center booking onboarding type
  + seed'
updated: 2026-06-30 15:42:43.498853
waiting_on: null
waiting_since: null
working_on: false
---

My PR, CI failing. https://github.com/canary-technologies-corp/canary/pull/48994