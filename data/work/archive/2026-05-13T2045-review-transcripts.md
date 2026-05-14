---
area: management
contexts: []
created: 2026-05-13 20:45:37.001973
defer_until: null
due: 2026-05-14
energy: medium
id: 2026-05-13T2045-review-transcripts
order: -18
output: '## Agent run 2026-05-14T12:35Z


  Reviewed the "Above Property Call Transcripts" design doc (ENT-5913).

  Notion: https://www.notion.so/canarytechnologies/Above-Property-Call-Transcripts-35881468615180efa569db321c85aa3b

  Status in Notion: TODO. Test plan property is empty. Linear Project / Linear Ticket
  properties are unset on the page even though the Linear ticket is linked inline.


  ### Overall

  Solid, thorough doc. Architecture diagram + frontend change map are clear. Scope
  guards are explicit. Two-tier permission (TRANSCRIPT_ACCESS vs RECORDING_ACCESS)
  is the right call. Phased rollout (canary → Wyndham → others) with 7-day soak per
  step is conservative and appropriate for a compliance-adjacent surface.


  ### Questions worth raising in review

  1. **Search-without-audit is a defensible position but needs an explicit compliance
  sign-off.** "Audit fires on row-open, not on search" — but search filters themselves
  can leak info (e.g., filtering by guest_name returns hotels that guest stayed in).
  For Wyndham this could matter. Worth confirming with Sec/Compliance, not just asserting.

  2. **PCI redaction backfill.** Doc covers `redact: pci` on Deepgram ingest going
  forward but is silent on historical transcripts. If Wyndham searches a 90-day window
  at launch, those transcripts pre-date the redaction pass. Either a re-ingest plan
  or an explicit acknowledgement that v1 has unredacted historical content (and that
  the launch cohort is OK with that).

  3. **Recording URL TTL (3600s JWT + 300s S3 presign).** 1-hour JWT feels long for
  an investigative surface where URLs are minted lazily on play/download. Easy accidental-share
  window. Consider 300–600s JWT.

  4. **No audit on download completion** — flagged as a v1 gap. Users can mint many
  URLs without downloading. For compliance posture this is the meaningful event. Worth
  either filing a follow-up ticket explicitly or moving the audit hook into `FileDownloadView`
  before launch.

  5. **US-only filter is silent.** `accessible_hotel_count` exists but there''s no
  signal that non-US hotels in the portfolio were excluded. UX risk: AP admin thinks
  portfolio has 30 hotels, sees 12 in dropdown, no explanation. Either a banner or
  an `excluded_hotel_count` field.

  6. **Phone-prefix normalization.** Doc notes the issue but doesn''t specify the
  normalization pass during search_vector population. Existing rows may have inconsistent
  formats. Recommend including the normalization in the backfill `refresh_call_search_vectors`
  task and explicitly testing prefix matches against formatted-vs-E.164 stored values.

  7. **`duration_seconds_min/max` filters on `ended_at - started_at` (unindexed expression).**
  On large windows this will be a post-filter scan. Either accept the cost (probably
  fine — keyset cursor on `started_at` already bounds it) or add a generated column.
  Worth explicitly choosing.

  8. **Cursor invalidation.** Keyset cursor encodes `started_at` + `id`. What happens
  when filters change mid-pagination? Doc doesn''t say. Usually fine (the cursor still
  decodes), but worth defining: does FE drop the cursor on any filter change?

  9. **`text_search` min_length=2.** Low for FTS — confirm stopword stripping is on
  the search vector config, otherwise `is`, `to`, etc. return everything.

  10. **`UserPortfolioHotel` re-derived per request.** Good for security but cost
  matters on large Wyndham portfolios. Worth a quick query plan / benchmark before
  flag flip — already implied by the "EXPLAIN ANALYZE Wyndham-sized" gate but call
  it out as a measure to record.

  11. **GrowthBook `portfolio_public_identifier` attribute.** New `BaseFeatures` context
  extension — make sure existing hotel-targeted flags don''t accidentally evaluate
  this attribute in a way that changes behavior. Probably zero risk but worth a unit
  test.

  12. **`forwarding_category` denormalization.** Denormalized from `ForwardNumber.Category`.
  What''s the stale-data behavior — what if the forward number''s category is reclassified
  post-call? Doc should say "snapshotted at call time" or similar.


  ### Minor nits

  - `accessible_hotel_count` in the `pagination` block is semantically not pagination
  metadata — consider a sibling top-level field.

  - "Tab visibility" is gated on transcript permission — confirm the router-level
  gate uses the same permission check, not a duplicated literal.

  - Open Q #1 (audit retention) is "pre-launch" but has no named owner aside from
  "event-platform team + Sec/Compliance". Needs a single accountable name before flag
  flip.

  - Open Q #2 (canary-internal portfolio for smoke test) is concrete and should be
  resolvable quickly.


  ### What''s missing

  - **Test plan** property in the Notion page is empty. For a surface this size (6
  endpoints, new permission model, new FTS path, new FE route + 7 components) the
  doc should at least list the test categories before merge.

  - **Latency SLO for search.** Failure-signals section has 5xx and audit DLQ but
  no p95 latency threshold for `POST /search`. Worth setting before launch.


  ### Did NOT do (awaiting explicit approval)

  - Did not post review comments to Notion.

  - Did not file Linear follow-up tickets for the v1 gaps (download-completion audit,
  PCI backfill).

  - Did not change the doc''s TODO status.


  Recommend: paste questions 1–4 + the test plan/SLO gaps into the design review meeting
  or as a Notion comment thread, and pick up 5–12 in async review.


  ### Follow-up: portfolio-scoped sibling endpoints (history check)

  Author originally proposed reusing the per-hotel detail/transcript endpoints (carried
  in the "Previous Comments" toggle). Reviewer (user 4721bcff, 2026-05-07) flagged
  the permission-model mismatch: per-hotel `VoiceProductAuth` is hotel-scoped product
  access, but a portfolio viewer may have portfolio-tier voice access without per-hotel
  product access. Author pivoted to the current sibling-endpoints design with `PortfolioVoiceTranscriptAuth`
  / `PortfolioVoiceRecordingAuth`. Pivot is defensible — bending `VoiceProductAuth`
  to span both would conflate boundaries.


  Two cleanup asks:

  - Lift one sentence of "why we didn''t reuse" into §3 above the sibling-endpoints
  table. Right now the rationale lives only in a Notion discussion + the Previous
  Comments toggle; a cold reader of the current doc won''t see the tradeoff.

  - Resolve the reviewer''s unresolved discussion thread with a pointer to the new
  sibling structure so it doesn''t look like an open objection.

  '
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 15
title: review transcripts
updated: 2026-05-14 13:31:59.016069
waiting_on: null
waiting_since: null
working_on: false
---

https://www.notion.so/canarytechnologies/Above-Property-Call-Transcripts-35881468615180efa569db321c85aa3b?source=copy_link