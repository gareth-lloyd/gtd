---
area: null
completed_at: null
contexts:
- react
created: 2026-08-05 07:33:38.020648
defer_until: null
due: null
energy: medium
id: 2026-08-05T0733-follow-up-on-taylor-s-opera-cloud-credential-centr
order: null
output: |
  ## Agent run 2026-08-05T13:59

  Read the full thread (13 replies, ended 2026-08-04 20:36 EEST; no new activity since —
  searched Slack for OCIM/"credential centralization" after 2026-08-03).
  Thread: https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1785850461696089

  **State: the thread produced all the ingredients for Neil's answer, but nobody has
  composed the reply to Neil yet, and one of Taylor's asks got zero response.**

  What was settled in-thread:
  - Sharon validated the approach: point IHG at the Developer Portal (linked from their
    Opera Cloud Admin panel). Multiple ChainCodes but all on the same Enterprise ID.
    Wyndham-style onboarding works: as long as each environment exists in Canary Admin
    onboarding values, the gateway + accounts scripts run the same way.
  - Connor's two-piece model (Sharon +1'd via the onboarding-values comment):
    1. Environment-level (infrequent): OHIP admin grants Canary API access per
       environment; credentials shared; created as onboarding values.
    2. Per-property (regular, automatable): IHG tells us environment + hotel code per
       property — ideally a scheduled bulk feed like Wyndham's sheet
       (https://docs.google.com/spreadsheets/d/1peaVyY2qKkf3XWCCNzJZazM2CTjWEZUL1PEn6XlY1NI/edit?usp=sharing).
  - Business Streaming is a SEPARATE approval: publishers must be set up in Opera Cloud
    per property, and the main environment must be approved first. Sharon: IHG
    environments are NOT yet streaming-enabled — being handled as part of the ongoing
    environment migration, but IHG still has to approve each.

  Open pieces (candidate next actions):
  1. **Store ID + terminal ID in bulk** — Taylor's payment-gateway ask got NO response
     in the thread. Nobody from payments/gateway weighed in. This is the clearest
     dropped ball.
  2. **Customer-facing streaming doc** — Sharon rejected Fred's internal Loom
     (https://www.loom.com/share/b4cb10dda7cd4c3484873924c0a2b1f0) and asked for the
     customer-facing "Approval and Publisher Doc". Fred posted
     OHIP_Business_Event_Streaming_Setup.docx (file F0BMXLF1Q7Q) but flagged it has no
     screenshots (no customer-mirroring OHIP sandbox exists). Unconfirmed whether this
     satisfies Sharon/Taylor.
  3. **Reply to Neil** — Taylor still needs to send Neil the consolidated answer
     (required access + provisioning flow). All content now exists in-thread.
  4. **Who at IHG does the OHIP admin work** — Taylor doubts Neil has access across
     environments; assumes IHG PMS team. Needs confirming with Neil, incl. asking for
     the scheduled environment+hotel-code feed (Connor's ask).

  Suggested follow-up (draft — NOT sent; needs your approval to post anywhere):
  "Two loose ends from yesterday: (1) the store ID / terminal ID bulk question never
  got an answer — who owns payment gateway config for OCIM sites? (2) Fred's streaming
  doc has no screenshots — is it customer-ready enough for Neil, or do we need a pass
  with Oracle's own portal docs?"

project: 2026-04-16T1351-ship
source_id: slack:C03V5P4B48P:ocim-centralization-2026-08-04
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 15
title: Follow up on Taylor's Opera Cloud credential centralization (IHG, with Neil)
updated: 2026-08-05 13:59:28
waiting_on: null
waiting_since: null
working_on: false
---

Taylor asked Sharon (CC Connor) to validate Canary's required Opera Cloud access and the account-provisioning flow as properties sign up; OCIM chain-admin adds + store/terminal IDs in bulk are the open pieces.
https://canarytechnologies.slack.com/archives/C03V5P4B48P