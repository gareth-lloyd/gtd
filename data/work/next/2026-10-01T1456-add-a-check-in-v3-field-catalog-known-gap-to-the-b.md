---
area: null
completed_at: null
contexts:
- craft
created: 2026-10-01 14:56:39.708152
defer_until: null
due: null
energy: low
id: 2026-10-01T1456-add-a-check-in-v3-field-catalog-known-gap-to-the-b
order: null
output: ''
project: 2026-04-16T1319-rules-based-config
source_id: null
tags: []
time_minutes: 15
title: Add a 'Check-in V3 field catalog' known gap to the Binding Rules Tree doc
updated: 2026-10-01 15:00:05.483270
waiting_on: null
waiting_since: null
working_on: false
---

From: call with Leandro Alvarez and Andrea Bradshaw, 2026-09-30 ("Step configurator and rules-based", https://notes.granola.ai/d/c12bc682-f460-41f8-83c1-65437690c98c).
Full notes and code references: data/work/archive/2026-10-01T1140-write-up-notes-from-call-with-leandro-actions-for.md
Derived from the call and a code check, not a commitment made on the call.

Doc: https://app.notion.com/p/canarytechnologies/Binding-Rules-Tree-3e58146861518147b489e3fa8e8aef09
The page has no mention of the catalog, StepForm or CatalogField (keyword search on 2026-10-01).

What to add:
- Step-level and bucket columns (`id_step`, `id_step_with_ocr`, `additional_guests_step`, `additional_guests_id`) stay the source of truth, so the planned first rules stand. Leandro confirmed the configurator writes back to `CheckInConfiguration` for these.
- Per-field ID collection settings for primary and additional guests move to catalog rows. On a catalog hotel the columns go stale, and since #57800 writes to 23 `additional_guests_*` columns are refused.
- In Appendix A "Migration", the Wyndham and IHG rows say the per-field `additional_guests_*` defines "Stay". Add the caveat that on catalog hotels drift on those keys compares a column the guest form no longer reads.