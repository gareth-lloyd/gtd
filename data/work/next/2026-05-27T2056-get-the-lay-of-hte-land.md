---
area: null
contexts:
- deep
- consume
created: 2026-05-27 20:56:03.997090
defer_until: null
due: 2026-05-28
energy: medium
id: 2026-05-27T2056-get-the-lay-of-hte-land
order: null
output: |
  ## Agent run 2026-05-27T21:00:00

  Slack thread: #C04STT7UPRQ, parent ts 1779903198.286139 (Terry Lin, 2026-05-27 20:33 EEST).

  **What it's about — Wyndham MCP initiative needs OAuth guidance.**

  Terry Lin + Dylan Moradpour (Wyndham team) are scoping an authenticated MCP integration so ChatGPT/Claude connectors can pull Wyndham member data (rates, points history) on behalf of a logged-in guest. Blake pulled me in because it's auth-shaped rather than a generic platform capability. I CC'd Andrea.

  **The setup they described:**
  1. Wyndham already has an OAuth pipeline on wyndhamhotels.com — login returns bearer tokens used for member-rate/points endpoints.
  2. Wyndham already ships a public MCP (https://www.wyndhamhotels.com/mcp-doc) live in the Claude/GPT app stores — unauthenticated.
  3. Original assumption: Wyndham MCP wouldn't need auth. That broke when they decided they want member-data in chat context.
  4. Proposed flow: ChatGPT/Claude → "Login to get your member rates" → Canary MCP → Wyndham OAuth → callback → back to ChatGPT/Claude. Canary acts as OAuth middleman.

  **Adjacent context Dylan flagged:**
  - Canary's internal MCP (the one EPD uses to hit Django) already does auth via Teleport.
  - Wyndham is also looking at OAuth for internal users on our internal MCP — Dylan wants to keep those as separate workstreams but expects the external Wyndham design to inform internal.

  **What's open:**
  - I asked "Any docs available?" — waiting on Dylan/Terry to share design notes or a Linear/Notion link.
  - Andrea hasn't responded yet.
  - No Linear ticket was linked in the thread; worth asking for one if this turns into real scoping.

  **My read on the ask:**
  They want a guided OAuth Q&A — specifically how Canary should behave as the middleman between the MCP client (ChatGPT/Claude) and the upstream identity provider (Wyndham). Standard authorization-code-with-PKCE-style proxy/relay design questions: token storage, refresh handling, per-user vs per-tenant credentials, MCP's OAuth 2.1 spec compliance, and how to bind the Wyndham user identity to the MCP session. No code or design yet — this is a "help us think through it" request.

  **Suggested next actions (for you to triage):**
  - Wait for Dylan's docs before scheduling anything.
  - When docs land, decide whether to absorb async or set up a 30-min OAuth design chat with Terry/Dylan/Andrea.
  - Worth pinging Andrea directly to make sure she saw the CC.

  ## Agent run 2026-05-27T21:05:00

  Two new replies in the thread:

  **Terry posted the docs** — Notion mini-PRD: "Mini-PRD: Wyndham MCP Authentication Findings" (owned by Terry, status Draft, in PRD Database). He flagged the `What V2 needs OAuth for` section as the relevant jump-to.

  **Dylan added** that the [OpenAI Apps SDK auth docs](https://developers.openai.com/apps-sdk/build/auth) say "we just need to implement OAuth 2.1 to do an authenticated MCP within an app" — i.e., from the ChatGPT/Claude client's perspective, the Canary MCP server itself needs to be an OAuth 2.1 authorization server (or proxy), independent of how Canary talks upstream to Wyndham.

  **What the Notion PRD actually says (this matters — it reframes the ask):**

  Terry's headline recommendation is **don't build OAuth for V1**. Punt user auth to the Wyndham website/checkout flow.

  Reasoning:
  - Wyndham's `detailPricing` API already returns member pricing without auth — member rates are identified by rate codes like `SWR1` (Wyndham Rewards Rate) flagged with `autoEnroll: true`. Standard rate is `RROD`.
  - For chat/search UX, the bot can show public + member rates side-by-side ("Public: $130 · WR member: $114.66 if you're a member"), letting users self-identify.
  - Skips months of auth engineering + Wyndham-side security/legal review for V1.
  - Risk: user claims member status but gets a different price after Wyndham login (dynamic pricing drifts ~15 min). Mitigated with disclaimer copy.

  **V2 is where OAuth becomes load-bearing** — for points balance, stay history, saved payment auto-apply, personalized promos, tier-specific perks (free upgrades, late checkout). All hit `/member/*` endpoints.

  **What Terry's already validated about Wyndham's OAuth (live probe, 2026-05-19):**
  - Auth0 OIDC tenant on `login.wyndhamhotels.com` (underlying `whr.us.auth0.com`)
  - OAuth 2.0 authorization code + PKCE + phone MFA (SMS/voice 6-digit)
  - 1-hour RS256 JWT + 90-char rotating refresh token (via `offline_access` scope)
  - Custom `membership_number` JWT claim is the loyalty join key
  - Token audience is `login.wyndhamhotels.com/api/v2/loyalty` + `whr.us.auth0.com/userinfo`

  **Important wrinkle to raise with Dylan/Terry** — the PRD documents an architectural snag: Wyndham runs **two parallel auth surfaces**. The Auth0 JWT's `aud` claim does NOT include WHGServices (`/WHGServices/loyalty/V4/member/profile`, etc.), which is where the actual member-data endpoints live. WHGServices uses session cookies + a separate encrypted token (`OT_WHG_SESSION`, `ency_access_token`). The SPA bridges them internally with a token-to-session exchange that Canary doesn't have visibility into.

  So if V2 needs `/member/profile` or `/member/activity`, the Auth0 JWT alone won't work — Canary would need either (a) Wyndham to expose a JWT-authenticated equivalent of WHGServices, (b) the token-exchange recipe, or (c) a different upstream API entirely. This is the single biggest unknown in the V2 design and is worth flagging back to Terry before any auth engineering starts.

  **Reframed view of what Canary's actually being asked:**
  - **V1 (recommended in PRD):** no Canary-side auth at all. Both sides agree on this direction.
  - **V2 (the actual OAuth question):** Canary MCP needs to be an OAuth 2.1 authorization server to ChatGPT/Claude (per Dylan's OpenAI link), AND act as a relying party to Wyndham's Auth0. The hard question isn't OAuth 2.1 spec compliance — it's the WHGServices audience gap above.

  **Suggested next actions (refined):**
  - Read Terry's PRD end-to-end (~15 min) before any meeting — answers most of the obvious OAuth Q&A already.
  - Raise the WHGServices audience gap with Terry/Dylan — it's the actual blocker for V2, not OAuth 2.1 spec questions.
  - Confirm with Dylan whether V1-no-auth is the agreed path. If yes, the immediate "OAuth Q&A" ask is much smaller and may not need a meeting at all.
  - Andrea still hasn't engaged — worth a direct ping if you want her in.
project: 2026-04-10T0840-ticket
source_id: null
tags: []
time_minutes: 15
title: Wyndham OAuth thread - react, comment on PRD
updated: 2026-05-28 12:27:39.174969
waiting_on: null
waiting_since: null
working_on: true
---

https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1779903198286139