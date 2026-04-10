---
area: null
contexts: []
created: &id001 2025-03-13 00:00:00
defer_until: null
due: null
energy: null
id: 2025-03-13T0000-ticket-fix-json-serialization-error
project: null
tags: []
time_minutes: null
title: 'ticket: fix json serialization error'
updated: *id001
waiting_on: null
waiting_since: null
---

Trying to serialize a set during event creation.

https://app.datadoghq.com/logs?query=%40CTX_onboarding_script__plan_names%3A%2A%20service%3Acanary-celery%20status%3Aerror&agg_m=count&agg_m_source=base&agg_q=%40error&agg_q_source=base&agg_t=count&cols=host%2Cservice&event=AwAAAZWLfk6T-N6oVAAAABhBWldMZmxJQkFBQ1BGeFVnTFJGMDlnQUwAAAAkMDE5NThiODAtY2U1Ny00Mzk5LThhMzAtYmM4NzcxYzQ4ZDBjAAedZA&fromUser=true&messageDisplay=inline&panel=%7B%22queryString%22%3A%22%40error%3A%5C%22TypeError%28%27Object%20of%20type%20set%20is%20not%20JSON%20serializable%27%29%5C%22%22%2C%22filters%22%3A%5B%7B%22isClicked%22%3Atrue%2C%22source%22%3A%22log%22%2C%22path%22%3A%22error%22%2C%22value%22%3A%22TypeError%28%27Object%20of%20type%20set%20is%20not%20JSON%20serializable%27%29%22%7D%5D%2C%22timeRange%22%3A%7B%22from%22%3A1741797918000%2C%22to%22%3A1741812318000%2C%22live%22%3Atrue%7D%7D&refresh_mode=sliding&storage=hot&stream_sort=desc&top_n=10&top_o=top&viz=query_table&x_missing=true&from_ts=1741797903467&to_ts=1741812303467&live=true