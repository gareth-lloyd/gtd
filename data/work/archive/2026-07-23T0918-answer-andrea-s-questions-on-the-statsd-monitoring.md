---
area: null
contexts:
- react
created: 2026-07-23 09:18:30.309852
defer_until: null
due: null
energy: medium
id: 2026-07-23T0918-answer-andrea-s-questions-on-the-statsd-monitoring
order: null
output: |
  ## Agent run 2026-07-23T13:45:00+03:00

  Found Andrea's two unresolved inline comments on the Notion proposal
  (https://app.notion.com/p/canarytechnologies/Monitored-Hotel-State-Monitoring-Dashboards-Proposal-3a581468615181afae66c8af7d8e3709),
  researched answers in the codebase, and drafted replies below. NOT posted —
  posting Notion comments needs your explicit approval. Say the word and I can
  post them, or paste them yourself.

  ### Q1 — "How does cohort size factor in?"
  (anchored on the coverage gauge bullet; comment link:
  https://app.notion.com/p/3a581468615181afae66c8af7d8e3709?d=3a58146861518087bd4a001c506b9e4f&pvs=42#c3891a465ce24516999345c7a55fe22c)

  Draft reply:

  > The cohort is the denominator. Each run first resolves the list of hotels it's
  > *supposed* to check from Salesforce (past go-live / training completed —
  > `CohortHotelService.list_salesforce_account_ids_which_require_checking`), then
  > works through it with a 3-worker threadpool. The run can end before finishing —
  > the list is shuffled precisely so every hotel still gets covered eventually
  > across runs — which means "hotels actually checked" can quietly fall below
  > cohort size. Emitting both as gauges is what gives dashboard B2 its coverage
  > ratio (checked ÷ cohort): it distinguishes "the fleet is healthy" from "we only
  > checked 60% of the fleet this run, so dashboard A is lying". A sudden move in
  > cohort size itself is also a signal on its own — it means the Salesforce-side
  > cohort resolution changed or broke, which would otherwise silently shrink the
  > monitored fleet.

  Grounding: backend/canary/monitoring/management/commands/cron_monitor_hotels.py
  (shuffle + threadpool, comment says the job "sometimes ends before all hotels
  are checked"); backend/canary/onboarding/services/cohort_hotel.py:657.

  ### Q2 — "what are 'activity metrics'?"
  (anchored on "Activity metrics" in Related follow-ups; comment link:
  https://app.notion.com/p/3a581468615181afae66c8af7d8e3709?d=3a581468615180609c5f001c78546028&pvs=42#39cb9f9190634941b1b00db224c90e7d)

  Draft reply:

  > Sloppy shorthand on my part — I mean the monitored checks that measure recent
  > guest/reservation *activity* rather than static configuration:
  > `reservation_arrivals_today` ("Arrivals: Today"),
  > `check_in_n_completed_last_7_days` ("Completed Check-ins — last 7 days"), and
  > `reservation_events_last_24_hours`. They exist to prove data is actually
  > flowing from the PMS. Unlike config checks (Twilio configured, SSO ID set),
  > they can legitimately flip healthy↔unhealthy on day/timezone boundaries or at
  > genuinely quiet properties — zero arrivals today doesn't necessarily mean
  > broken. The tension is that they're in the critical set for some onboarding
  > types (e.g. Wyndham MSA), so they drive the roll-up state and would pollute
  > the "newly-broken checks" widget — hence the follow-up: debounce them (e.g.
  > only treat as unhealthy after N consecutive failing runs) before they feed
  > alerting.

  Grounding: backend/canary/monitoring/models/monitored_check_type.py;
  backend/canary/onboarding/models/property_configuration_processes.py:1614
  (Wyndham MSA critical_check_types includes both activity checks).

  Slack thread for context: https://canarytechnologies.slack.com/archives/D061NMRMFB3/p1784736196376769
project: null
source_id: https://canarytechnologies.slack.com/archives/D061NMRMFB3/p1784736196376769
tags:
- morning-gtd
- slack
time_minutes: 15
title: Answer Andrea's questions on the statsd/monitoring doc
updated: 2026-07-23 13:53:29.361418
waiting_on: null
waiting_since: null
working_on: false
---

Andrea read the doc over and "added a few questions about some specifics you mentioned".
https://canarytechnologies.slack.com/archives/D061NMRMFB3/p1784736196376769