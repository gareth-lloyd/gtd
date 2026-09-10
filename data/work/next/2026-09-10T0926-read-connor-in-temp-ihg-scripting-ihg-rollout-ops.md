---
area: null
completed_at: null
contexts:
- consume
created: 2026-09-10 09:26:03.239308
defer_until: null
due: null
energy: low
id: 2026-09-10T0926-read-connor-in-temp-ihg-scripting-ihg-rollout-ops
order: null
output: |
  ## Agent run 2026-09-10T11:23

  Read-only research: Slack thread + Notion pages/DB. Nothing was posted or edited anywhere.

  ### What Connor posted (2026-09-01, #temp-ihg-scripting)
  Thread: https://canarytechnologies.slack.com/archives/C0BSBH7BELE/p1788302467604549
  Connor and Andrea built a single source of truth for IHG per-country readiness, to be kept up to date during testing sessions:
  - Country Status page: https://app.notion.com/p/3ce8146861518071979ce8ce790e9fa7 (under "IHG Script Changes – Scaling Prep", https://app.notion.com/p/3a381468615181aa97cccc47e6a2990a)
  - Per-country requirements: "Check in setup guide by country", https://app.notion.com/p/32e81468615180dcb772eed63ff1fab5
  Canary has little control over which countries arrive, but the team agreed it needs about a week of lead time per new country.

  ### The 6-stage process and owners
  1. Not Prioritized (~2 wks before training): no GMS Core/Core Plus signup from the country yet. Tay owns moving it to Requirements on signup.
  2. Requirements (1.5 wks): Vibhor + Sebastian Cahill write the country requirements into the setup-guide page.
  3. In Development (1 wk): Connor + Andrea add them to the scripts, then tell Lorena/Luan it's ready to test.
  4. In Testing (0.5 wk): Lorena + Luan test a property on staging and validate with the group.
  5. Active - Monitoring (training day): the whole group runs scripts in prod for the country's first property and iterates.
  6. Active - Automated: Tay marks the country active, scripting continues for later properties, and Tay files tickets for fixes.
  The DB also has a 7th status, "Ready - Not Active" (tested, but no prod property run yet). It isn't in Connor's list.

  ### Thread replies
  - Luan (09-02): Canada, UK and Germany staging tests passed, no new issues.
  - Tay (09-02): these 10 countries hold 5,591 of 6,371 IHG properties and are exempt from the ~2-week lead time: UK, Germany, Australia, Canada, Mexico, Spain, France, Italy, Thailand, Japan. Deployments can agree ~2 weeks for any other country.
  - Vibhor: Spain done before (quick update). Italy "in the next few days".
  - Lorena was out 09-03/04. Luan owns IHG QA while she's away.

  ### Current DB state (IHG Country Readiness, fetched 2026-09-10)
  - Active - Monitoring: US. To-do: remove two fields from the registration card.
  - Ready - Not Active: Australia (not run on a prod property yet). UK (blocker: "Region support").
  - In Testing: Canada (French translations). Germany (German translations + "Region support"). Spain (no requirements linked).
  - In Development: France
  - Requirements: Jordan
  - Not Prioritized: Mexico, Italy, India, Greece, UAE

  ### Gaps worth knowing (my read, not raised in the thread)
  - Thailand and Japan are on Tay's top-10 list but have no row in the DB at all.
  - Italy and Mexico are top-10 but still "Not Prioritized". Vibhor started Italy (checklist "[not complete]"). The Mexico checklist is marked "[NOT READY]".
  - Spain is In Testing but its Country Requirements field is empty. A "Spain … with OCR" checklist exists (https://app.notion.com/p/3cf814686151807282d7d9c53c0ad697) but isn't linked. The older Spain NO-OCR page is marked DO NOT USE.
  - "Region support" blocks both UK and Germany and isn't explained anywhere. If it's an engineering item (e.g. region/state fields in the check-in flow), it may land on our side. Worth asking Connor what it means.
  - Greece has setup checklists (with and without OCR) but is Not Prioritized. Probably fine: that work predates IHG.

  No action required of you in the thread. The Notion DB is the place to check IHG country status from now on.
project: 2026-08-31-ihg
source_id: https://canarytechnologies.slack.com/archives/C0BSBH7BELE/p1788302467604549?thread_ts=1788302467.604549&cid=C0BSBH7BELE
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 10
title: 'Read Connor in #temp-ihg-scripting: IHG rollout ops — Country Status Notion
  page with a 6-stage readiness process and owners'
updated: 2026-09-10 11:23:00
waiting_on: null
waiting_since: null
working_on: false
---

Promoted from the 2026-09-10 awareness report (Saved-for-context (Slack Later, no action)).
https://canarytechnologies.slack.com/archives/C0BSBH7BELE/p1788302467604549?thread_ts=1788302467.604549&cid=C0BSBH7BELE