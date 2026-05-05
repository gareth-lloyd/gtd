---
area: engineering
contexts:
- deep
created: &id001 2026-05-05 11:02:00
defer_until: null
due: null
energy: medium
id: 2026-05-05T1102-gtd-wire-up-waiting-since-for-stale-flagging
order: null
project: 2026-04-16T1348-ideas
source_id: null
tags:
- gtd-meta
- backend
time_minutes: 45
title: 'GTD: wire up waiting_since for stale-flagging'
updated: *id001
waiting_on: null
waiting_since: null
working_on: false
---

**Problem.** `Item.waiting_since` is a real field in the dataclass
and is serialized to YAML, but nothing ever sets it and nothing ever
reads it. Dead plumbing on a useful signal.

**Approach.**
- In `gtd_core/service.py:move()`, when destination is
  `Bucket.WAITING`, set `waiting_since = self._now().date()` if not
  already set. When moving OUT of waiting, leave `waiting_since`
  alone (history). Cleared only on completion or explicit edit.
- Update `.claude/skills/gtd-dashboard.md` to surface counts:
  - waiting >7d
  - waiting >14d
- Update `.claude/skills/gtd-review.md` waiting-list section to
  prompt for items >7d.
- Don't backfill: items currently in `waiting/` with
  `waiting_since: null` stay null. New behaviour starts forward.

**Verification.**
- New test in `gtd_core/tests/test_service.py` covers auto-set on
  move into waiting and persistence on move out.
- Manual: move an item to waiting via the UI, confirm
  `waiting_since` populated.

**Size.** S (~45 min)