---
area: null
completed_at: null
contexts: []
created: 2026-10-21 14:37:48.164857
defer_until: null
due: null
energy: low
id: 2026-10-21T1437-check-review-findings
order: null
output: ''
project: 2026-10-21-config-registry
source_id: null
tags: []
time_minutes: 5
title: check review findings
updated: 2026-10-21 14:37:48.315515
waiting_on: null
waiting_since: null
working_on: false
---

These look like they would lose data quietly or break a run:

  1. Reverse edges from bulk runs are dropped silently. CounterpartService.plan (counterparts.py:31) reads
     reverse_edges only when the result is a dict. The bulk workflow returns a list, so the command writes added=0
     and exits cleanly.
  2. A successful apply exits with an error. settings_field_guide_apply_counterparts.py:63 runs the check with
     --check after writing entries. New edges change depends_on in the indexes, so the check reports them out of
     date. Entries end up written, indexes not regenerated, and the command fails.
  3. Applied counterparts can fail the new check. An inferred edge with no evidence is written as evidence: [],
     which SR067 rejects (counterparts.py:621). A missing because raises a KeyError partway through planning.
  4. --amend sends findings to the wrong model. amendments_from_output (batch.py:433) gives every critic finding in
     a multi-model output to the one dir you pass.
  5. A mistyped --amend dir is discarded without an error (settings_field_guide_batch.py:134).
  6. Real findings are filtered out as empty. The "nothing to report" regex has no word boundary (batch.py:207). A
     finding starting "None of the mechanics…" is dropped, and the same regex exists in
     settings-field-guide-bulk.js.
  7. One malformed critic item crashes the run. _amendments_from_critic (batch.py:452) reads fields by subscript, so
     a missing field raises a KeyError and aborts the command.

  Smaller ones:
  - Duplicated work: each entry YAML is parsed twice and each seed read twice (batch.py:379).
  - Duplicated logic: HEAVY_READERS is defined but never used in Python, and the filter and amendment logic is
    copied between Python and JS (batch.py:204).
  - No slice validation: BatchSpec.parse accepts a reversed or out-of-range slice and launches an empty batch
    (batch.py:308).