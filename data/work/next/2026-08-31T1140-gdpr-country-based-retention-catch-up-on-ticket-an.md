---
area: null
completed_at: null
contexts: []
created: 2026-08-31 11:40:42.813502
defer_until: null
due: null
energy: low
id: 2026-08-31T1140-gdpr-country-based-retention-catch-up-on-ticket-an
order: null
output: |
  ## Agent run 2026-08-31T14:52 — catch-up: EMEA "GDPR: Country based retention"

  ### Where it stands
  - **Project:** [GDPR: Country based retention](https://linear.app/canary-technologies/project/gdpr-country-based-retention-d69330afb774) — team EMEA, lead **Marta Ochowicz Malarz**, initiative *EMEA - Compliance & Data Privacy*, label 26Q3B. Status **Backlog**, start 2026-08-27, target **2026-09-10**. No milestones, **no status updates ever posted**, no project comments.
  - **Contents: one ticket.** [EMEA-350 [Eng design] GDPR: Country-based default retention](https://linear.app/canary-technologies/issue/EMEA-350) — Todo, 3 pts, assigned Marta, High. Created 17 Jun, bounced Backlog↔Todo↔To Refine five times, moved into this project by James Saram on 3 Aug ("we're going to tackle it as a much wider delivery"). Not started. So the 10 Sep target is realistically an *eng-design* date, not a rollout date — nothing else is ticketed here.
  - Same work is referred to elsewhere as **PMS-9794** ("region-based default retention") — SEC-515 and the eng design still cite that ID. Worth collapsing the naming.

  ### The two design artefacts
  1. **[PRD: Country defaults](https://app.notion.com/p/3c18146861518041b442e32877e5c80d)** — owner **James Saram**, Draft, last touched 19 Aug. Sits under EMEA EPD Pod. Sourced from the [Country Data Breakdown DB](https://app.notion.com/p/28e8146861518095bf9df781da1b74bb).
  2. **[Scoped Obfuscation Retention Policies — Eng Design](https://app.notion.com/p/3ae814686151817a9a1bd6c2d3c0287a)** — Draft for discussion, 31 Jul. This is the mechanism; the PRD is the values.

  ### ⚠️ The two documents contradict each other on the core number
  - **Linear project description** (Marta, edited to 27 Aug): default is **30 days after check-out**, per ROPA, anchored on checkout, applied opt-out with CSM pre-notification.
  - **PRD** (James, 19 Aug): explicitly the opposite philosophy — *"Retention defaults maximise data availability, not minimise it… per country we default to the longest retention a hotel can legally justify."* Greece 3,650d; Austria/NL 2,555d; Ireland 2,190d; Spain 1,095d; Denmark **730** (statutory max); Germany **450** (intl only); France 180; Sweden 90; Hungary/Italy/Portugal **0**; **EU fallback 1,095d**; **non-EU = no retention period at all** (no purge).

  That is 30 days vs ~3 years for an unmapped EU hotel. Both docs are live and neither references the other's number. **This is the thing to resolve first** — it changes the Legal ask, the CSM notification wording, the rollout risk profile, and what SEC-515 can publish. You are named (with Blake) as final approver before full EU rollout, so it lands on you either way.

  ### Design shape (eng design, for context)
  Split **policy** (category + lag) from **rules** (conjunctions: hotel ∧ portfolio ∧ brand ∧ country ∧ country_group) from **resolution** (CSS-style specificity, tiers `hotel > portfolio > brand > geo`, ties → most restrictive + conformity warning), then **clamp to code-defined jurisdiction bounds** (`OverridePolicy.FINAL`) curated with Legal. Result materialised as `EffectiveHotelPolicy` (hotel × category → lag + provenance), recomputed on change plus nightly reconcile. **Canary resolves, Gateway executes** via the existing account PATCH channel; gateway admin FK becomes managed/read-only. Models move to a new shared Django app (first one installed in both services) alongside EMEA-354.

  ### Hard preconditions / risks already documented
  - **Snowflake deletion job hard-codes `lag = 7 days`** (`gdpr/services/snowflake_deletion.py:72`): any account on a non-7-day window gets **no warehouse cleanup** — pre-redaction copies persist. Must be generalised before rollout (this is exactly what SEC-500's durability test catches). Same literal-7-day pattern in Opera fetch exclusion (`vendors/integrations/opera/fetch/reservation.py:203`).
  - **Fetch-window resurrection**: if effective retention < vendor historical fetch window, re-fetches restore what the sweep just scrubbed (PMS-9787).
  - **Throughput**: Martijn (4 Aug) — ~10,000 reservations/day will need obfuscating; the sweep currently averages ~330. Expects timeouts like the take-down requests; asked for a perf ticket. Scale of the migration: ~4.2M EU + ~67.5M US guests currently on the `Default (none)` no-op (only **9 accounts** genuinely anonymise).
  - **Data quality**: `Hotel.country_code` is optional and needs a backfill; state/city/zip are free text, so v1 conditions are country/country-group only.
  - **Monitoring not built**: [EMEA-601](https://linear.app/canary-technologies/issue/EMEA-601) (alerting on obfuscation failures + EMEA alerts channel) is Todo, and sits in a *different* project (Anonymisation schedule), not this one — despite this project's description depending on it.
  - **[SEC-515](https://linear.app/canary-technologies/issue/SEC-515)** (publish country retention matrix on the security portal, an **IHG contracting requirement**) is Backlog and warns: publish only what the platform *actually enforces*. Today there is no general PII retention control in code — only `id_retention_days` and `authorization_retention_period`. APAC does not purge at all (SEC-519); guest ID images in S3 have no lifecycle expiry.

  ### Scope gap worth noticing
  The project description lists **five** schedules needing a country default (Canary anonymisation, PMS Gateway policy, document retention, audit events, messages). The eng design's v1 has **one** data category, `GUEST_STAY_PII` — and its open question 6 asks whether that's enough. The PRD doesn't cover documents/audit/messages at all. Either the project scope shrinks to the gateway+Canary pair for V1, or the design grows categories. The project's own "Open question" (one window per country vs a grid) is the same question, unanswered.

  ### Open decisions and who owes what
  - **Legal (Tanya):** EU fallback value (1,095d proposed); comfort with hard statutory maxima DE=450 / DK=730 / HU=IT=PT=0; whether non-EU "no purge" is an acceptable interim posture (Australia OAIC, California §1798.90.1 both restrict ID retention).
  - **Sebastian:** matrix coverage incomplete — **Belgium, Poland, Nordics beyond DK/SE missing; Canada and Mauritius WIP**. Must be complete before EU-wide rollout. Also owes the country list per EMEA-350.
  - **Martijn / Enterprise:** `OverridePolicy.FINAL` vs DEFAULT — can a property retain *longer* than its country default (the 3–5yr logbook case)? Plus tier ordering and which brand notion is authoritative.
  - **Eng:** clock start (checkout vs record creation — PRD recommends checkout); local-guest definition varies (FR = residency, AT = nationality).
  - **CS (Nathan):** cohort approval. **You + Blake:** final okay before full EU.
  - **PMS-9793** (national/international split, guest-origin axis, ≥5 origin classes incl. Nordic/GCC) is Backlog and explicitly sequenced *behind* EMEA-350. Still has no owner per the 19 Aug GDPR weekly.

  ### Recent signal
  - Slack #epd-emea-gdpr, 19 Aug (Martijn): *"We're live with the first obfuscated check-in within our Canary application"* — setup is manual, **without any country default** — "which is an upcoming project". Bug-bash across PMS/Gateway/Canary planned ~2 Sep. [link](https://canarytechnologies.slack.com/archives/C0B3EUYPRL4/p1787155252802089)
  - Sebastian's GDPR weekly (19 Aug): RIRA paused; decision *not* to anonymise EU citizens at US properties (flagged as not clear-cut, on the risk register); national-vs-international split spun out as its own workstream, **owner still needed**.
  - Nothing on this project in #epd-emea-gdpr since 21 Aug. No weekly update posted for w/c 26 Aug.

  ### Suggested next actions (not taken — no external writes made)
  1. Get James and Marta in a room on 30-days vs longest-defensible. Pick one, edit the losing doc so there is a single number.
  2. Once settled, send Legal a single grid (country × guest origin × data category) rather than a list — that also answers the project's own open question.
  3. Ticket the Snowflake 7-day generalisation as an explicit rollout blocker in *this* project; today it only lives in prose on EMEA-350.
  4. Decide whether the five-schedule scope is V1 or aspiration, and move the 10 Sep target accordingly (it currently reads as a rollout date with only an eng-design ticket behind it).
  5. Chase Sebastian on BE/PL/Nordics coverage — it's on the critical path for EU-wide.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: gdpr country based retention - catch up on EMEA linear project and design
updated: 2026-08-31 14:46:54.126548
waiting_on: null
waiting_since: null
working_on: false
---