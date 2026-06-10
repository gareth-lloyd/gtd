---
area: null
contexts:
- react
created: 2026-06-10 11:43:19.259972
defer_until: null
due: null
energy: medium
id: 2026-06-10T1143-review-jordan-s-api-auth-pr-stack-47487-47488-4749
order: null
output: |
  ## Agent run 2026-06-10T15:12:06

  Reviewed all 6 PRs (one parallel review agent per substantive PR; #47487 reviewed
  directly). CI green on all six. Nothing posted to GitHub — verdicts below are drafts
  for Gareth to act on.

  ### Verdicts
  - #47487 route rename — APPROVE. 1-file, 3-line rename of v1/Applications* ->
    lowercase. Independently verified in the monorepo that nothing references the
    capitalized paths (only the route definitions themselves); tests reverse by name=.
    Safe, should merge first (see ordering below).
  - #47488 PATCH applications — APPROVE-WITH-NITS. Clean PATCH migration, true
    partial-update semantics, auth narrowed to InternalServiceAuthValidator, good
    tests. One real gap: ApplicationService.update has no deleted_at/status-transition
    guard, and this PR newly exposes `status` over HTTP — an internal-service caller
    can PATCH a soft-deleted app back to active (stale deleted_at left set). Guard
    lives in pre-existing update(), so fast-follow ticket is fine; suggest a test
    "PATCH status on soft-deleted app -> 4xx".
  - #47496 GET application by sid — APPROVE-WITH-NITS after rebase. Code is correct
    and secure: scope check runs before the DB read (tested that the service isn't
    called on foreign sid), response has no sensitive fields (secrets live on the
    separate ApplicationSecret entity). The merge conflict is trivial — one import
    line in test_applications.py vs #47488 (keep `UUID, uuid4`); views/applications.py
    merges cleanly. Also note it registers against the capitalized route, so it must
    rebase over #47487 for the documented lowercase path to be true.
  - #47495 admin: auth tokens — APPROVE-WITH-NITS. Mirrors the Identity admin pattern;
    token hashes never displayed (correct); no N+1. Gap: revoke calls
    AuthTokenService.delete with NO audit of who revoked (create_token logs, delete
    doesn't). Ask Jordan to log request.user + token/identity sids in the revoke view.
  - #47500 admin: app secrets — APPROVE-WITH-NITS. The critical secret-handling is
    done right: cleartext shown exactly once in the POST response only (never in URL/
    redirect/log), HTML-autoescaped, secret_hmac never in template context (asserted
    by test), service logs sids only. Same audit gap: hard-delete with no actor
    recorded.
  - #47501 admin: OAuth grants — APPROVE-WITH-NITS. HMAC redaction correct and tested.
    Three things to raise: (1) service delete() docstring claims "audit trail lives in
    EventService" but delete() never calls EventService — inaccurate claim + no actor
    logged; (2) hard-deleting a grant does NOT revoke already-issued access tokens
    (they live until their own TTL) — confirm() copy is technically accurate but an
    operator revoking a compromised grant won't cut off live API access; confirm
    intended or cascade to AuthTokens; (3) the PR description says OAuthGrant.redacted()
    "does not exist" but it DOES exist in oauth_grant_service.py — the new _redact_grant
    helper duplicates it byte-for-byte; should call grant.redacted() instead.

  ### Stack-wide themes (worth one consolidated comment to Jordan)
  - Audit logging: all three admin pages (#47495/#47500/#47501) perform destructive,
    security-sensitive actions (revoke token, revoke secret, hard-delete grant) with
    no record of the acting admin user. Consistent with the existing Identity admin
    precedent, but this stack is where the pattern becomes canonical for credentials —
    recommend actor-attributed logging (or EventService) before it spreads.
  - Permission gating: every admin action is gated only on is_staff via
    admin.site.admin_view; the sidebar perms dicts are cosmetic. Any staff user can
    mint/revoke app secrets and hard-delete grants. Matches precedent (DynamoDB-backed,
    no Django model to hang add-admin-permission on), but deserves a conscious team
    decision.
  - Merge ordering: #47487 first, then #47488, then rebase #47496 (trivial import
    conflict). Admin PRs #47495/#47500/#47501 are independent of the route PRs.

  ### Suggested next actions (user's call)
  - Approve #47487 as-is.
  - Reply to Jordan with the consolidated themes + per-PR nits (draft above); the only
    near-blocker conversation is grant-delete-vs-live-access-tokens on #47501.
  - Possible fast-follow ticket: deleted_at guard in ApplicationService.update (#47488).
project: null
source_id: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1781071671760909
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 45
title: 'Review Jordan''s API-auth PR stack (#47487, #47488, #47496, #47495, #47500,
  #47501)'
updated: 2026-06-10 16:59:03.490527
waiting_on: null
waiting_since: null
working_on: false
---

Jordan asked in #epd-enterprise for reviews on the API auth stack: route rename (#47487), PATCH applications (#47488), GET application by sid (#47496, merge conflict), admin pages for auth tokens (#47495), app secrets (#47500), OAuth grants (#47501).
Ask: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1781071671760909
Start: https://github.com/canary-technologies-corp/canary/pull/47487