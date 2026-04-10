---
area: null
contexts: []
created: &id001 2025-08-25 00:00:00
defer_until: null
due: 2025-08-25
energy: null
id: 2025-08-25T0000-check-that-404s-are-reduced-after-deploy
project: null
tags:
- focus
time_minutes: null
title: Check that 404s are reduced after deployment of this work
updated: *id001
waiting_on: null
waiting_since: null
---

https://linear.app/canary-technologies/issue/RES-5074/confirm-were-properly-handling-jonas-chorum-changes#comment-4974897d

https://app.datadoghq.com/logs?query=%40route%3A%22%5Erest%2Fv1%2Fcheck_ins%2F%3Cstr%3Ahotel_slug%3E%2F%3Cstr%3Aconfirmation_id%3E%2Fexternal_urls%22%20%40code%3A404&agg_m=count&agg_m_source=base&agg_t=count&clustering_pattern_field_path=message&cols=host%2Cservice&messageDisplay=inline&refresh_mode=sliding&storage=hot&stream_sort=desc&viz=stream&from_ts=1754300547219&to_ts=1754905347219&live=true