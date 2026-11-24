---
area: null
completed_at: 2026-11-23 17:23:18.307059
contexts:
- consume
created: 2026-11-23 00:00:00
defer_until: null
due: null
energy: low
id: 2026-11-23T0000-review-friday-s-show-tell-recording
order: null
output: |
  ## Agent run 2026-11-23T14:36

  SUPERSEDED by the 15:33 run below, which summarises the actual transcript. Original text: NOT WATCHED. I found the recording but could not open it, so there is no summary of what was actually said. What follows is the link plus a pre-read of the agenda built from Notion and Slack.

  ### Recording (Friday 2026-11-20)
  - Zoom: https://canarytechnologies.zoom.us/rec/share/UVBJQPwZ40veTmdtINv4nTfJj2sPZ9MTBcInWmnKFPNxfHcjmXmXxkCGfXVinW-i.x30JXLq4nYAfx4FT
  - Passcode: e@@V4zeW
  - Notion row: https://app.notion.com/41e8146861518189aa49ede8b3bd8ec2

  ### Why it was not watched
  - The recording is passcode-gated. Submitting the passcode from a script was blocked by the auto-mode permission classifier (Unauthorized Access), and I did not work around it.
  - The Playwright browser was locked by another session, so I could not open it that way either.
  - No Granola note exists for the session.
  - To get a real summary: watch it, or re-launch with the browser free and approve the passcode step so the Zoom transcript can be pulled.

  ### Agenda for 2026-11-20 (from the Notion sign-up DB; not confirmed against the recording)
  Sign-up DB: https://app.notion.com/p/16f81468615180369a9fec6138b939d9

  Show & Tell slot:
  - Orbital: multi-agent alert investigation, Jason Flax (https://app.notion.com/41d81468615181799849c4c205d54275). Coordinator agent paired with SRE Agent on live on-call alerts, worker agents over git history and open PRs in canary and canary-kubernetes, a verifier agent before posting back. Moving from Jason's laptop to cloud. Source thread: https://canarytechnologies.slack.com/archives/C0CJ7M5FQMQ/p1795028463946439
    - Thread context worth knowing: the plan is to clone Overlord's agents and jobs into Orbital, run side by side for weeks, then cut over (Jason: "a clone followed up a cutover"). Enablement (Daga) takes the infra side: reuse the overlord-golem E2B template, route canary-mcp/Sentry/Groundcover through a server-side MCP router so Sallyport tokens leave the sandbox. Workup and Atlas cutovers are named as workflows to move, which touches the Workup work.
  - Canary Public MCP (first customer), Dylan Moradpour (https://app.notion.com/41d81468615181c1bbbffc9f85f565ea). Public MCP server with a Snowflake data tool, staff-login identity resolution and sensitive columns stripped, handed to its first demo customer last week. Source: https://canarytechnologies.slack.com/archives/C06MU2WUFSP/p1794932962487239 (column-stripping PR: https://github.com/canary-technologies-corp/canary-dagster/pull/612)
  - Encrypted fields [TBC], Piotr Wysocki (https://app.notion.com/41d814686151804ebf67e3f5e799209d). Short announcement on encrypting third-party secrets at rest. Marked TBC, so it may not have run. I found no Slack source for it.

  Huddle slot (same day, may be a separate session from the recording):
  - CS-Self-Serve Portfolio Mgmt, Andrés Figueira (https://app.notion.com/41481468615180ea866ccdc18e9c2bd1). No description.
  - Insights dashboards: 1-minute guided tours, Daniel Choy (https://app.notion.com/41d8146861518174a9c4dd4f034691d0). "Take the 1-minute tour" button on every property Insights and above-property portfolio dashboard, running on the customer's own data. Source: https://canarytechnologies.slack.com/archives/C024LKAN727/p1794521421749269

  ### Notes
  - Slack #demo-recordings (https://canarytechnologies.slack.com/archives/C06TB1R3DPZ) is stale: the last recording post is 2025-12-19. The Notion Recordings DB is the live source.
  - Coming up: Staff Notes in the messaging inbox on 2026-11-27 (https://app.notion.com/41d8146861518171a31cea466a283676), Multi-room check-in on 2026-12-04 (https://app.notion.com/41d81468615180c48b2ccc23bba3f77c).

  ## Agent run 2026-11-23T15:33

  Summary of the 2026-11-20 session (61 min), from the Zoom transcript and chat files you downloaded to ~/Downloads (GMT20261120-155905_Recording.transcript.vtt and GMT20261120-155905_RecordingnewChat.txt). I read text only, so anything shown on screen but not spoken is missing. Timestamps are recording offsets.

  ### What matters for you
  - Workup moves onto Orbital first. Blake: Orbital becomes the new harness running Workup, the first production use. Jason said it already works locally and should run in the cloud in shadow mode "next week", which is this week (week of 2026-11-23), pending a large PR stack with Daga. [00:39-00:42]
  - Workup memory gets split up. Blake said memory at the Workup level is "pretty dilutive" and context sprawl gets bad fast; the plan is per-area durable agents with co-located memory (Zendesk drafting, PMS investigations, messaging investigations). Teams keep contributing to Workup as today; Blake called the move a "mechanical translation". Jason owns both the harness swap and the reconfiguring. [00:50-00:53]
  - You were named. Jason, showing the triage agent: "I guess Gareth wants me to call work up again, because triage was the old name." [~00:28]
  - Security sprint trumps everything else (details below). Two product changes Blake named touch auth forms and check-in: stop ever showing a raw credit card to a hotel (authorizations and check-ins), and fix the QR code lookup, which was the attack vector.

  ### 1. Security sprint, Blake Vanlandingham [00:04-00:18]
  - The incident: first proper data leak last week. Reservation information for about 15,000 reservations across roughly 300 properties, through an endpoint that had been in production for years. The endpoint's URLs showed up on hacker lists. A retro is coming.
  - Stance change: assume frontier-level agents target Canary; obscurity no longer works; small leaks get stacked into bigger attacks. Controls must restrict first and notify humans to undo, not warn.
  - The sprint runs until SJ and Blake judge the meaningful issues fixed. Scope: account takeover, data exfiltration, network attacks, developer and employee machine takeover.
  - Structure: a strike team ("Falcon team") fixes what it can, and product teams get the rest, prioritised. Blake coordinates. Core team: security team, Andy, Henny, Charles, Chris (IT).
  - Ask of everyone: look at your own surface areas, and file anything security-related as a bug to triage on the security team Linear board. Z wants every change and risk recorded in the register.
  - Company-wide: Google OAuth will be turned off for any app not on an allow list (about 600 apps in use, about 75 judged fine, list still under review). New MDM and Okta in front of services.
  - Customer reaction (Stephen Reddekopp asked): positive in aggregate because Canary was proactive, with some very upset customers. Blake does not expect it to slow momentum, "but we can't have multiple of them".
  - Jason asked about agentic pen testing: no official process yet, it is on the list.
  - Tommy Slater asked later whether this displaces committed work [00:56-00:59]: yes, it is top priority, but no spray of tickets across teams. The strike team categorises first, then projects are dropped or re-scoped deliberately, including resetting expectations with enterprise customers.

  ### 2. Encrypted third-party secrets, Piotr Wysocki [00:18-00:25]
  - Third-party credentials (PMS, ticketing and payment gateway passwords, API keys, tokens) were stored in plain text in the databases. Since October, all secrets in PMS Gateway are encrypted with AWS KMS keys using envelope encryption.
  - The solution is generic: the third-party secrets module in the shared backend library. Payments is rolling it out now. Blake: every sensitive field, including ticketing gateway and other gateways, will be encrypted through this framework, prioritised very highly.
  - Django Admin: secrets are masked by default, and revealing one is written to the audit log.
  - Caveats: encrypted fields cannot be searched or filtered. Ian Clark: bulk operations over thousands of rows mean N KMS calls unless handled deliberately; his team will help. The older encrypted field in the monolith should be migrated away from (one key guards everything); David Franco hit minor difficulty doing that.
  - Write-up: https://app.notion.com/p/canarytechnologies/Security-of-third-party-secrets-40c814686151805fbdd8e2408c733688
  - Chat, Yasmin Lucero: the handoff of customer credentials to onboarding is a likely vector; build an endpoint to collect them so they never land in a spreadsheet or email. Well received.

  ### 3. Orbital, Jason Flax [00:25-00:56]
  - Live demo on Jason's laptop, slow under memory pressure. He launched a three-model swarm to build a weather app, showed Atlas (the new knowledge bot) answering a Slack question, sent a dry-run alert to the SRE agent, and opened the Workup agent, whose room has three agents: classifier, code investigator, workup lead.
  - Vocabulary: a durable agent is persistent, has memory and connections, and can be invoked in different contexts. A room is a swarm (Jason may rename it), and a deployed single agent is a one-agent room. Automations are a third term, and the line between an automation and a durable agent is not settled.
  - Direction: the same runtime that runs locally will run in the cloud as a shared workspace. Instead of writing Overlord code, teams adjust an agent by talking to it (models, swarm shape, tools), with approvals.
  - Mandate (Ishwar asked): shared company agents (Golem-style, Workup, Hawk, SRE Agent) will all be on Orbital. Personal use is not mandated until the value is obvious. Jason offered a bridge and a sidecar feature for people with their own setups. No benchmark against local dev yet.
  - Alternatives: Blake said they looked at Warp and found it immature for this, and would switch if another platform were clearly better.
  - Settings agent: Blake said Orbital targets internal use cases first. A resolution agent combining what a settings agent and Workup do is a later build, not where they start.
  - New agents on the current framework take about 2 hours to set up (Luke Curran, on Hawk); the target is minutes.
  - Repos: https://github.com/canary-technologies-corp/Orbital, plus orbitalJS and orbital-server. Jason said he would publish a new build the same day.
  - Chat: Austin Irvine asked for a dev tooling survey (Daga: on his list, behind). David Thomson: gateway alone has three or four versions of "software factories".

  ### Did not happen
  - Canary Public MCP: Dylan Moradpour dropped off to run the customer demo, so it was not shown.
  - CS-Self-Serve Portfolio Mgmt and the Insights guided tours were not in this recording.

  ### Possible follow-ups (your call, nothing done)
  - Talk to Jason about the Workup shadow-mode run this week and how the memory split maps onto the Workup accuracy work.
  - Check your areas (auth forms raw card display, QR code lookup) against the sprint and file anything to the security team Linear triage.
project: null
source_id: null
tags: []
time_minutes: 30
title: Review Friday's show & tell recording
updated: 2026-11-23 17:23:18.307054
waiting_on: null
waiting_since: null
working_on: false
---

Watch this week's Friday Demos / Show & Tell recording.

- Recordings DB (links + passcodes): https://app.notion.com/p/fa30f9afce544accadd42eb2efbc90d8
- Slack #demo-recordings: https://canarytechnologies.slack.com/archives/C06TB1R3DPZ


Orbital