---
area: engineering
contexts: []
created: 2026-05-05 08:34:00
defer_until: null
due: null
energy: low
id: 2026-05-05T0834-surface-snapshot-push-failures-currently-silently
order: null
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 20
title: Surface snapshot push failures (currently silently swallowed)
updated: 2026-05-05 15:05:39.569523
waiting_on: null
waiting_since: null
working_on: false
---

`snapshot.snapshot()` catches `(GitCommandError, ValueError)` and sets `pushed=False` with no error message. The API view returns `{committed: true, pushed: false}` — user assumes "push deferred" when in reality push failed.

Fix: capture the exception message into `SnapshotResult.push_error: str | None` and surface it in the API response so the UI can toast "committed locally but push failed: <reason>".