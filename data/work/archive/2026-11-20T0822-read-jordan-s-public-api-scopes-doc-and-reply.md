---
area: null
completed_at: 2026-11-23 17:59:24.899082
contexts:
- consume
created: 2026-11-20 08:22:30.708390
defer_until: null
due: null
energy: medium
id: 2026-11-20T0822-read-jordan-s-public-api-scopes-doc-and-reply
order: null
output: |
  ## Agent run 2026-11-20T13:09

  Read the doc and all 6 comment threads. Nothing sent or posted. Draft reply and review points below.

  Doc: Public Api Scopes (https://app.notion.com/p/41881468615180dd9367fb44b7247e03), status "REVIEW ME!", owner Jordan, you are a listed reviewer and have not commented yet.
  Jordan's DM: https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1795125130135899
  Linear project: https://linear.app/canary-technologies/project/public-api-scopes-0ced63414cc6

  ### What the doc proposes

  - Every public API operation names exactly one scope in the Global API Definition file (`backend/public-api/parser/global-api.yaml`). I checked the file: 115 operations are `auth: required`, matching the doc, and none has a scope yet.
  - Scope format is `product-group:product:access`, with `read` or `write`. No wildcards, write does not include read, names never change.
  - Umbrella scopes (`canary:read`, `canary:write`, `canary-guest:read`, `canary-guest:write`) cover every product in a group, including future ones.
  - Applications, auth tokens and OAuth grants each get a `scopes` list. A scope counts only if it is on both the token and its application. Identity service decides on `/authenticate` and returns 403 `insufficient_scope`.
  - Application installs (which hotels or portfolios an app can reach), purchases and user permissions are out of scope.
  - Rollout: an empty list means full access until the last step, then no access. Existing applications are backfilled with every umbrella scope.

  ### Decisions Jordan is asking reviewers for

  1. Should guest be its own product group (`canary-guest`), or should everything be `canary`? The doc calls this one of the big decisions.
  2. The actual scope list. Each team has final say on its own names.

  ### Review points (my suggestions, not yet your views)

  1. **Emptying a scope list grants full access during the rollout.** Removing the last scope from an application, or PATCHing a token to `[]`, flips it from restricted to unrestricted until step 7. Suggest null means "legacy, not yet scoped" and `[]` means "no access" from day one. That also removes the semantic flip at step 7.
  2. **The backfill conflicts with deleting the MCP sid list.** Step 4 gives every existing application every umbrella scope. If `/mcp` requires any scope in the `canary` group, every backfilled application can call `/mcp`, so the hard-coded list in public-mcp cannot be deleted (a stated success criterion). `/mcp` needs a scope outside the umbrellas, or the backfill has to be narrower. "Which scope `/mcp` requires" is listed as an open question, so this is input to it.
  3. **Nobody owns narrowing after the backfill.** After step 7 every existing application still holds everything, including future products. The doc plans per-application logging of operations called. That could drive a backfill from observed usage, or at least limit the backfill to the product group an application actually uses.
  4. **Keep `canary-guest` as a group.** The segment really encodes the audience (guest versus staff), and umbrellas are per group. Folding guest into `canary` means a staff-facing partner holding `canary:read` also gets every guest surface, and a staff user's OAuth consent screen lists guest scopes. Anand's `canary:guest:*` (comment: https://app.notion.com/p/41881468615180dd9367fb44b7247e03?d=41d814686151806a9f17001c1e4288d4) breaks the three-part format and loses per-product guest scopes.
  5. **Jordan asked "would anyone use guest except us?"** (same thread). Worth answering from the enterprise side: brand apps embedding the mobile SDK (Wyndham) are the likely case. I did not verify which application the SDK authenticates as, so check before asserting it.
  6. **Cross-product flows.** Vipul asked how check-in works when it pulls reservations, upsells and payments (https://app.notion.com/p/41881468615180dd9367fb44b7247e03?d=41e814686151808e8eb9001cecafcf22). Jordan floated coarser scopes in reply. An alternative is a stated rule: a scope follows the surface an operation lives under, not the data it touches downstream. The doc's own example already works that way (`/guest_api/check_ins/.../purchase_order` is `canary-guest:check-in:write`).
  7. **`canary:payments:write` is a wide bundle.** It covers payment methods, payments and gateway configs. Names are permanent, so splitting gateway configs out later means a new name and a migration. Cheaper to split now.
  8. **Small points.** Several scopes cover 1 to 3 operations (`canary-guest:hotels`, `canary-guest:mobile-login`, `canary:sales-agent`), which works against "the list stays short". An umbrella scope on an OAuth grant means the user consents to products that do not exist yet, so its description should say that.

  ### Existing comments, for context

  - Andrea: not everything is hotel-oriented (SSO org, portfolio, brand). Jordan reworded to "data" and deferred to the Installs project.
  - Kevin Li: asked about `canary:chat`, `canary:voice` and knowledge base. Jordan: the list only covers what is in the public API today.
  - N. Garnier: compendium covers far more than wifi details. Also asked whether F&B needs its own scope separate from upsells. Both unanswered.

  ### Draft Slack reply to Jordan (not sent)

  > Read it, nice doc. I'll leave comments in Notion. Main ones:
  > 1. Empty list = full access during rollout means removing an app's last scope (or PATCHing a token to []) escalates it to everything. Null for "not scoped yet" and [] for "no access" from day one would avoid that.
  > 2. If we backfill every app with the umbrella scopes, they can all call /mcp once it needs a canary scope, so the sid list can't go. /mcp probably needs a scope outside the umbrellas.
  > 3. I'd keep canary-guest as its own group. It's really the audience, and it keeps the umbrellas and the consent screen meaningful.
  > 4. canary:payments:write bundling gateway configs with taking payments feels too wide given names are permanent.

  ### Not done

  - No Notion comments posted and no Slack message sent. Both need your explicit go-ahead.
  - Did not read the two images or the linked Canary Public API and OAuth docs.
  - Did not locate the hard-coded sid list in the MCP server code to confirm point 2 against the implementation.

  ## Agent run 2026-11-23T14:18

  Follow-up asked: "Boil this down to the most actionable feedback. Give me a high level summary of what I'm looking at. Check my friday granola call with Connor for additional context"

  Re-read the doc and its comments (now 12 threads, up from 6) and the Friday call with Connor (https://notes.granola.ai/d/9bd860bb-744c-47e8-b586-9a8fbf6cc1f2). Nothing sent or posted.

  ### What you are looking at

  Jordan's design doc (https://app.notion.com/p/41881468615180dd9367fb44b7247e03) for permission scopes on the public API. Today any application with a token can call every public route. The proposal: each of the 115 operations names one scope such as `canary-guest:check-in:write`, each application and token carries a list of scopes, and the identity service returns 403 when they do not match. OAuth users see the scopes on a consent screen. Which hotels an app can reach (installs) is a separate, later project. Existing apps are backfilled with umbrella scopes (`canary:read` and so on), so nothing changes for them at launch.

  Jordan wants two things from reviewers: whether guest should be its own group (`canary-guest`) or folded into `canary`, and a check of the proposed scope list.

  ### What the Connor call adds

  - Connor said Jordan keeps sending API specs to the PM group (he named Kevin, Babur, Nico and himself) and they are pitched too technically for product to help. What is missing for him is why we are building this and what it will be used for.
  - You agreed on the call: the problem statement is technical and states no user problem.
  - Connor will give Jordan that feedback himself and asked you to help corral and review, because he knows the work matters and is still finding the right way to give Jordan feedback.
  - Timing: Connor called it a next-week thing, nothing here moves quickly. That is this week.

  One caveat on the framing point. The doc does have a problem statement and one concrete case (the MCP connector's hard-coded sid list). What it lacks is who the consumers are and what each one needs, so say that rather than "no problem statement".

  ### The feedback worth giving (4 points, in order)

  1. **Add the consumers and use cases.** Ask for a short section listing the applications that exist or are planned (MCP connector, brand apps on the mobile SDK, partner OAuth apps, the staff app) and the scopes each would hold. This is Connor's point made concrete, and it is what the open decisions depend on: Jordan's own question "would anyone use guest except us?" (https://app.notion.com/p/41881468615180dd9367fb44b7247e03?d=41d814686151806a9f17001c1e4288d4) cannot be answered without it, and neither can the scope list be tested. Agree with Connor who says it, so Jordan does not get it twice.
  2. **The backfill stops the MCP sid list from being deleted.** Every existing app gets `canary:read` and `canary:write`, and the doc says MCP uses ordinary read and write scopes. So every backfilled app passes the `/mcp` check, and the hard-coded list (a stated success criterion) has to stay. `/mcp` needs a scope the umbrellas do not cover, or a narrower backfill. Nobody has raised this. I have not checked it against the public-mcp code.
  3. **Keep `canary-guest` as its own group.** This answers the decision Jordan flags as the big one. The group is the audience (guest versus staff). Folding it into `canary` hands every staff-facing partner with `canary:read` all guest surfaces. From the enterprise side, brand apps on the mobile SDK (Wyndham) are the likely outside users of guest scopes. I have not verified which application the SDK authenticates as.
  4. **Split gateway configs out of `canary:payments`.** One scope covers taking payments and editing gateway configs, and names are permanent. Splitting later means a migration.

  ### Dropped from the earlier list, and why

  - **Null versus `[]` during rollout.** G. Wilson posted this on Friday night (https://app.notion.com/p/41881468615180dd9367fb44b7247e03?d=41e8146861518030a3c3001c879fed3c). A +1 on that thread is enough.
  - **Nobody narrows apps after the backfill.** The doc now says so itself in Appendix B, and G. Wilson asked to refuse umbrella scopes in OAuth consent (https://app.notion.com/p/41881468615180dd9367fb44b7247e03?d=41e814686151802aaa3c001cf69e4542).
  - **Cross-product flows and the small scopes.** Real but minor. Point 1 covers them once the consumers are listed.

  G. Wilson also left four other comments on Friday night (logs look clean straight after the backfill, refuse unmatched routes at step 4, a cache time limit, SOC 2 audit record). None needs you.

  ### Revised draft Slack reply to Jordan (not sent)

  > Read it, will leave comments in Notion. Short version:
  > 1. Biggest gap for me is who this is for. A short list of the apps we expect (MCP connector, brand apps on the SDK, partner OAuth apps) and the scopes each would hold would let us test the scope list and answer the canary-guest question.
  > 2. If every existing app is backfilled with canary:read/write and /mcp uses ordinary scopes, they can all call /mcp, so the sid list can't be deleted. /mcp probably needs a scope outside the umbrellas.
  > 3. I'd keep canary-guest as its own group. It's the audience, and brand apps on the SDK are the likely outside users.
  > 4. I'd split gateway configs out of canary:payments now, since names are permanent.

  ### Not done

  - No Notion comments posted and no Slack message sent. Both need your explicit go-ahead.
  - Did not check the public-mcp sid list or the SDK's application in code (points 2 and 3).
  - Only read the first 9 minutes of the Connor transcript, where the doc was discussed. Granola's summary lists no other mention of it.
project: null
source_id: https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1795125130135899
tags:
- morning-gtd
- slack
time_minutes: 20
title: Read Jordan's Public API Scopes doc and reply
updated: 2026-11-23 17:59:24.899078
waiting_on: null
waiting_since: null
working_on: false
---

Jordan: 'i got a doc for api scopes you should take a look when you have time' https://app.notion.com/p/canarytechnologies/Public-Api-Scopes-41881468615180dd9367fb44b7247e03
https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1795125130135899