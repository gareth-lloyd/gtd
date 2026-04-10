---
area: null
contexts: []
created: &id001 2025-06-09 00:00:00
defer_until: null
due: null
energy: null
id: 2025-06-09T0000-try-the-validations-in-a-specific-order
project: null
tags: []
time_minutes: null
title: try the validations in a specific order - authenticate, fetch res, then fetch
  run
updated: *id001
waiting_on: null
waiting_since: null
---

Misleading that fetch run doesn't exist is failing when fetch run failed to work due to authentication

https://app.datadoghq.com/logs?query=%40env%3Aproduction%20%40CTX_account_uuid%3A74c17a21-58c6-4b89-81c0-d1929549ccb5&agg_m=count&agg_m_source=base&agg_t=count&cols=host%2Cservice&event=AwAAAZc6s2lc2p_siAAAABhBWmM2czJ1SEFBRHJyUXJfOEpjVmZ3QVEAAAAkMDE5NzNhYjMtNzlmNi00MTczLWEyNTctYzY3NTQwZDA5YmNmAAAbYQ&fromUser=true&messageDisplay=inline&refresh_mode=sliding&storage=hot&stream_sort=desc&viz=stream&from_ts=1749036033848&to_ts=1749036933848&live=true