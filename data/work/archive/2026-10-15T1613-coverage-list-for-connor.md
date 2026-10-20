---
area: null
completed_at: 2026-10-19 13:56:36.209059
contexts: []
created: 2026-10-15 16:13:14.699747
defer_until: null
due: 2026-10-19
energy: low
id: 2026-10-15T1613-coverage-list-for-connor
order: 2
output: |-
  ## Agent run 2026-10-19T13:45

  Sources: Connor <> Gareth 1:1 page, 2026-10-15 entry (https://app.notion.com/p/canarytechnologies/Connor-Gareth-1ae8146861518002b563c3fc97fca9f3), plus Granola notes from Oct 1-16. No separate Granola recording of the Oct 15 1:1 exists. Neither source gives Connor's exact out dates: the Oct 6 notes only say "the week before the BW convention", and Lauta is out too.

  ### Covering for Connor (his 4, in his order)

  1. **Best Western Staff App / SSO**. Connor called this the "number one thing to focus on next week".
     - Connor asked me to keep tabs on it and check in with Mike and Ishwar.
     - Jason has opened a direct line to BW properties (Mike), so we can watch their logins.
     - BW user export/import plan: get a list of all users.
     - QR code will NOT be the login method for the conference.
     - Brand selector: a dummy screen listing all brands, with only BW at launch. This is not the final design.
     - Diana's org-selection SSO flow has a draft PR. Some product/design decisions are still open. It could merge Monday Oct 19 if they're resolved. Target is the BW conference (standup Oct 16: https://notes.granola.ai/d/7b0bc068-7a94-44cf-be04-bcf87bf29496).
     - SCIM: don't rush it, it's not for the conference. Andreas picks it up when he's back (ENT standup Oct 8: https://notes.granola.ai/d/f464554a-0071-4566-af32-bb953f27ca76). If revisited, the MVP is pre-creating users only; the risks are first-sync reconciliation and safe SSO testing (Andrea 1:1 Oct 6: https://notes.granola.ai/d/0a336711-6b67-4c13-a2e2-2af9a41cc29f).
     - Still open from Oct 1: review Lauta's SCIM eng design and break down the project (https://notes.granola.ai/d/fa150f28-4026-487d-9a19-9275a9c6e0a2).

  2. **Mobile analytics**
     - Observability is bad. Groundcover is the main tool. Snowflake has no identifier for "this happened on mobile".
     - Need: a dashboard of check-in/checkout counts, split by iOS vs Android and mobile vs web. Wyndham needs this visibility. Carmela is involved.
     - Connor's bar: "the first step of the full solution, not a hack".
     - Diana built Wyndham monitoring dashboards and said she'd tag me in the EPD post (Oct 14: https://notes.granola.ai/d/d0de2936-cdf1-44f8-a66a-8c3413970e56). Confirm that happened.
     - Related: Caitlyn's priority this week is monitoring and alerting for the IHG scaled launch (thousands of hotels, now mid-November).

  3. **Wyndham launch**
     - Connor's concern: we aren't treating it as a big enough deal internally. Caitlyn, Manu and Diana need to hear that the job isn't done and this stage is more critical.
     - Status: the launch went well, with a low error rate and no critical client issues (Diana, Oct 14). Wyndham controls rollout with a user-level switch.
     - Open item: Sofya's Wyndham login issue. Escalation is via the Wyndham channel and Manu (Oct 16).
     - Wyndham upsells/in-stay SDK work: Caitlyn and David to review the TestFlight build. Open questions: summary page and tax display.

  4. **Explo -> Omni**
     - GrowthBook flag: https://growthbook.canarytechnologies.com/features/omni-embedded-reporting
     - Daniel is OOO this week. Andrea and Andres are on point.
     - Omni is still migrating custom reports for us. The hard deadline is Explo's sunset on Oct 31.

  ### Also in the Oct 15 notes (context, not explicitly handed to me)
  - **Wyndham Aspire**: 70 hotels in Germany signed. Not on Opera, not onboarding to Canary; they're keeping their stack. Connor will tag me into the monitoring thread. We feel good about the compliance list. Aspire Requests DB: https://app.notion.com/p/c6177516685041a2bf022849d1bff16a
  - **Accor accessibility**: Connor hasn't heard of it affecting other brands. His line: "if we've started, do it if cheap". (Mobile side is paused, per Diana Oct 14. Stephanie 1:1 Oct 16 had no summary: https://notes.granola.ai/d/29079fc9-1798-478e-8210-563a6d642e36.)
  - **Nathan** (starts Nov 2): IHG scripting changes Q4, Wyndham Barclays, BW rebrand.
  - **Caitlyn** is moving to tipping and hasn't moved the Guest App forward. Nathan may get involved; we're still hiring. The mobile PM hire is progressing.

  ### My open actions that touch Connor's areas
  - Ping Blake about David's app transfer (Oct 14).
  - Ask Connor about Nathan's mobile scope and guest app ownership. The Oct 15 notes partly answer this.
  - Raise team ownership questions (Staff App, messaging, guest app) at today's Blake 1:1 (Oct 19).
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Write a list of things I'm coverign for connor, from notes and transcripts
updated: 2026-10-19 13:56:36.209049
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/Connor-Gareth-1ae8146861518002b563c3fc97fca9f3