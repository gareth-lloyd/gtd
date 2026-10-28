---
area: null
completed_at: 2026-10-27 14:20:32.772916
contexts:
- react
created: 2026-10-27 05:36:42.541425
defer_until: null
due: null
energy: medium
id: 2026-10-27T0536-review-pr-61019-for-sam-kariu-epd-core-engineers
order: null
output: "## Agent run 2026-10-27T13:32\nPR #61019 (https://github.com/canary-technologies-corp/canary/pull/61019):
  [TOOL-872] country definitions base provider + wiring. Slack ask: https://canarytechnologies.slack.com/archives/C08RJU9Q7FV/p1793036799183729\n\n**State:**
  already APPROVED by ramironieto, gpercu-canary, and andresfigueira (the A/D sign-off
  Ramiro deferred to), plus the policy auto-approve. CI clean, mergeStateStatus CLEAN.
  Your review is not blocking. Ramiro's two scope comments (mirror/TOOL-869) were
  resolved by Sam's rebase. Macroscope's blocking note (Salesforce read inside the
  savepoint) is fixed: `catalog_fields_to_add()` now runs before `transaction.atomic()`.\n\n**Verdict:**
  sound, small, and safe to merge. The registry is empty, so DEFAULT onboarding behaves
  exactly as before. Nothing blocking. The questions below are optional, for whoever
  owns TOOL-873/874.\n\nOptional comments, drafted and NOT posted:\n1. **Country fields
  are only added on the first move.** `ConfigureCheckInPlan.execute` returns `skipped`
  when the hotel is already on the catalog or `is_live`. A hotel moved before its
  country was defined, or one that went live first, never gets the legally required
  fields, and nothing records why. Worth confirming that TOOL-873 monitoring catches
  \"country hotel on the catalog without its country fields\".\n2. **Additional guests.**
  Country fields go only on the `REGISTRATION_CARD` step form. If Italy (TOOL-874)
  needs per-guest data (alloggiati), the additional-guest form will need them too.
  Is that planned in the design doc?\n3. **Reruns overwrite settings.** On a rerun
  of the card plan, `check_in_settings` and `id_document_settings` are always rewritten
  (only `id_step_with_ocr` respects a hand-set value). A CS edit to retention or purge
  settings would be reverted. The default provider already treats `rollout_check_in_v2_level`
  the same way, so this is consistent; it just should be deliberate.\n4. **Nit: the
  OCR purchase is read twice,** once per plan (two live Salesforce calls), and `catalog_fields_to_add`
  makes the call even when no field is `ocr_fillable`. You could short-circuit when
  there are no `ocr_fillable` fields. If Salesforce flips between the two plans, the
  settings and the form could disagree. The risk is low.\n5. **Nit: the error path
  is still untested.** Sam lists `ERROR_NO_REGISTRATION_FORM_FOR_COUNTRY_FIELDS` as
  \"needs an ORM mock\". Macroscope's suggestion works without one: call `add_catalog_fields`
  directly on a stub hotel with no registration step form and assert the error code.\n\nChecked
  and fine: the `User.objects.get(username=\"SupportUser\")` fallback matches existing
  onboarding code (hotel_products_plan.py:428 and others). The new `ConfigureCheckInPlan`
  collection has no `DEFAULT_PROVIDER`, so it resolves to None and is a no-op (covered
  by a test). `CatalogFieldWriteService.create` takes the hotel lock and nests in
  the outer atomic, so a failure rolls back the whole move.\n\nSuggested action: approve
  or leave a \U0001F44D in Slack. If you want to post anything, items 1 and 2 are
  the useful ones. Nothing was posted.\n"
project: null
source_id: https://canarytechnologies.slack.com/archives/C08RJU9Q7FV/p1793036799183729
tags:
- morning-gtd
- slack
time_minutes: 20
title: 'Review PR #61019 for Sam Kariu (#epd-core-engineers)'
updated: 2026-10-27 14:20:32.772897
waiting_on: null
waiting_since: null
working_on: false
---

Sam asked the core-engineers group for a review; read but not actioned.
https://github.com/canary-technologies-corp/canary/pull/61019
https://canarytechnologies.slack.com/archives/C08RJU9Q7FV/p1793036799183729