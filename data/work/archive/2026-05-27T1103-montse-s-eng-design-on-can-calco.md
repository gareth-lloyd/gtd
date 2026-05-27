---
area: null
contexts: []
created: 2026-05-27 11:03:07.323229
defer_until: null
due: 2026-05-27
energy: low
id: 2026-05-27T1103-montse-s-eng-design-on-can-calco
order: null
output: |
  ## Agent run 2026-05-27T11:30:00

  Found Montse's eng design and supporting context in Notion + Linear.

  **Primary artifact (review this):**
  - [Portfolio Voice — eng design doc](https://www.notion.so/36181468615180db97c9dcaa715a3170) — Status: TODO, awaiting your review. You are listed as reviewer.

  **Supporting context:**
  - [PRD: Can Calco — Voice AI Above-Property Flow](https://www.notion.so/35c81468615181f3931dce8f9bddf2cd) — James Saram's PRD (6 properties, one Twilio number, no live transfers, $20.7K ARR)
  - [Linear project: Can Calco: Voice AI flow - above property](https://linear.app/canary-technologies/project/90191657-f083-48aa-b660-ce30d794abed) — Lead: Montse Pladevall. Status: Eng Design. Target: Jun 5–19 2026.
  - [EMEA-238: Eng design - above property Can Calco](https://linear.app/canary-technologies/issue/f2eafe9e-abfb-4a4c-a9b9-6815a48e66c0) — the eng-design ticket
  - [EMEA-290: Draft engineering design for CallCenterAgent](https://linear.app/canary-technologies/issue/90a2e435-3ff6-4206-8fe1-01423d7a7713) — follow-on design assigned to Montse (created May 26)

  **Key design decisions to be aware of when reviewing:**
  - Mirrors Mitsis chat pattern: portfolio modeled as JSON dict (`portfolio_voice_properties`) on `VoiceConfiguration`, not a new table — throwaway-friendly with `# TODO(VOICE-PORTFOLIO):` markers
  - No live transfers ever for Can Calco: `transfer_call` tool dropped from registry when `no_transfer_fallback_message` is set; enforced in `BaseAgent`, not orchestration agent, to prevent sub-agent leakage
  - New `PortfolioVoiceOrchestrationAgent` subclasses `CanaryOrchestrationAgent`; gated by GrowthBook `voice-portfolio-call` + `voice_deployment_level = "portfolio"`
  - Booking links must strip `gclid`/`gbraid`/`gad_source`/`gad_campaignid` (assertion before SMS/WhatsApp send) to protect Google Ads attribution
  - Proposed 4-part Linear breakdown: EMEA-273 (data shape + disambiguation), EMEA-274 (admin + searchable KB), EMEA-275 (orchestration agent), EMEA-276 (integration)

  **Open threads:**
  - Segmented KB UI at ~1,000+ entries — unconfirmed it supports search/filter at scale
  - VOX-2421 (per-property voice assignation) unresolved, flagged High risk on critical path
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Find Montserrat Pladevall's  Eng design on can calco from notion
updated: 2026-05-27 11:51:08.218226
waiting_on: null
waiting_since: null
working_on: false
---