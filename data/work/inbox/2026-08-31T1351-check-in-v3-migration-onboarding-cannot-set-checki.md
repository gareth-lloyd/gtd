---
area: null
completed_at: null
contexts:
- deep
created: 2026-08-31 13:51:49.869556
defer_until: null
due: null
energy: high
id: 2026-08-31T1351-check-in-v3-migration-onboarding-cannot-set-checki
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: 30
title: 'Check-in V3 migration: onboarding cannot set checkin_version=v3 + 5 related
  gaps'
updated: 2026-09-10 10:20:37.619335
waiting_on: null
waiting_since: null
working_on: false
---

Raised by reviewing the 2026-08-11 check-in V3 migration/ownership call (I was absent; Stephanie Barry relayed my position on scripting ownership and it was accepted). Followed up with a code exploration of `backend/canary/{guest_experience,check_in,onboarding}` and the guest frontends. The meeting closed the ownership question but left a set of concrete engineering gaps with no named owner.

## Decision to make

Who picks up gap #1 (below), and does it become a ticket on A&D or on Enterprise/Onboarding? It has a hard ordering dependency: it must ship BEFORE the bulk Wyndham/Best Western migration, or every hotel onboarded during the migration window silently lands on the version we are migrating away from.

## How V3 migration actually works (verified in code)

- "Migrating a hotel to V3" is two flags on `check_in.models.Configuration`: `checkin_version="v3"` and `rollout_check_in_v2_level="stable"`. See `guest_experience/services/v3_migration.py:308` (`_enable_check_in_v3`).
- Routing is entirely CLIENT-SIDE. No backend read of `checkin_version` decides anything; it is serialized in `check_in/schemas/check_in_configuration_external.py:37` and the SPA branches on it (`frontend/guest/src/components/reservationActions/CheckInAvailable.vue:35` -> `/guest-experience/...` vs `/reservation/.../check-in`). The flag flip IS the cutover, instantly, per hotel.
- `compute_desired_flow_spec(hotel)` (`v3_migration.py:146`) is a pure derivation from CheckInConfiguration + RegistrationCard.schema + Incode config + `hotel.has_addons`. `create_or_update_flow()` persists idempotently and only sweeps steps in `owned_keys`.
- The registration card enters V3 as ONE step's config blob: `SchemaFormStepConfiguration.schema_form_json`, loaded by `_load_schema_form_json()` (`v3_migration.py:352`). There is NO V2->V3 reg-card transformation; V3 consumes the same FormSchema JSON verbatim.
- Sync is push + pull. Push: `guest_experience/signals.py` post_save on Configuration / Hotel (only has_addons, supported_languages, default_guest_language, country_code) / RegistrationCard (kind=CHECK_IN only) / IncodeFullVerificationFlowConfig, plus a pre_save that hard-raises `V3MigrationBlocked`. Pull: `services/v3_reconcile.py` via `manage.py reconcile_hotel_v3_flow --all-v3 [--repair --commit]`.
- Blockers live in `get_compatibility_blockers()` (`v3_migration.py:109`): additional guests, credit_card_upload_policy in {always, high_risk}, surcharge manual correction, CMP-without-deposits. `--force` bypasses.

## Issues to resolve (ranked)

### 1. Onboarding is STRUCTURALLY incapable of setting checkin_version=v3  [highest priority]

`CheckInConfigurationUpdates` (`onboarding/configuration_providers/configs/registration_card.py:8`) is a frozen dataclass with fields: id_step, id_step_with_ocr, the five additional_guests_*, and rollout_check_in_v2_level. There is NO `checkin_version` field. Every provider sets only `rollout_check_in_v2_level=STABLE`:
  - default: `onboarding/plans/registration_card_plans.py:29`
  - Best Western: `onboarding/configuration_providers/best_western/registration_card_provider.py:56`
  - Wyndham: `onboarding/configuration_providers/wyndham/wyndham_registration_card_provider.py:289`

Model default is `checkin_version = V2` (`check_in/models/configuration.py:264`). Repo-wide only TWO places write checkin_version at all: `_enable_check_in_v3` and `revert_hotel_from_v3`.

=> Every hotel onboarded today lands on V2 by construction. Fixing it needs a dataclass field + provider changes + tests, NOT a script tweak. This is Connor's Best-Western-created-on-V1 bug repeating one version up, and worse than he framed it in the call: it is not a script someone forgot to update, it is a field that does not exist.

### 2. "Flip the default to V3" only covers one of Dana's two cases

Dana named both cases on the call: (a) net-new property, (b) existing customer newly enabled on check-in. Changing the model default fixes (a) only. Case (b) hotels already have a Configuration row sitting at v2; a default change never touches an existing row. Enabling check-in on an existing customer needs an EXPLICIT write of checkin_version=v3 somewhere in that path. Nothing writes it today and that path does not go through the migration service.

### 3. bulk_update silently desyncs the reg card on already-migrated hotels

The RegistrationCard post_save signal is the ONLY thing pushing a reg-card change into the V3 flow's schema_form_json. Four commands mutate `schema` via bulk_update, which does not fire signals:
  - `check_in/management/commands/format_reg_cards_for_v2_check_in.py:99`  <-- the V1->V2 command Dana is about to run on ~700 hotels
  - `check_in/management/commands/revert_reg_cards_to_v1_check_in.py:107`
  - `check_in/management/commands/update_two_column_equivalent_reg_cards.py:66`
  - `check_in/management/commands/onetime_fix_reg_card_heading_id.py:77`

`format_reg_cards_for_v2_check_in` also bulk-updates CheckInConfiguration, bypassing BOTH the pre_save blocker enforcement and the post_save reseed.

Failure mode: V3 hotel's reg card edited by script, DB reg card correct, guest keeps seeing the old one, no error anywhere. Exactly the path Connor said he was not worried about ("we would do it via scripting anyways").

Mitigation exists (`reconcile_hotel_v3_flow` reports CONFIG_MISMATCH, `--repair` fixes) but I found NO cron/workflow/schedule invoking it. It is manual and someone has to remember. Cheapest win: schedule `reconcile_hotel_v3_flow --all-v3` before anyone runs the 700-hotel V1 batch.

Safe-by-contrast path: `ExtendableRegistrationCardService.update_portfolio_extendable_registration_card` cascades with `.save()` per hotel (`check_in/services/extendable_registration_card.py:83`), so portfolio-card fan-out fires signals correctly.

### 4. Duplicate reg cards resolve silently by lowest pk

`_load_schema_form_json` does `.filter(hotel, kind=CHECK_IN).order_by("pk").first()`. `V1RegCardService._classify` already flags duplicates as NEEDS_REVIEW with the comment "migration may use wrong one" — so it is known, but resolution is a silent arbitrary pick rather than a refusal.

### 5. Onboarding actively writes a V3 blocker, per country

Wyndham's `ADDITIONAL_GUEST_STEPS_BY_COUNTRY` (`wyndham_registration_card_provider.py:188`) assigns additional guests to a long list of non-US countries (Colombia, France, Ireland, Italy, India, Philippines, Saudi Arabia, Netherlands, and dozens more). Those are Wave 2 and cannot migrate.

Sharp edge: once Wave 2 ships and that blocker is relaxed, or if the country map changes, an idempotent onboarding plan re-run against an already-migrated hotel can raise `V3MigrationBlocked` out of a pre_save signal — a bare exception, not the `raise_expected_error` contract onboarding plans are required to use (`onboarding/CLAUDE.md`, "Plan Error Handling"). Surfaces to onboarding as an unhelpful 409/500 with no WHAT_TO_DO.

### 6. Open question for Dana — the "LLM reg card rewrite" script

On the call Dana described the V1->V3 reg-card work as "a script that uses an LLM to rewrite the reg cards" because of HTML elements. That script is NOT in the repo. What IS in the repo says close to the opposite: `format_reg_cards_for_v2_check_in` only strips three layout ids (title, property_info, check_in_out_info), and `guest_experience/services/v1_reg_card_service.py` states "HTML elements in the schema are safe (presentational only) and do not trigger NEEDS_REVIEW". Either the LLM script is local/uncommitted, or the understanding moved on and the meeting statement is stale. Cannot resolve from code — ask Dana.

---

# AGENT LOG

## Source

`/Users/garethlloyd/Downloads/GMT20260811-190157_Recording.transcript.vtt` — Zoom transcript, 2026-08-11 19:01 UTC, ~23 minutes, 245 cues.

Attendees: Vibhor Sachdeva, Dana Levine, Guido Luz Percu (A&D / arrivals-departures), Connor Swords, Andrea Bradshaw, Stephanie Barry (Enterprise / Onboarding). I was absent — noted at the top of the call ("he is dealing with a medical thing").

Two agenda items: check-in V3 migration ownership, and new-hotel setup scripting.

## Decisions reached on the call

1. **A&D owns the V3 migration.** Vibhor argued it is one-time, the scripts already exist (Guido/Dana built them), and A&D has been babysitting rollouts already. Connor agreed: "you guys know the most about this migration, I am inclined to let you handle it... I am inclined to do whatever the easiest path here, and it seems like it is that." Enterprise stays looped in but does not do the work. Connor asked to be kept informed on timing and offered guidance on good/bad windows to migrate.

2. **Management command, not the rollout framework.** Andrea offered the configuration-scripts "rollout" pattern for the backfill, then conceded it is overkill because V2->V3 is copy the config + flip two flags. Her caveat, which got waved through: the V1 reg-card rewrite "ideally would have probably been a service method that our rollout would have called". Worth remembering if that rewrite needs re-running. (Andrea's framework = `onboarding/models/rollouts.py` + `onboarding/models/targeted_rollout.py`, RolloutRecipe / TargetedRollout / the /manage Rollouts page.)

3. **Batching: the Ishwar pattern** — ~10 hotels, then ~100, then everyone. Vibhor recalled it; Connor confirmed "that is generally the pattern we follow". Guido separately proposed batching by hotel COMPLEXITY / feature count rather than raw size, starting with hotels resembling the Wyndham UAT properties. Nobody reconciled "3 batches by size" with "batches by complexity" — both were agreed to loosely.

4. **Scope order.** US + Canada first (no additional-guests requirement there — Vibhor: "in North America it is the same"; Connor: "outside of North America, they do"). Wyndham and Best Western are already on V2 (Dana migrated the V1 stragglers). IHG is the last enterprise on V1 and goes straight to V3, but in the second or third group, not the first — Dana: "we will make sure we have a clean migration process that we have run before we do them." Explicitly the Intercontinental Hotel Group brand, not the POC portfolio.

5. **Scripting ownership split — my relayed position, accepted.** Stephanie: "I will relay Gareth's feedback as well, since he is not here. So his point of view on the scripting stuff should be that you guys are, or for any team, like, you guys know the features best, and generally those initial ones should be set up by you guys for the individual product; where we come in is anything that comes top-down from Salesforce, like onboarding values and things like that." Vibhor agreed "100%", adding that ongoing maintenance sits with onboarding and A&D provides guidance on new feature releases: "it does not make sense for us to own the maintenance of it. The first iteration and new feature releases, that is where we should provide the guidelines, guidance."

   Stephanie carved an exception for THIS project — onboarding wants to be more heavily involved than the default split, "A, from a knowledge piece, and also just timeframe and importance of doing this."

## Volumes and state (as stated on the call)

- ~700 hotels still on V1 in the US region, ~70 in EU, APAC unknown (Dana had to check). Dana was migrating a first batch that same day.
- Code cross-check: `v1_reg_card_service.py` docstring says ~1,970 active V1 hotels, using `rollout_check_in_v2_level="none"` as the correct V1 filter and noting `checkin_version` "was backfilled incorrectly" (ref: vault/checkin-v3-migration/v1-hotels-investigation.md). The meeting numbers and the code numbers do not obviously agree — may be region-scoped vs total.
- Wyndham/Best Western V1 stragglers were already migrated to V2. IHG is the only enterprise still on V1.
- Wyndham UAT properties have been on V3 for some time (Connor).
- ~10 Wyndhams collect deposits (Connor). Regular payment step already worked; the deposit path was what Guido was testing that day.

## Blockers named on the call

- Additional guests (Wave 2) — Dana: "we should be able to do additional guests in the next few weeks... we are pretty close, with the exception of ID OCR not working quite right."
- ID OCR solidity. Dana: "the only thing that is really blocking us... is making sure we really feel like the additional guests is solid, and OCR is solid."
- Configurator not yet built — NOT a migration blocker. Dana: you can migrate everything now; the only thing you cannot do pre-configurator is configure a V3-ONLY feature, because there is no way to edit it afterwards. No V3-only features have shipped yet (welcome amenities was the example given).

## The sequencing agreement (Dana + Vibhor, ~18:00-19:15 in the call)

Dana initially said "we probably should set that [rollout default] as default before we start migrating hotels over." Vibhor pushed back: "we should migrate some over, see that things are not broken." Dana agreed and restated the order:

  migrate ~100-200 hotels successfully -> flip the default to V3 -> then move the remaining V2 population "hopefully in fairly short order".

## Connor's warning (~19:17 — the origin of issue #1)

"For IHG, Wyndham, Best Western, we also create their reg cards through enterprise scripts that are separate. I know that for Best Western, we hadn't updated one of those, and as a result some of the Best Westerns got created on V1. So when we are ready to net new properties for those enterprises to be created with V3 as well, we need to update those on the enterprise side."

And on ordering: "basically, like, right before you guys migrate all of the Wyndoms, or all of the Best Westerns, we just need to include that in the scripts."

Dana confirmed both cases needed covering: "if you have someone who is already a customer who is not on Checkin, you enable on Checkin, we want them to do a V3, and if you create a new property as well, we want to make sure that they are on V3. I think these are the two cases we need to cover." Resolution was "we will coordinate with you guys" — NO OWNER, NO TICKET. That is the gap this item exists to close.

## Timeline / commercial pressure

- Vibhor hopes to migrate Wyndham + Best Western to V3 within this block; Dana called that "very reasonable".
- Connor flagged a Wyndham feature planned for Q4 block 1 that depends on the payments pod's unified payment submitter, which needs Wyndham on V3: "we have a vested interest in this getting out to Wyndham too, to unblock that work, so however we can help you guys get through Wyndham, we want help."
- Dana said A&D delayed other work so Guido could do the payment piece: "if you roll out with V3, you are going to have the payment stuff."
- Stephanie noted Rami is almost done unifying the expansion and non-expansion onboarding workflows into one — relevant to where the checkin_version write should land.

## Docs mentioned (worth chasing — unclear if they were actually circulated)

- Vibhor: a country-by-country config doc, already shared with Connor.
- Stephanie: a draft of the overall onboarding target state, to be reshared with the group; she was also to name collaborators per team for the "full engine design".
- Connor: a Notion page generated from the configuration scripts listing which countries have additional guests. Code equivalent is `ADDITIONAL_GUEST_STEPS_BY_COUNTRY` in `wyndham_registration_card_provider.py:188`.
- Guido said he would search Slack for a prior conversation about the ownership split.

## Exploration method

Read the transcript in full, then grepped and read: `guest_experience/services/v3_migration.py`, `v3_reconcile.py`, `v1_reg_card_service.py`, `migration_stats.py`, `guest_experience/signals.py`, `guest_experience/admin_views.py`, `check_in/management/commands/{migrate_hotel_to_v3,format_reg_cards_for_v2_check_in,revert_hotel_from_v3,reconcile_hotel_v3_flow}.py`, `check_in/models/{configuration,registration_card}.py`, `check_in/services/extendable_registration_card.py`, `check_in/schemas/check_in_configuration_external.py`, `onboarding/CLAUDE.md`, `onboarding/plans/registration_card_plans.py`, `onboarding/configuration_providers/configs/registration_card.py`, the BW and Wyndham reg-card providers, `onboarding/models/{rollouts,targeted_rollout}.py`, and the guest/check-in frontends.

NOT verified: nothing was run against staging or production; all counts above are from the transcript or from code comments, not from a live query. No tests were run.