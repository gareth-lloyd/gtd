---
area: null
completed_at: 2026-10-27 13:27:16.183365
contexts:
- autopilot
created: 2026-10-27 05:36:42.629285
defer_until: null
due: null
energy: low
id: 2026-10-27T0536-resolve-merge-conflict-on-pr-59781-ent-7806-fix-ov
order: null
output: |
  ## Agent run 2026-10-27T06:34Z

  Merged origin/master into glloyd/ent-7806-payments and pushed merge commit b14e94f5225.
  PR #59781 (https://github.com/canary-technologies-corp/canary/pull/59781) is now MERGEABLE (state BLOCKED, as expected for a draft/pending CI).

  - Conflict: adyen_client/client.py `charge()`. Master's PAY-3230/PAY-3232 (Google/Apple Pay via Adyen, #60195/#61089) removed `assert payment_method.card` and made billingAddress conditional (wallet card rows have no address). Kept master's logic, kept the PR's `data: dict[str, object]` annotation.
  - Master also brought 3 new no-matching-overload errors in that file (`data.update(self._three_ds_request_data(...))` on unannotated dicts, lines ~109/459/587). Since this PR removes the pyproject ignore for the file, CI would have failed; annotated those three `data` dicts as `dict[str, object]`, matching the PR's existing fix pattern.
  - Verified: pyrefly on all 7 PR files: 0 errors. ruff check/format clean.
  - Not verified locally: pytest (borrowed main venv double-registers shared plugins in the worktree). Change is annotation-only; watch CI.
  - Merge commit has the default message (no Co-Authored-By trailer).
  - Worktree left at /Users/garethlloyd/projects/canary-ent-7806-payments (remove with `git worktree remove` when done).
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/59781
tags:
- morning-gtd
- github
time_minutes: 15
title: 'Resolve merge conflict on PR #59781: [ENT-7806] Fix overload type errors:
  payments'
updated: 2026-10-27 13:27:16.183355
waiting_on: null
waiting_since: null
working_on: false
---

Draft, CI green, merge conflict.
https://github.com/canary-technologies-corp/canary/pull/59781