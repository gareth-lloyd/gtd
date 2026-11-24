---
area: null
completed_at: 2026-11-23 17:22:54.038953
contexts:
- react
created: 2026-11-23 09:30:58.910930
defer_until: null
due: 2026-11-23
energy: low
id: 2026-11-23T0930-check-the-two-wyndham-sla-at-risk-tickets-are-movi
order: null
output: |
  ## Agent run 2026-11-23T15:17Z

  **Neither ticket is moving.** Checked at 15:17 UTC. Both are still Todo, never started, with no human activity since Friday 2026-11-20.

  ### ENT-8363: breaches 17:18 UTC (about 2h left)
  https://linear.app/canary-technologies/issue/ENT-8363/add-thai-and-chinese-simplified-languages-wyndham-jomtien-pattaya-site
  - Todo, assignee Ryan Rogers, `startedAt` null. Last update 2026-11-20 19:43 UTC (the move from Triage to Todo).
  - Only comments are the automated triage ones. No human comment, no PR attached.
  - No Slack mention anywhere except the SLA bot post: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1795367925294399
  - Work is config only on EU hotel 538: turn on Thai and Simplified Chinese (English stays default), re-run Base Configuration. Optional: add th/zh to additional-guest languages, registration card translations.
  - Triage rated urgency Low (planned request, no outage), so a breach here costs the SLA metric rather than a hotel.

  ### ENT-8367: breaches 19:27 UTC (about 4h10m left)
  https://linear.app/canary-technologies/issue/ENT-8367/wyndham-50659-switch-to-elavon
  - Todo, assignee Marta Ziaei, `startedAt` null. Last update 2026-11-20 21:30 UTC (Triage to Todo).
  - Only human comment: rcuadra, 2026-11-20 20:16 UTC, "moving to @mziaei for assistance". Nothing from Marta.
  - No Slack mention except the SLA bot post, no thread replies: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1795375661106329
  - This one has real impact: Days Inn Calgary North Balzac (50659, hotel 1598) cannot process cards submitted through Canary until Elavon is configured. Zendesk 219608 and 219288 are attached.
  - Triage recommended the INT team (new payment gateway config), high confidence. It sits in ENT with Marta, so it may also be misrouted.

  ### ENT-8327: already breached (2026-11-20 15:37 UTC)
  https://linear.app/canary-technologies/issue/ENT-8327/no-token-when-they-tried-to-charge-the-reservation-in-opera-cloud
  - In Review with Marta, last update 2026-11-18 16:59 UTC. Nothing since.
  - The hotel fix is done (`integration_auto_post_cc_to_pms` turned on for hotel 5232). Still open: Marta confirming with Wyndham which processor 51978's OPI uses, the Voice AI gateway question (Shiji token vs Elavon OPI), and Andrea Bradshaw's unanswered question about hotels 5141 and 7035 having the same flag off.

  ### Not checked
  - I did not read production config, so I cannot rule out that someone made either change without touching the ticket. Ticket and Slack evidence says no.
  - DMs between other people are not visible to me.

  ### Draft nudges (not sent, need your explicit OK)
  To Ryan, DM or thread on the bot post:
  > ENT-8363 (Thai + Simplified Chinese for Wyndham Jomtien Pattaya, 57106) breaches SLA at 17:18 UTC today and is still in Todo. Can you pick it up now, or should I reassign? It is config only: enable the two languages on EU hotel 538 and re-run Base Configuration.

  To Marta, DM or thread on the bot post:
  > ENT-8367 (Wyndham 50659 switch to Elavon) breaches SLA at 19:27 UTC today and is still in Todo. The hotel cannot process cards submitted through Canary until Elavon is set up. Are you on it today, or does it need to go to INT? Triage recommended INT for the gateway config.
project: null
source_id: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1795375661106329
tags:
- morning-gtd
- slack
time_minutes: 10
title: 'Check the two Wyndham SLA-at-risk tickets are moving today: ENT-8367 and ENT-8363'
updated: 2026-11-23 17:22:54.038947
waiting_on: null
waiting_since: null
working_on: false
---

SLA bot in #epd-enterprise: ENT-8367 (Wyndham 50659 switch to Elavon, Todo, Marta) must complete by ~19:27 UTC today; ENT-8363 (Thai + Simplified Chinese for Wyndham Jomtien Pattaya 57106, Todo, Ryan) by ~17:18 UTC today. ENT-8327 (Opera Cloud no token) already breached, In Review with Marta.
https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1795375661106329