---
area: null
contexts: []
created: 2026-05-06 09:39:33.183729
defer_until: null
due: null
energy: low
id: 2026-05-06T0939-improve-dedupe-behavior
order: 7
output: ''
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: Improve dedupe behavior
updated: 2026-06-25 12:17:49.616303
waiting_on: null
waiting_since: null
working_on: false
---

# Plan: cycle-aware source_id for PR review items

**Goal**: each new review round on a PR gets its own dedup key, so archived "completed reviews" don't block fresh re-review work.

## Steps

1. **Add head SHA to PR breadth facts.** In `fetch_breadth.py`, the GH query that produces `kind=review_personal` / `mine_action_needed` already pulls PR metadata. Add `headRefOid` (or short SHA) to the per-PR fact dict.

2. **Suffix source_id when a new cycle is detected.** In the same fetcher, after assembling each PR item:
   - First-ever review request (`my_last_review is None`, `re_review_after_changes is False`): keep bare PR URL.
   - Re-review case (`re_review_after_changes is True`) **or** there are commits after `my_last_review`: emit `source_id = "<pr-url>#sha-<short_sha>"`.
   
   Display title/body still use the bare URL; only the dedup key carries the suffix.

3. **No changes to capture script.** Existing dedup just works — the new key won't collide with the archived bare-URL item.

4. **Verify with one real case.** Pick a PR currently in archive that has been re-pushed. Run breadth, confirm new item gets a `#sha-…` source_id and is captured.

## Open decisions

- **Suffix grammar**: `#sha-abc1234` is human-readable and debuggable. Alternative `#cycle-2` requires counting state we don't have. Pick SHA.
- **Same pattern for Linear / Slack?** Out of scope for this change. Note as follow-up: Linear could use `#comment-<latest_comment_id>`, Slack threads `#ts-<latest_reply_ts>`.

## Risk

Low. Old archived items keep bare URLs, new items get suffixed keys, no migration. Worst case: tiny commits bump the SHA and trigger re-capture for trivial pushes — acceptable cost (still debouncable by trash).

## Done when

- Breadth blob shows suffixed source_ids for at least one re-review item.
- Re-running an evening capture against that breadth creates a new inbox item even with archived predecessor present.