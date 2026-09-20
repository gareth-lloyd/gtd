---
area: null
completed_at: null
contexts: []
created: 2026-09-17 17:08:27.644093
defer_until: null
due: 2026-09-18
energy: low
id: 2026-09-17T1708-consider-whether-the-wyndham-onbaording-screen-stu
order: null
output: |-
  ## TL;DR (as of 2026-09-18, covers both agent runs below)
  - Wyndham "onboarding experience" (first-login modal sequencer, PRs #10999 / #11000) is NOT a checklist foundation: completion is a write-once row, no owner, no deep link, no nudges, no above-property view. Worth keeping from it: the item-registry shape (stable key + eligibility predicate + typed response), `ExperienceResults` as the model for manual sign-off items, and the modal as an Appcues replacement for a few data-collection items.
  - `backend/canary/monitoring/` IS the engine for the "ticks and unticks itself" half: per-run results, HEALTHY<->UNHEALTHY transitions with `resolved_at`, estate-wide queries, per-check help copy, on-demand refresh. Staff-only today; nothing notifies off it.
  - Two mismatches to design around: (1) existing ~55 checks describe Canary's work (config matches the onboarding script), not the property's - property-owned checks must be written, cheaply; (2) a hotel is only monitored via Salesforce opportunity + scripted OnboardingType, near/after go-live - too late and too narrow (fits IHG/Wyndham/BW, likely misses mid-market).
  - Missing entirely: per-item owner and Canary-vs-property side, deep links, manual sign-off, customer-facing API, notifier. Nudges for never-done items must read latest results - a first run is not recorded as a transition.
  - Cheapest test: read-only property view over latest results for IHG hotels (TOOL-615) plus 3-5 new property-owned checks.
  - Unverified: prod state of `ENABLE_FIRST_TIME_ONBOARDING_EXPERIENCES`, Wyndham completion counts, how many hotels have a `MonitoredHotelState`, real sweep cadence.

  ## Agent run 2026-09-18

  ### Verdict
  Limited direct utility. The Wyndham "onboarding experience" framework is a *blocking first-login modal sequencer*, not a checklist. Reuse the pattern for one narrow slice (human sign-off / info-collection items); do not build the checklist on it. The better existing foundation for the checklist's core ("items the product can see tick and untick themselves") is the `monitoring` app, not this.

  Notion read: Hotel Action Checklist (https://app.notion.com/p/3db814686151818b9316ffff0b388e50). Related: TOOL-615 (https://linear.app/canary-technologies/issue/TOOL-615/onboarding-checklist), prototype https://pages.cnry.cloud/hotel-action-checklist/

  ### What the Wyndham work is
  Built as "Wyndham FTE" (first-time experience): PR #10999 models (https://github.com/canary-technologies-corp/canary/pull/10999), PR #11000 / COR-848 API + functionality (https://github.com/canary-technologies-corp/canary/pull/11000), fixes in #28415 and #29403.

  Backend (`backend/canary/onboarding/`):
  - `configuration_providers/onboarding_experience.py` - `OnboardingExperienceProvider` Protocol: `step_name`, `response_schema`, `should_show_experience(hotel, user) -> bool`, `handle_response(hotel, user, response)`.
  - `services/onboarding_experience.py` - `OnboardingExperienceService`: in-memory registry (registered in `apps.py`), `get_user_experience_journey()` returns outstanding step names, `submit_experience_results()` validates + stores.
  - `models/experience_results.py` - `ExperienceResults(step_name, user, hotel, results JSON)`; a key-value "this user/hotel did this step" table. Read-only in Django admin.
  - `views/onboarding_experience.py` - GET/POST `api/onboarding/experiences/<hotel_slug>[/<step_name>]`.
  - Wyndham steps (`configuration_providers/wyndham/wyndham_onboarding_experience.py`): video trainings (per user), T&Cs (per hotel, user-management permission), payment gateway info collection - EIN / contact email / notes (per hotel, same permission). All gated on `settings.ENABLE_FIRST_TIME_ONBOARDING_EXPERIENCES` + hotel having a WYNDHAM_SITE_ID. All three `handle_response` are no-ops - the answers just land in the JSON blob.
  - A 4th, non-Wyndham step reuses it: `merge_sso_non_sso_users__001` (`configuration_providers/merge_sso_non_sso_users.py`).

  Frontend: `frontend/hotels/src/onboarding/useOnboardingExperiences.ts` + `OnboardingExperienceContainer.vue` (mounted in `App.vue`), modal components in `frontend/packages/shared/onboarding/providers/`. On hotel load it fetches outstanding steps and shows them one at a time as modals until none remain.

  Prod status (Groundcover, last 3h on 2026-09-18): framework is live - 6 journey logs and 4 successful submissions, all `merge_sso_non_sso_users__001`. No Wyndham steps seen in that window. NOT verified: whether `ENABLE_FIRST_TIME_ONBOARDING_EXPERIENCES` is on in prod (not set anywhere in this repo), or historical Wyndham completion counts (`onboarding_experienceresults` is not mirrored into CANARY_RAW Snowflake).

  ### Fit against the checklist goals
  | Checklist goal | Onboarding-experience framework |
  | --- | --- |
  | Items tick AND untick from live product state | No. Completion = a stored row, write-once. No re-evaluation, no regression. Opposite of the doc's "read rather than recorded". |
  | Human sign-off items ("Mark done", "Canary confirms") | Partial fit. `ExperienceResults` is exactly a sign-off record (who, which hotel, when, payload). But no owner, no Canary-vs-customer side, no un-sign. |
  | Per-item owner, reassignable | No. Targeting is a predicate over (hotel, user), not an assignee. |
  | Deep-link to the page that fixes it | No. Steps are self-contained modals. |
  | Notifications / nudges / weekly digest | No. Only fires when the user is already logged in - the doc's own open question notes those are the people least likely to be blocking. |
  | Above-property aggregate view | No. API only answers "what is outstanding for this user at this hotel"; no listing of completed/all items, no cross-hotel query. |
  | Only show items for the hotel's products / viewer's role | Yes - `should_show_experience(hotel, user)` does this, incl. permission checks. Pattern worth copying. |
  | Recommendations with evidence + apply button | No. |

  ### What is worth taking from it
  1. The provider-registry shape: one class per item, stable versioned key (`__001`), an eligibility predicate, a typed response schema. A checklist item definition wants the same shape plus `owner_side`, `deep_link`, and `evaluate(hotel) -> outcome` for auto items.
  2. `ExperienceResults` as precedent (or literal storage) for the "can't know" items - training held, test bookings run. Would need owner/side fields and a way to revoke.
  3. The modal sequencer as one *delivery surface*: a required item that needs data from the customer (the Wyndham EIN form is exactly this - "guide users to input required info for activation", the TOOL-615 problem currently patched with Appcues) could be pushed as a blocking modal. That is an Appcues replacement for a few items, not the checklist.
  4. Cautionary lesson: all three Wyndham `handle_response` hooks are no-ops, so collected EIN/contact data sits in a JSON blob someone has to go read in admin. That is the "record, not a trigger" failure the Notion doc calls out. Whatever the checklist collects should write to the real setting.

  ### Better foundation already in the repo
  `backend/canary/monitoring/` (actively developed - last commits 2026-09-04 ENT-7446, 2026-08-28 TOOL-557):
  - `MonitoredCheckType` - ~30+ per-hotel checks already defined: Twilio configured / brand + campaign approved, payment gateway config valid, guest journey messages enabled/scheduled/sent, SSO org set, reg card configured, room upgrade images, membership gateway, expected onboarding plans run, check-ins completed last 7 days.
  - `MonitoredCheckResult` (outcome + value + JSON per check run), `MonitoredCheckTransition` (previous_outcome -> new_outcome, `resolved_at`), `MonitoredHotelState` (state, go_live).
  - `onboarding/services/health.py` `OnboardedPropertyHealthService` and `onboarding/checks/` (pre/post-run checks returning `None | list[str]`).
  This is already the "reads product state, flips both ways, records the transition" engine - i.e. group one of the Required items, and the transition table is the natural trigger for nudges. It is internal/enterprise-facing today (no customer UI, no owner, no deep links), so the checklist work would be a customer-facing surface + ownership + notifications layered on it. I did not read the monitoring app in depth - worth a proper look before the checklist design hardens.

  ### Suggested next actions (yours to decide)
  - Tell whoever owns the Notion doc that `monitoring` exists; it answers part of "who writes the rules" for Required items (ENT/TOOL already do).
  - If the modal-push idea is interesting, check whether `ENABLE_FIRST_TIME_ONBOARDING_EXPERIENCES` is on in prod and how many Wyndham `ExperienceResults` rows exist (Django admin -> Onboarding -> Experience results) to see if hotels actually completed the EIN form.

  ## Agent run 2026-09-18 (2) - Notion summary + monitoring deep-dive

  ### Product doc summary (Hotel Action Checklist, https://app.notion.com/p/3db814686151818b9316ffff0b388e50)
  - What: one live per-hotel checklist covering onboarding setup, configuration and ongoing improvement. Reframed from "onboarding checklist" - same mechanism, broader scope.
  - Why: shorten time to activation. Client-side missing items are tracked and chased manually by CS today; that does not scale. Needs to work with or without a dedicated CS contact. Automation/AI onboarding stays the priority; the checklist covers the residue that needs humans / third parties.
  - Evidence of demand: CS's vibe-coded go-live generator (https://tools.thesaeed.com/), per-group spreadsheets (Triumph), IHG scale onboarding TOOL-615 (https://linear.app/canary-technologies/issue/TOOL-615/onboarding-checklist) currently patched with Appcues, and the upsell digest prototype (https://upsell-digest.vercel.app/upsells).
  - Three failures of today's tools: no live status, status triggers nothing, they sit outside the product (no path from item to fix).
  - Design: Required vs Recommended. Required splits into (1) what the app can see - ticks AND unticks itself, so no permanent "completed" state and regressions reappear for free; (2) what it cannot see (training held, test bookings) - signed off by name: property "Mark done", Canary "Canary confirms". Per-item owner (default property manager), every item deep-links to the fixing page, onboarding items fall away as the property matures. Two views: Property and Above-property (worst-first list, drill-in, "most often wrong" estate-wide, nudge one property or one item across all properties).
  - Recommended half: evidence from the hotel's own data + specific recommendation + apply button (e.g. "191 guests asked about parking - add Parking upsell").
  - Prototype: https://pages.cnry.cloud/hotel-action-checklist/ (v1: https://pages.cnry.cloud/onboarding-checklist/).
  - Open questions: where the core value sits (CS visibility / client visibility / nudging / removing CS tracking); who writes recommendation rules; in-app vs email; monitoring surface vs checklist for enterprise; which products hurt most.

  ### How monitoring works today (`backend/canary/monitoring/`, ~1.8k lines)
  - Trigger: `cron_monitor_hotels` sweeps every Salesforce account returned by `CohortHotelService.list_salesforce_account_ids_which_require_checking()` - opportunities with go-live in the past, training within 2 days, training completed, or a completed GOLIVE script. 3 workers, shuffled order because the job "sometimes ends before all hotels are checked". On-demand refresh exists: `refresh_monitoring_state_async` Celery task + POST on the API.
  - What a check is: for each `OnboardingType` the hotel has, for each plan that should have run, the plan's config provider `check_hotel_configuration(hotel)` returns `(MonitoredCheckType, CheckResultData(outcome, value, results))`. 27 plan/provider files implement it. Plus one rules-based-config conformity check. Leaf checks are tiny functions, e.g. `monitoring/checks/twilio_is_configured.py` returns `list[str] | None`.
  - Storage: `MonitoredCheckResult` per (hotel_state, type, check_run_uuid); `MonitoredHotelState` holds `latest_check_run_uuid`, rolled-up `state`, `go_live`. History thinned to one run/day after 30 days.
  - Transitions: `MonitoredCheckTransition` recorded only on HEALTHY<->UNHEALTHY flips, `resolved_at` set when the check stops being UNHEALTHY (recovered, degraded, errored, or dropped out).
  - Relevance filter: `critical_check_types` per OnboardingType in `ONBOARDING_TYPE_CONFIG` - defined for WYNDHAM_CONNECT_PLUS, WYNDHAM_MSA, BEST_WESTERN_MSA, IHG_GMS_CORE, IHG_GMS_CORE_PLUS, IHG_MESSAGING, IHG_PILOT, DEFAULT.
  - Surface: `GET/POST api/monitored_hotel_states`, `StaffUserGatekeeper` only. UI is the staff Cohorts pages in `frontend/manage/src/views/Cohorts/`. `monitoredCheckHelp.ts` there already carries `whatWentWrong` / `howToFix` copy for every check type.
  - Consumers of transitions: I found none outside the app itself and the staff UI. Nothing notifies on them today.

  ### Mapping to the checklist
  | Checklist need | Monitoring today | Gap |
  | --- | --- | --- |
  | Auto items tick and untick | Yes - recomputed every sweep, latest run is the truth, no sticky "done" | Freshness: cron sweep, not "the moment it becomes true". Fix by calling the existing on-demand refresh when the checklist opens or the relevant setting saves |
  | Broken item reappears without a regression mechanism | Yes - exactly `MonitoredCheckTransition` + `resolved_at` | none |
  | Only items for this hotel's products | Yes - plans-that-should-have-run + `critical_check_types` per OnboardingType | Keyed on onboarding type, not on products/role of the viewer |
  | Above-property: worst-first, drill-in, most-often-wrong, nudge one item across properties | `get_states_for_hotels(hotel_ids)` and `get_unhealthy_hotels_for_check_type(hotel_ids, check_type)` are already these queries | Staff-only; needs a portfolio-scoped customer gatekeeper |
  | "What went wrong / how to fix" per item | Exists for every check | Staff-worded ("run the Assign Phone Number script"), lives in manage frontend TS, not backend |
  | Nudges / digest | Transition rows are a natural trigger | No consumer exists. And first run is NOT a transition (prev outcome None is skipped), so never-done onboarding items emit nothing - nudges for those must read latest results, not transitions |
  | Per-item owner, Canary vs property side | None | New |
  | Deep link to fixing page | None | New |
  | Manual sign-off items | None - every result is computed | New (this is where an `ExperienceResults`-style table fits) |
  | Recommendations with evidence + apply | `value` + `METRIC_ONLY` outcome could carry evidence numbers | Does not answer "who writes the rules" or the apply action |

  ### The two structural mismatches (more important than the table)
  1. Whose work the checks describe. Almost every existing check asks "does the hotel match what Canary's onboarding script intended" - Twilio sub-account, SSO org, MSA products, reg card defaults, rule-based conformity. When these fail, the fix is Canary's ("run onboarding scripts"). The Notion doc's target is the opposite: items the *property* must do (escalation contact, staff list, amenity hours, training). So the existing ~55 check types mostly populate the "Canary confirms" side. Customer-owned checks have to be written. The cost per check is low - the function shape is `hotel -> list[str] | None`.
  2. Who gets monitored, and when. Entry is via Salesforce opportunity + an OnboardingType with scripted plans, and only from ~2 days before training / after go-live. That covers IHG, Wyndham, BW well (good fit for TOOL-615) but not mid-market groups like Triumph unless they run through DEFAULT with an opportunity, and it starts too late for a tool whose goal is shortening time *to* activation. Customer-owned checks also do not need `OnboardingPlanData` or a Salesforce id at all.

  ### Suggested shape
  - Keep: result + transition storage, latest-run semantics, on-demand refresh, the estate queries, the check-function convention, `critical_check_types`-style relevance.
  - Add a checklist item registry on top: `{key, title, customer copy, side: canary|property, eligibility, deep_link, resolver}` where resolver is either a `MonitoredCheckType` or a manual sign-off. This is the provider-registry shape from the Wyndham onboarding-experience work.
  - Add a hotel-keyed check path that does not depend on Salesforce plan data, and widen the selector to hotels in onboarding, not just near go-live.
  - Add a notifier: open-UNHEALTHY latest results joined to item owner, skipping `side=canary` items so properties are never chased for Canary's work.
  - Customer-facing read API with hotel / portfolio gatekeepers.
  - Recommendations stay a separate problem; monitoring only offers a place to store the evidence number.

  ### Cheapest way to test the idea
  IHG is the live pain (TOOL-615) and has four OnboardingTypes with `critical_check_types` already populated. A read-only property view over the latest `MonitoredCheckResult`s for IHG hotels, with 3-5 new property-owned checks added, would show whether the engine carries the product before any owner/nudge work. Not done: I did not check how many hotels have a `MonitoredHotelState` or the sweep's real cadence/duration in prod.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Think through how monitored health checks could be useful for onboarding checklist
updated: 2026-09-18 15:22:46.520656
waiting_on: null
waiting_since: null
working_on: true
---

read this notion: https://app.notion.com/p/canarytechnologies/Onboarding-Configuration-Checklists-3db814686151818b9316ffff0b388e50?source=copy_link

First step, find the work that was done to show onboarding experiences. 
Find whether it has any utility for the product goals of onboarding checklists.