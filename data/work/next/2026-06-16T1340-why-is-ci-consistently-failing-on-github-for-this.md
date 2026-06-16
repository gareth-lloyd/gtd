---
area: null
contexts: []
created: 2026-06-16 13:40:04.330059
defer_until: null
due: null
energy: low
id: 2026-06-16T1340-why-is-ci-consistently-failing-on-github-for-this
order: null
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
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: why is CI consistently failing on Github for this project?
updated: 2026-06-16 13:50:00.000000
waiting_on: null
waiting_since: null
working_on: false
---