---
area: null
contexts:
- consume
created: 2026-04-29 12:47:56.473163
defer_until: null
due: null
energy: low
id: 2026-04-29T1247-get-up-to-speed-on-step-configurator
order: 4
output: |
  ## Agent run 2026-05-06T13:03:48Z

  Pulled Notion page "Step Configurator Approach" + related Linear projects via notion-context skill.

  ### What it is
  - A framework for the mobile arrival experience where guest journeys are composed of configurable, ordered "steps" with shared state, completion semantics, and progression logic — designed to be platform-agnostic.
  - Three-layer model:
    1. **Step framework** — data model + business logic + save/progression infra
    2. **Guest experience app** — configures which steps run, applies enterprise/regional templates
    3. **Front-end product UI/UX** — kiosk, mobile web, mobile SDK consume the ordered step list
  - Solves needing to flex per country/brand: regional compliance, per-brand or per-property variations.

  ### Proposed approach
  - Step framework owns "is this step finished?" semantics. A/D team builds per-step logic (e.g. reg card finished = submitted and saved).
  - Configuration tiers: **Brand (in code)** → Sub-brand (lock-down point) → Region → Property → Platform. Customers configure only below sub-brand.
  - APIs expose step state / progression / completion. Consumed by Mobile SDK + at least one other surface (kiosk, web, tablet).
  - A self-service flow builder for the CS team is being defined separately.

  ### Status & owners
  - Approach doc reads as planning / Q1 OKR scoping — not a final design.
  - Migration project ("Migrate hotels to flexible check-in v3") is in Implementation, on-track. Lead gpercu@canarytechnologies.com.
  - Self-service flow builder: Vibhor Sachdeva, Product Definition, due 2026-05-29.
  - Roadmap: M1 step framework, M3 mobile check-in on framework, M5 guest experience layers, M6 full migration.

  ### Decisions / constraints
  - Brand-level config lives in code, not customer-adjustable settings.
  - Focus is kiosk *supporting* guest experience rather than migrating kiosk itself now.
  - Kiosk Step Framework Shim is paused on dependencies.

  ### Open threads
  - Guest Experience App design doc is a stretch / aspirational KR4 — not yet written.

  ### Related Linear / docs
  - **DSN-1782** Step Configurator builder — design work by Miguel Santana, started 2026-04-09.
  - **AD-6865** Add generic step configurator — Matthew Jeffery, framework-level ticket.
  - **Web check in step configurator builder** — non-eng builder for web check-in flows.
  - **ENT-6100** Create new "rollout recipe" concept — my current branch; rollout-recipe concept likely intersects with the template/configuration tiers.

  ### Connection to current work
  My active branch (`glloyd/ent-6100-create-new-rollout-recipe-concept`) sits in the same conceptual space as the configuration-tier model (Brand → Sub-brand → Region → Property → Platform). Worth checking how rollout recipes relate to enterprise/regional templates referenced in the approach doc.

  ### Nothing found for
  Dedicated Slack threads or Notion design follow-ups beyond the primary page. Search returned only Linear hits.

  Primary source: https://www.notion.so/canarytechnologies/Step-Configurator-Approach-2e381468615180018a40c532b2f0e4c1
project: 2026-04-10T0840-ticket
source_id: null
tags: []
time_minutes: 15
title: Get up to speed on step configurator
updated: 2026-05-06T13:03:48Z
waiting_on: null
waiting_since: null
working_on: false
---

https://www.notion.so/canarytechnologies/Step-Configurator-Approach-2e381468615180018a40c532b2f0e4c1?pvs=26&qid=1%3A7d16a450-2dd2-4054-a6fd-8e6a8d4a67c6%3A2