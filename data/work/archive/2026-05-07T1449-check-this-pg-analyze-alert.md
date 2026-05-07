---
area: null
contexts: []
created: 2026-05-07 14:49:38.683189
defer_until: null
due: null
energy: low
id: 2026-05-07T1449-check-this-pg-analyze-alert
order: null
output: "## Agent run 2026-05-07T15:05:00Z\n\n**Verdict: drop the index — it's safely
  redundant.**\n\n### The alert\npgAnalyze flagged `monitoring_monitoredcheckresult_hotel_state_id_df4b37a3`\non
  `public.monitoring_monitoredcheckresult` as unused for 14 days.\nSize: 2.7 GB. (Slack
  thread: C09FHDTT94P / 1776392850.706839.)\npgAnalyze later auto-marked it \"Resolved\"
  but that's just the threshold\nflipping; the index is still the same redundant artifact.\n\n###
  Why it's redundant\nThe model `MonitoredCheckResult` has three indexes:\n1. Django
  auto-FK btree on `hotel_state_id` alone — the 2.7 GB one flagged.\n2. Composite
  `(hotel_state, type, created_at)` (`monitoring__hotel_s_29a59a_idx`).\n3. Unique
  constraint on `(check_run_uuid, hotel_state, type)`.\n\nIndex #2 has `hotel_state`
  as its leftmost column, so Postgres can use it\nfor any query that filters on `hotel_state`
  alone. That makes #1 redundant\nfor read paths.\n\nAuditing all callers in `backend/canary/`
  (services, admin, tmp scripts):\nevery query filters on `hotel_state` together with
  `type` and/or\n`check_run_uuid` — never on `hotel_state` alone. So even without
  the\nleftmost-prefix property, no production query would hit #1.\n\n### Risks /
  caveats\n- Index size is 2.7 GB → use `RemoveIndexConcurrently` from\n  `django.contrib.postgres.operations`
  so the drop doesn't hold an\n  `ACCESS EXCLUSIVE` lock on the table. Standard table-level\n
  \ DROP INDEX would block writes.\n- Foreign-key cascade/PROTECT semantics still
  work without this index;\n  Postgres doesn't require an index on the referencing
  FK column. But\n  deletes from `monitored_hotel_state` would do a seq scan against\n
  \ `monitored_check_result` to validate the PROTECT — current usage\n  rarely deletes
  hotel states, so not a concern, and the composite\n  index covers it anyway.\n-
  The unique constraint on `(check_run_uuid, hotel_state, type)` does\n  NOT cover
  `hotel_state`-only lookups (wrong leftmost column), so we\n  are relying on the
  composite index. Don't drop the composite index.\n\n### Suggested implementation\n1.
  On `MonitoredCheckResult.hotel_state`, set `db_index=False`.\n2. `makemigrations`
  will produce an `AlterField`. Replace the generated\n   index removal with `RemoveIndexConcurrently`
  (and add\n   `atomic = False` to the migration) — see other monitoring/hotels\n
  \  migrations in the repo for the pattern.\n3. Roll it through staging first; pgAnalyze's
  index-usage stats on\n   staging are a useful sanity check before prod.\n\n### Done
  in this run\n- Read Linear issue + Slack thread for context.\n- Reviewed `monitoring/models/monitored_check_result.py`
  and every\n  caller (`monitoring/services/`, `monitoring/admin.py`,\n  `onboarding/services/cohort_hotel.py`,
  `tmp/repeatable/*`,\n  `tmp/onetime/*`).\n- Confirmed no `hotel_state`-only filters;
  composite index covers all\n  callers either by leftmost prefix or full match.\n\nNo
  code changes made. Next step is a small PR per the implementation\nnotes above —
  happy to do that as a follow-up.\n"
project: null
source_id: null
tags: []
time_minutes: 5
title: Check this pg analyze alert
updated: 2026-05-07 14:56:08.619185
waiting_on: null
waiting_since: null
working_on: false
---

https://linear.app/canary-technologies/issue/ENT-5975/review-alert-to-determine-if-index-should-be-dropped