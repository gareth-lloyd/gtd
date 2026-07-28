---
area: null
contexts:
- deep
created: 2026-07-27 14:58:34.095157
defer_until: null
due: 2026-07-28
energy: medium
id: 2026-07-27T1458-follow-up-julius-pms-foundations
order: null
output: |
  ## Agent run 2026-07-28T13:00:00+01:00

  Read the doc: "GFS Reservation & Guest Data Migration: Plan"
  (https://www.notion.so/canarytechnologies/GFS-Reservation-Guest-Data-Migration-Plan-3a5814686151811db820f7ca99b7aacf).
  Status IN REVIEW, owned by PMS Gateway team; you are listed as a reviewer. Companion
  design doc "GFS Reservation Explicit Loading" (https://app.notion.com/p/390814686151807396e4f06bb6f2a5f0)
  holds the "why"; this doc is the "how". Tickets live in the Gateway Foundation Service
  Linear projects.

  ### TL;DR
  Canary keeps a full synced copy of reservation + guest data that pms-gateway already
  owns (~30 columns on guest.Reservation, guest profile on guest.Guest, 6 child copy
  tables). The plan deletes the copy in many small reversible steps: each surface
  explicitly switches to reading Gateway (reservation.get_gateway_reservation() /
  with_gateway_reservations()), and a copied column is dropped only after its last
  reader has switched. End state: a slim reference row (ids, FKs, Canary workflow
  state, query-feeding columns) — NOT full deletion of Reservation (that would mean
  re-keying ~45 FKs; deferred to a possible Phase 8+ decision).

  ### Mechanics
  - Rollout: GfsRolloutService, per-entity + per-hotel + percentage-of-reservations;
    kill switch env var (GFS_ROLLOUT_ENABLED, and GFS_GATEWAY_CONTENT_ENABLED for
    gateway reads) — no deploy needed to revert.
  - Gateway reads are isolated, strict timeout budget (200ms single / 1s bulk up to
    500 reservations — acknowledged as arbitrary/unproven), never raise; failed read
    returns None and code falls back to the local copy.
  - Column retirement is 3-stage: stop ingestion write (wait 2 weeks) -> deprecate
    (loud logging on straggler reads) -> drop. Preceded by a parity audit command
    and zero-reader grep.
  - Phases: 0 foundations (kill switch, shared extractors, parity audit, dashboards);
    1 pilot = front-desk workbench room number; 2 caller upgrades surface by surface
    (check-in is the heaviest); 3 column retirement; 4 move Canary-owned state out
    (checked_in_at -> CheckIn, etc.); Phase 5 (gateway search for query surfaces)
    was struck out / moved to "removed parts", timing open; 6 SQS -> Kafka slim
    events; 7 guest track; 8 endgame.
  - Ingestion converges to a "reactor": only updates the slim row + fires events.

  ### Things relevant to me / worth raising in review
  - Enterprise angle: broadcast eligibility (is_eligible_for_messaging), exact
    phone/email suppression matching, and confirmation-number matching all stay on
    local columns until the deferred Phase 5 gateway-search work lands — that phase
    is currently struck from the plan with timing open, so query-feeding columns
    and the confirmation-numbers table can't finish retiring. Worth asking how/when
    Phase 5 gets rescheduled since it gates completing Phase 3.
  - Local dev: running PMS Gateway alongside Canary becomes increasingly mandatory;
    they commit to convenient bi-directional local setup before steps 3/4. Doc asks
    teams to flag how painful this is now.
  - Latency: +200ms worst case per surface, per-surface decision to bulk-prime or
    flag-gate. Gateway hitting the budgets "out of the box is unproven".
  - Native/walk-in/demo reservations keep local nullable columns (no Gateway push);
    revisit if Mock PMS lands.
  - Warehouse/ETL reads of dropped columns only addressed as a Phase 8 checklist
    item — deprecation window is the notice mechanism.
  - Doc invites inline comments; open questions concentrated in the Phase 5 timing
    and ingestion-route (slim SQS vs Kafka) threads.

  Next action suggestion: follow up with Julius with review comments (esp. Phase 5
  sequencing and enterprise messaging-suppression dependency). No comments were
  posted anywhere — read-only run.
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: 5
title: read pms foundations document
updated: 2026-07-28 14:13:36.621720
waiting_on: null
waiting_since: null
working_on: true
---

https://www.notion.so/canarytechnologies/GFS-Reservation-Guest-Data-Migration-Plan-3a5814686151811db820f7ca99b7aacf?source=copy_link