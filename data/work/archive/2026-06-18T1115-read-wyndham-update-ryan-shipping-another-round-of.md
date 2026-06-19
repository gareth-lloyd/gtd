---
area: null
contexts:
- consume
created: 2026-06-18 11:15:53.392390
defer_until: null
due: null
energy: low
id: 2026-06-18T1115-read-wyndham-update-ryan-shipping-another-round-of
order: null
output: |
  ## Agent run 2026-06-18T14:15

  **TL;DR — awareness only, nothing required from you.** This round of Compendium
  updates has already shipped (ENT-6479 Done, PR merged & deployed 6/16). The only
  forward-looking thread is the July AEM-automation round — no firm date from Wyndham yet.

  **Connor's heads-up (Slack):** #wyndham, Connor Swords, 2026-06-17
  (https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1781643972388459) —
  pinged Marta Ziaei and Ani that Ryan Rogers had another *manual* round of Compendium
  offer updates going live 6/17. Canary and the Wyndham marketing team have aligned to
  pursue the automated solution leveraging Adobe Experience Manager (AEM) with the *next*
  round in July; Wyndham has not decided an exact date. No thread replies; 2x reaction.

  **Linear ENT-6479** — "6/17 Wyndham Offers Compendium update"
  (https://linear.app/canary-technologies/issue/ENT-6479/617-wyndham-offers-compendium-update):
  Status **Done** (completed 2026-06-17 23:27 UTC). Assignee Ryan Rogers, created by
  Connor Swords, Enterprise team, Wyndham label. Five offers this round: (1) Wyndham
  Rewards Earner Plus Card — up to 100k bonus points; (2) 4 Million Points Sweepstakes;
  (3) Upgrade to Wyndham Rewards Insider; (4) Grubhub+ free delivery; (5) Applebee's free
  delivery. Source docs (PDF/DOCX + Google Doc) attached to the issue.

  **PR #48100** — https://github.com/canary-technologies-corp/canary/pull/48100
  "[ENT-6479] Update Wyndham Offers compendium content for 6/17", by Ryan Rogers (rrgrs),
  **merged to master 2026-06-16 22:59 UTC**, 2 files, +72/-43 — i.e. a content-only swap
  of the offers data, deployed. (Linear briefly cycled Deployed -> In Progress -> Done
  while confirming the 6/17 go-live; single PR, no follow-up code.)

  **What to watch:** these recurring manual content PRs (at least the 2nd round) are the
  toil the AEM automation is meant to retire. The July round would be the first automated
  one, pending a Wyndham date. A Bear-notes check found NO tracked AEM project — documented
  automation thinking to date centers on Salesforce/SFDC compendium ingestion (e.g.
  ENT-6102), not AEM. If you own the eng side, worth confirming a Linear issue / PRD
  exists for the AEM integration before July.

  **Action:** none now; informational. Reasonable next moves (your call): archive, or
  convert to a "track July AEM-automation round" waiting/someday item.
project: null
source_id: https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1781643972388459
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 10
title: 'Read #wyndham update: Ryan shipping another round of Compendium updates (ENT-6479)'
updated: 2026-06-18 14:30:25.442862
waiting_on: null
waiting_since: null
working_on: false
---

Connor's heads-up in #wyndham: Ryan has another round of Compendium updates going in; automated AEM solution deferred to July (no date from Wyndham yet). https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1781643972388459