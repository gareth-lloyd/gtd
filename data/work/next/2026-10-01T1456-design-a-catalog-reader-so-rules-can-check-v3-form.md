---
area: null
completed_at: null
contexts:
- deep
created: 2026-10-01 14:56:39.816784
defer_until: null
due: null
energy: high
id: 2026-10-01T1456-design-a-catalog-reader-so-rules-can-check-v3-form
order: 7
output: ''
project: 2026-04-16T1319-rules-based-config
source_id: null
tags: []
time_minutes: 60
title: Design a catalog reader so rules can check V3 form fields
updated: 2026-10-05 14:08:13.016260
waiting_on: null
waiting_since: null
working_on: false
---

From: call with Leandro Alvarez and Andrea Bradshaw, 2026-09-30 ("Step configurator and rules-based", https://notes.granola.ai/d/c12bc682-f460-41f8-83c1-65437690c98c).
Full notes and code references: data/work/archive/2026-10-01T1140-write-up-notes-from-call-with-leandro-actions-for.md
Derived from the call and a code check, not a commitment made on the call.

Later work, not for binding-tree releases 1 to 3.

The engine keys are dotted paths to one scalar column. A legal field requirement under the catalog is "this form contains field X and it is required", which is a property of a set of rows.

Idea from the call (mine, not agreed): Leandro said the SchemaForm data model is unchanged and a step form still composes into the same JSON blob. So test a predicate against the composed JSON instead of diffing relations, following the reader pattern the doc already uses for retention.

Depends on standard fields keeping a stable tag across hotels, which is an open question for Leandro.
Doc: https://app.notion.com/p/canarytechnologies/Binding-Rules-Tree-3e58146861518147b489e3fa8e8aef09