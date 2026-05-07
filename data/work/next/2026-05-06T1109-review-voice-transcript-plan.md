---
area: null
contexts: []
created: 2026-05-06 11:09:49.710284
defer_until: null
due: null
energy: low
id: 2026-05-06T1109-review-voice-transcript-plan
order: 5
output: |
  ## Agent run 2026-05-07T14:35

  Reviewed Andres's design for **Above-Property Call Search** (ENT-5913, "design complete; ready for review"). New "Call Search" tab in the AP dashboard letting portfolio admins search calls across all hotels in a portfolio. v1 = Wyndham, US-only. Read-only over existing voice infra (Deepgram-redacted transcripts in PG `voice_call`, recordings in S3). Single new endpoint `POST /api/voice/portfolios/<uuid>/calls/search`, two new permission constants (transcript / recording), one new audit table `CallAccessLog`, three new composite indexes on `voice_call`. Frontend reuses per-hotel components; new `PortfolioCallSearch.vue` shell.

  ### Top review comments to send Andres

  1. **`text_search` is under-specified — and at portfolio scale it likely needs `pg_trgm`.** The doc says it searches "summary + caller info" but doesn't pin the SQL operator. The new composite indexes are `(hotel_id, started_at, id)` and `text_pattern_ops` for phone fields — neither helps `ILIKE %term%` against summaries. Wyndham at scale will table-scan within each hotel partition. Either spec the operator + add a trigram GIN index, or restrict text search to prefix-only and say so in the schema.

  2. **Synchronous fail-closed audit on the hot read path is load-bearing — confirm the operational plan.** Every detail/transcript/recording fetch writes a `CallAccessLog` row in the same tx; insert failure → 5xx + no data. Strong PCI/SOC2 story, but it ties read availability to write health of a monotonically-growing log. Want to see: (a) partitioning strategy from day one (BIGSERIAL with no partitioning + 1y hot retention is a pain to retrofit), (b) bound on per-modal-open writes (does opening detail → transcript tab → recording tab fire 3 audit rows for one user action?), (c) what the Datadog alert thresholds will be for the audit insert path itself.

  3. **Search enumeration is unlogged.** Only row-opens write `CallAccessLog`; the 5σ alert is on `RECORDING_URL_ISSUED`. A bad actor with `PORTFOLIO_HAS_VOICE_TRANSCRIPT_ACCESS` who only reads summary previews from the search response is invisible. Worth at minimum a sampled/aggregated `SEARCH_EXECUTED` row, or a one-line risk-accept in the doc.

  4. **Per-hotel detail endpoint reuse by `hotel_slug` needs an explicit endpoint audit.** Detail/transcript reuse the existing `/api/voice/<hotel_slug>/calls/<uuid>/...` endpoints, gated by "the central scope helper". Asserted, not demonstrated. I'd want a list in the doc enumerating every existing per-hotel voice endpoint these portfolio users will hit and confirming each is converted to `CallSelector.get_call_for_user_in_portfolio`. Easy to miss one and have an existing endpoint bypass the new portfolio-scope check.

  5. **Phone prefix index assumes normalized storage.** `text_pattern_ops` on `from_number` and `forwarding_destination_number` only works as a prefix index if storage is canonicalised (E.164, no spaces). We have a known issue with spaces in `sms_phone` breaking Twilio lookups — confirm the same isn't true here, or note the normalization step. Otherwise prefix search will silently miss calls.

  ### Smaller flags

  - **Worst-case post-revoke window ~66 min** (60s flag cache + 3600s JWT + 300s S3 presign). Acknowledged in the doc; fine, but flag it explicitly to Security in case PCI evidence requires shorter.
  - **`CompletedList.vue` 4→5 column refactor** is a shared component used by the per-hotel page. Regression risk on the existing front-desk Calls UI — explicit visual review checklist or screenshot test before merge.
  - **`CallDetailsModal.vue` adds a 3rd "Recording" tab** to a shared component — same regression-surface point.
  - **`download_filename` validation rules unstated.** Server generates `{hotel_slug}-{call_uuid}.mp3` (good), but the JWT claim flows into S3 `ResponseContentDisposition`. Want the validation rules in the doc to rule out header-injection.
  - **404 (flag off) vs 403 (no permission) is a tiny info leak.** Probably fine; acknowledge.
  - **`accessible_hotel_count` envelope** — confirm it's computed from the same membership query that scopes the search, otherwise two calls can disagree.

  ### Things that look good (don't push back)

  - POST over GET for search (body size + no caching benefit) — correct call.
  - Keyset cursor pagination, opaque base64 of `(started_at, id)`, no `COUNT(*)`. Right shape for this access pattern.
  - Two-tier permissions (transcript vs recording) with separate audit access_types. Clean.
  - Two-hop URL pattern for audio (Canary JWT → mint S3 presign at redemption). Right pattern; matches existing `FileDownloadView`.
  - GrowthBook flag with 60s cache, smoke-test on canary-internal portfolio before Wyndham. Sensible rollout.
  - Datadog APM + 5σ baseline on `RECORDING_URL_ISSUED`. Good for the recording path; just the search-side gap noted above.

  ### Open questions Andres has called out

  - `OPEN-CALLACCESSLOG-RETENTION` — hot/cold retention policy (default 1y PG + multi-year S3 cold).
  - `OPEN-CANARY-INTERNAL-PORTFOLIO` — which portfolio runs Step 1 smoke test.

  Both are reasonable to leave open at this stage; (1) becomes urgent if comment #2 above lands and partitioning/retention need to be co-designed.

  Vercel prototype (https://above-property-call-search.vercel.app/) shows ~14k calls in the demo dataset — the FE filter set matches the design spec.

  **Recommendation:** approve with the top 5 comments raised on the doc. Comments 1, 2, 4 are the load-bearing ones; 3 and 5 are quick wins. Smaller flags can ride along.

  ## Agent run 2026-05-07T14:50 — overall shape

  Stepping back from line-level comments to assess whether the design coheres, sequences sensibly, and respects Canary conventions.

  ### Does it hang together? Mostly yes.

  Scope is proportionate: one endpoint, one audit table, two perms, three indexes, one FE shell. No new service, no search engine, no LLM, no Kafka. The whole design rests on "we already have all the data — just expose it scoped + audited," which is the right framing. Ingestion, transcription, and storage are untouched — that's the strongest signal the shape is healthy.

  ### Does the sequencing make sense? Not as written — bundled too tightly.

  The doc reads like one PR + a feature flag. In practice this should be **three discrete merges**:

  1. **Migrations only**: `CREATE INDEX CONCURRENTLY` on `voice_call` + `CallAccessLog` table. Per `docs/development-process/prs-with-model-migrations.md`, splitting these is the Canary convention. `CONCURRENTLY` on a hot, large table shouldn't ride with code.
  2. **Auth widening + `CallSelector.get_call_for_user_in_portfolio`**: the riskiest piece. Existing per-hotel `/api/voice/<hotel_slug>/...` endpoints need their auth widened to honor portfolio-level permission *before* the search endpoint exposes call UUIDs to portfolio users. This is a textbook case for the `@isolate` decorator from `shared.utils` — the doc doesn't mention it.
  3. **Search endpoint + FE**: behind the GrowthBook flag.

  Bundling them means the auth-widening regression and the new-feature regression share a rollback story. Worth pushing back on.

  ### Does it respect Canary conventions? One notable miss.

  **The bespoke `CallAccessLog` model doesn't engage with the existing event-logging substrate.** Canary has `EventService` / `EventSpec` (the `chat/events/` pattern, plus a registered `backend:event-logging` skill — confirmed in repo). Andres is proposing a parallel audit-table implementation without justifying why it isn't a new event spec. Two valid answers exist — PCI evidentiary requirements the existing log doesn't satisfy, or "Andres didn't know about the pattern." The doc needs to pick one and say so. Re-implementing audit logging is a lot of surface to maintain separately.

  Second smaller convention concern: **`CallAccessLog` partitioning is listed as an open question.** It shouldn't be. Synchronous fail-closed writes on a hot read path + 1y hot retention + un-partitioned BIGSERIAL = future-you doing a painful migration on a load-bearing PCI table. Declarative range-partition by `accessed_at` from day one. Promote from "open" to "decided."

  ### Smaller convention checks

  - If `voice_call` is `SoftDeleteModel`, the design needs to be explicit about `.objects` vs `.every` — doc is silent. (SoftDeleteModel exposes `.every / .objects / .deleted`; there is no `.all_objects`.)
  - The portfolio-membership scoping query should reuse whatever `PortfolioService` exposes as the canonical membership read, not roll its own join — same source of truth as the audit `hotel_uuid` check.
  - `frontend/hotels` SPA placement is correct (matches the AP dashboard surface).
  - msgspec `@validate_request`, POST-with-body, Vue 3.5 `script setup`, GrowthBook with `BaseFeatures`, two-hop JWT→S3-presign, 7-day burn-in, canary-internal smoke first — all aligned with existing conventions.

  ### Verdict on shape

  Architecture: approve. Push back on three shape-level items before this becomes implementation tickets:

  1. Unbundle into 3 PRs; wrap the auth-widening one in `@isolate`.
  2. Justify (or replace) bespoke `CallAccessLog` against `EventService`.
  3. Promote `CallAccessLog` partitioning from "open question" to "day-one decision."
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: review Andres's voice transcript eng design
updated: 2026-05-07 14:50:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://above-property-call-search.vercel.app/
https://www.notion.so/canarytechnologies/Above-Property-Call-Transcripts-35881468615180efa569db321c85aa3b?source=copy_link
