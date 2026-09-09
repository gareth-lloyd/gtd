---
area: null
completed_at: 2026-09-08 16:53:32.770484
contexts: []
created: 2026-09-08 11:43:27.531316
defer_until: null
due: 2026-09-07
energy: low
id: 2026-09-08T1143-find-ihg-notion-overview-doc
order: null
output: |
  ## Agent run 2026-09-08T16:15

  ### Notion context: IHG enterprise rollout — who's doing what, CS org

  **Most relevant docs**
  - IHG Enterprise Runbook (https://app.notion.com/p/3338146861518145954dfb1e84c3f973) — canonical owner map, escalation matrix, rules of engagement. Auto-generated April 2026, owner Dianna Kertz, still marked unverified.
  - Enterprise Team Structure (https://app.notion.com/p/26481468615180789120ddf15f4e020b) — three-role model (EIM / Enterprise CSM / Sales) explicitly modelled on IHG: Taylor deploying, Dianna as CSM, DJ/Harman in sales.
  - Confirm support staffing model for IHG (https://app.notion.com/p/3c1814686151803abacde04bc5a430b0) — IHG support queue captains: Asel (EMEA), Jacob (NAMER); backups Wafa, Lyn. Marked done 2026-08-27.
  - CSM OnBoarding Account Assignment (https://app.notion.com/p/2e481468615180adacbeea80849225ee) — IHG accounts tiered "Global Brands"; APAC CSM = IM (Bonnie Wai for AU/NZ).

  **CS / Canary-side owners (per Runbook)**
  - Dianna Kertz — Head of Strategic Accounts; relationship + commercial
  - Taylor Kirchwehm — Enterprise CSM; brand standards, GJ config, onboarding scripts
  - Brad Andrews — integrations / SSO / loyalty
  - Sharon Hales — PMS validation
  - Bree Sullivan — kiosk / mobile key
  - DJ Singh — pricing
  - Bri Kapellas — support alignment
  - Sebastian Cahill — EMEA
  - Bonnie Wai — APAC
  - Caitlyn Levine — loyalty / CRM

  **IHG-side contacts (per Runbook)**
  - Andy Todd/Sealock — exec sponsor
  - Priyanka Jahr — GTX product decisions, key contact
  - Chanda Cheung — day-to-day ops, US deployments
  - Neil Fairall — APAC

  **Escalation channels**
  - #ihg (brand/corporate), #project-ihg-pilot (kiosk/key/onboarding), #epd-enterprise (PMS) — source: Runbook

  **Constraints**
  - No engagement in Greater China; MSA covers Messaging and Tipping only — source: Runbook

  **Open threads**
  - Bridge agreement expired 2026-05-31; Runbook not updated on enterprise agreement outcome.
  - Support routing automation when captains are offline still TBC; no APAC queue captain (staffing doc).
  - Hapi upsells for HotelKey blocked (Brad) — Runbook.

  **Nothing found for**: an IHG-specific RACI (only a PMS Gateway partner-integrations page surfaced).

  Read-only run: no Notion, Linear, Slack, or Salesforce writes.

  ## Agent run 2026-09-08T16:25 — direct read of IHG Enterprise Runbook

  Source: IHG Enterprise Runbook (https://app.notion.com/p/canarytechnologies/IHG-Enterprise-Runbook-3338146861518145954dfb1e84c3f973)
  Location: Customer Success Homebase / Enterprise / IHG Pilot Homebase (parent: https://app.notion.com/p/229814686151806d8478fc416662eb76)
  Status: auto-generated 2026-04-01 from Gmail/Slack/Notion/Linear; last edited 2026-07-08; Notion verification = unverified; "Last verified: Pending". Content reflects March 31 2026 state (bridge agreement through 2026-05-31). It does NOT describe post-enterprise-agreement rollout staffing.

  ### CS organization for IHG (how it actually works)
  Two-tier CSM model, per the Swim Lane framework (Section 3):
  - Enterprise CSM tier = Taylor Kirchwehm (Enterprise CSM) + Dianna Kertz (Head of Strategic Accounts). Owns anything touching GXP Pilot products (DCI, Messaging, Upsells, DCO, Compendium) and any property in the GXP pilot. Other CSMs redirect to them immediately.
  - Regional / Property CSM tier = the property's assigned CSM. Handles non-enterprise products (Tipping, Auths, AI Voice, Tablet) and directly-contracted non-pilot IHG properties; escalates to #ihg only for brand guidance or anything that could reach IHG corporate.
  - Regional leads: Sebastian Cahill (EMEA Product Ops; backups Bendix Urlbauer, Isaac Sheahan), Bonnie Wai (APAC; backup is IHG's Neil Fairall).
  - Support: Bri Kapellas (Head of Support) owns support swim-lane alignment with IHG; Julian is interim backup. Support alignment meeting was Gurtej / Dianna / Bri / Taylor (late Mar/early Apr 2026).
  - Onboarding operations: Taylor Kirchwehm primary, Noor Elgamal backup (#project-ihg-pilot).
  - Rule: anything uncertain, sensitive, or corporate-facing -> pause and post in #ihg before acting.

  ### Canary internal owners table (Section 2, verbatim roles)
  - Dianna Kertz — Head of Strategic Accounts; primary IHG relationship owner, weekly calls, commercial negotiations, exec comms with Andy & Priyanka
  - Taylor Kirchwehm — Enterprise CSM; brand standards & GJ config lead, onboarding scripts, pilot deployments, property-level config
  - Connor Swords — Product Liaison; pilot ops, roadmap discussions
  - Jeff Thoman — Head of Enterprise Sales; IHG Enterprise Agreement
  - Bree Sullivan — Guest Journey; drives kiosk and mobile key
  - Sebastian Cahill — EMEA Product Ops; EMEA compliance
  - Brad Andrews — Engineering / Integrations; PMS integrations, VGS proxy, SSO architecture, loyalty data pipeline
  - Bri Kapellas — Head of Support; support swim-lane alignment
  - DJ Singh — Commercial / Pricing; expansion product sales
  - Sharon Hales — Integrations Team Lead; PMS validation (Opera V5, OHIP, HotelKey), onboarding-plan automation

  ### Internal escalation matrix (Section 6: topic — primary / backup — channel)
  - Brand standards & GJ config — Taylor / Dianna — #ihg
  - IHG corporate relationship — Dianna / Gurtej Gill — #ihg
  - Pricing & commercial — DJ Singh / Harman — #ihg
  - Kiosk opportunities — Bree Sullivan / Aman Shahi — #project-ihg-pilot
  - PMS / integration issues — Brad Andrews / Sharon Hales — #epd-enterprise
  - EMEA deployments — Sebastian Cahill / Bendix Urlbauer, Isaac Sheahan — #ihg
  - APAC deployments — Bonnie Wai / Neil Fairall (IHG) — #ihg
  - Loyalty & CRM integration — Caitlyn Levine — #project-ihg-pilot
  - Onboarding operations — Taylor / Noor Elgamal — #project-ihg-pilot
  - Support team alignment — Bri Kapellas / Julian — #ihg
  - Product marketing — Rich Warner — #ihg
  - Digital Key / Access — Bree Sullivan / Mehul Parekh — #project-ihg-pilot

  ### Other named workstream owners (Sections 8-9)
  - Choose Your Room discovery — Bree Sullivan / SJ Sawhney (IHG: Neil Fairall)
  - Quore (Greener Stay housekeeping) — Kevin Li
  - Mobile App SDK and SFDC/LCPT CRM push — Caitlyn Levine
  - Hapi upsells for HotelKey (blocked) — Brad Andrews
  - Mid-stay message cleanup (Mar 2026 incident) — Taylor + Martin Rodriguez
  - Bridge/enterprise agreement — Dianna / DJ / Harman
  - Canada FPS prospecting — Jason Lugo (IHG: Chanda Cheung)

  ### IHG-side (post-reorg, as of 2026-03-31)
  - Andy Todd/Sealock — VP GTX, exec sponsor (last resort)
  - Priyanka Jahr — Director, Digital Guest Experience Products; now owns full DGX guest journey; key contact
  - Chanda Cheung — PM, GTX; day-to-day ops, US deployments
  - Neil Fairall — Sr Consultant APAC (Sydney), reports to Priyanka
  - Catherine Carson — Digital Departures/Billing, absorbing Access Control
  - Richard Gibson -> EMEA regional role (transitioning); Albert Maes for EMEA business partnering
  - Jen Miller — Product Marketing & Adoption, now outside GTX
  - Ben Heiland — Payments (Hapi)

  ### Related docs linked from the Runbook
  - IHG Global Rules of Engagement: https://www.notion.so/31e814686151801c9fa7dbc34550a48e
  - Enterprise Customers Swim Lanes (WIP): https://www.notion.so/31481468615180c693accb94ed5a6f4b
  - IHG Messaging Standards (Feb 2026): https://www.notion.so/305814686151802782a8deee20c74aa0
  - IHG Org Charts (Google Slides, maintained by Dianna): https://docs.google.com/presentation/d/14KzN5RUW4r9sh0_4d4CheNgS0u4qfjZvnW503FNdv30/edit
  - Slack: #ihg (C03V5P4B48P), #project-ihg-pilot (C08FQ3U01N2), #epd-enterprise
  - Suggested verifiers per the page: Taylor (Sections 3, 5), Brad (8), Bree (kiosk/mobile), DJ (pricing)

  ### Gaps
  - No RACI for the current enterprise rollout; the Runbook is a pilot-era snapshot and nothing in Notion covers staffing after the 2026-05-31 bridge expiry.
  - The Enterprise Customers Swim Lanes page is marked WIP and may be the closer match for CS org — not yet read.

  Read-only run: no Notion, Linear, Slack, or Salesforce writes.
project: 2026-08-31-ihg
source_id: null
tags: []
time_minutes: 5
title: Search notion for any documentation of who's doing what on the IHG enterprise
  rollout project, currently underway
updated: 2026-09-08 16:53:32.770471
waiting_on: null
waiting_since: null
working_on: false
---

In particular, how is teh CS team organization for IHG?

Everything going through Taylor

Check all hands transcript