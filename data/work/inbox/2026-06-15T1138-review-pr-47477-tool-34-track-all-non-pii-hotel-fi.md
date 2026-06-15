---
area: null
contexts:
- react
created: 2026-06-15 11:38:19.086324
defer_until: null
due: null
energy: medium
id: 2026-06-15T1138-review-pr-47477-tool-34-track-all-non-pii-hotel-fi
order: null
output: |
  ## Agent run 2026-06-15T12:55 — Review of PR #47477

  PR: https://github.com/canary-technologies-corp/canary/pull/47477
  [TOOL-34] Track all non-PII Hotel fields via CONFIG_FIELDS — ramironieto, OPEN.
  +386/-3 across 4 files (change_tracker.py, hotel.py, 2 test files). Base: master.

  ### Verdict
  Solid, well-tested change. The `_json_safe` normalizer is the right fix (it
  addresses the root cause rather than the symptom of dispatch being silently
  swallowed). The exhaustive per-field parametrized test is excellent and is the
  real safety net. No blocking correctness bugs found. A few things worth raising
  with the author before approving — most important is a performance concern and an
  undocumented behavior change.

  ### Things to raise (in rough priority order)

  1. PERF — snapshot query now loads ~all columns + extra FK queries on every save.
     `ChangeTracker._pre_save` does `sender.objects.only(*all_tracked_fields).get(pk=...)`
     and then `getattr(old, f)` for each tracked field. With CONFIG_FIELDS expanded to
     ~163 fields (PRODUCT+CONFIG ≈ all of Hotel), `.only(...)` effectively selects the
     whole row, and 6 of the tracked fields are relations (company, brand,
     feedback_configuration, image_group, request_to_contact_template, sso_organization).
     The dict comprehension `{f: getattr(old, f) ...}` dereferences each FK, so the
     snapshot fires ~6 extra SELECTs on EVERY Hotel.save() that touches a tracked field
     — even when none of those FKs changed. A full `Hotel.save()` (update_fields=None)
     now always triggers this. Hotel saves are hot. Suggest snapshotting relations via
     the `_id` attribute (e.g. read `getattr(old, f + "_id")` for relation fields) to
     avoid the N+1, and confirm the extra full-row SELECT-per-save is acceptable at
     Hotel save volume. This mechanism pre-existed but PRODUCT_FIELDS had ~no FKs; the
     expansion is what amplifies it.

  2. SCOPE / UNDOCUMENTED — the diff also adds `update_fields` filtering in `_post_save`
     (skip a tracked field when `update_fields is not None and field not in update_fields`).
     This is a real, sensible behavior change (its comment about db_default sentinels on
     freshly-created instances is a good catch) but it is NOT mentioned in the PR
     description, which only covers CONFIG_FIELDS + `_json_safe`. Ask the author to call
     it out in the description so reviewers/future archaeologists see it. Logic itself
     looks correct: None → check all (full save), list → only those written.

  3. PII consistency question — `notification_emails` is excluded as PII (good, and the
     test now uses it as the "untracked" case), but `email_address`, `custom_email`,
     `phone`, `sms_phone`, `whatsapp_phone_number` ARE tracked. These are property-level
     contact channels (defensible as config, not guest PII), but worth a one-line
     confirmation from the author on why the staff-email list is PII while the property
     contact email/phone are not — just so the allowlist boundary is intentional and
     documented for the next person adding a field.

  4. Field count nit — description says "all 165 non-PII Hotel fields"; the list actually
     has 163 newly-added entries + 1 pre-existing (`pms_payment_slot_identifier_auths`)
     = 164. Minor, but reconcile the number in the description.

  ### Checks performed (all passed)
  - No EncryptedCharField / token / secret / credential / api_key field on Hotel appears
    in CONFIG_FIELDS (grep of hotel.py field defs — only hit was an unrelated AVS_STRATEGY
    constant).
  - No duplicates within CONFIG_FIELDS.
  - No overlap between CONFIG_FIELDS and PRODUCT_FIELDS (so no field emits two events).
  - `_json_safe` type handling is correct: None/str/int/float/bool pass through (bool is
    int subclass — fine), Model→pk, FieldFile→name or None, date/datetime/time→isoformat
    (datetime is a date subclass, ordering correct), Decimal→str, list/tuple/set→recursive,
    else→str. FK equality (`old_val == new_val`) still works because it compares pk.
  - Test coverage is strong: generic `_json_safe` per-type test + a Decimal end-to-end
    payload-serializes test in test_change_tracker.py, AND an exhaustive parametrized test
    over every CONFIG_FIELDS entry that asserts exactly one event + json.dumps(asdict(payload))
    survives the stdlib encoder. This is the right guard against a future field type that
    `_json_safe` can't serialize.

  ### Not done
  - Did not run the test suite locally (review only). The parametrized test is the key one
    to confirm green in CI.
  - Did not post anything to GitHub (no external writes per session rules). The findings
    above are drafted for you to relay/post as you see fit.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/47477
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #47477: [TOOL-34] Track all non-PII Hotel fields via CONFIG_FIELDS'
updated: 2026-06-15 12:56:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

Personal review request from ramironieto. Expands CONFIG_FIELDS to an allowlist of all 165 non-PII Hotel fields for config-changed events; excludes secrets/PII. Open, review required.
https://github.com/canary-technologies-corp/canary/pull/47477