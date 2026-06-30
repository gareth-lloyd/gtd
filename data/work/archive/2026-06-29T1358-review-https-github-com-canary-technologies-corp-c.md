---
area: null
contexts: []
created: 2026-06-29 13:58:32.503829
defer_until: null
due: null
energy: low
id: 2026-06-29T1358-review-https-github-com-canary-technologies-corp-c
order: null
output: |
  ## Agent run 2026-06-29T14:15 — Review of PR #48870

  PR: [ENT-6602] Add nullable portfolio_identifier attr + GSI to applications; dual-write
  https://github.com/canary-technologies-corp/canary/pull/48870
  Author: Ryan Rogers (rrgrs) · base master · OPEN · +100/-2, 6 files

  ### Verdict: APPROVE — clean, well-scoped, correct. No blocking issues.

  Small, surgical, mirrors the existing portfolio_uuid pattern field-for-field. Tests are
  meaningful. Backward-compatible across the shared boundary. Findings below are minor / FYI only.

  ### What it does
  Adds a nullable `portfolio_identifier` (e.g. `WYNDHAM_STAGING`) to the global `applications`
  DynamoDB record + a `portfolio_identifier-created_at-index` GSI, and dual-writes it alongside
  the region-local `portfolio_uuid` in `ApplicationService.create`. Identifier is consistent
  across regions/envs; uuid is not. Prerequisite for backfill (ENT-6605) and eventual read/authz
  switch. Adds selector `list_applications_by_portfolio_identifier`.

  ### Correctness checks (all pass)
  - `_application_from_record` / `_application_to_record` both map the new field. ✓
  - `update()` preserves `portfolio_identifier` (same guarantee portfolio_uuid had — a name/status
    edit won't drop the row from the new GSI). ✓
  - Field ordering valid: `Application` dataclass and `ApplicationRecord` msgspec struct both put
    the new defaulted field after the no-default `portfolio_uuid` / before `oauth_redirect_url`. ✓
  - Backward compatible: nullable w/ default None, so decoding old rows (no attr) and routing-service
    reading the shared struct both work without lockstep deploy. ✓
  - GSI is sparse — rows without the attr simply aren't indexed ("identifier-less for now"), intended. ✓
  - HTTP caller (api_gateway/views/application_collection.py:74) and provision_with_credentials
    intentionally do NOT pass portfolio_identifier — correctly deferred to ENT-6641. ✓
  - Type stays `str | None` end-to-end (no UUID conversion), consistent. ✓

  ### Deploy ordering — noted, but low risk (NOT blocking)
  Companion prod-GSI PR: canary-kubernetes #3408 (https://github.com/canary-technologies-corp/canary-kubernetes/pull/3408).
  PR body says it "should deploy before/with this." Analyzed the failure modes:
  - If this Python PR ships first w/o the GSI: writes of the attribute still SUCCEED (DynamoDB
    doesn't require an attr to be indexed). When the GSI is later created, DynamoDB backfills
    existing items carrying the attr — no data loss in the gap.
  - The only thing that errors before the GSI exists is QUERYING it (the new selector) — and nothing
    calls the selector yet. So ordering is a "nice to have," not a hard dependency. Reassuring.

  ### Minor notes (FYI, author's discretion — none blocking)
  1. PR body claims tests cover "update-preservation," but there is no test that sets a non-None
     `portfolio_identifier` on the stub, runs an update, and asserts the saved record kept it.
     `_record_stub` gained the param but no update test exercises it. (Same gap exists historically
     for portfolio_uuid, so it's consistent — just slightly overstated in the description.) A one-line
     assert in an existing test_update_* would close it.
  2. Localstack `dynamodb.sh` uses `create-table ... || true` for idempotency; with PERSISTENCE=1
     the table already exists so create-table is a no-op and the new GSI won't be added until a dev
     wipes localstack state. Standard footgun for any GSI addition to localstack; worth a heads-up to
     the team but not a code problem.

  ### Tests
  Author reports: 122 passed (service + selector), 5 passed (bootstrap), ruff clean. Did not re-run
  locally (review-only task). Coverage added is appropriate: dual-write asserts both fields; absent
  identifier → None; selector asserts correct IndexName + empty case; round-trip preserves field.

  ### Note: review is local only. Nothing was posted to GitHub. If you want this left as a PR comment,
  say so and I'll draft the exact text for approval first.
project: null
source_id: null
tags: []
time_minutes: 5
title: review https://github.com/canary-technologies-corp/canary/pull/48870/changes
updated: 2026-06-29 14:48:32.438359
waiting_on: null
waiting_since: null
working_on: false
---