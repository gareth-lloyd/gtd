---
area: null
completed_at: 2026-11-20 14:08:37.982369
contexts: []
created: 2026-11-19 22:44:57.150733
defer_until: null
due: null
energy: null
id: 2026-11-19T2244-make-sure-andrea-and-the-ent-team-know-about-lab-h
order: null
output: |
  ## Agent run 2026-11-20T13:06:35+0200

  Nothing sent. Draft below is for #epd-enterprise-engineers (private, C0B1MN8F869, https://canarytechnologies.slack.com/archives/C0B1MN8F869).

  ### Draft Slack message

  @Andrea and team: checking you all know about Lab Hacker, David Thomson's MCP for the PMS test labs. If you're testing anything PMS-facing, you can ask Claude Code to do the lab side for you: "book a 2-night stay on CAN2 arriving today, add a deposit and check it in."

  • Labs: CAN1 and CAN2 (OPERA Cloud), WyndhamOhipUAT, Kiosk-1, Kiosk-2 and Sales-1 (OPERA v5), CanarySPH (Synxis, a few gaps)
  • It creates reservations, runs front desk steps (card, deposit, assign room, check in, post payment, check out, cancel), edits reservations and guest profiles, and sets room statuses
  • Every change is real in a shared lab, so Claude posts a QA notice saying what you're testing before the first change
  • For now this is for testing against production: the OPERA Cloud lab accounts live only in the production gateway, so the reservations show up in a prod test hotel pointed at the lab, not in staging, a live branch or local dev. Juan's project will open the labs to live branches and laptops: https://linear.app/canary-technologies/project/shared-ohip-lab-access-for-dev-gateways-ocim-dbb9b3cb5390
  • Caps per person per hour: 10 creates, 10 cancels, 60 changes in total. Reads are free. Ask David if the caps get in your way
  • Set-up takes a couple of minutes with WARP on: https://reservation-lab.cnry.cloud/connect
  • Docs: https://app.notion.com/p/40081468615180958141f7c893c943ad and a 4-minute demo: https://tv.canary-engineering.com/watch/28efefc5-f945-4af1-b769-ab3608087155

  Is anyone already using it? If something you need for Wyndham or IHG testing is missing, David has offered to add it.

  ### What I checked

  - No mention of Lab Hacker in #epd-enterprise-engineers so far. David announced it in #canary-uses-ai (https://canarytechnologies.slack.com/archives/C0B1DFKN7V1/p1793919688274899), #epd-general and #pms-support only.
  - Lab list and caps come from the Notion page (https://app.notion.com/p/40081468615180958141f7c893c943ad). It names seven labs, more than the item body lists. Kiosk-1/Kiosk-2/Sales-1 are "Opera Kiosk" there; I labelled them OPERA v5 from David's OKR update, which calls Kiosk-2 an OPERA v5 lab.
  - CanarySPH (Synxis) does not support room status, cancel, queue, profile UDF reads or guest count changes.
  - "David has offered to add it" is from his #pms-support post on 2026-11-02 ("If you need new ohip features added just let me know"). He said OHIP features; the draft stretches that slightly to Wyndham/IHG, so trim if you'd rather not speak for him.
  - Pat's thread (https://canarytechnologies.slack.com/archives/C0CGTM7DM98/p1795119219221339): Pat asked David to raise the create cap to about 30 an hour for a room-queue test. Correction 2026-11-20: David did reply in the channel (not in the thread): "I can ease up on the restriction", the cap exists to stop unneeded reservations and night-audit clean-up, and the dashboard (https://reservation-lab.cnry.cloud/) creates reservations with no cap. The draft now says "ask David if the caps get in your way".
  - Prod-only line added 2026-11-20 at Gareth's direction. Source is Juan's 2026-11-11 summary in #project-local-ohip-lab-access (https://canarytechnologies.slack.com/archives/C0CGTM7DM98): lab accounts live only in the production gateway, staging has none that work. That covers CAN1/CAN2; I did not check where the Kiosk, Synxis and Wyndham UAT labs are connected.
  - Andrea's Slack ID is U05G106T8S1 for the mention.
project: null
source_id: null
tags: []
time_minutes: null
title: Make sure Andrea and the ENT team know about Lab Hacker MCP
updated: 2026-11-20 14:08:37.982356
waiting_on: null
waiting_since: null
working_on: false
---

Output draft slack to #epd-enterprise-engineers checking that they know they can use this for PMS testing. 

Lab Hacker is David Thomson's MCP for driving the PMS test labs (OPERA Cloud CAN1/CAN2, OPERA v5, Synxis, Wyndham UAT) from Claude Code: create reservations, run front desk steps, edit reservations and guest profiles, set room statuses.

- Caps per person per hour: 10 creates, 10 cancels, 60 total changes. Changes need a QA notice on the lab.
- Set-up (WARP on): https://reservation-lab.cnry.cloud/connect
- Notion page: https://app.notion.com/p/40081468615180958141f7c893c943ad
- Announcement: https://canarytechnologies.slack.com/archives/C0B1DFKN7V1/p1793919688274899
- Prompted by Pat's message: https://canarytechnologies.slack.com/archives/C0CGTM7DM98/p1795119219221339