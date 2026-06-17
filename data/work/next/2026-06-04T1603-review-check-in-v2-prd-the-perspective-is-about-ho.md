---
area: null
contexts: []
created: 2026-06-04 16:03:49.648218
defer_until: null
due: 2026-06-16
energy: high
id: 2026-06-04T1603-review-check-in-v2-prd-the-perspective-is-about-ho
order: 1
output: |
  ## Agent run 2026-06-04T16:32:00

  Reviewed Leandro's PRD "[WIP] PRD: Flow builder/step configurator" (the check-in v2
  / step-framework authoring layer), linked from the Slack thread. Lens: how it lands
  for enterprise MSA hotels that are provisioned via onboarding scripts, not by CS
  clicking through Manage.

  **What the PRD proposes (1-liner):** a CS-facing UI to (Job 1) generate a hotel's
  check-in flow from brand/country/Salesforce standards, (Job 2) edit the flow + a
  shared Field Library, and (Job 3) let hotel admins self-serve minor edits. MVP is
  mobile-web only, v3 step framework only.

  **How enterprise MSA hotels are configured TODAY (grounded in the code):**
  - Brand standards live in CODE: onboarding/configuration_providers/{ihg,wyndham,
    best_western}/registration_card_provider.py (e.g. BW_MSA_TEMPLATE, Wyndham/IHG
    reg-card templates), driven by Salesforce fields + DeciderAttributes
    (PARENT_BRAND, MANAGEMENT_COMPANY_ID, HOTEL_COUNTRY).
  - Onboarding plans (AddRegistrationCardPlan etc.) are idempotent and re-runnable,
    run in bulk waves (ENT-6032: 25 IHG hotels at once; Bessemer dual-brand shares one
    integration). They write the RegistrationCard + CheckInConfiguration toggles.
  - Most MSA hotels are on checkin_version "v2" (RegistrationCard served directly). v3
    (Flow + Steps) is seeded on-demand by `seed_guest_experience_flow` — there is NO
    onboarding plan for v3 yet.

  **Top concerns to raise with Leandro (strongest first):**

  1. TWO authoring paths for the same config, no reconciliation. The PRD's "Generate
     config" engine and the existing brand ConfigProviders both claim to author the
     reg card / flow from brand+country+Salesforce. The PRD is silent on which wins
     and on idempotency. If a CS edits via the configurator and an onboarding plan
     later re-runs (PMS re-config, go-live re-run, a fleet fix across 25 hotels), does
     it clobber the edits? The IHG provider ALREADY does "layout detection to avoid
     overwriting customizations" — that protection must extend to configurator edits,
     or the two systems overwrite each other. Need an explicit source-of-truth/merge
     model.

  2. Generation engine must be callable headless/in-bulk, not just from the UI. Job 1
     is described as per-hotel, CS-reviews-then-publishes. Enterprise MSA onboarding is
     scripted across whole waves. If the only way to generate config is a CS clicking
     "Generate" per hotel, enterprise onboarding REGRESSES to manual clicking. Ask:
     can the onboarding scripts call the SAME generation engine the UI calls (shared
     service, headless), so scripts stay the bulk path and the UI is the edit surface?

  3. Where does "brand standard" live going forward? Today it's PMS-vendor-aware code
     (templates, policy markdown fetched from the PMS/CPM, OCR policies). If the
     configurator introduces a new Salesforce-seeded brand-standard store, the careful
     provider logic risks being duplicated or diverging. Define whether the providers
     FEED the new engine or are REPLACED by it.

  4. Hotel self-serve editing (Job 3) vs MSA brand governance. Letting hotel admins
     reorder fields / edit labels / manage translations is exactly what brands (IHG,
     Wyndham, BW) often want LOCKED for portfolio consistency / MSA compliance. There
     is no portfolio/brand-level toggle to disable or constrain hotel self-edit for
     MSA-managed properties. This maps naturally onto existing portfolio + decider
     attributes — flag it as a required governance control, not a fast-follow.

  5. PMS mappings as a CS-authored UI field is a regression for MSA hotels. The Field
     Library says CS sets PMS mappings "once here". For MSA hotels these are derived
     per-PMS-vendor by provider logic, and some PMSes can't expose certain data (e.g.
     the Grecotel/Protel companions-table limitation). Hand-authoring mappings in a UI
     is error-prone for enterprise. The generation engine must populate PMS mappings
     from provider logic; the PRD should state CS does not author them from scratch for
     MSA hotels.

  6. v2 -> v3 migration is an unstated prerequisite. The configurator is v3-only, but
     the enterprise fleet is largely v2 and has no onboarding plan that seeds v3. Before
     the configurator is usable for MSA hotels we need (a) a v3 seeding step in the
     onboarding plans and (b) a defined v2->v3 migration for the existing fleet. The
     PRD assumes v3 exists everywhere — it does not yet for enterprise.

  7. Per-hotel publish doesn't fit fleet-wide MSA changes. Validation + publish are
     per-flow/per-hotel. A real MSA change ("update consent copy across all Wyndham
     hotels") would be N individual publishes. Ask whether a brand/portfolio-standard
     edit can cascade, or enterprise stays on scripts for fleet changes (which loops
     back to concern #2 — keep the scripted path first-class).

  8. Accompanying Guest is net-new backend; make sure the engine (not just the UI) can
     set the per-brand path. Today additional-guest ID behaviour is per-brand in
     CheckInConfiguration. The generated default also won't be executable on every PMS
     (Protel companions-table caveat) — validation should account for PMS capability,
     not just schema validity.

  **Net:** PRD is solid for the SMB/self-serve CS workflow. The gap is that it treats
  the UI generation+edit path as the only path, while the enterprise MSA fleet is
  bulk-provisioned by idempotent scripts encoding brand standards in code. The single
  most important ask: make the generation engine a shared headless service the
  onboarding scripts call, with a clear source-of-truth/merge story and a
  brand-governance lock — so scripts and configurator don't fight over the same config.

  (No external writes made — Slack thread + Notion PRD read-only. Did not comment on
  the PRD; raise these directly with Leandro if useful.)
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 30
title: Review check-in v2 PRD. The perspective is about how this affects enterprise
  MSA hotels which are configured via onboarding scripts.
updated: 2026-06-17 12:37:57.463557
waiting_on: null
waiting_since: null
working_on: true
---

https://canarytechnologies.slack.com/archives/C0B4QD01GP8/p1780491110778609