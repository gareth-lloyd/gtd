---
area: null
contexts: []
created: 2026-06-03 22:41:19.623230
defer_until: null
due: 2026-06-05
energy: low
id: 2026-06-03T2241-get-threads-from-ani-for-next-step-of-wyndham-conv
order: null
output: |
  ## Agent run 2026-06-05T15:42

  Consolidated the Wyndham AI context into a new PRIVATE Notion doc (created with explicit approval this session).

  **New Notion page:** Wyndham AI Work — Consolidated Context (incl. MCP OAuth)
  https://app.notion.com/p/37681468615181bbb32ee69f80a07ca5

  **Sources pulled together:**
  - AI Assisted Search (MCP) project page (full relationship history + timeline)
  - Mini-PRD: Wyndham MCP Authentication Findings (OAuth deep dive)
  - PLAT/auth Slack thread (C04STT7UPRQ, May 27 — Canary-as-middleman question)
  - Jaeyanthi's June 2 feedback (from the meeting-invite context in this item)

  **Doc structure:** TL;DR · Background & history · Jaeyanthi's June 2 reframe ·
  MCP OAuth findings (no-auth V1 logic, what V2 needs OAuth for, Auth0+PKCE+MFA flow,
  the WHGServices dual-surface wrinkle) · the middleman question (internal vs external
  MCP auth) · open questions/next steps · source links.

  Local draft (full, with live URLs) preserved at:
  gtd/data/work/next/wyndham-ai-context-draft.md

  **Note on the title:** this item's filename says "get threads from Ani for next step"
  but the body task was "consolidate context ... OUTPUT: new private Notion doc" — I did
  the consolidation. I did NOT chase Ani for additional threads; if that's still wanted,
  it's an open sub-action.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: 'consolidate context for the Wyndham AI work. INcluding MCP oauth. OUTPUT:
  New private Notion doc.'
updated: 2026-06-05 16:05:59.843575
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/AI-Assisted-Search-MCP-2f881468615180eebdc2ca2ea271a4f0?v=2b6814686151806e876c000c9cb32c81&source=copy_link
Slack thread: https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1779903198286139
Oauth MCP doc: https://app.notion.com/p/canarytechnologies/Mini-PRD-Wyndham-MCP-Authentication-Findings-365814686151802ebaf4e983587c6016

Meeting invite context:
Discuss Jaeyanthi Feedback on our proposal:

**ROI over replacement.**
She does not want the MCP connector replacement as a standalone first phase. Adoption on the existing apps is very low. Under 100 visits since the start of the year on one app, a few hundred on the other, both still under 1,000. ChatGPT app has been live since end of March. Her point: spending 2-3 months rebuilding the same features on a new platform with no new capability gets her no ROI. Replacement only flies if it’s bundled with new functionality, not the lead.

**How she wants it sequenced.**
Prioritize what doesn’t exist today over rebuilding what already exists. The unauthenticated discovery experience already exists (it’s the current app). The authenticated Loyalty Concierge doesn’t, and nobody has built one. Her three priorities:
1. Perplexity / net-new LLM surfaces. Can we get Wyndham in? This is her top ask.
2. In-stay capabilities on the existing MCP app.
3. Loyalty Concierge.

**Auth vs. unauth split.**
She sees a clean division. Excluding hotel stays, loyalty benefits have no overlap with what the unauthenticated version needs. So we can build the concierge without rebuilding the existing base. Worth noting the loyalty data is distributed across partners (Snowstorm for Wyndham Rewards Insider, etc.) with transactions on partner sites via SSO, so we’ll need a strategy there.

**Adoption is her real problem.**
Moving the pilot above the fold only took engagement from 0.4% to 0.8%. Her frustration: a partner hands over a product and then her internal teams have to figure out messaging and placement, across a separate team, with lots of disconnect. She doesn’t just want a product. She wants us advising on how to position it for adoption.  A/B testing is now a core requirement, not just for features but for UX and placement (search bar vs. a hovering chat box, messaging like “Discover your ideal vacation” vs. “try our AI search”). We need to state this explicitly in the revision.

**App vs. web.**
App users are loyalists, low volume but high conversion, who come in direct and go straight to the search bar. Website is broader traffic, lower conversion, often referred from Google for a specific property. Her lean is to give loyal app users the Loyalty Concierge. Build everything so it’s easy to enable on either app or web so we can pivot quickly.

**Brand.com phasing.**
She rejected the V0/V1/V2 framing and wants user-facing phases only. V0 is invisible backend so it’s dropped. Everything collapses to phase one = support discovery and exploration of the portfolio. She’s skeptical V1 and V2 are meaningfully different and thinks V1 already does the heavy lifting. We need to nail down the actual V1 vs. V2 distinction because Carly and I weren’t sure it’s more than UI.

**Security.**
Wyndham mandates an AI-specific security posture before any PII/PCI flows in chat. If we don’t provide it, they have to, which costs time and money. This is separate from the toll-free Connect+ voice solution. The chat solution needs the security layer. We need a clear answer from our team.

**Timelines she’s working with.**
Brand websites/app phase by end of year is feasible. She wants to know if the Loyalty Concierge can launch early next year if we pull the LLM piece out of scope.

Next steps on our side:
- Confirm whether we have an inroad to Perplexity. This is the priority.
- Rework sequencing so replacement ties to new functionality, not as the lead.
- Come back with a Loyalty Concierge timeline.
- Nail down the real V1 vs. V2 difference and whether phase one ships on app, web, or both.
- Make A/B testing and advisory support on adoption explicit in the proposal.
- Get tactical updates on first-party hotel data source conversations with the model labs.
- Get a clear answer from security on AI-specific threat protection.