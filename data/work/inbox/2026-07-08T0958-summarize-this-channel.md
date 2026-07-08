---
area: null
contexts: []
created: 2026-07-08 09:58:12.774968
defer_until: null
due: null
energy: low
id: 2026-07-08T0958-summarize-this-channel
order: null
output: |
  ## Agent run 2026-07-08T10:05 (summary of #temp-securing-vibe-coded-apps)

  Channel: #temp-securing-vibe-coded-apps (C0BFJEP503V)
  https://canarytechnologies.slack.com/archives/C0BFJEP503V
  A short-lived incident/policy channel created 2026-07-07. ~26 messages over ~1 day. No open questions to you (Gareth) — you joined but did not post.

  ### What it's about
  Blake VanLandingham raised an alarm: application admins (e.g. Salesforce) have been handing out **non-scoped API keys** to enable "vibe-coded" / AI-built internal apps, some running on personal Vercel accounts. Blake is fine with OAuth-scoped apps (they follow a user account, limited blast radius) but sees raw API keys as a security risk needing controls. Goal: agree a policy *today* (2026-07-07) to present at All Hands the next day (2026-07-08).

  ### Key points / findings
  - **Scope of exposure is significant.** Chris Carter compiled a rough "API Key Tracker" spreadsheet (https://docs.google.com/spreadsheets/d/15pyOr4gonlTZCnWCz_zkuKY-nN7KCP2SBVNAiBFwgfI/edit) — says there's a fairly large surface area to review. Most at-risk apps are Sales-owned (Salesforce, Salesloft, GetAccept, Gong).
  - **IT has NOT been handing out API credentials** — Chris Carter deliberately delayed those requests because no process existed. But he can't fully vouch for apps where Platform/Eng aren't the only admins.
  - **Gurtej Gill's inventory** of Anthropic/Gong keys he issued for AI/vibe-coded tools over ~2 months: Ricardo Ramirez (Anthropic, CSA translation tool), Anais Chen (Gong transcripts + Anthropic dashboard), Chris Henriquez (Gong, post-demo email skill), Bryan Creagh (Anthropic workspace), Baylee Magee (Anthropic, Parakeet/copilot), Ryan Chapin (Anthropic AI tool).
  - **Concrete leak found:** Laura DeWald flagged a real example of an API key committed in **client-side source code** (from Ricardo Ramirez — original in #C0B1DFKN7V1). Blake: "yeah that's really painful."
  - **Two specific apps surfaced** (fwd from Stephanie Barry, offering help with API keys): Implementation Team Pipeline App "Atrium" (owner Anais Chen, Zoom walkthrough linked) and a Go-Live Checklist App at tools.thesaeed.com.
  - **Existing tooling that could help:** Bernard Pietraga noted Canary already has **Agent Vault**, a secrets gateway that can issue TTL-scoped tokens in both envs (agentvault.stg.cnry.land / agentvault.prod.cnry.land).
  - **Zivago Lee**: wants to stop people using personal Vercel etc.; he has created some keys himself (e.g. Parakeet) but acknowledges many keys are "out in the open."

  ### Emerging direction / proposed policy
  - Standard process for getting an API key should be an **IT ticket** (Gurtej proposed; Chris agreed).
  - First action item: build the **list of apps with admins outside Platform/Eng** (that's where most keys originate), then decide which systems are allowed to issue keys.
  - Prefer OAuth-scoped access over raw API keys; use Agent Vault for TTL-scoped tokens where keys are needed.
  - Loop in the sales-ops team; Chris to post in `#lawl`.

  ### Status / open loops (as of last message)
  - Chris Carter still compiling the full tools list (got sidetracked by "the Google issue"); tracker spreadsheet is the working artifact.
  - No finalized written policy in-channel yet — this was being assembled ahead of the 2026-07-08 All Hands.

  Participants: Blake VanLandingham (driving), Chris Carter (IT/list owner), Zivago Lee, Gurtej Gill, Bernard Pietraga (Agent Vault), Laura DeWald, Andrew Monroe, Gareth Lloyd (you, observer).
project: null
source_id: null
tags: []
time_minutes: 5
title: summarize this channel
updated: 2026-07-08 10:05:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C0BFJEP503V