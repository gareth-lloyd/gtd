---
area: null
completed_at: null
contexts:
- consume
created: 2026-09-28 07:41:13.952877
defer_until: null
due: 2026-09-30
energy: medium
id: 2026-09-28T0741-follow-up-on-review-step-configurator-demo-recordi
order: null
output: |-
  ## Agent run 2026-09-28T14:49

  ### Verdict

  Lea's point is correct and it is wider than the Binding Rules Tree. Take the 30 minutes they offered. Nothing in binding-tree releases 1-3 is blocked, but two things need an owner and a date, and the docs do not settle either.

  Not sent, not scheduled: no Slack reply, no calendar invite. Draft reply is at the bottom.

  ### What I reviewed

  - Demo: I did NOT watch the Zoom video. I read the Notion AI notes and full transcript of the same session (2026-09-17), "Check-in step configurator": https://app.notion.com/p/3de81468615180c9a93fcf15b8fd4451 . The transcript has no speaker labels, so who said what is inferred.
  - Recording thread (Zoom link, passcode reported broken, access by request): https://canarytechnologies.slack.com/archives/C029BPP02H0/p1789742116153609
  - Lea's replies to you: https://canarytechnologies.slack.com/archives/C0A5Z7LE5AL/p1790347733658459?thread_ts=1790339063.940229&cid=C0A5Z7LE5AL
  - TDD "Check-In V3 Configuration" (APPROVED, edited 2026-09-25): https://app.notion.com/p/365814686151808c805efb429b821412
  - "Proposal: Schemaform Field Catalog" (2026-08-12): https://app.notion.com/p/3a581468615180909522f2e4127f21f7
  - Your doc, Binding Rules Tree: https://app.notion.com/p/canarytechnologies/Binding-Rules-Tree-3e58146861518147b489e3fa8e8aef09
  - Code on origin/master (fetched today): guest_experience/models/{catalog_field,step_form,step_form_element}.py, services/additional_guest_flow_generation.py, steps/schema_form/handler.py, check_in/models/configuration.py, enterprise_ihg/configs, enterprise_wyndham/configs.
  - Linear project "Step configurator flow builder" (lead Leandro Alvarez, due 2026-10-09, on track): https://linear.app/canary-technologies/project/d20b159a-188d-4dec-b925-c4fe0c2aa241
  - Figma (not opened): https://www.figma.com/design/SH9uOmxQwB3VuCb7dZG1IW/Check-in-Configuration?node-id=370-63830

  ### What the configurator changes

  - Two kinds of setting, treated differently.
    - Bucket settings (ID Settings, Payment Settings) are typed facades over existing columns. No migration. `id_step_with_ocr`, `id_options`, consent text stay on `CheckInConfiguration`. The ID bucket derives `id_step_mode` and `is_ocr_enabled` from `id_step_with_ocr` and writes that column back.
    - Guest-data fields move to three per-hotel tables: `CatalogField` (definition), `StepForm` (one per schemaform step), `StepFormElement` (ordered placement). The form JSON is composed from rows on read.
  - The schemaform step is reused for the primary registration card, the primary ID/OCR review, and the additional-guest form. That is why per-field columns stop being the authoring surface.
  - Additional-guest catalog is undecided. Demo: "up in the air", "95% sure" it needs its own catalog or grouping because PMS mappings differ. Also said: additional-guest fields "usually don't need tags".
  - Hotel admins get a restricted view: they can reorder and remove catalog fields from their forms and edit text. They cannot create fields or change PMS mappings.

  ### Where the code is today (verified)

  - `Configuration.uses_field_catalog` exists, default False. Nothing on the guest path reads it yet. `steps/schema_form/handler.py` still serves `configuration.schema_form_json`.
  - Extraction landed 2026-09-24 (AD-8176, #56116): `extract_hotel_catalogs`, primary registration card only.
  - The additional-guest form is still generated from columns: `additional_guest_flow_generation.py` reads 24 `ci.additional_guests_*` columns plus `ci.id_document_date_of_issue`.
  - So today the columns are still what v3 reads. The risk is medium-term, not immediate.

  ### Impact on the Binding Rules Tree

  1. The planned first rules are safe. `EU_ID` / `ES_ID` on `id_step` and `id_step_with_ocr`, German retention, membership push, and the Italy `additional_guests_id` question are all step-level or bucket columns. These stay columns.
  2. One sentence in your Slack message overreaches. "Adds safety without requiring changes to Check-in v3 ... columns v3 already reads (`id_step`, `id_step_with_ocr`, `additional_guests_*`)" holds for the first two and for `additional_guests_step` / `additional_guests_id`. It stops holding for the per-field `additional_guests_<field>` columns once a hotel is on the catalog.
  3. The bigger exposure is the existing brand trees, not the binding tree. IHG's country modules and Wyndham define 21 per-field `additional_guests_*` keys and 13 `id_document_*` keys. After a hotel flips, those defines check columns the guest form no longer reads. Drift would report green while the form diverges.
  4. The engine has no shape for this. Keys are dotted paths to one scalar column. A legal field requirement under the catalog is "the additional-guest form contains a field for X and it is required", which is a property of a set of rows. The doc's predicates (`OneOf`, `AtMost`, `Empty`, `SubsetOf`) have no "must contain" form.
  5. There is no stable cross-hotel handle unless tags are kept. `element_id` is unique per hotel. `tags` (`CheckInSchemaFormTag`) is the only identifier a rule could address across hotels, and the demo suggests dropping tags for additional-guest fields.
  6. Hotel self-serve removal is the compliance risk. A Spanish hotel admin removing second last name or nationality from the form is exactly what a binding rule should stop, and the catalog write path (`CatalogFieldWriteService`, `StepFormElementService`) has no hook for it.
  7. Seeding is assigned to your team. The TDD puts "Config seeding / generation" out of scope: "enterprise owns it (onboarding scripts + rules framework)". Lea's message is therefore an ask on the onboarding providers, which the Binding Rules Tree doc also puts out of scope (section 12). Neither side currently owns creating `CatalogField` / `StepForm` rows at onboarding.
  8. Already noted by A&D as open: the TDD says there are no FINAL/FREE locks in scope, "a CS edit can diverge from an enterprise-seeded value", and lists alignment with Enterprise on "the FINAL/FREE locking direction" as a dependency.

  ### Questions for the 30 minutes

  1. Which columns stay bucket settings and which become catalog rows? My reading: `id_step*`, `id_options`, `additional_guests_step`, `additional_guests_id` stay; `additional_guests_<field>` and `id_document_<field>` become rows. Confirm.
  2. After a hotel flips, what happens to the per-field columns: frozen, kept in sync, or dead? Do v2, tablet registration and kiosk keep reading them?
  3. Additional-guest catalog: separate or shared, and when is that decided? Can standard fields keep a tag or another stable key so a rule can address them?
  4. Who writes catalog rows for a new hotel, and could that seeder call `binding_rules_for_country(country)`?
  5. Where would a legal constraint hook into catalog writes, and can the restricted hotel view render a locked field with the rule's explanation?
  6. Flip timeline: when does the first production hotel compose from the catalog, and when does additional-guest follow?

  ### Suggested doc changes (yours to make)

  - Add a known-gap note: per-field guest-data requirements move to catalog rows; binding and brand rules on those columns stop describing v3 hotels after the flip.
  - Narrow the "no changes to Check-in v3" claim to step-level and bucket columns.
  - Add A&D (Lea) to the open-questions table for the row-shaped key problem.

  ### Minor: design doc vs code

  The Field Catalog proposal is older than the code. `StepForm` is one-to-one with `Step` and has no `flow` or `position`; `mappings` became `tags` + `selectors`; the placement FK is `RESTRICT`, not `PROTECT`. The demo also showed the CS configurator under hotel settings via SAG impersonation, while the TDD says `/manage`.

  ### Draft reply to Lea (NOT sent)

  > Went through the demo notes, the TDD and the Field Catalog proposal. You're right, and it reaches further than the binding tree: our IHG and Wyndham trees already define the per-field `additional_guests_*` and `id_document_*` columns, so once a hotel composes from the catalog those rules stop describing what the guest sees. The step-level ones (`id_step`, `id_step_with_ocr`, `additional_guests_step`, `additional_guests_id`) look unaffected, which covers the first rules we plan to ship.
  >
  > Let's take the 30 minutes. What I'd like to cover: which columns stay bucket settings vs become catalog rows, what happens to the columns after a hotel flips, whether additional-guest fields can keep a tag or other stable key so a rule can address them across hotels, and who seeds catalog rows at onboarding. I'll send an invite.

  ## Agent run 2026-09-29T14:54

  > Follow-up asked: "eli10"

  Plain-language version of the 2026-09-28 run above. No new research: nothing was re-checked today, and nothing was sent or scheduled.

  ### The one-paragraph version

  Lea's team is changing where the check-in form's questions are stored. Our rules engine checks the old place. For some rules that is fine forever. For others, the rule will keep saying "all good" while looking at something the guest never sees.

  ### The picture

  Every hotel has a control panel full of switches.

  - Big switches: "do we ask for an ID?", "do we scan it?", "do we ask about additional guests?".
  - Small switches, one per question: "ask the extra guest for nationality?", "ask for the date the ID was issued?".

  Our rules engine is an inspector. It walks along the panel and checks each switch is where the law or the brand says it must be.

  The step configurator changes the panel:

  - The big switches stay where they are.
  - The small switches are replaced by a stack of question cards per hotel. The form is whatever cards are in the stack, in that order. Hotel staff can reorder cards and take cards out.

  ### Why that matters to us

  1. The first binding rules we plan to ship only look at big switches. They are safe.
  2. The IHG and Wyndham rules we already have look at 34 small switches (21 additional-guest, 13 ID-document). Once a hotel moves to cards, those switches are still on the panel but wired to nothing. The inspector reports green and the form can be wrong.
  3. The inspector only knows how to check a switch. "Is there a nationality card in this stack, and is it marked required?" is a different kind of check. The engine cannot express it today.
  4. Cards have no shared name. Each hotel's nationality card has its own ID. The only label common to all hotels is a tag, and the demo suggested additional-guest cards may not get tags. Without a shared label a rule cannot say "the nationality card".
  5. Hotel staff can remove a card. A Spanish hotel could take out a question the law requires, and nothing stops that today.
  6. Nobody fills the stack for a new hotel. Lea's TDD says our team does it. Our doc says it is out of scope. So it has no owner.

  ### How urgent

  Not today. The card tables exist, but the guest form does not read them yet: the switch that turns cards on (`uses_field_catalog`) is off by default and nothing on the guest path looks at it. The additional-guest form is still built from the old small switches. This was true on 2026-09-28; their project is due 2026-10-09 (https://linear.app/canary-technologies/project/d20b159a-188d-4dec-b925-c4fe0c2aa241).

  ### What to do

  Take the 30 minutes Lea offered (https://canarytechnologies.slack.com/archives/C0A5Z7LE5AL/p1790347733658459?thread_ts=1790339063.940229&cid=C0A5Z7LE5AL). Four questions in plain words:

  1. Which switches stay, and which become cards?
  2. After a hotel moves to cards, do the old switches die, freeze, or stay in sync?
  3. Can cards keep a shared label so a rule can point at them?
  4. Who fills the stack for a new hotel, and how do we stop a hotel removing a card the law requires?

  ### Picture to real names

  - Switch: a column on `CheckInConfiguration`.
  - Big switch: step-level or bucket setting (`id_step`, `id_step_with_ocr`, `additional_guests_step`, `additional_guests_id`).
  - Small switch: per-field column (`additional_guests_<field>`, `id_document_<field>`).
  - Card: `CatalogField`. Stack: `StepForm` plus `StepFormElement`.
  - Shared label: `tags` (`CheckInSchemaFormTag`).
  - Inspector: the rules engine and its drift check.
  - Docs: TDD https://app.notion.com/p/365814686151808c805efb429b821412 , Binding Rules Tree https://app.notion.com/p/canarytechnologies/Binding-Rules-Tree-3e58146861518147b489e3fa8e8aef09

  ### Still open

  The Slack reply to Lea and the calendar invite are not sent. The draft reply is in the run above.

  ## Agent run 2026-09-29T15:17

  > Follow-up asked: "Review the relevant AD team code at a high level, and then re-explain the issue here with concrete code references"

  Read-only review of origin/master at 48fa7c13384 (2026-09-29). Paths are relative to `backend/canary/`. Nothing was run, sent or scheduled.

  ### Refinement to the 2026-09-28 run

  No per-field column rule is affected by the catalog code that exists today. Extraction covers the registration card only, and that form was never driven by per-field columns. The collision starts when the additional-guest form and the ID review form get a `StepForm`. Both are still generated from columns.

  ### Today: a column rule reaches the guest in four hops

  1. A rule pins a column. `enterprise_ihg/configs/countries/australia.py:99` defines `additional_guests_first_name` as FINAL / REQUIRED. Spain defines `additional_guests_nationality` at `enterprise_ihg/configs/countries/spain.py:270`.
  2. Saving the configuration re-seeds the v3 flow: `guest_experience/signals.py:75` (`sync_v3_flow_on_config_save`).
  3. The generator turns the column into a form element. `guest_experience/services/additional_guest_flow_generation.py:185` reads `ci.additional_guests_nationality`, emits an element tagged `NATIONALITY` (line 198), and stores the whole form in `SchemaFormStepConfiguration.schema_form_json` (line 500).
  4. The handler serves and validates with that stored JSON: `guest_experience/steps/schema_form/handler.py:162` and `:130`.

  The ID review form works the same way: `guest_experience/check_in/defaults/default_id_information_review.py:135` reads `ci.id_document_nationality`.

  So today the column is a truthful stand-in for the form, and a drift check on the column means something.

  ### What A&D has built

  - `CatalogField` (`guest_experience/models/catalog_field.py:82`): one field definition per hotel. Carries `tags` (line 140), `is_required` (154), `is_standard` (162), `is_active` (167). `element_id` is unique per hotel only (line 176).
  - `StepForm` (`guest_experience/models/step_form.py:27`): one-to-one with a schemaform `Step` (line 49).
  - `StepFormElement` (`guest_experience/models/step_form_element.py:20`): a placement. It holds order and nothing else.
  - Composer (`guest_experience/services/schema_form_composer.py:34`): builds the form from placements whose field is active (line 39). "Required" comes from `catalog_field.is_required` (line 95). The module never reads `CheckInConfiguration`.
  - Extraction (`guest_experience/services/catalog_extraction.py:51`): copies a hotel's existing form into rows and refuses if the round trip differs (line 116). Registration step only (line 150). Skips portfolio-managed hotels (line 53).
  - Write services: `guest_experience/services/catalog_field.py:34` and `guest_experience/services/step_form_element.py:15`.
  - Flag: `check_in/models/configuration.py:1115` (`uses_field_catalog`, default False).

  Nothing on the guest path reads the flag or calls the composer. The composer's only callers are extraction (`catalog_extraction.py:114`) and write-time validation (`services/catalog_field.py:116`).

  ### Where the chain breaks once a form composes from rows

  1. Hops 2 to 4 are bypassed. The composer reads rows, not columns. `additional_guests_nationality = REQUIRED` can sit in the column while the form has no nationality placement. The engine checks the column and reports conformant.
  2. Two writers, no decision. `signals.py:75` still rewrites `schema_form_json` from columns on every Configuration save. After the flip that write is either ignored or it fights the catalog. Nothing in the code settles which.
  3. No stable name for a rule to point at. `_next_element_id` (`services/catalog_field.py:98`) names hotel-created fields by type plus a counter: `text_input`, `text_input1`. Extracted fields keep whatever id the hotel's form used. `tags` is the only shared vocabulary and it is optional (`blank=True, default=list`, `catalog_field.py:140`).
  4. Three unguarded ways a required field disappears:
     - Delete the placement: `StepFormElementService.delete_element` (`services/step_form_element.py:40`) deletes and logs an event. The view's gatekeeper lists `CHECK_IN_HAS_SETTINGS_ACCESS` (`guest_experience/views/step_form_element.py:156`). I read that as settings access being enough; I did not open the `hotel_any` / `hotel_all` line.
     - Deactivate the field (`is_active=False`): advanced access only.
     - Clear `is_required`: advanced access only. Settings-only users can edit `label` and `translations` (`services/catalog_field.py:26`, enforced at line 91).
     None of these services imports anything from `rules_based_configuration`.
  5. No seeder for a new hotel. `StepForm`'s docstring calls flow wiring "the seeder's business" (`step_form.py:30`) and `is_standard` means "seeded from the default template" (`catalog_field.py:162`). The only row writer I found is extraction, which needs an existing form. I did not search exhaustively for a default-template seeder.

  ### The columns cannot simply die

  Other surfaces read the per-field columns directly: v2 check-in (`check_in/views/base_check_in_view.py`, `guest/views/id_document_view.py`, `guest/views/guest_id_document_view.py`), hotel serialization (`hotels/utils/api/serialize_hotel.py`), and kiosk for `id_document_*` (`kiosk/steps/check_in/id_information_review/step.py`, `kiosk/steps/check_in/collect_identity_details/step.py`). After a flip, a column rule stays correct for v2 and kiosk and stops describing v3 web.

  ### Smaller findings

  - `uses_field_catalog` is already in the engine's key list (`rules_based_configuration/services/conformity.pyi:217`). A brand tree could pin it to False as a stopgap. Unverified beyond the key being listed.
  - v3 already ignores some `id_document_*` columns. First name, last name and other identity-critical fields always render as required (`default_id_information_review.py:61`), so `spain.py:130` (`id_document_first_name`) has no effect on the v3 web form.
  - Key count confirmed from the brand configs: 21 per-field `additional_guests_*` keys plus 13 `id_document_*` keys.

  ### Extra questions for Lea from the code

  1. Are IHG and Wyndham hotels portfolio-managed for registration cards? If so, extraction skips them (`catalog_extraction.py:53`).
  2. When the additional-guest form gets a `StepForm`, what happens to the reseed in `signals.py:75`?
  3. Will standard additional-guest fields carry the same tags the generator emits today (`additional_guest_flow_generation.py:89` onward)? That would give rules their stable handle.

  ## Agent run 2026-09-29T15:22

  > Follow-up asked: "State what Leandro actually said, in straightforward form"

  Re-read the thread today: https://canarytechnologies.slack.com/archives/C0A5Z7LE5AL/p1790347733658459?thread_ts=1790339063.940229&cid=C0A5Z7LE5AL

  ### Lea's three messages (2026-09-25), verbatim

  1. "Still reading through it, thanks for sharing! One thing to note, as you are calling out the `additional_guest_*` fields is that as part of the configurator we are building a better authoring surface for forms. The additional guest id fields stop being a hardcoded configuration and are instead `StepForms` that contain `CatalogFields` that CS defines for properties. So the seeding for that and also the `id_*` fields (gender, dob, etc) will need to start creating `CatalogFields` and a `StepForm` for primary guest id and another for additional guest OCR review in EU"
  2. "I think the easiest way to discuss this would be to schedule half an hour to show you where we stand on the configurator, but if you don't have the time I can share the design docs and a guide on how to see the configurator locally"
  3. "There's als a recording for an internal demo we did last week" plus the recording link.

  ### In plain terms

  - Lea had not finished reading the doc.
  - One point only: the additional-guest ID fields and the `id_*` fields stop being hardcoded configuration. They become `StepForm`s holding `CatalogField`s, which CS defines per property.
  - One consequence only: seeding has to create those rows. Two forms are named: primary guest ID, and additional-guest OCR review in the EU.
  - One offer: 30 minutes to demo the configurator, or the design docs plus a local setup guide.

  ### What Lea did not say

  Everything else in the runs above is my inference, not Lea's: stale drift checks, the IHG and Wyndham trees, missing tags, hotels removing required fields, the missing write hook, and who owns seeding. Lea raised no objection to the proposal and did not say the binding tree is blocked.

  ### Two ambiguities worth asking about

  - "The additional guest id fields" could mean only the ID fields or all `additional_guests_*` fields. The two forms Lea names are both ID/OCR review forms. The additional-guest details form is not mentioned.
  - "The seeding" does not say whose. The TDD assigns it to enterprise.
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C0A5Z7LE5AL/p1790347733658459?thread_ts=1790339063.940229&cid=C0A5Z7LE5AL
tags:
- morning-gtd
- slack
time_minutes: 30
title: 'Follow up on: review step-configurator demo recording and docs (promised Leandro)'
updated: 2026-09-29 15:28:25.559543
waiting_on: null
waiting_since: null
working_on: false
---

I told Leandro on 09-25 I'd review the recording and docs and schedule time if needed. His point: additional_guest_* and id_* fields become StepForms/CatalogFields, which changes how the Binding Rules Tree seeds them.
Recording: https://canarytechnologies.slack.com/archives/C029BPP02H0/p1789742116153609
https://canarytechnologies.slack.com/archives/C0A5Z7LE5AL/p1790347733658459?thread_ts=1790339063.940229&cid=C0A5Z7LE5AL

https://www.figma.com/design/SH9uOmxQwB3VuCb7dZG1IW/Check-in-Configuration?node-id=370-63830&p=f