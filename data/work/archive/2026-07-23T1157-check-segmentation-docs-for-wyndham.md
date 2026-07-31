---
area: null
contexts: []
created: 2026-07-23 11:57:30.682215
defer_until: null
due: null
energy: low
id: 2026-07-23T1157-check-segmentation-docs-for-wyndham
order: null
output: |
  ## Agent run 2026-07-24T10:22:19+03:00
  Searched Notion (AI search across Notion + connected sources) for the Wyndham segmentation rollout eng design docs. Found:

  **Most relevant**
  - Enterprise Rollout: Segmentation for Wyndham (Linear project, status "Eng Design", lead Andrés Figueira, Jul 1–31 2026): https://linear.app/canary-technologies/project/96bb77fa-cff6-412d-859a-1d56e90026f5
  - PRD: Upsells Segmentation (canonical PRD, status GA — scope, attribute matrix, architecture, Wyndham-driven requirements): https://app.notion.com/p/31181468615180b192ded4f77fdd61be
  - Wyndham Test Run Report - Upsell Segmentation (QA run 2026-06-10, 0 defects, cleared for UAT/controlled rollout): https://app.notion.com/p/699814686151834c9b9901f02d10de16
  - PRD: Segmentation (Guest Communications) (platform segmentation module the upsell work depends on): https://app.notion.com/p/2638146861518000a13ef67655240450

  **Key decisions/constraints**
  - Rule precedence on conflict: Hide from > Offer for free > Show only to (Upsells Segmentation PRD)
  - Segments resolve on reservation create/update, not at storefront load; no-segment/no-rule fallback shows item to all guests (Upsells Segmentation PRD)
  - Gated by ROLLOUT_UPSELL_GUEST_SEGMENTATION flag; Upsell Segmentation overrides Dynamic Pricing when both enabled (Test Run Report)
  - Wyndham launch bundles multiple segmentation features into one UAT pass: https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1776284596368289

  **Open threads**
  - Migrating legacy hardcoded IHG/BW/Wyndham loyalty upsell logic into segmentation without disruption (Upsells Segmentation PRD)
  - Segment deletion/inactivation changes guest outcomes immediately; admin operational docs still needed (Test Run Report)
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Read Wyndham segmentation eng design + PRD docs and review
updated: 2026-07-31 11:17:39.742056
waiting_on: null
waiting_since: null
working_on: false
---

Read these docs and review:

- Eng design / rollout project: [Enterprise Rollout: Segmentation for Wyndham](https://linear.app/canary-technologies/project/96bb77fa-cff6-412d-859a-1d56e90026f5) (Linear, status "Eng Design", lead Andrés Figueira, Jul 1–31 2026)
- [PRD: Upsells Segmentation](https://app.notion.com/p/31181468615180b192ded4f77fdd61be) — canonical PRD: scope, attribute matrix, architecture, Wyndham-driven requirements
- [PRD: Segmentation (Guest Communications)](https://app.notion.com/p/2638146861518000a13ef67655240450) — platform segmentation module the upsell work depends on
- [Wyndham Test Run Report - Upsell Segmentation](https://app.notion.com/p/699814686151834c9b9901f02d10de16) — QA run 2026-06-10, 0 defects, cleared for UAT/controlled rollout