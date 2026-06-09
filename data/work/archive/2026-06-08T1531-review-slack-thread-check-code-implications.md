---
area: null
contexts: []
created: 2026-06-08 15:31:48.877869
defer_until: null
due: null
energy: low
id: 2026-06-08T1531-review-slack-thread-check-code-implications
order: null
output: |
  ## Agent run 2026-06-08T15:45 (-04:00)

  Thread (#C08FKQG5MKL, Andrea Bradshaw 2026-06-05): "Are there enterprise
  migration implications for the compendium beautification project?" Nico +
  Facu answered. Summary + verified code state below.

  ### What the thread concluded
  - Redesign is feature-flagged; rolled out gradually.
  - Only migration needed = backfill existing sections with a `layout` value.
    Enterprise keeps the **Carousel** layout they use today.
  - Only forced visible change for enterprise = **header + menu** -> needs
    validation/approval before rollout (Nico).
  - Open design Q: image cropping across layouts. Decision: **retain the
    original image**, let users re-crop after a layout change. "Good for MVP."
  - Luciano flagged: no per-layout preview, so editor can't see "this addon
    image looks bad" in the chosen layout. Deemed fixable later, not a blocker.
  - Facu has a draft doc pending (cropping behaviour) that "may have
    implications on the scripts as well."

  ### Code reality (verified against origin/master, not this worktree branch)
  The backend layout work is **already merged to master** (this worktree
  branch `worktree-portfolio-analytics-agent` predates it, so the field is
  absent locally — that's expected, not a gap):
  - `0018_compendiumsection_layout.py` (STAY-3652, PR #46874): adds
    `layout` CharField, choices carousel / vertical_list / full_image /
    inspirational_cards, `db_default="carousel"`, `atomic=False`.
    => The "backfill" is handled automatically by db_default; existing
       sections become carousel with no separate data-migration script. This
       confirms Nico/Facu — enterprise is transparent on the data side.
  - STAY-3653 (PR #46882) write path + STAY-3654 (PR #46937) read/serialize
    path both merged. `CompendiumSectionLayout` TextChoices in
    backend/canary/compendium/models/compendium_section.py:20-74.
  - Image handling: backend/canary/documents/services/image_group.py stores
    crop coords in Image.processing_config ({"crop":{x,y,width,height}})
    rather than destructively cropping — i.e. the "retain original + re-crop"
    decision is already implemented on the data layer.
  - Feature flag exists: `COMPENDIUM_ENHANCEMENT` (compendium-enhancement),
    default off — the gating flag for the redesign.

  ### Still open / in-progress (not yet on master)
  - Frontend rendering of the new layouts: branch
    `origin/dryzhkov/cc-2540-phase-3-fe-rendering` (+ many other compendium
    FE branches). Guest-side layout rendering is the remaining piece.
  - Re-crop-on-layout-change UX and the per-layout preview gap (Luciano's
    point) are design-stage only.

  ### Implication for my enterprise work
  - No action forced on enterprise data; db_default covers existing sections.
  - Onboarding/POC scripts that create compendium sections will inherit
    carousel automatically, but if a script should set a non-default layout
    it now has a `layout` field to set. Relevant to branch
    `glloyd/ent-3764-...set-compendium-product-tier...` (IHG POC) — worth a
    look when that script touches sections. Facu's pending script-implications
    doc is the thing to watch for.
  - Real enterprise gate before rollout = header/menu approval (Nico). That's
    a product/validation task, not a code task.

  No code changes made; read-only investigation.
project: null
source_id: null
tags: []
time_minutes: 5
title: Review slack thread, check code implications
updated: 2026-06-08 15:56:24.260430
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C08FKQG5MKL/p1780678780072919