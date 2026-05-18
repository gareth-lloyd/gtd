---
area: null
contexts:
- craft
- react
created: 2026-05-18 12:03:08.777984
defer_until: null
due: 2026-05-18
energy: medium
id: 2026-05-18T1203-review-sam-saps
order: null
output: "## Agent run 2026-05-18T13:47:35\n\nReviewed Sam Kariu's design doc \"\U0001F510
  Support Access Approval Flow — Engineering\nDesign\" (Notion 11f8da83d8504e89b1f07cd06cc4145a,
  Linear TOOL-112, project owner\nskariu). Doc Status is already APPROVED with 7 discussions
  (a few unresolved,\nmostly from ldewald). Sam wants a fresh pass from you. Below
  is a review you can\nuse as-is. NOTHING was posted to Notion/Slack — see \"To post\"
  at the end.\n\n### Verdict\nStrong, build-ready design. The hard parts (concurrency,
  audit, migration\nsafety, Slack ingress hardening, blast-radius control) are thought
  through and\nmostly correct. No blockers. A handful of items worth nailing down
  before\nPhase 3b/5a — listed first.\n\n### Should resolve before build\n1. **Backfilled
  rows vs. the \"zero off-flow SAG\" audit.** Backfill copies every\n   legacy `SupportAccessPeriod`
  row, but legacy rows never went through\n   request→approve. If backfilled ACTIVE/EXPIRED
  rows land with no `decided_by`\n   (or a synthetic one), the Phase-6 success criterion
  (\"100% of ACTIVE grants\n   reached via the two-user flow; zero Django-shell creations;
  Security audits\n   for off-flow rows\") will false-positive on migrated data. Ask
  Sam to add an\n   explicit discriminator (e.g. `source=BACKFILL` / `decided_by=NULL`)
  so the\n   security audit query can exclude migrated rows cleanly. Currently unspecified.\n\n2.
  **Action attribution gap (impersonation still via shared ephemeral user).**\n   The
  doc audits *granting* access but actions in `control_hotel` run as the\n   shared
  ephemeral `support_user`, not the requester. \"Every session audited\"\n   is true
  for the grant, not for what's done under it. The doc scopes this out\n   (\"covers
  granting access, not what is done with it\") and defers per-user role\n   grants
  to v2 — fine, but this is exactly the kind of limitation the Phase 3b\n   security
  review should sign off on *explicitly* rather than inherit silently.\n   Recommend
  calling it out as a named accepted-risk in the Security section.\n\n3. **Kill switch
  covers the request side, not the callback ingress.** Revoking\n   `add_supportaccessgrant`
  stops new requests but the Slack interactivity\n   endpoint doesn't gate on that
  permission (it gates on the approver set +\n   signing secret). If the *callback
  endpoint itself* is the problem (bad deploy,\n   signature bug, scope leak), the
  documented kill switch doesn't disable it.\n   Ask Sam to document the inbound-endpoint
  kill switch separately (rotate/unset\n   `SLACK_SUPPORT_ACCESS_SIGNING_SECRET` /
  OAuth token, or short-circuit the\n   view) — independent of the request-side permission
  gate.\n\n4. **Approver coverage / timezones (extends ldewald's open comment).**
  A core\n   goal is cutting cross-timezone delay, but segment routing is single-primary
  +\n   thin backup pool (Diego cross-cutting). APAC (Diane) in particular: if the\n
  \  primary is OOO/asleep and only one backup exists, you reintroduce the very\n
  \  timezone bottleneck the project exists to remove. ldewald's noise question is\n
  \  still unresolved; the inverse risk (too few reachable approvers) deserves an\n
  \  answer too. Suggest documenting expected approver SLA + PTO/coverage policy,\n
  \  not just the routing table.\n\n### Minor / questions\n- EXPIRE notification:
  doc says \"after every state transition we DM the\n  requester,\" but the flow diagram
  only draws DMs on approve/deny. Confirm the\n  PENDING→EXPIRED auto-expiry actually
  notifies the requester (not just a silent\n  badge flip).\n- Requester reachability:
  requester notifications are Slack-only. If\n  `find_slack_user_by_email` can't resolve
  the requester they only learn the\n  outcome by polling Manage UI. Acceptable for
  v1 volume; worth one sentence.\n- Single open grant per hotel (partial unique) blocks
  two Support members\n  needing the same hotel concurrently. Almost certainly fine
  at stated volume —\n  just confirm it's an intentional v1 limitation, not an oversight.\n\n###
  Strengths worth affirming to Sam\n- `select_for_update` + `@transaction.atomic`
  on every write with the explicit\n  \"atomic alone is insufficient — two approvers
  both read PENDING\" reasoning;\n  `GrantNoLongerPending` driving the \"already approved
  by X\" chat.update.\n- Side effects via `transaction.on_commit` (no Slack DMs on
  rolled-back txns).\n- Pre-auth Slack rejections deliberately *not* written to the
  Event table\n  (attacker-controlled grant_id = poison-event vector) — genuinely
  good security\n  instinct, with counter+structlog as the compensating control.\n-
  Migration is safe: dual-read shim, precedence rule, freeze rule with a CI grep\n
  \ regression test, `both_tables_active` detection counter, idempotent backfill.\n-
  `@isolate(remove_after=...)` per phase + permission-as-rollout-gate (instant\n  per-user
  kill) is consistent with repo blast-radius guidance.\n\n### Open Notion discussions
  still unresolved (FYI)\n- ldewald: reviewer-list noise (resolved=false).\n- ldewald:
  \"new app vs reuse\" — Sam deferred pending the Slack-as-channel\n  decision (resolved=false
  but answered).\nRequest-framework-v2 comment was addressed (\"Done\" + rejected-with-rationale
  in\nthe doc body).\n\n### To post (NOT done — needs your approval)\nNothing was
  sent. If you want this delivered, two options:\n(a) reply in Sam's DM thread (Slack
  D04UH06R738, ts 1779094947.835089), or\n(b) leave the substantive items as Notion
  comments on the doc.\nTell me which and I'll draft the exact payload for your sign-off
  before sending.\n"
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 15
title: review sam SAPs
updated: 2026-05-18 14:04:11.539423
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/D04UH06R738/p1779094947835089