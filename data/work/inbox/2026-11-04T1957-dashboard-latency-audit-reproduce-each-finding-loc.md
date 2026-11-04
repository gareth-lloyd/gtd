---
area: null
completed_at: null
contexts:
- deep
created: &id001 2026-11-04 19:57:26.337946
defer_until: null
due: null
energy: high
id: 2026-11-04T1957-dashboard-latency-audit-reproduce-each-finding-loc
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: 240
title: 'Dashboard latency audit: reproduce each finding locally and file tickets to
  the owning pods'
updated: *id001
waiting_on: null
waiting_since: null
working_on: false
---

Follow-up to the 2026-11-04 dashboard latency audit (one item, nine findings).

## Action
1. For each finding, reproduce locally with a query-count assertion (django_assert_num_queries or CaptureQueriesContext) against seeded data, so the ticket carries a before/after number rather than a reading of the code.
2. File one ticket per finding to the owning pod (map paths via CODEOWNERS), with the file:line, the repeated SQL, the fix, and the impact estimate. Link the audit page.

## Findings to ticket (owner area -> endpoints)
- Messaging: GET /api/chat/threads (fresh Reservation query per thread discards prefetch), GET /api/chat/search (single 12.5s UNION/LIKE query), GET /api/chat/messages (hotel+config join on every row, missing select_related)
- Contracts / auths: GET /api/contracts (combiner refetch, 377 q/req, Jinja compiles; plus Count("signers") soft-delete bug at api_views.py:691), GET /api/authorizations (COUNT over UNION for num_pages, per-row payment method fetch)
- Tipping: GET /api/hotels/{slug}/wallets and /departments (per-wallet payout vendor chain, terms latest())
- Arrivals: GET /api/hotels/{slug}/check_ins/search (3.5s count, missing relations block)
- Ticketing: GET /api/ticket_gateway/recommended_tickets (unbounded queryset, GFK N+1, 890 q/req)
- Platform: SELECT 1 health check reset on nested @readonly_database (readonly_database.py:40-41)

## Sources
- Audit page (private until shared): https://claude.ai/artifact/QzNanTU2XKUkdEscaJYJUD
- Full evidence in the source GTD item output: data/work/inbox/2026-11-04T1921-claude-made-that-discovery-so-easy-just-then-worth.md
- hotels/{slug} fix already in flight: https://github.com/canary-technologies-corp/canary/pull/63267
- Discovery thread: https://canarytechnologies.slack.com/archives/C019TQLQDJP/p1793811389605919?thread_ts=1793808707.680909&cid=C019TQLQDJP