---
area: null
completed_at: 2026-08-06 15:04:55.781129
contexts: []
created: 2026-08-05 21:28:11.722232
defer_until: null
due: 2026-08-06
energy: low
id: 2026-08-05T2128-update-core-knowledge-base-support-access-period-g
order: null
output: "## Agent run 2026-08-06T13:35\n\nDrafted the rewrite of the Core KB doc.
  **NOT yet published to Notion — awaiting your go-ahead.**\n\nDraft file: `/private/tmp/claude-501/-Users-garethlloyd-projects-canary/74b60118-0cae-4abe-a5dc-63d61d7fc830/scratchpad/impersonation-doc-draft.md`\n\n###
  Docs involved\n- Target (engineering, out of date): [Read-only and read-write Impersonation
  by Canary staff](https://app.notion.com/p/2e78146861518041beacfd081d4ea930) — Core
  knowledge base, Enterprise pod. Last edited 2026-07-29.\n- Input (CS-facing, Draft
  status): [\U0001F510 Requesting Support Access to a Hotel](https://app.notion.com/p/3a581468615181f8abccc50d4cd1afd4)
  — Canary Knowledge Base, owned by Internal Tools.\n\n### What was stale in the engineering
  doc\nVerified against HEAD of `backend/canary`:\n1. Whole \"Support Access Period\"
  section is dead. `SupportAccessPeriod` service, admin, views, backfill command and
  Google-group perms were deleted in `ea969f6df91` ([TOOL-209] PR 1, #50365). Model
  class + table survive only until the drop migration (TOOL-209 PR 2). Replaced with
  `SupportAccessGrant`.\n2. Timers wrong: doc said 7-day window created straight from
  Django admin. Reality is `DECISION_TTL = 3 days` / `ACCESS_TTL = 24 hours` (`internal_support/services/support_access_grant.py:28`),
  with a request → Slack-approval step in between.\n3. Missing entirely: two-eyeballs
  self-approval block (`TwoEyeballsViolation`, service layer, → 403), reason-code
  enum, one-open-grant-per-hotel DB constraint, approver routing table, Linear-webhook
  auto-close on terminal issue state.\n4. Permissions table listed `add/change/view_supportaccessperiod`.
  Correct set is `add_supportaccessgrant` (request), `change_supportaccessgrant` (approve/deny/revoke
  — single approver perm), `view_supportaccessgrant` (queue).\n5. Read-only allowlist
  table was ~8 rows; `IMPERSONATOR_URL_CONFIG` is now ~105 entries. Replaced the table
  with a pointer to source + the one behavioural change worth stating: `/payment_gateways/`
  is now blanket-allowed in middleware except `async_refund`, `payment_refunds`, `reverse_payment_intents`,
  `cancel_payment_intents`.\n6. Audit section conflated the two trails. `ImpersonationLog`
  still has only IMPERSONATE/UNIMPERSONATE; the authorization trail is the six `SupportAccessGrant__*`
  events.\n\nKept as still-accurate: the Dec-2023 background, the `is_live` ratchet,
  training-user model, the access-code path (line ref refreshed to `hotels/models/user_profile.py:155`),
  and the 1-hour session timeout — I added the caveat already in the code that expiry
  only fires on the `unimpersonate` URL, so the 24h grant window is the real bound.\n\n###
  Discrepancies found — worth raising, not silently papering over\n- **The CS doc
  says \"anyone can *request* support access, but approving... is permissioned.\"**
  That is wrong. The API view enforces `internal_support.add_supportaccessgrant` on
  request (`internal_support/views/support_access_grant.py:380`), and Django admin
  creation is gated the same way (`internal_support/admin.py:340`). Only the service-layer
  `can_request_grant` is permissionless (active staff). Frontend hides the button
  via `can_request_support_access`. → the CS doc needs a correction, or the perm needs
  granting broadly.\n- **The CS doc says \"Support Access is available in all regions
  — US, EU, and APAC\"**, while its own FAQ says stalled requests are \"usually a
  regional setup gap... a datacenter where approver notifications were not yet wired\".
  Those contradict. The CS doc is still `Publication Status: Draft` with an explicit
  TODO to verify that exact line before publishing.\n- **Segment routing is a stub.**
  `internal_support/services/hotel_segments.py::get_hotel_segment()` always returns
  `None`, so \"segment-matched approver\" describes design, not runtime — every request
  currently DMs all primaries + all backups and logs `segment_routing_fallback`. Called
  out in the draft.\n- **`Hotel.is_live` help_text is stale** (`hotels/models/hotel.py:505-507`)
  — still says \"CS staff can request a limited 'Support access period'\". Small code
  fix, separate from the doc; not made.\n\n### PUBLISHED 2026-08-06T13:52\nYou approved;
  the rewrite is live on [Read-only and read-write Impersonation by Canary staff](https://app.notion.com/p/2e78146861518041beacfd081d4ea930).
  Full page content replaced. Verified by re-fetching. Nothing written to Linear,
  Slack, or GitHub.\n\n### Follow-ups still open (not actioned)\n1. CS doc [\U0001F510
  Requesting Support Access to a Hotel](https://app.notion.com/p/3a581468615181f8abccc50d4cd1afd4)
  says \"anyone can request\" — contradicts `add_supportaccessgrant` being enforced
  at `internal_support/views/support_access_grant.py:380`. Owner is Internal Tools;
  doc is still Draft. Needs either a doc correction or the perm granted broadly.\n2.
  Same doc's \"available in all regions\" contradicts its own FAQ about unwired regional
  approver notifications. It carries an explicit TODO to verify that line before publishing.\n3.
  `Hotel.is_live` help_text (`hotels/models/hotel.py:505-507`) still says \"Support
  access period\". One-line code fix, no PR raised.\n4. TOOL-209 PR 2 (drop migration
  for the `SupportAccessPeriod` table) has not landed. The doc says so explicitly,
  so it stays accurate either way.\n"
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: 5
title: update core knowledge base support access period -> grant
updated: 2026-08-06 15:04:55.781124
waiting_on: null
waiting_since: null
working_on: false
---

this doc is out of date: https://app.notion.com/p/canarytechnologies/Read-only-and-read-write-Impersonation-by-Canary-staff-2e78146861518041beacfd081d4ea930?source=copy_link

Take this into account: https://app.notion.com/p/canarytechnologies/Requesting-Support-Access-to-a-Hotel-3a581468615181f8abccc50d4cd1afd4?source=copy_link&utm_content=3a581468-6151-81f8-abcc-c50d4cd1afd4&utm_campaign=T4PJH2UQL&n=slack&n=slack_link_unfurl&pvs=6