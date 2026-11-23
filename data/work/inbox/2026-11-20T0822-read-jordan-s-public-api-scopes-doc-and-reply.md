---
area: null
completed_at: null
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
project: null
source_id: https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1795125130135899
tags:
- morning-gtd
- slack
time_minutes: 20
title: Read Jordan's Public API Scopes doc and reply
updated: 2026-11-20 15:37:38.194738
waiting_on: null
waiting_since: null
working_on: false
---

Jordan: 'i got a doc for api scopes you should take a look when you have time' https://app.notion.com/p/canarytechnologies/Public-Api-Scopes-41881468615180dd9367fb44b7247e03
https://canarytechnologies.slack.com/archives/D07HCMQU5FY/p1795125130135899