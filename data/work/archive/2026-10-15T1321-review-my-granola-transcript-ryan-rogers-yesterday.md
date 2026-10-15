---
area: null
completed_at: 2026-10-15 13:44:00.958407
contexts: []
created: 2026-10-15 13:21:55.919797
defer_until: null
due: null
energy: low
id: 2026-10-15T1321-review-my-granola-transcript-ryan-rogers-yesterday
order: null
output: |-
  ## Agent run 2026-10-15

  ### What was said (Granola, 1:1 with Ryan, 2026-10-14)
  Meeting: https://notes.granola.ai/d/847ed41f-bd7d-4a7d-9991-b079ff88be25
  - Ryan raised converging onboarding with drift detection and wants to stay involved.
  - You brought up his earlier spike on redefining IHG GJ messages as a registry. You said the missing piece for rules-based GJM is "a registry of message specs that takes a set of use cases and turns it into the more populated spec." You promised to send your one-pager to Ryan and Tincho "next couple of days" and asked whether he still had the branch.
  - Ryan only vaguely remembers the old work but has fresh ideas. He sees drift coverage on GJ messages as a real gap ("could be harmful to the operations of hotels if they're misconfigured"). Andrea told him Tincho owns the GJ messaging side, and that other pieces need to land before a bigger improvement.
  - **Your open commitment:** share the one-pager with Ryan and Tincho.

  ### Evidence of Ryan's registry work (Feb–Mar 2026)
  1. **Spike PR #38258**, "[ENT-5364] Simplify IHG message registry into flat data-driven lookup" (https://github.com/canary-technologies-corp/canary/pull/38258). Draft, +1231/−961, opened 2026-02-11, closed unmerged 2026-04-06. Branch `origin/rrogers/ihg-declarative-message-registry` still exists, so the answer to "do you still have the branch" is yes. It added `ihg_message_registry.py` with `SYSTEM_MESSAGES_BY_REGION`, `CustomMessageDef` checkout lists keyed by brand/region, `LOYALTY_SEGMENTS` built via `_brand_segments()`, and a `CheckoutPaths` dataclass. You requested changes: organise around use cases, then step back to a design doc. You also tagged @martinrodriguezcanary to review.
  2. **Design doc "IHG Guest Journey Message Registry Redesign"** (https://app.notion.com/p/3118146861518039ba72f9909012d708). Owner Ryan, reviewer you, created 2026-02-24, Status **TODO**, last edited 2026-02-24. Core ideas:
     - flat `SYSTEM_MESSAGE_SPECS` / `CUSTOM_MESSAGE_SPECS` dicts keyed by `IHGGuestJourneyMessageUseCases`
     - variants nested on the spec
     - `template_overrides[(brand, region)]` on custom specs
     - `BRAND_VARIANT_OVERRIDES`
     - an imperative `get_use_cases(brand, region, onboarding_type)` that makes pilot a first-class use-case set and kills the `PILOT_DEPARTURE_MESSAGES_TITLES_TO_REMOVE` hack
     - WhatsApp applied by region in the provider
     - an old-vs-new equivalence test across every combination

     It judged the pattern worth it for IHG only, modest for Wyndham, and no gain for BW (hotel-list experiments). It rejected an abstract registry base class.
  3. **ENT-5364** "Eng design for improved specification of guest journey messages" (https://linear.app/canary-technologies/issue/ENT-5364). Ryan, Done 2026-03-10.
  4. **ENT-5558** "Implement declarative message registry for IHG guest journey messages" (https://linear.app/canary-technologies/issue/ENT-5558). Created 2026-03-10, unassigned, sat in Backlog, **Canceled 2026-10-02**. It records that your PR #41274 (https://github.com/canary-technologies-corp/canary/pull/41274, merged 2026-03-19) already delivered inline `variants` on specs, `message_specs_with_variants`, and removal of `message_variant_specs`. Still not done from Ryan's plan: the registry file, `template_overrides`, the provider rewrite, dead-code cleanup, and sharing constants with `ihg_variant_creation_service.py`.

  ### Current state (origin/master)
  - No `ihg_message_registry.py` exists. `guest_journey_messages_provider.py` has grown to 1,345 lines (it was ~1,060 when Ryan wrote the doc). A second provider, `gms_core_ihg_guest_journey_messages_provider.py`, has 1,444 lines, and `ihg_variant_creation_service.py` has 1,223.
  - Recent GMS Core GJM work comes from lmenaolivares (ENT-7318/7389/7393/7058) and Martin Rodriguez (ENT-7635, #57953). The problem Ryan described has roughly doubled.

  ### How it connects to your one-pager
  Your doc: "Guest journey messages in rules-based configuration" (https://app.notion.com/p/3f9814686151813da661eb802029d0eb). WIP, created 2026-10-14, ENT-7726.
  - **Same:** the use case is the key, and a per-portfolio registry maps use cases to specs that feed the unchanged plan.
  - **Difference 1:** your doc replaces Ryan's hand-written `get_use_cases()` with a brand-tree `FINAL SupersetOf(...)` plus a reader. Drift then comes for free.
  - **Difference 2:** your registry entries are *factories* (use case + slot + factory(Hotel)), not static specs plus `template_overrides`. Ryan's `template_overrides`, nested variants and region-applied WhatsApp are good candidates for what those factories do internally.
  - **Reuse directly:** Ryan's equivalence-test safety net, and the "IHG main + GMS Core could share one registry" point, which your doc already raises.
  - Ryan's Wyndham/BW applicability table is a useful sanity check against your "one registry per portfolio" choice: BW's hotel-list experiments map to your "per-hotel exceptions stay in `perform_hotel_configuration`".

  ### Suggested next steps (not done; your call)
  - When you send the one-pager, link the Ryan Notion doc and the `rrogers/ihg-declarative-message-registry` branch as prior art.
  - Decide whether to reopen or replace ENT-5558. It was cancelled 2 weeks ago, and its remaining steps 4–7 overlap the registry half of your design.
  - Unverified: I assumed "Tincho" is Martin Rodriguez (@martinrodriguezcanary, recent IHG GMS Core GJM PRs, and you tagged him on #38258). Confirm before sending.
  - No Slack, Linear or Notion writes were made.
project: null
source_id: null
tags: []
time_minutes: 5
title: Review my granola transcript Ryan Rogers yesterday. Search notion and github
  for evidence of his guest journey message registry refactor/design
updated: 2026-10-15 13:44:00.958396
waiting_on: null
waiting_since: null
working_on: false
---