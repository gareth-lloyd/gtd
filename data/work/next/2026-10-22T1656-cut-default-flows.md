---
area: null
completed_at: null
contexts: []
created: 2026-10-22 16:56:51.991813
defer_until: null
due: null
energy: low
id: 2026-10-22T1656-cut-default-flows
order: null
output: ''
project: 2026-10-21-config-registry
source_id: null
tags: []
time_minutes: 5
title: cut default flows
updated: 2026-10-22 16:56:52.135801
waiting_on: null
waiting_since: null
working_on: false
---

# Remove flow lists

## Context

Each key's investigation traces a hand-written "flow list" (`DEFAULT_FLOWS` in `settings_field_guide/services/batch.py:83`, plus a generic suffix at `.claude/workflows/settings-field-guide-investigate.js:54`). Nothing derives or checks these lists. The chat and voice critics spent much of their output on flows the lists missed, and a list patched after each critic never catches up.

The flow lists try to answer "which paths respect this setting" for every key up front. That question is better answered later, case by case, when someone asks it ("does mobile check-in respect this flag?"), using the entry's claims and edges as the starting point. So the lists go, with no declared replacement.

The compensation is a short trace that starts from each key's own code, so there is nothing to keep up to date:

- **Reach**: callers of the deciding symbol, up to an entry point.
- **Bypass**: other callers of the gated outcome. This finds the voice `call_tree` case, which never reads the column.

**Accepted loss:** paths that are neither reachable from a reader nor callers of a gated outcome. These are mainly the parallel implementations the lists named: check-in kiosk, v3, tablet and new registration; authorization's sales booking, contracts, payment links and travel-company APIs; check-out's kiosk, auto-checkout and export. An entry no longer states that such a path ignores the value unless a trace finds it.

**Out of scope** (separate plans if wanted): declared implementations, sibling consistency, correction leaks, writer and edge-lens fixes, the README own-column rule, re-running committed entries, any workflow run.

## 1. Remove flow lists

- **`services/batch.py`:** delete `DEFAULT_FLOWS`, `BatchOptions.flows` and the `batch["flows"]` copy (lines 83, 162, 248).
- **`management/commands/settings_field_guide_batch.py`:** delete the `DEFAULT_FLOWS` import, `--flows` and `flows=` (lines 15, 41, 74). Keep `MappingProxyType`; `amendments` still uses it.
- **`settings-field-guide-investigate.js`:**
  - Delete `FLOWS`.
  - Delete the flows bullet in `searches()` (line 167).
  - Delete the flow text in `completePrompt` (line 222) and `criticPrompt` (line 363).
  - In `searches()`, change "(two onboarding paths, two flows)" to "(two onboarding paths, two entry points)".

## 2. Compensating trace

- **One `TRACES` constant in the workflow, inserted where the flow text was** in `searches()`, `completePrompt` and `criticPrompt`:
  - Reach: for each symbol that decides from the value, follow its callers up to an entry point (view, Celery task, management command, Kafka consumer, LiveKit agent or task, webhook). Name the branch that routes each entry point there. Stop after four hops or at the first entry point on each chain.
  - Bypass: for each gated outcome, grep its other callers and open at most ten. A caller that reaches the outcome without passing the decision is a scope-boundary claim citing that caller. When the key carries a `requires` edge, narrow its `because` or `when` to the paths that pass the gate rather than dropping the edge.
  - Replay and revert: when the value is captured into a task or event payload, check the retry and DLQ paths that reuse it. When the value is pushed to another system, check the push's revert path (deny, expire, cancel). These two items move here from the deleted generic suffix.
  - Record where a trace stopped in `checked` (complete) or `unresolved` (investigate).
- **Not applied to trivial keys:** `TRACES` sits inside `searches()`, which the trivial path already skips.
- **Heavy readers:** the `HEAVY_READERS` path keeps its cap of 40 opened symbols. Reach and bypass apply only to symbols that decide.
- **Admin raw writes:** already covered by the writer search in `investigatePrompt` step 3. No new text.
- **Guest and kiosk frontends:** already covered by the frontend search in `searches()`. No new text.
- **Staff CSV exports:** dropped; listed as lost.

## 3. Wording that named flows

- **`VALUE_BAR` item 2:** "a flow or a path that does not read the value" becomes "an entry point or path that does not read the value, or reaches the gated outcome without it".
- **`VALUE_BAR` last sentence:** "A 'flow X never reads it' claim cites the flow's entry point" becomes "A scope-boundary claim cites the entry point or the bypassing caller".
- **`README.md`:**
  - Line 63: the same wording for bar item 2.
  - Line 79: change "a scope boundary (v3, kiosk, tablet, new registration)" to "a scope boundary".
- **`PIPELINE.md`:**
  - Rewrite the flows clause in the prompts summary (line 159).
  - Add a Record entry, "Flow lists removed", giving the reason (answer path questions case by case, not up front), the compensating trace and the accepted loss above.
  - Under Known gaps, add: the critic uses the same traces, so it is not an independent check of path coverage.
  - Move the critic gaps about missing flows out of "Open critic gaps", noting that they are superseded rather than fixed.

## Commits (no push)

1. Remove flow lists and add the compensating trace (sections 1 to 3, except `PIPELINE.md`).
2. Update `PIPELINE.md`.

Follow the backend Python rules already loaded (comments, style, typing, control flow). No tests change unless one covers `--flows` or `DEFAULT_FLOWS`; grep `tests/` first.

## Verification

- `grep -rn "FLOWS\|args.flows\|--flows\|flows=" .claude/workflows backend/canary/settings_field_guide` returns nothing outside entries and the `PIPELINE.md` record.
- `node --check` on both workflow files.
- From `backend/canary`:
  - `direnv exec . pytest settings_field_guide --nomigrations -q` passes.
  - `python manage.py settings_field_guide_batch check_in_configuration:0:3 --preset light` writes a launcher with no `flows`. Read it, then delete it.
- `ruff format`, `ruff check` and `pyrefly check` on the changed Python files.
- Render one investigate prompt and one critic prompt with node and stub args. Confirm the trace text is present and no flow text remains.
- Not verified: whether the trace finds what the lists found, or what it costs per key. The next bulk run is the first measurement, against the chat and voice rows in `PIPELINE.md`.