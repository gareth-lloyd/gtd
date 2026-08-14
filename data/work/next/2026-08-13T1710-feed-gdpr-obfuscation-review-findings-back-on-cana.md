---
area: null
completed_at: null
contexts: []
created: 2026-08-13 17:10:37.786700
defer_until: null
due: null
energy: null
id: 2026-08-13T1710-feed-gdpr-obfuscation-review-findings-back-on-cana
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: null
title: 'Feed GDPR obfuscation review findings back on canary PR #52646 (EMEA-512)'
updated: 2026-08-14 06:57:28.099571
waiting_on: null
waiting_since: null
working_on: false
---

Multi-agent review of https://github.com/canary-technologies-corp/canary/pull/52646 (EMEA-512, Martijn Dekker). Stacked on `mdekker/canary-gdpr-2-models`. Engine mechanics are solid; the problems are coverage + observability. Design fails open in both directions.

## Critical (block merge)

1. **PII tag set far smaller than the PII present.** Three fail-open gaps:
   - `_PII_REG_CARD_TAGS` (check_in/models/check_in.py:145) covers 28 of 75 `CheckInSchemaFormTag` members. ~33 PII-bearing tags survive erasure verbatim, incl. SPECIAL_REQUESTS (free text, Art. 9 special-category), PLACE_OF_BIRTH, NATIONALITY, all 4 PASSPORT_*, all 5 TRAVEL_DOCUMENT_*, 3 VEHICLE_*, 8 COMPANY_*.
   - Mirror scalar columns ~80% untagged: registration_card_notes (CharField 2056, free text), visa_number, ip_address, cc_number/cc_first_six/cc_last_four.
   - `IMAGE_BLOB_DELETE` applied to ZERO real fields. Every ID scan + signature image untagged (id_front/id_back/id_face/cc_front/signature). `signature` is the clearest bug: the SIGNATURE reg-card tag IS covered and AdditionalGuest.policy_signature IS tagged, so same concept covered twice and missed on the column. identity_document_purge_service time-purges at 365/60d, which covers the sweep but NOT obfuscate_erase.
   - Fix: invert polarity - enumerate the small non-PII set, scrub everything else, + exhaustiveness test.

2. **obfuscate_erase composes search terms with OR** (check_in_obfuscation.py:96-110 uses `match |=`). Adding params WIDENS the erase. The too-broad handler literally tells the operator to add more parameters. MAX_SEARCH_CANDIDATES=10_000 is not a meaningful single-subject guard.

3. **obfuscate_erase reports a count it never obtained.** execute_plan return value discarded (obfuscate_erase.py:94), prints len(results) = pre-erasure search count. With isolate_rows=True, 400/1000 swallowed rows still print "obfuscated 1000". One-shot run, nothing retries.

4. **Admin destroys data with zero feedback.** No message_user anywhere. batch_execute_plan swallows TransitionNotAllowed with no log. Other exceptions -> 500, remaining plans silently skipped. No confirmation interstitial, sits next to "Delete selected", runs synchronously in a web request, search_request editable after execution.

## Important

5. Sweep exits 0 regardless of hotel failures. RDS failover fails all ~8k hotels -> logs total_obfuscated=0 at INFO, identical to a clean quiet run. report_heartbeat fires BEFORE any work. Precedent: chat/management/commands/cron_post_chat_analysis.py:225.
6. ObfuscationPlan.state unreliable both ways: COMPLETED does not imply erased; FAILED does not imply not-erased.
7. Dry-run takes a different transaction path AND nests the subtransactions the real path's docstring warns about (per-row atomic gated on isolate_rows alone, not dry_run). --commit is opt-in, so dry-run is the DEFAULT mode. VERIFIED.
8. Admin Execute Plan button runs inside Django's changeform atomic (options.py:1843) -> per-row commits become savepoints -> same >64 subxid pathology. VERIFIED against Django 5.2.
9. Nothing schedules the sweep. No beat/cron/task registration despite "scheduled retention sweep (Trigger 1)".
10. No index supports the sweep query - CheckIn.Meta.indexes has nothing on departure_date or obfuscated_at. Martijn already self-flagged this inline.
11. Scope never validated - command calls adapter.search() directly, bypassing InvalidScope. Typo'd --hotel-id prints a clean "obfuscated 0". Phone matched exactly, no normalisation.
12. Test gaps: NO test for the search-vector short-circuit (the diff's own change - delete it and everything still passes while obfuscated check-ins stay searchable by name/email); JSON_TAG_SCRUB never runs against a real CheckIn; no test makes any row or plan fail; no drift guard for _PII_REG_CARD_TAGS (~15 lines, no DB, catches finding 1 recurring).

## Suggestions

- TypeVar bound to models.Field on obfuscatable_field - it is a runtime identity fn, so the signature needlessly erases CharField to Field, which forced the report_for_hotel.py:72-82 widening. Answers Marta's inline comment directly.
- Collapse the three __obfuscation_* dunders into one frozen record on the ObfuscatableField Protocol; overwrite.py currently reads them via getattr(..., DEFAULT) where a typo silently changes erasure semantics.
- SweepPlanContext subclasses a type it cannot be used with (passing it to search() always raises). Sibling types over a shared base.
- Two registries keyed by the same model (_ADAPTERS, _HYDRATORS) with asymmetric failure modes. Merge.
- AdditionalGuest has no marker of its own -> any guest row added after the parent is stamped is never scrubbed. Matches Marta's documentation question.
- executor.py:23 states the wrong reason for the stamp ordering (cascade branches on the STAMP, not on already-scrubbed-ness) - reorder-and-silently-reindex trap.
- update_fields omits updated_at, so obfuscation never bumps it - incremental CDC/ETL never sees the redaction.
- Cleanup: 3 stray `# Act` comments; MAX_QUERIES_PER_ROW=5 where real cost is 3; test_canary_executor__is_idempotent_on_rerun does not test idempotency; hardcoded Entity(kind="hotels.Hotel") where HOTEL_SCOPE_KIND is imported.

## Confirmed fine

mark_safe/pygments XSS-safe (verified empirically). Executor ordering correct as written. obfuscate_related cannot miss AdditionalGuest rows. .every used consistently. Keyset paging sound, skipped rows genuinely retry. Empty-predicate guard exists + tested. _portfolio_ids_in_scope cycle-safe. No migration needed. Per-row failure logs carry SearchResult, not the model - no PII in logs.

CI: make test-backend failing on infra (corrupt venv, cygrpc invalid ELF header), not this PR. E2E failures are the non-blocking add-ons suite.

Nothing posted to GitHub yet.

---

## Added 2026-08-13 from a decision-review pass (non-overlapping only)

Second read framed as decisions-with-alternatives rather than defects. Everything above reproduced or was found richer there; below is what it did not cover.

### New — critical-ish

**The erasure record is itself an unswept PII store.** `ObfuscationEngine.plan()` persists `search_request=search_request.model_dump()` (shared/gdpr/services/obfuscation.py:74), i.e. the DSAR subject's `{first_name, last_name, email, phone}` verbatim into `ObfuscationPlan.search_request` — a JSONField on a table with no retention policy, no `obfuscated_at`, no tagged fields, and a `PROTECT` FK to `created_by` so the row cannot be cleaned up by deleting the operator. `entities` additionally holds a `repr` per row (`CheckIn {slug} (hotel {id})`) plus a live admin deep-link. `gdpr/admin.py:41` exposes `search_request` as an editable form field (finding 4 notes the tamper angle; the retention angle is separate).

Net effect: honouring an Art. 17 request mints a permanent new record of exactly the identifiers it was asked to erase. Only the DSAR path is affected — the sweep writes an all-`None` `GuestSearchParams` (obfuscate_scheduled_sweep.py:183), so `search_request` there is clean.

Honest counter-argument: you need *some* durable artifact to evidence that the request was honoured, and that is the stated purpose of the plan table. So this is a "wrong shape", not "should not exist" — the usual resolution is a salted digest of the search terms plus the existing free-text `notes`, which preserves provability without preserving the identifiers. Worth deciding explicitly rather than by default; right now nothing in the code or the doc indicates it was considered.

### New — important

**Retention anchors on `departure_date`, unvalidated.** `get_overdue_queryset` filters `departure_date__lte=cutoff` (check_in_obfuscation.py:74). `departure_date` is PMS- or guest-supplied and non-null but not sanity-checked, so any row carrying a wrong or far-future date is never swept and never reported — the same silent-fail-open shape as finding 1, on the time axis instead of the field axis. Also unclear how no-shows and cancellations that never had the date corrected behave. Alternatives: `created_at`, `processed_at`, or `GREATEST(departure_date, created_at)`. Whichever is chosen is what finding 10's missing index has to cover, so the two should be settled together.

**Dry-run leaves an audit row that lies.** Complements finding 7: `_execute_plan_atomically`'s `transaction.set_rollback(True)` rolls back not just the obfuscation but the plan's own `start()`/`complete()` writes, so a previewed plan lands back in `CREATED` with `started_at`/`finished_at` NULL. `test_erase__dry_run_writes_nothing_but_records_preview_plan` asserts `CREATED`, so this is deliberate — but combined with finding 6 it means plan state is uninformative in a third direction: it cannot distinguish "previewed" from "never run".

### Useful context (not defects)

**`shared.gdpr` has exactly one consumer.** Grepped `ObfuscationEngine` / `ScheduledObfuscationRunner` across `backend/` — no hits outside `shared/gdpr` itself and this PR. Two consequences: (a) the shared-API changes in this PR (`obfuscate`/`execute_plan` return `None`→`int`, `objects.get`→`_base_manager.get`, dropped `structlog_log_context` from the log line) break nobody, so that contract churn is free today and needn't hold up merge; (b) it is direct evidence for the sibling item's design-doc blocker 2 — "hoist the toolkit to `shared` now" is speculative generality while the abstraction has one caller. The Canary-local-first reading (§7 v1, §4 code comment) is the better-supported one until a second host app exists.

**Cross-links to the EMEA-354 doc review** (sibling inbox item, 2026-08-13T1705):
- Doc blocker 5 (`hotel.country` free-text lookup) does **not** apply to the shipped code — the sweep keys directly on `Hotel.pii_retention_days` (obfuscate_scheduled_sweep.py:155), never on country. Code took the safer path; drop that one from the code conversation, keep it for the doc.
- Doc item 6 (name-match DSAR erases every John Smith) is exactly code finding 2, now shipped. The doc review predicted it and the implementation confirms it — worth citing that lineage when raising it, it is stronger than either alone.
- Doc item 10 (does EMEA-356 replace `identity_document_purge_service` or run alongside?) now has an empirical answer: alongside, with a coverage seam — see finding 1's note that the time-purge covers the sweep but not `obfuscate_erase`.
- Doc item 4 (v1 default off vs active everywhere) is resolved in code as fail-open: `Hotel.objects.filter(pii_retention_days__isnull=False)` means zero hotels are swept until someone configures each one. Consistent with §10, contradicts §6.4. That is a deliberate rollout posture and probably right for v1, but it means "shipped" and "compliant" are not the same event and the gap needs an owner.

### Extra nits

- `cc_cardholder_name` is still fed unconditionally into `update_search_vector` (check_in_search.py:19-22, untouched by this PR), so every obfuscated row's `search_text` gains a unique `__redacted__<hex>` token. Not a privacy leak, but it pollutes the index and makes obfuscated rows mutually distinguishable — and it is a second reason the missing short-circuit test in finding 12 matters.
- obfuscate_erase.py:68-73 constructs an `ObfuscationPlanRequest` and immediately discards it, purely to trigger its `check_at_least_one` validator. It works, and `get_subject_queryset`'s empty-predicate guard backs it up, but the idiom reads as dead code — someone tidying it away silently removes a guard.