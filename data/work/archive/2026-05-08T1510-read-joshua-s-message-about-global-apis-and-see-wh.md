---
area: null
contexts: []
created: 2026-05-08 15:10:06.991547
defer_until: null
due: null
energy: low
id: 2026-05-08T1510-read-joshua-s-message-about-global-apis-and-see-wh
order: null
output: "## Agent run 2026-05-11T14:10Z\n\n### What Joshua is asking for\nSDM built
  the authN half of the new global/public API in Q1 and now wants to hand the\nremaining
  work off to the teams who own the adjacent areas. For Enterprise, the ask is\nprimarily
  authZ (no permissions model exists) and ownership of pieces that couple to\nthe
  User model. He wants a meeting to walk through state + agree on next steps.\n\n###
  What exists today (from `backend/canary/api_gateway/` survey)\n- **Django app**:
  `api_gateway/` (no README/CLAUDE.md). Models: `Application`, `AuthToken`\n  in Postgres.
  Bulk operational state in **global DynamoDB tables**: `applications`,\n  `auth-tokens`,
  `identities`, `devices`, `attestation-evidence` (schemas in\n  `shared/shared/aws/public_api_dynamo_db.py`).\n-
  **AuthN flow**: Istio gateway → canary `/authenticate` → SHA3-512 hash lookup in\n
  \ DynamoDB `auth-tokens` → app ACTIVE check → returns `identity_sid`. Header format\n
  \ `Authorization: Bearer $application_sid:$auth_token` (SDM-4124, SDM-4128).\n-
  **v1 endpoints exposed**: `/v1/devices/{challenge,register,attest,<sid>}`,\n  `/v1/identities`
  CRUD, `/v1/auth/{login,refresh}`. Each app has unrestricted access\n  to every endpoint
  — gating is only by IdentityType for a couple of internal-only views.\n- **IdentityType**
  enum has `APPLICATION`, `DEVICE`, `INTERNAL_SERVICE`,\n  `COMPANY_HOTEL_USER`. The
  COMPANY_HOTEL_USER value is the seam to the enterprise\n  User model — defined but
  **unused** today.\n- **ApplicationRecord.portfolio_uuid** field exists (always `None`
  currently) — the\n  placeholder for portfolio-scoping that authZ would build on.\n-
  **No `ApplicationPropertyRoleGrant`** anywhere in the codebase. Nothing similar.\n-
  Recent api_gateway commits are all SDM-prefixed (SDM-4471 .. SDM-4510): identity\n
  \ CRUD endpoints, lenient validator for expired keys, admin pages, Application\n
  \ credential service lockdown.\n\n### Linear state\n- **Initiative**: \"SDM: KR
  - TMC APIs live with 1 client (Rippling) processing volume,\n  validating 90% auth
  approval rate\" — anchor goal is Rippling/TMC, not IHG SDK.\n- Active projects under
  it:\n  - \"Global Public API Infrastructure\" — status: Eng Design (SDM-4139, SDM-4128
  done).\n  - \"Pre-Release final touches on global Canary Public API\" — Backlog,
  target 2026-04-09,\n    High priority, lead fgario@.\n- \"Public API Feb 11 IHG
  Deliverables\" project is **Completed**.\n- No existing ENT- tickets for authZ on
  this. Closest adjacent ticket is mine:\n  **ENT-5368** (Backlog, replace AnalyticsRoleGrant
  with PropertyRoleGrant) which is\n  relevant prior art for \"extend property-role-grant
  pattern\".\n\n### Prior thinking (Bear)\n- No Bear notes mention `api_gateway`,
  `ApplicationPropertyRoleGrant`, the Identity\n  DynamoDB tables, or Joshua's pitch.
  He hasn't discussed this with me before.\n- Adjacent: my 2024 portfolio-permissions
  work (`AllHotelsInPortfolioRoleGrant`,\n  `PropertyRoleGrant`, portfolio permission_context).
  Wyndham brand-vs-hotel tension\n  is captured in my notes and is exactly the shape
  of the \"brand-mandate / hotel-opt-out\"\n  product question Joshua flags.\n\n###
  What needs to happen — recommended next steps\n1. **Accept the meeting.** I don't
  have prior context on the project; a 30–45 min sync\n   to walk current state +
  open questions is the right move. Ask Joshua to share the\n   Notion design doc
  (referenced by SDM-4139:\n   `notion.so/canarytechnologies/Canary-Public-API-2ef8146861518080bcc3dfce8a33759c`).\n2.
  **Before the meeting, read**:\n   - The Notion design doc above.\n   - SDM project
  pages \"Global Public API Infrastructure\" and \"Pre-Release final touches\".\n
  \  - `api_gateway/models/application.py`, `api_gateway/services/auth_token.py`,\n
  \    `api_gateway/views/authenticate.py`, `shared/shared/aws/public_api_dynamo_db.py`.\n3.
  **Scoping questions to bring to the meeting**:\n   - **Use case forcing function**:
  Joshua is honest that IHG SDK doesn't need authZ.\n     What forces this work onto
  the roadmap — Rippling/TMC? A specific partner ask?\n     Without a use case, this
  should sit in Enterprise backlog, not active scope.\n   - **Identity ↔ User coupling**:
  confirm the seam. `IdentityType.COMPANY_HOTEL_USER`\n     is the bridge — is the
  plan to mint Identities for each CompanyHotelUser, or to\n     resolve User from
  Identity at request time? Who owns that mapping table — Enterprise?\n   - **AuthZ
  shape**: `ApplicationPropertyRoleGrant` should reuse PropertyRoleGrant /\n     Role
  machinery (and ENT-5368's consolidation work). It is NOT a parallel system.\n     Confirm
  with Joshua before committing to the name.\n   - **Portfolio-install semantics**:
  brand-mandate vs hotel-opt-out is a product call,\n     not eng. Who is the product
  partner — does this need Brad / a PM? Wyndham WHR is\n     the obvious test case.\n
  \  - **DynamoDB ownership**: Enterprise has no other DynamoDB tables today. If we
  own\n     `identities` and friends going forward, that's a new operational surface
  — confirm\n     on-call / runbook expectations.\n4. **Do NOT start coding yet.**
  This is plan-and-align work until (a) the meeting\n   happens and (b) a concrete
  use case + product answer exists. After that, file an\n   ENT- epic and break it
  into tickets.\n\n### Draft reply to Joshua (NOT SENT — for user to review/send manually)\n>
  Yeah, let's set something up. I haven't been close to the public API work so I'll\n>
  skim the Notion doc and the api_gateway code before we meet — can you drop the\n>
  Notion link? Going in I'd want to focus on (a) what's actually forcing the authZ\n>
  work onto the roadmap now (since the IHG SDK doesn't need it), (b) how\n> ApplicationPropertyRoleGrant
  fits on top of the existing PropertyRoleGrant /\n> Role machinery rather than next
  to it, and (c) the product questions on\n> portfolio install — who owns that decision
  on the product side? Toss me a couple\n> of times that work for you.\n\n### Outbound
  actions I did NOT take\n- Did not reply on Slack, did not create Linear tickets,
  did not move this GTD item.\n  All next steps are gated on the user's review.\n"
project: null
source_id: null
tags: []
time_minutes: 5
title: Read Joshua's message about global apis and see what needs to be done
updated: 2026-05-11 14:18:27.910540
waiting_on: null
waiting_since: null
working_on: false
---

Hi!

So SDM in Q1 was doing work on the stable\global\public API project, we are now trying to find a home for the parts of what we’ve built to teams that own the adjacent areas.

For enterprise team, the biggest thing is that so far we’ve only implemented the the authN story, not the authZ story. That is, the application IDs and secret keys can be used to gate an entire application to access our APIs at all, but we don’t have any way to gate access to specific APIs or specific resources within those APIs (no permissions). We had given consideration to that when designing originally but didn’t intend to implement this because we didn’t have a use case immediately (the IHG mobile SDK’s we were helping expose are guest facing and don’t need permissions). The logical next step would be to extend the permissioning system to some sort of ApplicationPropertyRoleGrant that would let us express authZ rules. The api_gateway also contains some global dynamoDB tables like Identity which might be closely coupled to the User model which enterprise owns and services related to generating the api keys.

There are also product-level open questions here about the details of how applications can be installed into portfolios (can brands mandate them, can hotels opt out), that we didn’t answer because we weren’t sure what enterprises would actually prefer, and it wasn’t central to our initial use case for IHG.

Can we set up a meeting to discuss the current state of public APIs if you’re not already familiar, the next steps for this project for authZ?

https://canarytechnologies.slack.com/archives/D04N5S9HPUM/p1778160173934539