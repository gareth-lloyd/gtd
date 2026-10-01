---
area: null
completed_at: 2026-10-01 14:49:59.736178
contexts: []
created: 2026-10-01 11:40:24.394012
defer_until: null
due: null
energy: low
id: 2026-10-01T1140-write-up-notes-from-call-with-leandro-actions-for
order: null
output: |
  ## Agent run 2026-10-01T14:36+03:00

  Notes and binding-tree actions from the call with Leandro Alvarez and Andrea Bradshaw, Wed 2026-09-30 9:11 PM (Granola: "Step configurator and rules-based", https://notes.granola.ai/d/c12bc682-f460-41f8-83c1-65437690c98c). Nothing was sent, posted or edited anywhere; the Notion doc is untouched.

  Headline: Leandro sees rules-based config and drift detection on Check-in V3 as feasible and raised no objection. The one change it forces is that per-field guest-data settings stop being columns, so the engine, the brand trees and the onboarding scripts all need to learn about catalog fields and step forms. The first binding rules (`id_step`, `id_step_with_ocr`, retention, memberships) are not affected.

  How this was produced: I read the Granola summary and the full transcript. The transcript labels Leandro and Andrea by name and you as the microphone, so attribution below is from the transcript, not the summary. You made no first-person commitments on the call. The "Actions for the binding tree" section is therefore my derivation from what was said plus a code check on local master (09dcddac88c, 2026-10-01), not a list of things you promised.

  ### What was said

  1. Feasibility (Leandro). Feasible. Only flag: A&D are mid-transition to the catalog and V3, and rules-based work should fit that rather than fight it. Likes drift detection because it controls what CS can and cannot do in the configurator. Wants drift surfaced in the configurator eventually; explicitly not a blocker for you.
  2. Sync direction (Leandro, correcting your assumption). You asked whether there is no reverse sync from the configurator back to `CheckInConfiguration`. There is: `CheckInConfiguration` is still the source of truth and the configurator surfaces it. Turning additional guests off in the configurator persists to the column. The exception is the ID collection fields for the primary guest and for additional guests: once a hotel uses the catalog, those are edited in the catalog and the columns stop being updated.
  3. Forward sync (your replay, confirmed with "Yeah, it is" by an unlabelled speaker, almost certainly Leandro). The V3 migration reads `CheckInConfiguration` and creates the matching V3 objects, and post-save signals repeat that when someone later changes a setting.
  4. Seeding changes (Leandro). "We won't be seeding registration cards, we will be seeding catalog fields and creating forms for them." Onboarding only needs to feed an initial set of catalog fields, and perhaps a couple of forms so the registration card exists on day one. One form maps to one step. A change to a catalog field propagates to every service using that form, including kiosk once it migrates.
  5. Diffing is the hard part (Leandro). The model is now relational: a step form holds several catalog field references. But the SchemaForm data model has not changed: a step form is read and composed into the same JSON blob the registration card used.
  6. Workaround (Leandro). You can still write a registration card and run the script that converts it into catalog fields. It stops working once CS splits a card into several step forms, which kiosk needs (about 10 steps). Long-run intent: retire the registration card model.
  7. ID OCR review step (Leandro). Previously hardcoded in the frontend, now a form too. CS can add fields and map each to a PMS value, so a request like mother's maiden name for an EMEA property needs no code.
  8. Rules engine today (you). Flat keys only (`hotel.<config object>.<attribute>`), one value per setting, cannot iterate registration cards. Onboarding scripts are imperative; rules-based only checks values after onboarding. You said the engine could be extended to the new objects.
  9. Registration-card churn (you, Andrea). Stable. Andrea: the only changes are IHG cards as countries are added.
  10. IHG on V3 (Andrea, you). Andrea is about 85% sure every IHG hotel is still on V2, copied from the pilot, and her read is that the switch waits on confirmation that V3 supports all flows. You cited Caitlin's thread from Thursday 2026-09-24 saying the aim is to move all IHG to V3. I did not look that thread up.
  11. V3 status (Leandro). Configurator rollout started with B-Works Test Hotel and the catalog migration worked; next is a few production hotels with complex registration cards. The additional-guest parity gap just closed. General release is blocked only on finishing the configurator. Several properties already run V3. Guido runs the migration and has a dashboard. The check-in version is a flag on the check-in configuration.
  12. Rules-based timeline (you). No date. Competes with GDPR, SDM and PMS-capabilities work for engineers.
  13. Andrea's takeaway. She had assumed V3 meant different field values; the scripts will instead need to create reusable field and form modules, not input a registration card form.

  Two places the Granola summary is off: it credits "not urgent" to Andrea, but that was your read of her position; and it leaves out the sync discussion entirely, including Leandro's correction in item 2, which is the part that matters most for the binding tree.

  ### What the code says today (checked on local master, 2026-10-01)

  This moved since the 2026-09-29 review in the step-configurator item, which found nothing on the guest path reading the catalog flag.

  - The guest path now reads `uses_field_catalog`. `SchemaFormService.get_schema_form_json` composes from the catalog when the flag is on (`backend/canary/guest_experience/steps/schema_form/service.py:248`).
  - Writes to catalog-owned columns are refused. A `pre_save` on `Configuration` raises `AdditionalGuestFormManagedByCatalog` when a write changes any of 23 per-field `additional_guests_*` columns on a catalog hotel (`guest_experience/signals.py:77-86`, list at `check_in/models/configuration.py:104`, from #57800 / AD-8447, 2026-09-29). `additional_guests_step` and `additional_guests_id` are not in the list, which matches Leandro's item 2.
  - Nothing outside `guest_experience` and one test references that exception. Onboarding, the enterprise configs and `rules_based_configuration` do not handle it.
  - `id_document_*` columns are not in that guard list. I did not search for a separate guard on them.
  - Moving a hotel to the catalog skips portfolio-managed registration cards (`guest_experience/services/guest_fields_source.py:52`).
  - A migration dashboard exists in admin and shows V3 and catalog status per hotel (`guest_experience/services/migration_stats.py`, `templates/admin/guest_experience/migration_dashboard.html`). This is probably Guido's dashboard.

  ### Actions for the binding tree

  None of these blocks releases 1 to 3. Ordered by how soon each bites.

  1. Check what an onboarding rerun does to a catalog hotel. (30 to 60 min, code reading)
     - A script that changes a per-field `additional_guests_*` column on a catalog hotel now raises in `pre_save`. IHG is the live case: its cards change as countries are added, and IHG's country modules define those keys.
     - Outcome wanted: either the scripts skip those columns when `uses_field_catalog` is true, or A&D agree not to move enterprise hotels until the scripts can seed the catalog.
  2. Add a "Check-in V3 field catalog" known gap to the Binding Rules Tree doc (https://app.notion.com/p/canarytechnologies/Binding-Rules-Tree-3e58146861518147b489e3fa8e8aef09). (15 min)
     - A keyword search of the page today found no mention of the catalog, `StepForm` or `CatalogField`. I read the headings and the matching passages, not the whole page.
     - Content: step-level and bucket columns stay the source of truth, so the planned first rules stand. Per-field ID collection settings for primary and additional guests move to catalog rows; on a catalog hotel the columns go stale and cannot be written.
     - In Appendix A "Migration", the Wyndham and IHG rows say the per-field `additional_guests_*` defines "Stay". Add the caveat that for catalog hotels drift on those keys compares a column the guest form no longer reads, so it can report green or red against nothing.
  3. Update the doc's "Open questions for others" table. (10 min)
     - Extend the existing A&D (configurator) row: Leandro wants drift surfaced in the configurator later; not a blocker.
     - New A&D row, owner Leandro: how a rule addresses a field across hotels (tags or another stable key), and where a legal constraint hooks into catalog writes. Neither came up on the call.
  4. Decide how drift treats the 23 catalog-owned keys for catalog hotels. (decision, then a small change)
     - Options: skip those keys when `uses_field_catalog` is true, or pin `uses_field_catalog` to False in the IHG and Wyndham trees as a stopgap. The key already exists in the engine (`rules_based_configuration/services/conformity.pyi:218`). The second option holds enterprise hotels off the catalog, so it needs Leandro's agreement.
  5. Later design: a catalog reader for the engine. (not for releases 1 to 3)
     - Leandro's item 5 suggests a cheaper route than diffing relations: test a predicate against the composed SchemaForm JSON, the same blob shape as before. This follows the reader pattern the doc already uses for retention. It depends on fields keeping a stable tag, which is question 3's open point. This suggestion is mine, not something agreed on the call.
  6. Onboarding seeding needs an owner. (outside the doc's scope, section 12, but it is your team's)
     - Leandro and Andrea both described the scripts creating a default set of catalog fields plus forms. The A&D TDD assigns seeding to enterprise. Candidate ticket, IHG first. The interim route is the registration card plus conversion script from item 6 above, which lasts until CS splits forms.
  7. Tell Blake the outcome, if you owe him one: feasible, A&D have no objection, no date, and the catalog work above is the cost. The call was framed around Blake's push at planning week; nobody on the call asked for a report back.

  ### Waiting on others

  - Leandro: will ask Guido how many properties run V3 and which are IHG. Confirmed in a labelled Leandro turn. You told him it is not urgent.
  - If you want it sooner, the admin migration dashboard above likely answers it, or I can run a read-only query against the Snowflake mirror on request. I did not query anything.

  ### Draft follow-up to Leandro (NOT sent)

  For the step-configurator thread (https://canarytechnologies.slack.com/archives/C0A5Z7LE5AL/p1790347733658459?thread_ts=1790339063.940229&cid=C0A5Z7LE5AL):

  > Thanks for yesterday, that cleared up most of it. Three things we didn't get to:
  > 1. Will standard fields keep a tag (or another key that is the same across hotels)? A rule like "Spain must collect nationality for additional guests" needs something to point at.
  > 2. I saw #57800 refuses writes to the per-field `additional_guests_*` columns on catalog hotels. Our onboarding scripts and IHG country configs still write those. Are any enterprise hotels in the next batch you move to the catalog? I'd like our scripts to skip those columns before that happens.
  > 3. Is the same guard planned for the primary `id_document_*` columns?

  ### Related item

  This call was the 30 minutes Leandro offered, so it likely settles "Follow up on: review step-configurator demo recording and docs (promised Leandro)" (next/2026-09-28T0741-follow-up-on-review-step-configurator-demo-recordi.md). The draft reply to Leandro in that item is now out of date. Of its six prepared questions, the call answered which columns stay, what happens to columns after the flip, who seeds, and the rollout stage; it did not cover tags or the write hook.

  ## Agent run 2026-10-01T14:50+03:00

  > Follow-up asked: "check 1"

  Action 1 checked: what an onboarding rerun does to a catalog hotel. Code reading only on local master (09dcddac88c); nothing was run, and no test was written to prove any path. Paths are relative to `backend/canary/`. The item was archived at 14:49 while this ran; I appended here and left it archived.

  ### Answer

  The onboarding scripts never reach the catalog guard. The registration card plan refuses every V3 hotel before it writes anything, and it has done since 2026-09-28. That corrects action 1 in the run above, which said the script "now raises in `pre_save`". The path that does hit the catalog guard is the rules engine's own `apply_portfolio_settings` command.

  ### Onboarding scripts: refused at the plan, whole run rolled back

  - `AddRegistrationCardPlan.execute` raises `ERROR_HOTEL_ON_CHECK_IN_V3` when `checkin_version == V3`, before the provider or any column write (`onboarding/plans/registration_card_plans.py:69-71`). Added by #57957 (ENT-7607, https://github.com/canary-technologies-corp/canary/pull/57957), merged 2026-09-28.
  - The operator message is: "Onboarding scripts do not support check-in v3 yet. Skip this plan for the hotel, or ask the team that owns check-in v3 to make the registration card changes." (`onboarding/exceptions.py:578`).
  - It is the only onboarding path that writes these columns. All the brand providers (IHG's nine country modules, Wyndham, Best Western) feed it, and it saves with `update_fields` at line 89. No registration card provider registers a targeted rollout, so rollouts do not bypass the check.
  - The refusal fails more than the card. Plans run in one transaction per hotel and an expected error re-raises (`onboarding/services/onboarding.py:715-737`), so every other plan in that script run rolls back too. The plan is wired into the IHG pilot, IHG GMS Core, Wyndham MSA and Best Western MSA processes; my grep suggests the `BASE_CONFIGURATION_NEW` stage in each, but I did not open each stage block to confirm. Rerunning that stage on a V3 hotel therefore fails outright unless the plan is skipped.
  - Consequence for IHG: once an IHG hotel is on V3, a registration card or country-settings change cannot be delivered by rerunning the script. This applies to V3 as a whole, not only to catalog hotels, so it bites at the V3 move that Caitlin's thread describes, before any catalog move.

  ### `apply_portfolio_settings`: this is the one that hits the guard

  - The command writes every value the brand tree resolves for a hotel and calls a full `obj.save()` with no `update_fields` and no V3 or catalog check (`rules_based_configuration/management/commands/apply_portfolio_settings.py:106-150`).
  - On a catalog hotel, if any of the 23 catalog-owned columns differs from the tree's value, the `pre_save` guard raises `AdditionalGuestFormManagedByCatalog` (`guest_experience/signals.py:77-86`).
  - Nothing catches it. That hotel's transaction rolls back and the command stops, so hotels earlier in the loop are already changed and later ones are untouched.
  - Exposure by tree: each of IHG's nine country modules defines 21 of the 23 guarded keys. Wyndham defines one (plus the two step-level keys, which are not guarded).
  - A second guard can fire on the same save: turning `additional_guests_step` on for a catalog hotel whose additional-guest name form has no catalog rows raises `AdditionalGuestsNeedCatalogForm` (`guest_experience/signals.py:89-97`). IHG's country modules define that key.
  - The command is manual and was last changed 2026-07-27. I do not know how often it is run.

  ### Paths that are safe

  - Drift detection only writes `StoredHotelAttributes` (`rules_based_configuration/services/drift.py:148`, `:177`). It never writes `Configuration`, so it cannot raise. It still reports against columns the guest form no longer reads.
  - `onetime_wyndham_disable_id_capture_gdpr` writes `id_step`, `id_step_with_ocr` and `additional_guests_id`, none of which is guarded.

  ### Two gaps in the guards themselves

  - The plan checks V3; the guard checks the catalog flag. They are not the same set. The admin dashboard only moves V3 hotels (`guest_experience/services/v3_migration.py:131`), but the `move_hotels_onto_catalog` command calls `GuestFieldsSourceService.move_to_catalog` directly with no version check. A non-V3 hotel moved that way would pass the plan's check and hit the `pre_save` guard as an unexpected error instead.
  - `QuerySet.update()` skips `pre_save`, so a bulk update can still change a guarded column. One existing one-off does this (`check_in/management/commands/onetime_hide_additional_guests_language_preference.py:56`).

  ### What this changes in the action list above

  - Action 1 is answered. Its "outcome wanted" (scripts skip those columns, or A&D hold enterprise hotels off the catalog) is moot for onboarding, because the scripts refuse V3 hotels entirely.
  - New, small: make `apply_portfolio_settings` handle catalog hotels. Skip the 23 guarded keys when `uses_field_catalog` is true, and log them, so one catalog hotel does not stop a portfolio run halfway. This is the same decision as action 4 (how drift treats those keys), so decide both together.
  - Action 6 (seeding owner) is more pressing than I wrote. ENT-7607 made "onboarding does not support V3" an explicit refusal, so the gap is no longer just the catalog: any IHG hotel on V3 is out of reach of the scripts today. Worth reading ENT-7607 for what was agreed as the follow-up; I did not open the ticket.
  - Question 2 in the draft to Leandro above is now wrong. Replacement (NOT sent):

  > 2. Since ENT-7607 our registration card plan refuses V3 hotels outright, so country changes for an IHG hotel on V3 have no script path. What is the intended route for those today: your team makes the change, or we teach the scripts to write catalog fields and forms? Separately, `apply_portfolio_settings` does a full save and will hit the #57800 guard on a catalog hotel, so we need it to skip the catalog-owned columns.
project: null
source_id: null
tags: []
time_minutes: 5
title: Write up notes from weds evening call with Leandro and andrea (granola), actions
  for binding tree
updated: 2026-10-01 14:50:07.000000
waiting_on: null
waiting_since: null
working_on: false
---