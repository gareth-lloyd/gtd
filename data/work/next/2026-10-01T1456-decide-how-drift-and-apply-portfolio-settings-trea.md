---
area: null
completed_at: null
contexts:
- deep
created: 2026-10-01 14:56:39.782305
defer_until: null
due: null
energy: medium
id: 2026-10-01T1456-decide-how-drift-and-apply-portfolio-settings-trea
order: 6
output: ''
project: 2026-04-16T1319-rules-based-config
source_id: null
tags: []
time_minutes: 30
title: Decide how drift and apply_portfolio_settings treat catalog-owned keys on catalog
  hotels
updated: 2026-10-05 14:08:15.478548
waiting_on: null
waiting_since: null
working_on: false
---

From: call with Leandro Alvarez and Andrea Bradshaw, 2026-09-30 ("Step configurator and rules-based", https://notes.granola.ai/d/c12bc682-f460-41f8-83c1-65437690c98c).
Full notes and code references: data/work/archive/2026-10-01T1140-write-up-notes-from-call-with-leandro-actions-for.md
Derived from the call and a code check, not a commitment made on the call.

Two symptoms of one decision:
- Drift reports against 23 per-field `additional_guests_*` columns that the guest form no longer reads once `uses_field_catalog` is true.
- `apply_portfolio_settings` does a full `save()` with no catalog check. On a catalog hotel where a guarded column differs from the tree it raises `AdditionalGuestFormManagedByCatalog`, uncaught, and the command stops partway (backend/canary/rules_based_configuration/management/commands/apply_portfolio_settings.py:106-150; guard at backend/canary/guest_experience/signals.py:77-86).
- IHG is the exposed tree: each of its nine country modules defines 21 of the 23 guarded keys. Wyndham defines one.

Options:
1. Skip the guarded keys when `uses_field_catalog` is true, in both drift and the apply command, and log them.
2. Pin `uses_field_catalog` to False in the IHG and Wyndham trees as a stopgap. The key already exists in the engine (conformity.pyi:218). This holds enterprise hotels off the catalog, so it needs Leandro's agreement.

Not for binding-tree releases 1 to 3, but the apply command fix is small and independent.