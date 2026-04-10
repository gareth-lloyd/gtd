---
area: null
contexts: []
created: &id001 2025-03-13 00:00:00
defer_until: null
due: null
energy: null
id: 2025-03-13T0000-separate-the-creation-of-onboarding-scri
project: null
tags: []
time_minutes: null
title: Separate the creation of onboarding script runs from the enqueuement of the
  tasks to avoid celery issue.
updated: *id001
waiting_on: null
waiting_since: null
---

https://app.datadoghq.com/logs?query=service%3Acanary-celery%20status%3Aerror%20%40error%3A%22OnboardingScriptRun%20matching%20query%20does%20not%20exist.%22&agg_m=count&agg_m_source=base&agg_q=%40error&agg_q_source=base&agg_t=count&cols=host%2Cservice&fromUser=true&messageDisplay=inline&refresh_mode=sliding&storage=hot&stream_sort=desc&top_n=25&top_o=top&viz=stream&x_missing=true&from_ts=1741797903467&to_ts=1741812303467&live=true