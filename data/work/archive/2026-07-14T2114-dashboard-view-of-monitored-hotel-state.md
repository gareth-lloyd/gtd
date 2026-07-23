---
area: null
contexts: []
created: 2026-07-14 21:14:37.613965
defer_until: null
due: 2026-07-21
energy: low
id: 2026-07-14T2114-dashboard-view-of-monitored-hotel-state
order: null
output: |
  ## Agent run 2026-07-21T12:53Z

  Explored the Monitored Hotel State platform (`backend/canary/monitoring/`) and
  grounded the findings against live log volume (Groundcover, canary-backend, 3h
  window on 2026-07-21). Recommendations for Datadog dashboards are at the bottom.

  ### How the platform works (the model)

  - **`MonitoredHotelState`** — one row per hotel (OneToOne). Fields: `state`
    (`healthy` / `degraded` / `unhealthy` / `checks_failed`), `latest_check_run_uuid`,
    `go_live`, `attributes` (JSON, e.g. Wyndham phase). This is the *current* rollup.
    Note: **`degraded` is defined in the enum but the service never sets it** — the
    rollup only ever produces healthy / unhealthy / checks_failed. A "degraded" widget
    would read a permanent 0.
  - **`MonitoredCheckResult`** — one row per (check_type, check_run) per hotel. ~45
    `MonitoredCheckType`s (Twilio, payment gateway, guest-journey messaging, SSO, MSA
    products, conformity-to-rule-based-config, voice/WhatsApp/SMS, etc.). `outcome` is
    a `CheckOutcome` (healthy / degraded / unhealthy / unknown / errored / metric_only /
    yes / no). Old runs are consolidated to one run/day after 30 days.
  - **`MonitoredCheckTransition`** — records **only** healthy↔unhealthy flips (added in
    migration 0012, the newest piece). Captures `check_type`, `previous_outcome`,
    `new_outcome`, `hotel_state`, `check_run_uuid`, `result_details`, and `resolved_at`
    (set when a check returns to healthy). Errored/unknown transitions are ignored.

  ### How it runs (the pipeline)

  - Driver: `cron_monitor_hotels` management command. Schedule lives in infra (not in
    repo). It builds a cohort via
    `CohortHotelService.list_salesforce_account_ids_which_require_checking()` (hotels
    past go-live / near training / completed go-live scripts), shuffles them, and runs
    `monitor_expected_onboarding` across a **3-worker threadpool**.
  - Per hotel: run all checks -> `record_monitored_check_results` (bulk_create) ->
    `record_transitions` (diff vs previous run) -> set rollup `state` -> save.
  - Comment in the cron notes the job "sometimes ends before all hotels are checked",
    hence the shuffle — so **daily coverage (hotels checked vs cohort size) is a real
    thing to watch.**
  - A second, async path exists — `refresh_monitoring_state_async` (Celery, ONBOARDING
    queue) via `refresh_monitoring_states_bulk`, plus the `POST /api/monitored_hotel_states`
    refresh/refresh_bulk actions. Currently **idle** (0 `celery.refresh_monitoring_state.*`
    events in 3h) — the cron threadpool is the only live driver today.
  - `GET /api/monitored_hotel_states` (StaffUserGatekeeper, replica-routed) returns state
    + latest results for a set of hotel_ids — this is the branch I'm on (ENT-6891).

  ### ⚠️ Biggest finding for a Datadog build: NO metrics instrumentation

  The monitoring app emits **zero StatsD / custom metrics** — only structlog events.
  So Datadog dashboards must be built from **log-based metrics** (Datadog Log Analytics
  or Groundcover), OR we add a handful of StatsD emissions. Available log events:

  | Event (dot-path)                                    | Useful fields                                   | Live volume (3h) |
  |-----------------------------------------------------|-------------------------------------------------|------------------|
  | `monitored_check_transition.recorded`               | `check_type`, `new_outcome`, `previous_outcome`, `hotel_id`, `check_run_uuid` | 148 |
  | `monitored_check_transition.resolved`               | `check_type`, `hotel_id`, `resolved_count`      | 54 |
  | `monitor_expected_onboarding` (log_elapsed)         | `ms=` CPU time, **sampled 10%**                 | 1021 samples (~10k runs) |
  | `monitor_expected_onboarding.hotel_missing`         | `salesforce_account_id`                         | **115** |
  | `monitor_expected_onboarding.conformity_check_error`| `hotel_id`, `error`                             | **69** |
  | cron threadpool per-hotel error (custom_error_log)  | traceback                                       | ~60 |
  | `celery.refresh_monitoring_state.{processing,success,error}` | `salesforce_account_id`, `check_run_uuid` | 0 (idle) |

  Structlog kwargs land as **indexed structured fields** (verified: `check_type`,
  `new_outcome`, `previous_outcome`, `hotel_id` are all groupable) — so group by those,
  don't free-text. Free-text caveat: `healthy` is a substring of `unhealthy`, so a
  content match on "healthy" over-counts; always filter on the `new_outcome` field.

  ### Grounded reality (3h, 2026-07-21)

  - Fleet check throughput ≈ **10k check-runs / 3h**.
  - Transitions are **dominated by a few flappy checks**, netting near-zero:
    - `guest_journey_messages_enabled`: 87 transitions, only 10 went unhealthy (flapping).
    - `reservation_arrivals_today`: 48 transitions, 0 went unhealthy (day-boundary noise —
      arrivals-today naturally hits 0 across timezones overnight).
    - Genuinely-actionable flips are the long tail: `reservation_events_last_24_hours`,
      `check_in_n_completed_last_7_days`, `guest_journey_messages_scheduled` (each 2 to
      unhealthy). **A raw "transitions" alert would be all noise** — separate
      net-new-unhealthy from flapping.
  - `hotel_missing` at 115/3h and `conformity_check_error` at 69/3h are steady background
    signals worth a visible counter (misconfigured Salesforce links / conformity check
    throwing).

  ### Recommended Datadog dashboard(s)

  Two dashboards: **(1) Fleet Health** (product/onboarding awareness) and **(2) Pipeline
  Health** (is the monitor itself working). Widgets, each with its data source:

  **Dashboard 1 — Monitored Fleet Health**
  1. **State distribution (rollup)** — count of hotels by `state` (healthy / unhealthy /
     checks_failed). *Source gap:* this is DB state, not in logs. Needs either a StatsD
     gauge (see below) or a scheduled query against `GET /api/monitored_hotel_states`.
     Highest-value widget; strongest reason to add instrumentation.
  2. **Unhealthy hotels by check_type** — top-N table. Same source gap → gauge per
     (check_type, outcome). Interim proxy: `recorded` transitions where
     `new_outcome:unhealthy`, grouped by `check_type` (undercounts persistent failures).
  3. **New unhealthy transitions (last 24h)** — timeseries, `monitored_check_transition.recorded`
     filtered `new_outcome:unhealthy`, grouped by `check_type`. This is the clean
     "something newly broke" signal.
  4. **Resolved / MTTR** — `monitored_check_transition.resolved` count, and if we surface
     it, distribution of `resolved_at - created_at` per check_type (how long checks stay
     broken). Requires emitting the duration; today only a resolve event fires.
  5. **Flappy-check leaderboard** — `recorded` grouped by `check_type` where net change ≈ 0
     (high recorded, low sustained-unhealthy). Directly flags noisy checks
     (`guest_journey_messages_enabled`, `reservation_arrivals_today`) for tuning.
  6. **Conformity failures** — `monitor_expected_onboarding.conformity_check_error` count
     over time (rule-based-config check erroring, 69/3h today).

  **Dashboard 2 — Monitoring Pipeline Health**
  7. **Coverage** — distinct `hotel_id` / check_runs per day vs cohort size, to catch the
     "job ended before all hotels checked" case. Best via a gauge of cohort size + runs;
     interim via distinct `check_run` count from transition/elapsed events.
  8. **Freshness** — time since last successful monitoring run (max `_time` of
     `monitor_expected_onboarding*` events). Alert if > expected cron interval → the
     monitor is dead and every other widget is silently stale.
  9. **Per-hotel errors** — cron threadpool error log + `conformity_check_error` +
     `hotel_missing`, as a stacked error timeseries. `hotel_missing` (115/3h) = broken
     Salesforce↔hotel links; a rising trend is a data-quality regression.
  10. **Run duration** — p50/p95 of `monitor_expected_onboarding` `ms`. Caveat: it's
      `time.process_time()` (CPU, not wall-clock) **and 10% sampled** — fine for trend,
      wrong for absolute latency. Flag to whoever builds it.
  11. **Async path health** — `celery.refresh_monitoring_state.{success,error}` ratio.
      Idle today; will matter if the bulk/API refresh path gets used.

  ### Recommended code change to unlock the best widgets (separate ticket)

  Widgets 1, 2, 7 want *current DB state*, which logs can't give cheaply. Add a small
  StatsD emission at the end of `cron_monitor_hotels.handle()` (no schema/migration):
  - `gauge` hotels by `state` (tag: state)
  - `gauge` latest-run outcomes by `check_type` (tags: check_type, outcome)
  - `gauge` cohort size + `count`/`gauge` hotels actually checked this run (coverage)
  - `increment` on transitions by (check_type, new_outcome) at record time
  Per repo rules use `Statsd.metrics.*` (`shared/logging/statsd.py`). This turns 1, 2, 5,
  7 from fragile log reconstructions into first-class Datadog metrics.

  ### Notes / caveats to hand to the dashboard builder
  - `degraded` state is dead — don't chart it (or fix the rollup first).
  - Dedup by `check_run_uuid` when counting runs; transition counts are noisy (flapping).
  - Task asked re: Datadog; live logs were verified in **Groundcover** — confirm these
    structlog events also ship to Datadog Logs (they should) before building there.

  Files reviewed: `monitoring/models/{monitored_hotel_state,monitored_check_result,
  monitored_check_transition,monitored_check_type,check_outcome}.py`,
  `monitoring/services/{monitored_hotel_state,monitored_check_transition,monitored_checks}.py`,
  `monitoring/views/monitored_hotel_states.py`, `monitoring/tasks/refresh_monitoring_state.py`,
  `monitoring/management/commands/cron_monitor_hotels.py`,
  `onboarding/services/cohort_hotel.py`.

  ## Agent run 2026-07-21T13:03Z — FINAL recommendations (refined via live data)

  Between runs, verified PR #49638 ("Make MSA portfolio health signals
  criticality-aware", merged 2026-07-16) against production via debug shell. That
  changed the recommendations materially. Live findings (WYNDHAM_MSA, 4,853 hotels):
  - `state` is no longer saturated: 56% healthy / 44% unhealthy (was ~97% unhealthy).
    The rollup is now criticality-aware, so **`state` is finally a trustworthy signal.**
  - Conformity drift cleared: `conforms_to_rule_based_configuration` 59% → 2.7% unhealthy.
  - The residual 44% unhealthy is REAL: dominated by `has_all_msa_products` (73.8% of
    unhealthy hotels, ~1,571 — a genuine WYNDHAM_MSA critical). `expected_onboarding_
    plans_run` shows 98.7% unhealthy but is NON-critical → drives nothing (red herring).

  ### Governing principle (the big lesson)
  Every widget MUST be **criticality-aware** and **cohort-segmented (by onboarding_type)**
  or it misleads. A naive check-outcome chart shows `expected_onboarding_plans_run` at
  97.7% unhealthy and triggers a false fire drill, while burying the real driver. Global
  fleet % is meaningless — brands have different critical sets.

  ### Dashboard A — Monitored Fleet Health (product/onboarding awareness)
  - A1 (top-line): hotels by `state`, split by onboarding_type. `state` is trustworthy now.
  - A2: top CRITICAL-check failures per cohort (ranked # unhealthy, latest run). Critical
    types only — this is where has_all_msa_products surfaces.
  - A3: non-critical WATCH panel, muted + labelled "informational, does NOT affect health"
    (expected_onboarding_plans_run, conformity, twilio brand/campaign). Stops re-panic.
  - A4: newly-broken CRITICAL checks (24h) from `monitored_check_transition.recorded`
    (new_outcome:unhealthy), critical types, minus the flappy activity checks.
  - A5: critical-unhealthy % trend per cohort (confirms the #49638 gain holds).

  ### Dashboard B — Monitor Pipeline Health (is the monitor trustworthy?)
  - B1: freshness/heartbeat — time since last run (alert > cron interval).
  - B2: coverage — hotels checked vs cohort size/day (cron "ends early" risk).
  - B3: run errors — threadpool errors + conformity_check_error (69/3h) + hotel_missing
    (115/3h, = broken Salesforce↔hotel links).
  - B4: flapping-check leaderboard (high churn, net-zero): guest_journey_messages_enabled,
    reservation_arrivals_today — flag for debounce.
  - B5: stuck-transition backlog — open unhealthy transitions on now-healthy hotels
    (~686 rows fleet-wide / 435 cohort; post-deploy leak ~0, so resolve-path fix works).
  - B6: run duration p50/p95 (⚠️ CPU-time + 10% sampled — trend only).

  ### P0 enabling change (do first): add StatsD to cron_monitor_hotels.handle()
  Logs can't cheaply express current DB state OR the critical/non-critical distinction —
  which is exactly what A1/A2/A5/B2 need. Emit (via `Statsd.metrics.*`, no migration):
  - gauge hotels by (onboarding_type, state)
  - gauge CRITICAL-only check unhealthy counts by (onboarding_type, check_type)
  - gauge cohort size + hotels checked (coverage)
  - increment transitions by (check_type, new_outcome, is_critical)

  ### Anti-patterns to avoid (hard-won)
  1. Never chart raw check-outcome % without the critical filter (the 97.7% panic).
  2. Never alert on transition counts without excluding flappy activity checks.
  3. Never show a single global fleet % — segment by onboarding_type.
  4. Don't chart `degraded` (dead enum value, never set).
  5. Confirm these structlog events reach Datadog Logs (verified live in Groundcover).

  ### Related follow-ups surfaced (not dashboards)
  - has_all_msa_products failing on ~1,571 Wyndham MSA hotels — product/onboarding review
    (real config gap vs over-strict check).
  - Activity metrics (reservation_arrivals_today, check_in_n_completed_last_7_days) are
    critical AND flappy — main source of remaining transition churn; consider debounce.
  - Stuck-transition backlog cleanup (~686 rows) — the deferred opt-in script from #49638;
    size by DISTINCT hotels (PR cited 157 hotels; my count was transition rows).
project: 2026-04-10T0840-ticket
source_id: null
tags: []
time_minutes: 5
title: 'Explore the Monitored Hotel State platform, along with monitored check transitions.
  Output: recommend useful datadog dashboard outputs for awareness and monitoring.'
updated: 2026-07-22 16:40:28.745281
waiting_on: null
waiting_since: null
working_on: false
---

/debug_in_shell if necessary to check real values.