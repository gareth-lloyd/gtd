---
area: null
contexts: []
created: 2026-05-19 14:45:01.219858
defer_until: null
due: null
energy: low
id: 2026-05-19T1445-search-notion-to-see-what-kind-of-uptime-slas-we-a
order: -21
output: "## Agent run 2026-05-19T15:10\n\nNavid's question (#C02MVAEJD0Q, ts 1779169923.053429):
  \"What uptime /\navailability SLAs do we typically commit to with our enterprise\ncustomers?
  (talking to a vendor, wants to ensure it lines up.)\"\n\nFindings from Notion/Drive
  search:\n- Standard/canonical Canary SLA: monthly uptime >= 99.9%\n  (Canary_Technologies_SLA_7.10.19.pdf,\n
  \ https://drive.google.com/file/d/1Sf2tOVyZWXL07APOfVMWyGP5-7CroIpr/view)\n- Wyndham
  SOW: Monthly Guaranteed Uptime >= 99.9%; Service Credit =\n  Monthly Plan Price
  x ((Outage minutes x 5) / minutes in month)\n  (https://docs.google.com/document/d/1HqQSXq5Nu0yjI5h1QM9y4qBZXtsEa4xp)\n-
  WHRO/Wyndham joinder negotiated higher: >= 99.95% monthly\n  (https://docs.google.com/document/d/1RPInKpUURQEHRuheK-AS5X8J0tnzglEq)\n-
  Best Western MSA: credit Monthly Cap = 50% of Monthly Plan Price;\n  scheduled maintenance
  excluded from Outage, capped <= 5 hrs/month;\n  72 hrs notice if planned downtime
  <= 2 hrs, else 7 business days\n  (https://docs.google.com/document/d/1f73o9u-_Aw5BvgDfrvqfM6zjhgzsSJbG)\n\nBottom
  line: standard commitment is 99.9% monthly uptime; some\nenterprise contracts (certain
  Wyndham entities) negotiate up to 99.95%.\nService credits and maintenance exclusions
  vary per contract.\n\nDrafted a Slack reply for Navid (below) — NOT sent, awaiting
  Gareth's\ngo-ahead.\n\n--- DRAFT SLACK REPLY (thread on ts 1779169923.053429) ---\nOur
  standard/canonical SLA commits to 99.9% monthly uptime. That's the\nbaseline in
  our standard SLA doc and in most enterprise contracts\n(e.g. the Wyndham SOW). A
  few negotiated enterprise deals go higher —\nsome Wyndham entities (WHRO joinder)
  are at 99.95%. Service-credit\nmechanics and maintenance exclusions vary by contract:
  e.g. Best\nWestern caps credits at 50% of monthly plan price and excludes\nscheduled
  maintenance (<=5 hrs/month, with advance notice). So when\ncomparing to the vendor:
  99.9% is our typical commitment, 99.95% is\nthe high end we've agreed to. Happy
  to pull the exact clause for a\nspecific customer if useful.\n--- END DRAFT ---\n\nReply SENT to Navid's thread with Gareth's explicit approval, citing sources: https://canarytechnologies.slack.com/archives/C02MVAEJD0Q/p1779191840490709?thread_ts=1779169923.053429&cid=C02MVAEJD0Q\n"
project: null
source_id: null
tags: []
time_minutes: 5
title: Search notion to see what kind of uptime SLAs we agree to with enterprise customers
updated: 2026-05-19 14:57:04.598150
waiting_on: null
waiting_since: null
working_on: false
---

respond to Navid https://canarytechnologies.slack.com/archives/C02MVAEJD0Q/p1779169923053429