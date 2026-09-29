---
area: null
completed_at: null
contexts:
- consume
created: 2026-09-28 07:41:13.952877
defer_until: null
due: 2026-09-28
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
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C0A5Z7LE5AL/p1790347733658459?thread_ts=1790339063.940229&cid=C0A5Z7LE5AL
tags:
- morning-gtd
- slack
time_minutes: 30
title: 'Follow up on: review step-configurator demo recording and docs (promised Leandro)'
updated: 2026-09-28 15:47:16.638944
waiting_on: null
waiting_since: null
working_on: true
---

I told Leandro on 09-25 I'd review the recording and docs and schedule time if needed. His point: additional_guest_* and id_* fields become StepForms/CatalogFields, which changes how the Binding Rules Tree seeds them.
Recording: https://canarytechnologies.slack.com/archives/C029BPP02H0/p1789742116153609
https://canarytechnologies.slack.com/archives/C0A5Z7LE5AL/p1790347733658459?thread_ts=1790339063.940229&cid=C0A5Z7LE5AL

https://www.figma.com/design/SH9uOmxQwB3VuCb7dZG1IW/Check-in-Configuration?node-id=370-63830&p=f