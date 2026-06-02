---
area: null
contexts: []
created: 2026-06-02 15:13:58.050184
defer_until: null
due: null
energy: low
id: 2026-06-02T1513-investigate-salesforce-reuqest-volumes
order: null
output: |
  ## Agent run 2026-06-02T15:45 (Datadog investigation)

  ### TL;DR
  The Salesforce API-volume spike that hit the governor limit on May 27 is NOT
  cohort creation (Martin/Tincho's theory). The dominant Canary-origin Salesforce
  consumer is a BROKEN AIRBYTE SALESFORCE SOURCE SYNC that has been falling back
  from the Bulk API to per-record REST ("STANDARD") calls continuously since
  ~May 18, 2026. Martin was right that it's READS not updates — but wrong that
  his cohorts were the cause.

  ### What the data shows (Datadog, verified)
  - service:airbyte-worker, host i-0e20e371371a5933e, EC2 instance
    `prd-uswest2-dw-airbyte` (tf_workspace prd-uswest2-core0-data-warehouse,
    image airbyte/worker:0.50.44). This is the "Canary Airbyte Integration /
    Canary Tech Analytics Sync" Gerson named.
  - Log fingerprint, ~continuous: "source > switch to STANDARD(non-BULK) sync.
    Because the SalesForce BULK job has returned a failed status".
      - FIRST appears 2026-05-18 (zero occurrences in the Apr 25–May 18 window) →
        a degradation that started ~May 18, not a one-off.
      - Volume since: ~2,300–2,900/day. May 27 = 2,345.
  - May 27 hourly: steady ~123/hr EXCEPT a dip 07:00–12:00 UTC (down to 2–5/hr) —
    consistent with Salesforce throttling/rejecting requests once the daily API
    request limit was reached, then recovering.
  - The same Airbyte instance also runs a Postgres CDC→S3 replication (event_event
    etc.) and Salesforce object streams (saw salesforce_OpportunityLineItem;
    Account/Opportunity/Contact also synced) → S3 (airbyte/replicated).
  - Recurring ERROR on the SF source: "Invalid date-time: Invalid timezone offset:
    0000" (DateTimeValidator, ~109 hits / 30 min) — likely the trigger that makes
    the Bulk job fail and forces the per-record STANDARD/REST fallback.
  - Canary backend (service:canary-command/cronjob) emitted only ~521
    salesforce-mentioning logs over 2 days — NOT a meaningful writer. The only
    backend code path that writes Salesforce Account objects is ad-hoc tmp/
    remediation scripts (wyn/bw portfolio + audit) — no evidence they ran at
    volume on May 27.

  ### Why it inflates request volume (inferred, high confidence)
  Bulk API = one job per stream. STANDARD/REST fallback = paginated GETs per
  record set, so request counts explode. Sustained since May 18, this is by far
  the largest Canary→Salesforce API consumer and the most likely cause of
  breaching the API-request governor limit on May 27. These are GET/query
  (reads) — matching Martin's "read only" comment; Gerson's "Account updates" is
  likely loose wording for API activity on Account objects.

  ### Where Tincho's explanation doesn't line up
  - He attributed the volume to cohorts he created via salesforce id and said
    "not really on the 27th." Both true and beside the point — cohort creation is
    not the driver.
  - Real factor = broken Airbyte SF source (Bulk→REST fallback since ~May 18).

  ### Suggested next steps (NOT actioned — for user)
  1. Fix the Airbyte Salesforce source connection so it uses Bulk API again. Root
     cause likely the malformed datetime record ("Invalid timezone offset: 0000")
     or a connector-version issue (worker 0.50.44). While broken it hammers REST.
  2. Reply to Gerson with the window: degradation began ~May 18; limit likely hit
     May 27 ~07:00–12:00 UTC. Confirm it's reads (source pull), not writes.
  3. Owner is the data-warehouse/Airbyte side, not the cohort/backend work.

  NOTE: did not check Groundcover — Airbyte runs on EC2 and logs to Datadog, where
  the answer was conclusive. Slack thread images (Gerson's screenshots) not opened.
project: null
source_id: null
tags: []
time_minutes: 5
title: investigate salesforce reuqest volumes
updated: 2026-06-02 15:45:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C08RJU9Q7FV/p1780067490269399

Tincho's don't line up. look for other factors in datadog/groundcover