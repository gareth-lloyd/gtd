---
area: null
completed_at: 2026-10-28 14:50:47.873396
contexts:
- react
created: 2026-10-28 11:10:00.725749
defer_until: null
due: null
energy: medium
id: 2026-10-28T1110-fix-ci-on-pr-51747-rebase-on-master-james-morton-s
order: null
output: |
  ## Agent run 2026-10-28 14:43:45.115383

  No rebase needed. Master had already been merged into the branch at 11:43 today (commit 2e7f80e79f, by you), and that brought in James's dependency fix.
  PR #51747 (https://github.com/canary-technologies-corp/canary/pull/51747), checks on the head commit:
  - `make test-backend`: SUCCESS (this was the failure in the task).
  - Backend linters, translations and Playwright critical tests: SUCCESS.
  - The only red check is **Birdline policy** (https://github.com/canary-technologies-corp/canary/runs/122795643472). It is red because the PR needs approvals: 0 of 1 from anyone but the author, and 0 of 1 from `@engineering`. Birdline says this check "is not a gate".
  - The PR has no reviews yet. Review is requested from pod-enterprise and abrad.

  The branch is now 2 commits behind master. It does not need another merge.

  Next step (yours): get an approval from pod-enterprise or abrad, then comment `/merge`. I did not push, comment or ping anyone.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/51747
tags:
- morning-gtd
- github
- resurfaced
time_minutes: 20
title: 'Fix CI on PR #51747: rebase on master (James Morton''s dependency fix has
  merged)'
updated: 2026-10-28 14:50:47.873387
waiting_on: null
waiting_since: null
working_on: false
---

Resurfaced: archived 2026-10-21 as `2026-10-21T0950-fix-ci-on-pr-51747-remove-pci-sso-re-authenticatio`, but new activity at the source since then.

[ENT-2604] Remove PCI SSO re-authentication org exceptions (Wyndham/BW). Canary Backend Tests are failing after a dependency bump. James says his fix has merged and a rebase on master should clear it.
https://github.com/canary-technologies-corp/canary/pull/51747