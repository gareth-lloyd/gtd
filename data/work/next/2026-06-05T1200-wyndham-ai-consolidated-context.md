---
area: null
contexts: []
created: &id001 2026-06-05 12:00:00
defer_until: null
due: null
energy: medium
id: 2026-06-05T1200-wyndham-ai-consolidated-context
order: null
output: ''
project: 2025-03-28T0000-wyndham
source_id: null
tags: []
time_minutes: null
title: Wyndham AI Work — Consolidated Context (incl. MCP OAuth)
updated: *id001
waiting_on: null
waiting_since: null
working_on: false
---

*Consolidation doc — pulls together the AI-Assisted Search (MCP) project, Jaeyanthi's latest strategic feedback, the MCP OAuth authentication findings, and the PLAT/auth Slack thread. As of 2026-06-05.*

---

## TL;DR — where it stands

- Wyndham wants Canary to be their **brand-owned, portable MCP infrastructure layer** for AI-assisted search and booking across Wyndham.com, the mobile app, and public LLM surfaces — explicitly *not* locked to a single LLM platform. This replaced the earlier Adobe/Mobi pilot path (those pilots went badly; Wyndham pulled back from them and chose to partner with Canary directly).
- **Jaeyanthi (Wyndham product) has reframed the proposal (June 2).** She does **not** want "replace the existing MCP connector" as a standalone phase one — adoption on the current apps is tiny and rebuilding the same features on a new platform gets her no ROI. She wants **net-new capability first**, with replacement only bundled in.
- Her priority order: **(1) Perplexity / net-new LLM surfaces** ("can we get Wyndham in?" — her top ask), **(2) in-stay capabilities on the existing MCP app**, **(3) Loyalty Concierge** (authenticated).
- **Auth is the V1/V2 dividing line.** A no-auth V1 (public + member rates surfaced without login) is buildable today because Wyndham's pricing API already returns member rates. The authenticated **Loyalty Concierge** (points, history, saved payment, tier perks) is the net-new piece that requires OAuth — and nobody has built it.
- **Open middleman question:** how Canary's MCP server brokers Wyndham's OAuth (Auth0 + PKCE + phone MFA) so ChatGPT/Claude connectors can carry member context. Validated technically; implementation pattern is the live design question (OpenAI Apps SDK says OAuth 2.1 is sufficient).
- **Security gate:** Wyndham mandates an AI-specific security posture before any PII/PCI flows through chat. We owe them a clear answer from our security team.

---

## 1. Background & relationship history

Wyndham is building a **full AI-mode retailing agent** in collaboration with **Google (Gemini)** — use cases: ARI ingestion, loyalty-based personalization, end-to-end booking. Google planned to announce Wyndham as a major travel partner. Wyndham's phased data approach: (1) public data ingestion → (2) enhanced property attributes → (3) loyalty personalization.

Core requirement: **agent portability.** Wyndham does not want lock-in to one AI platform; they want MCP-based infrastructure serving multiple LLM ecosystems. Shared conclusion from early discussions: LLMs will increasingly demand data directly from the source, which favours **brand-owned MCP infrastructure** over third-party abstractions (e.g. Moby, which quoted $150K/month for a POC and has execution risk).

**Timeline:**
- **Feb 2026** — Demo discussions; Jaeyanthi put "on ice" briefly due to competing priorities.
- **Apr 9–16** — Scope aligned: conversational webchat for discovery/search, deep-linking to Wyndham.com for booking. Two adjustments: deep links go to "Rooms & Rates" only (not booking), and international hotels in scope. 60-day pilot proposed. Adobe/Mobi pilots went badly → Wyndham chose to partner with Canary directly. Alignment that conversational search is *not* the primary booking entry point — model is closer to Airbnb (structured inputs first, NL to refine).
- **Apr 24** — MCP research published (Terry Lin: Claude vs ChatGPT MCP comparison — both do property search + details; GPT more steerable; Claude ignored instructions to deflect competitors). Webchat POC kicked off (Santiago, target May 1). Three parallel Linear workstreams: Webchat POC (Messaging), Support Webchat/MCP (Enterprise), Wyndham MCP (Applied AI).
- **May 12** — MCP Workshop.
- **May 18** — Workstreams defined after Tyler/Dylan debrief (auth research spike, POC for authenticated Wyndham Rewards app in a public LLM, sizing unauth flows; Wyndham.com search-bar research; discovery calls with Phaedon's MCP and Google's UCP pilot team).
- **May 27** — PLAT/auth Slack thread kicked off (see §4).
- **Jun 2** — Jaeyanthi's reframing feedback (see §2).
- **Jun 5** — Terry's revised proposals sent to Jaeyanthi & team.

---

## 2. Jaeyanthi's feedback (June 2) — the strategic reframe

**ROI over replacement.** She does not want the MCP connector replacement as a standalone first phase. Adoption on existing apps is very low — under 100 visits since the start of the year on one app, a few hundred on the other, both under 1,000. The ChatGPT app has been live since end of March. Spending 2–3 months rebuilding the same features on a new platform with no new capability gets her no ROI. Replacement only flies if bundled with new functionality, not as the lead.

**Sequencing — net-new before rebuild.** The unauthenticated discovery experience already exists (the current app). The authenticated Loyalty Concierge doesn't, and nobody has built one. Her three priorities:
1. **Perplexity / net-new LLM surfaces** — can we get Wyndham in? *Her top ask.*
2. **In-stay capabilities** on the existing MCP app.
3. **Loyalty Concierge.**

**Auth vs. unauth split.** Clean division: excluding hotel stays, loyalty benefits have no overlap with what the unauthenticated version needs — so we can build the concierge without rebuilding the existing base. Caveat: loyalty data is distributed across partners (Snowstorm for Wyndham Rewards Insider, etc.) with transactions on partner sites via SSO — we'll need a strategy there.

**Adoption is her real problem.** Moving the pilot above the fold only took engagement from 0.4% → 0.8%. Her frustration: a partner hands over a product and then her internal teams have to figure out messaging and placement across a separate team, with lots of disconnect. She wants us **advising on positioning for adoption**, not just shipping a product. **A/B testing is now a core requirement** — for features *and* for UX/placement (search bar vs. hovering chat box; messaging like "Discover your ideal vacation" vs. "try our AI search"). Must be stated explicitly in the revision.

**App vs. web.** App users are loyalists — low volume, high conversion, come in direct, go straight to the search bar. Website is broader traffic, lower conversion, often referred from Google for a specific property. Her lean: give loyal **app users the Loyalty Concierge**. Build everything so it's easy to enable on either app or web to pivot quickly.

**Brand.com phasing.** She rejected the V0/V1/V2 framing — wants user-facing phases only. V0 (invisible backend) is dropped. Everything collapses to **phase one = support discovery and exploration of the portfolio**. She's skeptical V1 and V2 are meaningfully different and thinks V1 does the heavy lifting. *Action: nail down the real V1 vs. V2 distinction — Carly and Ani weren't sure it's more than UI.*

**Security.** Wyndham mandates an AI-specific security posture before any PII/PCI flows in chat. If we don't provide it, they have to (costs time/money). Separate from the toll-free Connect+ voice solution — the **chat** solution needs the security layer. We owe a clear answer from our team.

**Timelines she's working with.** Brand websites/app phase by **end of year** is feasible. She wants to know if the **Loyalty Concierge can launch early next year** if we pull the LLM piece out of scope.

---

## 3. MCP OAuth — authentication findings (Mini-PRD)

*Source: "Mini-PRD: Wyndham MCP Authentication Findings" (Owner: Terry Lin, validated 2026-05-19).*

### The V1 recommendation: punt auth downstream
Original recommendation (now struck through in the source as the framing shifts, but the technical logic stands): **build the no-auth version as V1 for everything; punt user authentication downstream to the website** to apply member benefits/points.

Why it works:
1. Existing Wyndham APIs (`detailPricing`) **already include member pricing via rate IDs** — so auth can be deferred to the website/checkout flow.
2. For MCP and ChatGPT/Claude connectors, tool descriptions can tell the LLM there are public rates and member rates.
3. The search experience can show a member-rate filter or side-by-side rates.

**Risk:** a user claims a loyalty status but gets a different price after logging into Wyndham Rewards (dynamic pricing drifts ~15 min). De-risk with disclaimer copy and a 15-min validity cap; deep link re-queries on landing. Mitigation pattern: always show both rates to encourage signup — *"Public: $130 · WR member: $114.66 if you're a member."*

**Benefit:** skips months of user-auth engineering and the Wyndham-side security/legal check for V1, and lets us learn from real usage which member-rate fields actually matter.

**Live probe evidence** (Days Inn NY Chinatown, CRS 91867 — API matched the live UI to the cent): the `autoEnroll: true` flag is the durable member-rate signal (e.g. `SWR1` Wyndham Rewards Rate $521.55 vs `RROD` Standard Rate $549.00). Member rates are readable **without** authentication.

### What V2 actually needs OAuth for
Authenticated, member-scoped features — the **Loyalty Concierge**:
- Points balance ("you have 47K pts, 3 nights here") → `/member/profile`
- Stay history, saved properties → `/member/activity`, `MEMBER_LISTS`
- Saved payment / address auto-apply → `member/profile?includePaymentCardAccounts`
- Personalized promos, CUG rate codes (AAA/AARP/Military/Senior) → member-scoped
- Tier perks (free upgrades, late checkout) → member-scoped

### How Wyndham's OAuth works (validated 2026-05-19)
1. Wyndham runs an **Auth0 OIDC tenant** on a custom domain (`login.wyndhamhotels.com`, underlying `whr.us.auth0.com`).
2. Flow is **OAuth2 authorization code** with two safety layers: **PKCE** (prevents stolen auth codes being replayed) and **phone-based MFA** (SMS or voice, 6-digit code).
3. After login, Auth0 issues a **1-hour RS256 JWT bearer token** plus a **90-char rotating refresh token** (via `offline_access` scope).
4. Each JWT carries a custom **`membership_number`** claim — the durable join key into the loyalty backend. `acr`/`amr` claims prove MFA was performed; `aud` scopes which APIs the token is valid for.

### Important wrinkle: two auth surfaces side-by-side
Wyndham's consumer site runs **Auth0 JWT** for OIDC-protected services **and a separate session-cookie system** for the loyalty backend (`/WHGServices/`). The SPA bridges them with an internal token-to-session exchange. Evidence: the JWT `aud` claim **excludes** WHGServices; WHGServices fetches carry no `Authorization` header (cookies only); storage shows both token systems live simultaneously (`OT_WHG_SESSION`, `ency_access_token`, etc.). **Implication:** a Bearer JWT alone may not be sufficient for all member data — some of it sits behind the WHGServices session surface. This needs design attention.

---

## 4. The middleman question — internal vs external MCP auth (Slack, May 27)

*Channel C04STT7UPRQ — Terry Lin → PLAT, Gareth Lloyd looped in (Blake routed it as an auth use-case rather than a Platform capability). CC Andrea.*

- **The ask:** Wyndham MCP initiative needs an **authenticated** ChatGPT/Claude connector. Wyndham has an existing OAuth pipeline on their site (bearer token → member rates, points history) and an existing **public MCP** live in the Claude/GPT app stores (`wyndhamhotels.com/mcp-doc`). Proposed flow: **ChatGPT/Claude → "Login to get your member rates" → Canary MCP → Wyndham OAuth → callback → ChatGPT/Claude.** Question: how should Canary behave as the middleman?
- **Dylan's context:** Canary already built an **internal MCP** (the one EPD uses to access Django) with auth via **Teleport**. The plan was to replicate those internal MCP patterns for Wyndham *minus auth* — under the now-broken assumption Wyndham didn't need auth. They do (member data in ChatGPT app context), so we need to integrate an MCP server with Wyndham OAuth.
- **Scope split:** internal-MCP OAuth is a **separate workstream**, but how we do OAuth for the externally-facing Wyndham MCP will inform whether/how we set up OAuth for the internal MCP later.
- **Technical pointer:** OpenAI Apps SDK auth docs say we just need to implement **OAuth 2.1** to do an authenticated MCP within an app. (`developers.openai.com/apps-sdk/build/auth`)

---

## 5. Open questions & our next steps

From Jaeyanthi's feedback + the auth thread, the action list we owe back:

- [ ] **Perplexity inroad** — confirm whether we have a path to get Wyndham onto Perplexity / net-new LLM surfaces. *Top priority.*
- [ ] **Rework sequencing** so replacement ties to new functionality, not as the lead.
- [ ] **Loyalty Concierge timeline** — can it launch early next year if the LLM piece is pulled out of scope?
- [ ] **Nail down real V1 vs. V2 difference** and whether phase one ships on app, web, or both.
- [ ] **Make A/B testing + adoption advisory explicit** in the proposal (features, UX, placement, messaging).
- [ ] **First-party hotel data source** — tactical updates on conversations with the model labs.
- [ ] **Security** — clear answer from our team on AI-specific threat protection before any PII/PCI in chat.
- [ ] **MCP middleman design** — settle how Canary's MCP brokers Wyndham's Auth0/PKCE/MFA OAuth (and the WHGServices session wrinkle) for ChatGPT/Claude connectors.

---

## Source links

- AI Assisted Search (MCP) project — https://app.notion.com/p/canarytechnologies/AI-Assisted-Search-MCP-2f881468615180eebdc2ca2ea271a4f0
- Mini-PRD: Wyndham MCP Authentication Findings — https://app.notion.com/p/canarytechnologies/Mini-PRD-Wyndham-MCP-Authentication-Findings-365814686151802ebaf4e983587c6016
- PLAT/auth Slack thread — https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1779903198286139
- Wyndham public MCP doc — https://www.wyndhamhotels.com/mcp-doc
- OpenAI Apps SDK auth docs — https://developers.openai.com/apps-sdk/build/auth
- SoW — Wyndham MCP (Notion) · Webchat/MCP PRD (Notion) · Proposed Pilot Scope — Wyndham Conversational Webchat (Notion)
- Linear: Wyndham webchat POC · Support Wyndham Webchat/MCP · Wyndham MCP?