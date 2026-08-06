---
area: null
completed_at: null
contexts: []
created: 2026-08-05 15:47:01.349622
defer_until: null
due: null
energy: low
id: 2026-08-05T1547-review-connor-s-prd
order: null
output: |
  ## Agent run 2026-08-06T10:01:34Z

  Reviewed: [PRD: Revamped "Managed Context" for Wyndham](https://app.notion.com/p/3b281468615181f1ad39c871d9f15086)
  (Connor Swords, 2026-08-04, Draft, P3). Linear project:
  https://linear.app/canary-technologies/project/revamped-managed-context-for-wyndham-5dacdafdd264/overview

  Every code claim in the PRD was checked against the repo (branch
  glloyd/ent-7078-modify-country-china-to-greater-china). No code was changed. Nothing posted to
  Notion/Linear.

  ### Verdict
  Solid PRD — well-scoped, honest about why v1 is narrow, and the code inventory is accurate. Two
  correctness issues (#1, #2) should be resolved before it leaves Draft; #3 and #4 are rollout risks
  the doc doesn't currently name.

  ### Verified correct
  - `search_amenity_codes` / `alert_message` / `alert_priority_code` are parsed but consumed nowhere.
    Confirmed: only occurrences are the schema definition
    (`backend/canary/crs_gateway/mulesoft/schemas/property.py:231-232,257,289`). Premise holds.
  - `POPULATE_AI_CONTEXT` is in `ad_hoc_stages` only (`onboarding/models/property_configuration_processes.py:1308`
    for Wyndham; a Demo one at :2799). PRD cites ~L1086-1097 — line numbers have drifted, worth fixing.
  - MANAGED statements *are* retrieved by the AI, including in brand-property mode — confirmed by
    `chat/tests/.../test_knowledge_base_search_service.py:1068,1294`. The core value premise is sound.
  - `Configuration.has_managed_ai_answers` default `False` (`chat/models/configuration.py:343`), and
    the frontend renders MANAGED read-only
    (`frontend/hotels/src/chat/components/KnowledgeBase/KnowledgeBaseEntriesEditor.vue:245`).
  - BW precedent for a code->description map exists and is a reasonable template
    (`onboarding/services/vendor/bw/cpm/attributes.py`, 314 lines).

  ### Material issues

  **1. The Wyndham-corporate user story contradicts Non-Goal #2.**
  The story asserts "properties cannot edit or drift from it"; Non-Goal #2 says no server-side edit
  enforcement, frontend read-only is enough. Confirmed there is genuinely no guard:
  `chat/views/custom_statement_view.py` PATCH (:58) and DELETE (:75) have no MANAGED-group check, and
  `CustomStatementsService` doesn't filter by group either. So a property can edit or delete managed
  statements via the API today. Either soften the user story to "properties are not *shown* an edit
  affordance", or add the guard — it's a few lines in the service and would make the story true. As
  written, a stated acceptance criterion is one v1 explicitly won't meet.

  **2. FR-3's "replaced automatically" is false in exactly the case that matters.**
  `onboarding/plans/populate_ai_context_plan.py:35-39` returns early when `statements_to_create` is
  empty — *before* the delete at :42-43. A Wyndham property with blank `search_amenity_codes` and no
  `alert_message` therefore keeps its legacy fixed Q&A statements indefinitely. Since v1's whole point
  is removing that legacy content (the content Wyndham couldn't keep accurate), the properties most
  likely to have thin API data are the ones that silently retain it. Fix is small — move the delete
  above the early return — but FR-3 should state it rather than assume current behaviour covers it.

  **3. Phase 1 validates a code path Phase 2 won't ship.**
  `onboarding/management/commands/load_wyndham_ai_answers.py` does not go through
  `PopulateAIContextPlan` / `WyndhamAIContextConfigProvider` — it imports
  `build_property_ai_statements` and re-implements the flow. It also resolves the property differently:
  the command does `int(hotel.sso_hotel_id)`, the provider does Salesforce Wyndham Site ID through
  `fix_numeric_id(..., min_length=5)`
  (`onboarding/configuration_providers/wyndham/wyndham_ai_context_provider.py:34`). So the pilot can
  pass while onboarding resolves a different property or behaves differently. Recommend the command be
  refactored to call the plan as part of Phase 1, or the PRD should acknowledge the duplication.

  **4. FR-4 turns a Mulesoft outage into an onboarding-blocking failure, and the rollout flag isn't a gate.**
  Two coupled points the PRD doesn't cover:
  - The provider raises `ExpectedOnboardingPlanError` on any Mulesoft failure
    (`wyndham_ai_context_provider.py:43-46`), and `onboarding/services/onboarding.py:710-711` re-raises
    it. In `ad_hoc_stages` that fails one manual run; moved into creation/go-live it can fail the whole
    onboarding batch. FR-4 should state whether this stage is blocking or best-effort. Best-effort is
    almost certainly right — the AI KB shouldn't gate go-live.
  - The dependency table describes `has_managed_ai_answers` as a per-hotel gate you "flip on as
    properties are populated". It isn't a gate: `AIContextConfig.has_managed_ai_answers` defaults to
    `True` and the plan flips the hotel's flag on as a side effect
    (`populate_ai_context_plan.py:52-56`). Once FR-4 lands, every new Wyndham property gets managed
    answers enabled automatically with no separate control and no off-switch in the plan. Per
    `.claude/rules/backend/rollout-safety.md` this wants a real rollout control
    (`FeaturesService.get_feature_rollout`). Note the flag also selects the group — set `False` and the
    plan writes USER_CREATED, i.e. editable — so it's doing two jobs.

  ### Smaller notes
  - **Statement format change is unexamined.** Every existing managed statement is `"Question? Answer."`
    (`onboarding/utils.py:23-64`). FR-1 proposes bare declaratives ("This hotel has a Pool."). Retrieval
    is embedding-based over chunks, so dropping the question form changes what a guest question matches
    against. Phase 1's learning goal says "phrasing reads well to guests" — it should also include a
    retrieval sanity-check (does "do you have a pool?" actually hit the amenity chunk).
  - **Metric/mechanism mismatch.** The problem statement leans on Val's "Room attributes (+0.89pp)", but
    `search_amenity_codes` is property-level. Room-level data is `room_types` / `room_features` — also in
    the schema, also unconsumed. v1 mostly addresses the +0.48pp policy bucket. Either recalibrate the
    lagging-metric target or name `room_features` as the Phase 3 lever.
  - Open Question #1 (stale 2018 alerts) is the right one to resolve before Phase 2 — verbatim ingestion
    of an outdated alert is a guest-visible correctness bug, not just noise.
  - Notion inline comment already on the doc (unresolved): request to attach
    `property_api_response_sample.json` and `wyndham_amenities_codes_descriptions.json`. Still outstanding.

  ### Suggested additions to the PRD's Open Questions
  - Is the onboarding stage blocking or best-effort if Mulesoft is unavailable at go-live? (see #4)
  - What is the rollout control now that the plan auto-enables `has_managed_ai_answers`? (see #4)
  - Do amenity statements need to remain in Q&A form for retrieval to work? (see notes)

  ### Not done
  - No comment posted to Notion. If wanted, the above needs rewriting by a human before posting.
  - Did not assess whether Wyndham's amenity codes are actually accurate — that's a Wyndham-side data
    question the PRD correctly treats as a premise.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: review connor's PRD
updated: 2026-08-06 13:04:12.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/PRD-Revamped-Managed-Context-for-Wyndham-3b281468615181f1ad39c871d9f15086?source=copy_link