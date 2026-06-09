---
area: null
contexts: []
created: 2026-06-09 00:14:34.219929
defer_until: null
due: null
energy: low
id: 2026-06-09T0014-reviews-for-jordan
order: null
output: |
  ## Agent run 2026-06-09T00:16:49

  Jordan's Slack ask (C047K6WSUJY): review 3 stacked PRs for the new OAuth-grants
  admin API. All by jordan-canary, all touching api_gateway. Reviewed full diffs +
  cross-checked branches. NOTHING posted to GitHub/Slack — findings are for you to
  relay/post as you see fit.

  Stack shape:
  - #47213 [ENT-6407] GET /v1/oauth-grants/<sid>      base: master      (foundation)
  - #47286 [ENT-6409] GET /v1/oauth-grants (list)     base: ENT-6407
  - #47279 [ENT-6406] DELETE grant + route move       base: ENT-6407

  ### BLOCKER — the two leaf PRs disagree on the detail route
  #47286 and #47279 are *both* stacked on ENT-6407 but diverge on the URL:
  - #47286 keeps the detail route at `v1/oauth-grants/<sid>` and adds the list at
    `v1/oauth-grants`.
  - #47279 *moves* the detail route to `v1/oauth/tokens/<sid>` (and hangs DELETE off it).
  Consequences:
  1. Guaranteed merge conflict in `urls.py` + `views/oauth_grants.py` (both edit the
     same `oauth_grant_detail` lines).
  2. Worse, a semantic split if both land: list at `/v1/oauth-grants`, detail+delete
     at `/v1/oauth/tokens/<sid>`. The admin UI navigates to an `og_*` ref expecting
     one path root.
  3. #47279's move contradicts its own ticket — ENT-6406 is titled
     "DELETE /v1/oauth-grants/<sid>" (matches the Slack post), not /v1/oauth/tokens.
  Recommendation to Jordan: drop the route move from #47279. Keep everything under
  `v1/oauth-grants*` (consistent with #47213, #47286, and all three tickets). The
  move buys nothing — there's no collision; `v1/oauth/tokens` (POST exchange),
  `v1/oauth-grants` (list), `v1/oauth-grants/<sid>` (detail/delete) are all distinct.
  Putting the grant under the token-exchange path is actually *more* confusing.

  ### #47213 [ENT-6407] GET detail — LGTM, merge first
  - Cleanly relocates redaction from `OAuthGrant.redacted()` (model) to
    `OAuthGrantDetailResponse.from_grant` (serializer); drops the now-dead sentinel
    constants + TestRedacted. Redaction semantics preserved (authz hmac -> "redacted"
    always; refresh hmac -> "redacted" if exchanged else null). Tests assert the real
    at-rest hashes never hit the wire. Good.
  - InternalServiceGatekeeper (v2) instead of the ticket's v1 validator — correctly
    justified (v1 import linter + Request Framework mandate). Fine.
  - 404 on malformed/missing sid, 401 before lookup for non-internal callers (no
    enumeration). Solid. This is the foundation; merge it first, retarget the leaves.

  ### #47286 [ENT-6409] GET list — strong, two things to confirm
  - Nice DRY: extracts `parse_limit` into shared cursor_pagination_schema and
    refactors device_mfas.py onto it (old MAX_LIST_LIMIT=1000 -> MAX_PAGE_LIMIT=1000,
    behaviour identical). 28 tests, GSI query newest-first, opaque base64 cursor at
    the HTTP boundary, required identity_sid -> 400 (no "list all"). Clean.
  - CONFIRM (deploy ordering): query uses GSI `identity_sid_created_at_index`. The
    name constant is present on the branch, but the actual GSI provisioning is
    ENT-6408's job. This endpoint must not go live before that GSI exists in DynamoDB
    or every list call 500s. Worth a one-line confirmation from Jordan that 6408 is
    merged/deployed ahead of 6409.
  - MINOR: a cursor from identity A's page passed to identity B's query would make
    DynamoDB reject ExclusiveStartKey (-> 500, not 400). Cursors are opaque/internal
    so low risk, but worth a note.

  ### #47279 [ENT-6406] DELETE — route move aside (see blocker), two notes
  - Hard-delete, idempotent 204-even-if-gone (deliberately unlike
    ApplicationSecretDetailView's 404). Reasonable, well-documented; idempotent DELETE
    is RESTful. Selector/service/view layering + tests are clean.
  - DOCSTRING INACCURACY (worth fixing): service docstring says "the audit trail lives
    in EventService", but there is no EventService anywhere in api_gateway/services —
    the code just does `logger.info("oauth_grant.deleted", sid=...)`. The log line
    itself is consistent with the file's existing logging convention (good), but the
    docstring overstates the guarantee. Either drop the EventService claim, or — since
    this is a security-sensitive *revoke* — decide whether a real audit trail is
    needed. Note the log only carries the sid; identity_sid/application_sid are gone
    after the delete, so post-hoc "who was revoked" isn't answerable from the log.

  ### Suggested sequence for Jordan
  1. Merge #47213 to master.
  2. Reconcile the route: strip the `v1/oauth/tokens/<sid>` move out of #47279, keep
     `v1/oauth-grants/<sid>`.
  3. Retarget #47286 and #47279 to master; resolve the (now smaller) urls.py overlap.
  4. Confirm ENT-6408 GSI is live before #47286 ships.

  No blocking correctness bugs inside any single PR — the stack-level route conflict
  is the one thing that must be resolved before merge.
project: null
source_id: null
tags: []
time_minutes: 5
title: reviews for jordan
updated: 2026-06-09 11:37:38.961216
waiting_on: null
waiting_since: null
working_on: true
---

https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1780950221959999