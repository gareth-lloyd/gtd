---
area: null
completed_at: 2026-11-23 17:22:51.369947
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

  ## Agent run 2026-11-23T14:15:55+0200

  Follow-up asked: "Write an informal post intended for #epd-enterprise-engineers with what it is, why it's cool, and prompting thoughts"

  Nothing sent. This is a looser rewrite of the 2026-11-20 draft for the same channel (https://canarytechnologies.slack.com/archives/C0B1MN8F869). No new research: every fact comes from the run above.

  ### Draft Slack message (informal)

  Has everyone seen Lab Hacker? It's David Thomson's MCP that lets Claude Code drive the PMS test labs for you.

  *What it is:* you type something like "book a 2-night stay on CAN2 arriving today, add a deposit and check it in" and Claude does it in the lab. It covers CAN1 and CAN2 (OPERA Cloud), Wyndham OHIP UAT, the OPERA v5 labs and Synxis. It can create and cancel reservations, do the front desk steps (card, deposit, room, check in, post payment, check out), edit reservations and guest profiles, and set room statuses.

  *Why I think it's cool:* getting a reservation into the exact state you need is usually the slow, fiddly part of testing anything PMS-facing. Now it's one sentence, and you can ask for five variations as easily as one. You also don't need to know your way around OPERA to do it.

  *Worth knowing:*
  • For now it's for testing against production. The OPERA Cloud lab accounts live only in the prod gateway, so the reservations show up in a prod test hotel pointed at the lab, not in staging, a live branch or local dev. Juan is working on opening that up: https://linear.app/canary-technologies/project/shared-ohip-lab-access-for-dev-gateways-ocim-dbb9b3cb5390
  • The labs are shared and the changes are real, so Claude posts a QA notice before it changes anything
  • There are hourly caps per person (10 creates, 10 cancels, 60 changes). Ask David if they get in your way

  Set-up takes a couple of minutes with WARP on: https://reservation-lab.cnry.cloud/connect
  Docs: https://app.notion.com/p/40081468615180958141f7c893c943ad
  4-minute demo: https://tv.canary-engineering.com/watch/28efefc5-f945-4af1-b769-ab3608087155

  Some questions for the thread:
  • Is anyone already using it? What for?
  • Which bits of our Wyndham and IHG testing eat the most set-up time? Could this do them?
  • What's missing that would make it useful for you? David has said he's open to adding things
  • Is the prod-only limit a blocker for how you test today?

  ### Notes

  - I read "prompting thoughts" as questions to get the team talking. If you meant tips on how to prompt Lab Hacker, the draft has only the one example prompt and needs a section I can't write without trying the tool.
  - The "why it's cool" paragraph is written as your opinion. I have not used Lab Hacker, so "five variations as easily as one" is my inference from the tool list and has to fit inside the 10-creates-an-hour cap. Cut it if it oversells.
  - I dropped the @Andrea mention to keep it a general post. Her Slack ID is U05G106T8S1 if you want it back.
  - Same caveats as the first draft: "open to adding things" stretches David's "If you need new ohip features added just let me know", and the prod-only line is confirmed for CAN1/CAN2 only.

  ## Agent run 2026-11-23T17:19:00+0200

  Follow-up asked: "make post shorter"

  Nothing sent. This is a cut-down version of the informal draft above, for the same channel (https://canarytechnologies.slack.com/archives/C0B1MN8F869). No new research.

  ### Draft Slack message (short)

  Has everyone seen Lab Hacker? It's David Thomson's MCP that lets Claude Code drive the PMS test labs: OPERA Cloud (CAN1/CAN2), OPERA v5, Synxis and Wyndham OHIP UAT. You type "book a 2-night stay on CAN2 arriving today, add a deposit and check it in" and it does it.

  Getting a reservation into the right state is usually the slow part of testing anything PMS-facing, so this could save us a lot of set-up time.

  One catch: for now it's for testing against production. The OPERA Cloud lab accounts live only in the prod gateway, so it won't help on staging, a live branch or local dev yet. Juan is working on that.

  Set-up takes a couple of minutes with WARP on: https://reservation-lab.cnry.cloud/connect
  Docs: https://app.notion.com/p/40081468615180958141f7c893c943ad
  4-minute demo: https://tv.canary-engineering.com/watch/28efefc5-f945-4af1-b769-ab3608087155

  Is anyone already using it? And what's missing that would make it useful for Wyndham or IHG testing?

  ### Notes

  - About 130 words, down from about 330.
  - Cut: the list of actions it can do, the hourly caps (10 creates, 10 cancels, 60 changes), the QA notice, the link to Juan's Linear project (https://linear.app/canary-technologies/project/shared-ohip-lab-access-for-dev-gateways-ocim-dbb9b3cb5390), and two of the four thread questions. The docs page covers the caps and the QA notice.
  - Cut "David has said he's open to adding things", which stretched what he said.
  - The prod-only line is still confirmed for CAN1/CAN2 only.
project: null
source_id: null
tags: []
time_minutes: null
title: Make sure Andrea and the ENT team know about Lab Hacker MCP
updated: 2026-11-23 17:22:51.369942
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