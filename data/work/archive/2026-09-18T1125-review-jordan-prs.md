---
area: null
completed_at: 2026-09-18 14:39:39.018831
contexts: []
created: 2026-09-18 11:25:34.352371
defer_until: null
due: null
energy: low
id: 2026-09-18T1125-review-jordan-prs
order: null
output: |
  ## Agent run 2026-09-18T11:27

  Source: Jordan Sterling's review request in Slack (https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1789701041164189). Four PRs, all open, none human-reviewed yet. I read the PR descriptions, Linear tickets, file lists, and the ID-82 diff; I did not do a line-by-line review of the other three.

  ### Overall intention

  All four belong to the Linear project "identity-service" (https://linear.app/canary-technologies/project/identity-service-8053e9e4be1a), which Jordan leads: extract `api_gateway` from the monolith into the standalone identity-service, which owns global identities and powers the regional API Gateway entrypoint. The PRs are two threads of that extraction, both about the device / mobile-app (push notification) side:

  1. Make `mobile_apps` (push credentials, global Dynamo table, ~3 prod rows) region-safe, then give it an identity-service API. The rows store the regional Postgres `Portfolio.uuid`, which means nothing outside the minting region, so push-credential admin list/update/delete breaks there (push send is unaffected). The fix repeats the migration `applications` already went through (ENT-6602 to ENT-6607): key on the cross-region-stable portfolio `identifier` instead.
  2. Turn the monolith into an HTTP client of identity-service rather than calling `AuthTokenService` and friends in-process, starting with `device_gateway`.

  End state: mobile-apps and device auth data are owned by identity-service behind internal-only endpoints, the monolith reaches them only through `IdentityServiceClient`, and nothing global references a regional uuid. Downstream tickets this unblocks: ID-87 (convert push_notifications to client calls) and ID-65 (Canary admin page for mobile-apps).

  ### Per PR

  - PR #56737 (https://github.com/canary-technologies-corp/canary/pull/56737), ID-92 (https://linear.app/canary-technologies/issue/ID-92), base master, +499/-0. Expand step. Adds nullable `portfolio_identifier` to `MobileAppRecord`, dual-writes it on push-credential create, and adds a `onetime_backfill_mobile_app_portfolio_identifier` command. `portfolio_uuid` stays authoritative. The backfill is dry-run by default and reports rows whose portfolio is missing locally or has no identifier, so it doubles as the pre-flight check for ID-93.
  - PR #56772 (https://github.com/canary-technologies-corp/canary/pull/56772), ID-93, stacked on #56737, +268/-682. Contract step. Push-credential admin API takes and returns `portfolio_identifier`; auth and the portfolio scan key off it; `portfolio_uuid` and the backfill command are removed; adminland (Messaging.vue, PushCredentialSettingsModal, schemas) switches to the identifier. Merge gate stated in the PR: a clean production backfill dry run in all three regions, because any row the backfill missed becomes unreadable by the admin API.
  - PR #56775 (https://github.com/canary-technologies-corp/canary/pull/56775), ID-86 (https://linear.app/canary-technologies/issue/ID-86), stacked on #56737, +1937/-50, the big one. New identity-service endpoints `/api-gateway/v1/mobile-apps` (list/create) and `/{sid}` (read/update/delete), internal services only; `PATCH /api-gateway/v1/devices/{sid}` gains `push_token`/`push_bundle_id`; matching `IdentityServiceClient` methods for ID-87. Sid is `MobileAppSid.hash_of(provider, bundle_id)` with a conditional put, so uniqueness per pair comes from the key. Create validates `portfolio_identifier` against the portfolio registry (unknown = 400, registry failure = 500). List filters only on the two GSIs. Deploy gate: ID-101's two indexes must be ACTIVE in staging and every prod region. Deviates from the ticket on purpose: filters by `portfolio_identifier`, not the `portfolio_uuid` the ticket names.
  - PR #56736 (https://github.com/canary-technologies-corp/canary/pull/56736), ID-82 (https://linear.app/canary-technologies/issue/ID-82), base master, +260/-49. Partial conversion of `device_gateway`: only the auth-token revocation walks (enroll/revoke in `enrollment.py`, session revoke behind unplace in `session.py`) go through `IdentityServiceClient`. They now raise when identity-service is unreachable instead of reporting success. The rest stays in-process because identity-service lacks the routes (applications list lands with ID-100; identities POST refuses DEVICE references; auth-tokens POST has no `expires_at` and 404s in prod; `/authenticate` needs an application sid `resolve_device` does not have). Deploy gate: the production identity-service workload must be unpaused first.

  ### Things worth knowing before reviewing

  - Merge order matters. #56772 and #56775 both stack on #56737 and both touch `public_api_dynamo_db.py`, the selector, and `localstack-ready/dynamodb.sh`, so whichever lands second will need a rebase. #56775 makes `portfolio_uuid` optional while #56772 deletes it.
  - Three of the four carry out-of-band gates that CI cannot enforce (prod backfill dry run in three regions; ID-101 indexes ACTIVE; identity-service workload unpaused). These live only in PR prose.
  - #56736 scope is narrower than the ID-82 ticket title ("Convert device_gateway to identity-service client calls"). The PR title is honest about it, but ID-82 should not close on this alone.
  - Macroscope marked #56736 "Not approved / human required": `DevicePlacementService.unplace` (`backend/canary/hotels/services/device_gateway/placement.py:72-79`) deletes the placement and clears the label before calling `revoke_sessions`, which can now raise on a network failure. I confirmed the ordering in the code. I did not check whether callers wrap this in a transaction, which decides whether the placement delete rolls back. Worth asking Jordan.
  - #56772 removes the backfill command in the same PR that makes the identifier mandatory, so after merge there is no tool to re-run if a row was missed. With ~3 rows that is probably acceptable, but it is the reason the dry-run gate is load-bearing.
  - All four are Claude Code generated from a single session, and the tickets went In Progress to In Review in 15-25 minutes each. Descriptions are dense and accurate against what I checked, but the volume (about 2,950 added lines) has had no human review so far.
  - CI: only non-blocking Playwright E2E shards fail on all four (same `in-stay/compendium.spec.ts` failures, looks unrelated). #56772 additionally fails "Playwright Critical Tests" (1 of 50 failed); since that PR changes adminland, it needs a look rather than an assumption of flakiness. No PR has a human review.

  ### Suggested review order

  #56737 first (small, additive, unblocks the other two), then #56736 (small, independent, but resolve the unplace ordering question), then #56775 (large, additive, new surface), and #56772 last since it is the only destructive one and is gated on the prod dry run.

  ## Agent run 2026-09-18T11:39 (more context on Jordan's intentions)

  Sources: all 33 tickets in the identity-service Linear project, the repo's `backend/identity-service/docs/index.md` and `CLAUDE.md`, and the Notion page "Complete Architecture: Canary API gateway, identity and microservice authorization" (https://app.notion.com/p/3d48146861518059b5d2ec8ab79789e1, last edited 2026-09-09, unverified; I read sections 1, 8 and 9 only, not the whole 774-line page, and I do not know who wrote it). Slack search found no public discussion by Jordan about the project beyond the review request.

  ### The why, one level up

  The Notion architecture page states the target: identity-service becomes "the credential store and the token issuer", the monolith stays "the user and hotel store", and the edge is "a router and a verifier". External credentials get authenticated once at the edge by calling identity-service, and identity then crosses service boundaries as a signed, short-lived token rather than the current `Bearer id_<sid>`, which services trust because the header is present, not because anything verified it. The page lists that as gap 1 (EE-1495) and also flags (gap 12) that `/api-gateway/v1/*` is reachable on the web hostname outside the `/api/private` edge DENY.

  For that to work, identity-service has to exist as a real standalone service that owns the Dynamo identity plane, and the monolith has to stop importing `api_gateway` internals. That second part is what these four PRs are doing. Jordan is not adding product features here; he is cutting in-process dependencies one caller at a time so `api_gateway` can eventually be deleted from the monolith.

  ### The project plan, as the tickets show it

  He has run it in a consistent sequence since late August (the project was created 2026-08-31; the oldest tickets are from June):

  1. Stand up the shell: scaffold (ID-69, in progress), local dev (ID-68, done), CI/CD (ID-67, done), deploy infra (ID-66, in progress).
  2. Move shared plumbing out of the monolith: cursor pagination to `shared` (ID-63), `InternalServiceGatekeeper` to `shared` (ID-75), duplicate helpers into the service (ID-64). All done.
  3. Copy the Dynamo-plane endpoints into identity-service at the same paths (ID-80, done 2026-09-16), so the edge can move routes over one at a time while the monolith keeps serving them.
  4. Build the monolith's HTTP client with no callers (ID-81, done 2026-09-15), plus the global portfolio registry API (ID-79, done) that identity-service calls to validate a `portfolio_identifier`.
  5. Convert callers one by one to the client. Done: staff-dashboard application management (ID-83). In review: device_gateway (ID-82, PR #56736), AuthorizeHotelByApplicationPortfolio for amadeus/pms_gateway (ID-85), custom admin pages (ID-89), hotel-slug-routing handle (ID-88). In progress: create_staging_hotel (ID-84). Backlog: push_notifications (ID-87).
  6. Bigger pieces still in backlog: public-API auth validators call identity-service over HTTP to break the `rest.authenticators` / `api_gateway` import cycle (ID-76), auth-users fronted by identity-service (ID-77), re-home the app_version force-update gate (ID-90).

  ### Where the four PRs sit in that plan

  - #56736 (ID-82) is a step-5 caller conversion. It is partial because step 3 copied endpoints as they were, and those lack what device_gateway needs. ID-100 (applications list by portfolio_identifier, in review) fills one of those gaps.
  - #56775 (ID-86) is the one place the project adds API surface rather than copying it. `mobile_apps` never had api_gateway endpoints; the monolith's push_notifications code reads and writes the Dynamo table directly. To convert push_notifications (ID-87) there has to be an API first. ID-86 records a decision dated 2026-09-03 that mobile-apps stays identity-service data: global Dynamo, related only to devices/applications, no relation to monolith Postgres. An earlier attempt at the same API under an "api-gateway service" (ID-74, June) was cancelled, so this is the second framing of the idea.
  - #56737 and #56772 (ID-92/93) are a prerequisite he found along the way (tickets created 2026-09-10, a week after the rest). A service with no regional Postgres cannot resolve a regional `Portfolio.uuid`, so the record has to key on the global identifier before identity-service can own it. That is also why #56775 filters on `portfolio_identifier` despite its ticket saying `portfolio_uuid`.
  - ID-101 (the two GSIs #56775 depends on, Crossplane) was created and closed within 12 minutes on 2026-09-17. "Done" there likely means the manifest merged; whether the indexes are ACTIVE in every region is the thing the PR says to check.
  - ID-65 (admin page for mobile-apps, in review) is the consumer of #56775.

  ### Reading of his working style, relevant to reviewing

  - He is the only assignee on every ticket in the project and leads it. Nine tickets are in review at once, so review bandwidth, not authoring, is the bottleneck. The Slack ask in #epd-mobile is him looking for reviewers outside his usual pool because these touch the mobile/push surface.
  - The sequencing is careful in the expand/contract sense (copy endpoints before moving routes, client before callers, dual-write before drop). The risk is less in any single PR and more in the out-of-band gates and in stacked PRs landing out of order.
  - One unresolved design point the docs call out: identity-service's `/authenticate` returns only `identity_sid` and does not mint the signed `identity_token` the monolith's copy does, because the signing key is mounted on the monolith only. So the signed-token target from the architecture page is not something these PRs advance; they are groundwork for it.
project: null
source_id: null
tags: []
time_minutes: 5
title: Look at intent and content of Jordan's PRs. Report on the overall intention
  of his work
updated: 2026-09-18 14:39:39.018823
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1789701041164189