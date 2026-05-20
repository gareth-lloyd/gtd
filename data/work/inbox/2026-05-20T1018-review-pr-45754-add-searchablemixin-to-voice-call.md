---
area: null
contexts:
- react
created: 2026-05-20 10:18:44.715505
defer_until: null
due: null
energy: medium
id: 2026-05-20T1018-review-pr-45754-add-searchablemixin-to-voice-call
order: null
output: |
  ## Agent run 2026-05-20T12:00Z

  **Verdict: LGTM — safe to merge as-is.** Already approved by stephenreddek; no failing checks.

  ### What the PR does
  - Mixes `SearchableMixin` into `voice.Call`, adding nullable `search_text` (TextField) and `search_vector` (SearchVectorField).
  - Plain atomic `AddField` migration `0132_call_search_text_call_search_vector`, deps `voice.0131_forward_number_call_center`.
  - 3 unit tests: field attachment (TextField / SearchVectorField) + defaults to None on stubbed instance.

  ### Verification I did
  - Diffed migration against `check_out/0068_checkout_search_text_checkout_search_vector.py` precedent — byte-for-byte equivalent shape (two `AddField`s, both nullable, no index, no backfill). Same pattern also used by guest/0128, hotels/0573, reservations/0160.
  - Confirmed `SearchableMixin` is abstract (`backend/shared/shared/models/searchable_mixin.py:11-27`), and `TimeStampedModel` is also abstract `models.Model` — MRO `(TimeStampedModel, SearchableMixin)` has no conflict.
  - GIN index intentionally deferred (PR body says "no GIN index, no backfill, no callers yet"). Mixin docstring flags `SEARCHABLE_BASIC_INDEX = GinIndex(fields=["search_vector"])` with `AddIndexConcurrently` for the follow-up.

  ### Notes for the follow-up PRs (not blockers here)
  - Land the `AddIndexConcurrently` GIN index BEFORE any backfill begins, otherwise large writes will scan sequentially.
  - When the populate/backfill logic lands, consider whether `Call.save()` (or a signal) should refresh `search_vector` on update, or whether it's recomputed in batch — worth being explicit in that PR.
  - No callers/populate yet, so blast radius this slice = nil (two new nullable columns on `voice_call`).

  ### CI
  - All required checks pass; the long list of "skipping" checks are the standard PR-too-small / no-coverage-impact auto-skips. No failures.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/45754
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #45754: Add SearchableMixin to voice.Call'
updated: 2026-05-20 12:00:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

Andres Figueira (andres/ent-6216-1a-add-searchablemixin-fields-to-call). Already approved by stephenreddek. https://github.com/canary-technologies-corp/canary/pull/45754