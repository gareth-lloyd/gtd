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
output: "## Agent run 2026-05-06T13:03:48Z\n\nPulled Notion page \"Step Configurator
  Approach\" + related Linear projects via notion-context skill.\n\n### What it is\n-
  A framework for the mobile arrival experience where guest journeys are composed
  of configurable, ordered \"steps\" with shared state, completion semantics, and
  progression logic — designed to be platform-agnostic.\n- Three-layer model:\n  1.
  **Step framework** — data model + business logic + save/progression infra\n  2.
  **Guest experience app** — configures which steps run, applies enterprise/regional
  templates\n  3. **Front-end product UI/UX** — kiosk, mobile web, mobile SDK consume
  the ordered step list\n- Solves needing to flex per country/brand: regional compliance,
  per-brand or per-property variations.\n\n### Proposed approach\n- Step framework
  owns \"is this step finished?\" semantics. A/D team builds per-step logic (e.g.
  reg card finished = submitted and saved).\n- Configuration tiers: **Brand (in code)**
  → Sub-brand (lock-down point) → Region → Property → Platform. Customers configure
  only below sub-brand.\n- APIs expose step state / progression / completion. Consumed
  by Mobile SDK + at least one other surface (kiosk, web, tablet).\n- A self-service
  flow builder for the CS team is being defined separately.\n\n### Status & owners\n-
  Approach doc reads as planning / Q1 OKR scoping — not a final design.\n- Migration
  project (\"Migrate hotels to flexible check-in v3\") is in Implementation, on-track.
  Lead gpercu@canarytechnologies.com.\n- Self-service flow builder: Vibhor Sachdeva,
  Product Definition, due 2026-05-29.\n- Roadmap: M1 step framework, M3 mobile check-in
  on framework, M5 guest experience layers, M6 full migration.\n\n### Decisions /
  constraints\n- Brand-level config lives in code, not customer-adjustable settings.\n-
  Focus is kiosk *supporting* guest experience rather than migrating kiosk itself
  now.\n- Kiosk Step Framework Shim is paused on dependencies.\n\n### Open threads\n-
  Guest Experience App design doc is a stretch / aspirational KR4 — not yet written.\n\n###
  Related Linear / docs\n- **DSN-1782** Step Configurator builder — design work by
  Miguel Santana, started 2026-04-09.\n- **AD-6865** Add generic step configurator
  — Matthew Jeffery, framework-level ticket.\n- **Web check in step configurator builder**
  — non-eng builder for web check-in flows.\n- **ENT-6100** Create new \"rollout recipe\"
  concept — my current branch; rollout-recipe concept likely intersects with the template/configuration
  tiers.\n\n### Connection to current work\nMy active branch (`glloyd/ent-6100-create-new-rollout-recipe-concept`)
  sits in the same conceptual space as the configuration-tier model (Brand → Sub-brand
  → Region → Property → Platform). Worth checking how rollout recipes relate to enterprise/regional
  templates referenced in the approach doc.\n\n### Nothing found for\nDedicated Slack
  threads or Notion design follow-ups beyond the primary page. Search returned only
  Linear hits.\n\nPrimary source: https://www.notion.so/canarytechnologies/Step-Configurator-Approach-2e381468615180018a40c532b2f0e4c1\n"
project: 2026-04-10T0840-ticket
source_id: null
tags: []
time_minutes: 15
title: Get up to speed on step configurator
updated: 2026-05-07 12:18:40.660927
waiting_on: null
waiting_since: null
working_on: false
---

https://www.notion.so/canarytechnologies/Step-Configurator-Approach-2e381468615180018a40c532b2f0e4c1?pvs=26&qid=1%3A7d16a450-2dd2-4054-a6fd-8e6a8d4a67c6%3A2