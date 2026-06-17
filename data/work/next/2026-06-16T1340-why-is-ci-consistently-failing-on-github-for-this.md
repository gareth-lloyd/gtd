---
area: null
contexts: []
created: 2026-06-16 13:40:04.330059
defer_until: null
due: null
energy: low
id: 2026-06-16T1340-why-is-ci-consistently-failing-on-github-for-this
order: 19
output: |
  ## Agent run 2026-06-16T13:50

  **TL;DR:** CI fails on every push because of 5 git-related backend tests that
  assume the local branch is named `main`. They pass on your Mac (your git
  `init.defaultBranch=main`) but fail on GitHub's ubuntu-latest runner, where
  `init.defaultBranch` is unset and git defaults to `master`. It's a
  test-environment bug, not a real product regression.

  ### Evidence
  - Latest run: https://github.com/gareth-lloyd/gtd/actions/runs/27609820551 (and
    every run back through at least 2026-06-09 — all `failure`).
  - Only the `backend` job fails. `552 passed, 5 failed in 8.49s`. Failing tests:
    - test_cloud_sync.py::TestCommitAndPush::test_pushes_new_inbox_file_to_remote
    - test_cloud_sync.py::TestPullLatest::test_picks_up_remote_commit
    - test_cloud_sync.py::TestPullLatest::test_throttled_within_interval
    - test_snapshot.py::TestPull::test_applies_remote_commit_and_reports_changed
    - test_snapshot.py::TestPull::test_autostashes_local_edits
  - Two failure signatures, same root cause:
    - `git.exc.GitCommandError: ... error: src refspec main does not match any`
    - `AssertionError: assert False` on a `.../task1.md".exists()` check.

  ### Root cause
  The test fixtures do `git.Repo.init(origin, bare=True)` then only ever create
  and push a branch named `main` (`repo.git.branch("-M", "main")` /
  `push("main")`). The bare repo's HEAD symref points at
  `refs/heads/<init.defaultBranch>`:
    - On your machine that's `main` → everything lines up → tests pass.
    - On CI it's `master` → the bare repo's HEAD points at a branch that never
      gets created. Consequences:
      1. A fresh `clone_from(origin)` checks out the nonexistent default
         (`master`) → empty working tree → `.exists()` assertions fail.
      2. Secondary clones land on an unborn `master`; committing then
         `push("main")` fails with "src refspec main does not match any".

  Confirmed locally: `git config --get init.defaultBranch` → `main`. CI leaves it
  unset.

  ### Recommended fix (test-only, makes fixtures hermetic)
  Pin the bare repo's initial branch so tests don't depend on the host's git
  config. In every `git.Repo.init(<path>, bare=True)` that later receives a
  `main` branch, add `initial_branch="main"`:

      git.Repo.init(origin, bare=True, initial_branch="main")

  GitPython forwards this as `git init --initial-branch=main` (git >= 2.28; CI's
  ubuntu-latest and your 2.39 both satisfy this). Call sites to update:
    - gtd_core/tests/test_cloud_sync.py — the `remote_and_clone` fixture (~line 38).
    - gtd_core/tests/test_snapshot.py — bare inits at ~lines 44, 125, 219 (audit
      each; fix the ones whose remote gets a `main` push).

  Alternative (cheaper, but papers over the test fragility): add a step to
  .github/workflows/ci.yml before pytest:
      git config --global init.defaultBranch main
  This greens CI but leaves the tests host-config-dependent for any contributor
  whose git defaults to master, so the fixture fix above is preferable.

  ### Side note
  The `deploy` job (`needs: [backend, frontend-mobile]`) has never run because
  backend is red — so green-main auto-deploys to Render have been silently
  blocked this whole time. Fixing the tests re-enables deploys.

  I did NOT change any code — diagnosis only. Say the word and I'll apply the
  fixture fix red/green and run `uv run pytest`.

  ## Agent run 2026-06-16T14:05 — fix applied (uncommitted)

  You approved the fix. Done red/green:

  1. Reproduced the failure locally by forcing git's default branch to master
     (`GIT_CONFIG_GLOBAL` with `init.defaultBranch=master`) → same 5 failures.
  2. Applied the fixture fix: added `initial_branch="main"` to the bare
     `git.Repo.init(..., bare=True)` call in both fixtures, with a comment.
     - gtd_core/tests/test_cloud_sync.py (remote_and_clone fixture)
     - gtd_core/tests/test_snapshot.py (remote_and_clone fixture)
     Left the other bare inits untouched — test_unborn_head_with_remote... never
     pushes, and test_successful_push_clears_error uses push("HEAD") consistently
     (both default to master in CI, so they already pass).
  3. Re-ran under the simulated master default → 31 passed (was 5 failed).
  4. Full suite under normal config: `uv run ruff check .` clean,
     `uv run pytest` → 557 passed.

  **Changes are applied to the working tree but NOT committed or pushed** — that's
  your call. To ship: commit just these two test files (code commit, separate from
  any data snapshot per the repo convention), push to main, and CI should go green
  for the first time since at least 2026-06-09. That also unblocks the `deploy`
  job, so expect a Render deploy to fire on the next green main.

  ## Agent run 2026-06-16T14:20 — committed, pushed, CI surfaced a 2nd issue

  Committed the fix as bf2173eb ("Fix CI: pin initial branch to main in git test
  fixtures") and pushed to main. Triggered CI run 27613833660
  (https://github.com/gareth-lloyd/gtd/actions/runs/27613833660).

  RESULT: the test bug is FIXED — `backend` ✓ and `frontend-mobile` ✓ both pass
  for the first time since ~2026-06-09.

  BUT the run is still red, now for a *different, previously-masked* reason: the
  `deploy` job (gated on the test jobs passing, so it had never run before) fails
  at "Trigger Render deploy":
      RENDER_DEPLOY_HOOK_URL:            <- empty
      curl: (3) URL rejected: Malformed input to a URL function
      ##[error]Process completed with exit code 3
  `gh secret list` shows NO Actions secrets configured in the repo at all. The
  workflow's deploy step (.github/workflows/ci.yml:45-48) curls
  `$RENDER_DEPLOY_HOOK_URL`, which is empty → curl errors → job red.

  This is a config gap, not a code bug. Options (your call — I did not touch
  secrets or the workflow):
    1. Add the `RENDER_DEPLOY_HOOK_URL` Actions secret (Render dashboard →
       service → Settings → Deploy Hook). Then deploy goes green and main
       auto-deploys to Render.
    2. If you don't want CI-driven Render deploys, make the deploy step tolerate
       a missing hook — e.g. guard with `if: ${{ secrets.RENDER_DEPLOY_HOOK_URL
       != '' }}` or `[ -n "$RENDER_DEPLOY_HOOK_URL" ] && curl ... || echo "no
       hook configured, skipping"`.
    3. Drop the deploy job entirely if Render autoDeploy is handling it.

  Unrelated warning (non-failing): the workflow uses Node 20 actions
  (checkout@v4, setup-uv@v5, setup-node@v4) which GitHub is deprecating — worth a
  bump to current major versions at some point, but it's not why CI is red.

  ## Agent run 2026-06-16T14:35 — deploy job removed, CI fully GREEN

  Compared with the sibling project ~/projects/villacollective: it has NO deploy
  job in CI — Render handles deploys via `autoDeploy: true` + `branch: main` in
  its render.yaml; CI is purely an advisory check. gtd had the opposite
  (CI-gated deploy via a hook secret that was never set). You chose to match
  villacollective.

  Done (commit 13181b20, "CI: drop deploy job, let Render autoDeploy on main"):
    - render.yaml: `autoDeploy: false` → `true` (+ updated comment).
    - .github/workflows/ci.yml: removed the `deploy` job entirely; CI is now just
      `backend` + `frontend-mobile`.
  Pushed to main → CI run 27614414245
  (https://github.com/gareth-lloyd/gtd/actions/runs/27614414245) is GREEN.

  NOTE / action for you: `autoDeploy: true` in render.yaml only takes effect if
  the Render service reads its config from the Blueprint. If the service was
  created manually (not via Blueprint sync), also flip Auto-Deploy to "Yes" in
  the Render dashboard (service → Settings → Build & Deploy). Render will now
  deploy on EVERY push to main, including red commits — that's the tradeoff of
  this model vs. the old CI-gated one.

  Still-open (optional, not blocking): bump the Node-20 GitHub Actions to current
  majors to clear the deprecation warnings.
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: why is CI consistently failing on Github for this project?
updated: 2026-06-17 13:53:06.260581
waiting_on: null
waiting_since: null
working_on: false
---