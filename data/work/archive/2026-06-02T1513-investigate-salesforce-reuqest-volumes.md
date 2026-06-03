---
area: engineering
contexts:
- craft
created: 2026-06-02 15:13:58.050184
defer_until: null
due: 2026-06-03
energy: medium
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

  ## Agent run 2026-06-03 (owner + fix routing + drafted reply)

  ### Owner / routing
  - Airbyte data-warehouse instance (Postgres CDC + Salesforce source -> S3) =
    pod-platform (CODEOWNERS: /backend/canary/data_warehouse/ -> pod-platform).
    Route the fix here.
  - In-app SF integration (/backend/canary/salesforce/) = pod-enterprise — loop in
    for context, but not the broken component.
  - Actual Airbyte connection config (streams, SF creds, connector version) lives
    in terraform workspace prd-uswest2-core0-data-warehouse (infra repo, NOT this
    repo). Worker image observed: airbyte/worker:0.50.44 (old).

  ### Root-cause hypothesis for the fix
  "Invalid date-time: Invalid timezone offset: 0000" = classic Airbyte SF-source
  bug: a SF datetime field returns a zero/invalid TZ offset, schema validator
  rejects it, Bulk query job fails, connector falls back to per-record REST.
  Fix order: (1) upgrade Airbyte SF source connector; (2) exclude offending
  stream/field; (3) short-term pause/slow the connection to stop burning quota.

  ### Slack reply — DRAFTED, NOT SENT (awaiting Gareth's go-ahead)
  Destination: thread in C08RJU9Q7FV (reply to Stephanie/Martin). Content covers:
  not cohorts; Airbyte SF source Bulk->REST fallback since ~May 18 (~2,400/day);
  likely breached API limit May 27 (~07:00-12:00 UTC dip); these are READS not
  updates; trigger = malformed datetime; fix sits with pod-platform.

  ### Slack reply — SENT 2026-06-03
  Posted to thread C08RJU9Q7FV:
  https://canarytechnologies.slack.com/archives/C08RJU9Q7FV/p1780478971046909

  ### Linear search for existing reports (done 2026-06-03)
  NO open ticket covers this specific issue (SF source Bulk->REST fallback since
  ~May 18 -> API-limit breach May 27). Closest:
  - DATA-752 (In Progress, Data Platform, Incident) = Airbyte pod scheduling +
    Snowflake-destination Crossplane errors. DIFFERENT failure, not a dup, but the
    active Airbyte-health incident.
  - PLAT-3562 (Backlog) = Upgrade Airbyte to 2.0 — relevant to the FIX (worker is
    old 0.50.44; datetime-parse bug fixed upstream).
  - DATA-73 (Done Jan 2026) = SF OpportunityLineItem sync silently broke before
    (precedent). DATA-77 (Done) = prior SF/Airbyte error sweep.
  - Backend SF rate-limit theme recurring + unsolved: TOOL-35 ("long term solution
    for SF rate limiting") was CANCELLED; ENT-1984/ENT-5353 cancelled/dup.

  ### Ownership CORRECTION (supersedes "pod-platform" above)
  Live Airbyte connections/pipeline operated by DATA PLATFORM team (DATA-* issues;
  Carmela Beiro / Johannes Schmidt / Maycon Viana Bordin; "Airbyte improvements"
  project) — NOT pod-platform. pod-platform owns only backend data_warehouse/ code.
  Route the fix to Data Platform.

  ### Still open
  - Groundcover corroboration (task body asks for it) — NOT yet done.
  - ENT-6367 read-only SalesforceContact prod lookup — NOT done (needs approval).
  - File new Data Platform ticket — DONE: DATA-862 (High, Triage, no assignee,
    Incident label, Airbyte improvements project; related DATA-752/PLAT-3562/DATA-73)
    https://linear.app/canary-technologies/issue/DATA-862
  - Groundcover corroboration (task body asks for it) — NOT yet done.
  - ENT-6367 read-only SalesforceContact prod lookup — NOT done (needs approval).

  ## Agent run 2026-06-03 (assumption challenge — CORRECTIONS)
  Adversarial re-check broke several earlier claims; DATA-862 rewritten to match:
  - "Began ~May 18" = FALSE. Log-retention artifact (airbyte-worker hot logs ~15d;
    floor slid May 18 -> May 19 overnight). Onset unknown, likely older.
  - Concrete bulk failure = HTTP 400 Bad Request on Salesforce Bulk API v2
    /services/data/v57.0/jobs/query -> REST fallback. NOT a rate-limit. Airbyte
    never logs 429/403/REQUEST_LIMIT; governor breach known only Salesforce-side.
  - May 27 "dip = throttling" = UNSUPPORTED; worker was actively syncing + hitting
    400s during the dip.
  - Backend is ALSO a heavy SF consumer: @logger:canary.salesforce ~100k-190k
    events/day (canary, canary-celery-onboarding, canary-incidents-handler).
    Earlier "backend negligible" was wrong (searched wrong service names).
  - No May 27 spike in Airbyte OR backend; load flat -> multi-factor / chronically
    near daily ceiling. Airbyte = a contributing factor, NOT proven sole cause.
  - DateTimeValidator "Invalid timezone offset: 0000" may be independent of the 400.
  NET: identified A real issue (chronic Airbyte bulk-API failure -> REST fallback),
  not provably THE cause of May 27. Missing: 400 response body (root cause) +
  per-consumer API-call quantification.
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: null
title: Investigate salesforce reuqest volumes
updated: 2026-06-03 12:30:11.911833
waiting_on: null
waiting_since: null
working_on: true
---

https://canarytechnologies.slack.com/archives/C08RJU9Q7FV/p1780067490269399

Current hypotheses don't line up. look for other factors in groundcover