---
area: null
contexts: []
created: 2026-07-08 21:29:01.997721
defer_until: null
due: null
energy: low
id: 2026-07-08T2129-figure-out-kafka
order: null
output: |
  # Kafka in Canary — findings

  Investigated 2026-07-08. Read the Kafka framework, both produce sites, all
  consumers, config, and the governing rule (`.claude/rules/backend/share-data-with-kafka.md`)
  in the canary monorepo.

  ## Headline

  Kafka here is **new, narrow, and opt-in**. `KAFKA_ENABLED` defaults to
  `False`; the local stack sits behind a `kafka` docker-compose profile.
  Despite a real shared framework there are only **two produce sites** and
  **two first-class topics** (`reservation-created`, `reservation-modified`).
  It is the sanctioned mechanism for *new cross-domain data sharing*, explicitly
  replacing a legacy in-process `Signal()` / callback bus.

  ## How it's set up

  - **Client:** `kafka-python==2.3.0` (pure Python — not confluent-kafka /
    aiokafka / faust).
  - **Serialization:** Apache Avro via `fastavro`, Confluent/Apicurio wire
    format (magic byte + schema id + binary). One legacy raw-JSON path for the
    payment CDC pipeline.
  - **Schema registry:** Apicurio 3.x, read-only from services. `.avsc` files
    code-generate into dataclasses; CI validates schema changes against staging
    + 3 prod registries.
  - **Producer entry:** `KafkaProducerClient.kafka_produce(topic, messages)`
    (`backend/shared/shared/utils/kafka_producer.py`). Topic registry is the
    `KafkaTopic` enum in the same file.
  - **Consumer base:** `BaseKafkaConsumer[Payload]`
    (`backend/shared/shared/utils/kafka_consumer.py`) — an abstract **Django
    management command** with manual offset commits, retry-with-backoff, and
    automatic DLQs (`{topic}-dlq`).
  - **Deployment:** consumers are long-running management commands run as k8s
    pods (manifests live in a separate `canary-kubernetes` GitOps repo).

  ## Concrete end-to-end examples

  **1. Reservation synced → auto-create card authorizations.**
  pms-gateway syncs a reservation from one of 25+ PMS integrations. The load
  path emits an `EventKind`; `KafkaDeliveryService` maps it to
  `reservation-created` and a registered provider serializes a **thin pointer
  event** (`event_sid`, `event_time`, `account_uuid`, `reservation_uuid` — not
  the full reservation). The canary monolith consumes it
  (`reservation-tracking-consumer-group`), takes a distributed lock,
  **re-fetches** the full reservation, matches it against the hotel's
  `ReservationTrackingFilter`s, and if one matches auto-creates a credit-card
  authorization hold.
  Producer: `pms-gateway/delivery/services/kafka_delivery_service.py` →
  Consumer: `canary/authorization/services/reservation_tracking_consumer_service.py`.

  **2. Same event → push mobile key to OpenKey (the fan-out).**
  The *same* `reservation-created` event is independently consumed by a second
  group (`openkey-reservation-consumer`). It checks the hotel has mobile-key
  enabled, re-fetches the reservation, maps PMS status → OpenKey state
  (`in-house` → CHECKEDIN, `checked-out` → delete), and POSTs a push payload to
  `ok-api-v5`. One produced event, two unrelated downstream domains
  (payments/auth vs. mobile keys) — pms-gateway knows about neither.
  Consumer: `canary/mobile_key/services/openkey_reservation_consumer.py`.

  **3. Payment status change → event stream (CDC / Debezium).**
  Two-stage pipeline. Debezium captures row-level DB changes on the payment
  table into a raw CDC topic. A transformer command consumes that, filters for
  real status transitions, enriches with the payment-intent UUID, and
  re-produces a clean `PaymentStatusChangeEvent` (keyed by `payment_uuid` for
  per-payment ordering) onto `payment-status-changes`. A second consumer
  subscribes to it — **but it is in shadow mode (logs only); no business logic
  wired yet.** Value of CDC: DB state transitions become a durable, replayable
  stream without adding produce-calls into transactional payment code.
  `canary/payment_gateways/management/commands/payment_cdc_transformer.py` →
  `payment_event_consumer.py`.

  Reality check: pms-gateway's in-process `EventService` and the
  `@receiver(post_save)` bus are **not** Kafka — they are the legacy patterns
  being replaced.

  ## Kafka vs. a traditional backend worker (Celery)

  Advantages of Kafka:
  - **True fan-out / pub-sub** — produce once, N independent consumer groups
    react, producer never changes (example 2). Celery couples the caller to
    every downstream task.
  - **Cross-service decoupling via a versioned contract** — producers and
    consumers depend only on the Avro schema, so the same event works across
    pms-gateway and the monolith.
  - **Durable log + replay** — events persist and are re-readable by offset;
    new/fixed consumers can reprocess. Celery tasks are consume-once.
  - **Per-key ordering** (e.g. per-`payment_uuid`).
  - **CDC** — turn DB writes into events with zero changes to the write path.
  - **Backpressure** — consumers pull at their own pace; a slow one lags, it
    doesn't drop work.

  Disadvantages of Kafka:
  - **Heavy operational surface** — brokers, Apicurio, Debezium/Connect, health
    probes, DLQs. Celery reuses the broker you already run.
  - **More ceremony per event** — `.avsc` + topic enum + generated dataclass +
    provider + consumer command + CI validation vs. one decorated function.
  - **At-least-once → must design for duplicates** — both real consumers
    re-fetch state and take distributed locks precisely because events may be
    redelivered.
  - **No native scheduling / retry-with-delay / result-return** — Celery gives
    these free; Kafka's retry/backoff/DLQ had to be built into
    `BaseKafkaConsumer`.
  - **Harder debugging + stack fragmentation** — tracing spans producer → topic
    → offset → consumer-group lag → DLQ; and the repo now has three async
    messaging styles (Avro framework, raw-JSON CDC, legacy signal bus).

  Rule of thumb: reach for **Kafka** when *sharing a state change* across
  domain/service boundaries or fanning out to multiple independent consumers;
  reach for a **Celery worker** when *doing your own task* that needs
  scheduling, delayed retries, or a result and that no other domain observes.

  ## The "don't load the full monolith" argument (the strongest one)

  The pioneer's headline advantage. The thrust is about **what a consumer has
  to *be* to react to an event** — really an argument about the contract.

  A Celery worker in a Django monolith must **import and boot the entire
  application** — full app registry, every installed app, all models, all
  import-time side effects — because any task can be dispatched to it. So every
  worker is a full copy of the monolith in memory even for a tiny job.

  Kafka changes the dependency: a consumer's contract with the producer is
  **just the versioned Avro schema**, not Python imports. To understand
  `reservation-created` you need the `.avsc` and the kafka client — none of the
  producer's models, migrations, or dependency soup. So the consumer no longer
  *has to be* the monolith. It can be a lean standalone deployable that boots
  fast, holds a small footprint, has its own dependency set, deploys/scales on
  its own cadence, and isolates blast radius.

  Contrast with what it replaces: the in-process `Signal()` bus required your
  reacting code to live in the **same Python process** as the producer — same
  deployable, same import graph, synchronous. Kafka severs that.

  Honest caveat: today the shipped consumers are `BaseKafkaConsumer` subclasses
  of Django's `BaseCommand`, so *those specific* consumers still boot the
  monolith. The claim is partly about an **affordance the architecture unlocks**
  — but it is already realized at the seam that matters: producer in
  pms-gateway, consumers in canary, two separate services talking only through a
  schema. Once the contract is a schema instead of a shared process, you can
  keep peeling focused consumers off into whatever lean service makes sense.

  ## Open follow-ups (noted, not actioned)

  - Schema-sync CI globs `backend/kafka-schema-registry/*.avsc` but schemas
    actually live at `backend/shared/shared/kafka_schema_registry/schemas/*.avsc`
    — possible stale path; worth verifying the sync workflow fires.
  - `reservation-created` vs `reservation-modified` split is transitional; the
    created-consumer is slated for retirement once modified covers both.
  - Payment event consumer is shadow-mode only — no business effect yet.

  ## Reference

  Full writeup rendered as an artifact:
  https://claude.ai/code/artifact/a0768a66-13c1-4ace-8bf8-8d68b4b2a30c
project: null
source_id: null
tags: []
time_minutes: 5
title: figure out kafka
updated: 2026-07-08 22:25:00.383284
waiting_on: null
waiting_since: null
working_on: false
---