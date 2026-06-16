---
area: null
contexts:
- react
created: 2026-06-16 11:31:36.255973
defer_until: null
due: null
energy: medium
id: 2026-06-16T1131-respond-on-data-862-salesforce-bulk-api-job-limit
order: null
output: ''
project: null
source_id: https://linear.app/canary-technologies/issue/DATA-862/salesforce-airbyte-source-chronically-failing-bulk-api-400-on
tags:
- morning-gtd
- linear
time_minutes: 15
title: 'Respond on DATA-862: Salesforce Bulk API job-limit fallback (Airbyte)'
updated: 2026-06-16 11:31:36.323800
waiting_on: null
waiting_since: null
working_on: false
---

@glloyd @rami tagged: 400s are LIMIT_EXCEEDED (max 10k bulk v2 query jobs/24h) forcing per-record REST fallback, inflating SFDC API usage. https://linear.app/canary-technologies/issue/DATA-862/salesforce-airbyte-source-chronically-failing-bulk-api-400-on