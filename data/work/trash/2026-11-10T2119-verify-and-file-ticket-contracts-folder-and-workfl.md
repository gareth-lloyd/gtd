---
area: null
completed_at: null
contexts: []
created: 2026-11-10 21:19:47.811416
defer_until: null
due: null
energy: null
id: 2026-11-10T2119-verify-and-file-ticket-contracts-folder-and-workfl
order: null
output: |-
  ## Agent run 2026-11-12

  **Verdict: the bug is real in code but has never fired in production. Nothing filed. I recommend not filing it as a standalone correctness ticket.**

  ### Production count (read-only, `canary prod-db query`, reader replica, 2026-11-12)

  | Region | Signers | Soft-deleted signers | Contracts with a soft-deleted signer |
  | --- | --- | --- | --- |
  | US | 1,120,129 | 0 | 0 |
  | EU | 8,849 | 0 | 0 |
  | AP | 24 | 0 | 0 |

  No row in `contracts_contractsigner` has `deleted_at` set, in any region. No contract is stuck in pending for this reason, so there is nothing to tell CS.

  I also found no application code that soft-deletes a `ContractSigner` (searched `backend/` for `.delete()` and `deleted_at` writes on signers; only read-side filters exist). The model is a `SoftDeleteModel`, so the path is possible (admin, shell, a future "remove signer" feature) but nothing uses it today.

  ### Code verification

  - Repro test `backend/canary/contracts/tests/views/test_contracts_list_soft_deleted_signer.py` fails with the master line restored: `assert [] == ['<contract url>']`. Confirmed today.
  - With the fix (`Count("signers", filter=Q(signers__deleted_at=None))` at `contracts/views/api_views.py:691`), `contracts/tests/views` passes: 122 passed.
  - Caveat on that run: I had to pass `-W "ignore::jwt.warnings.InsecureKeyLengthWarning"`. Locally the new test reaches `ContractSignerJWT.dump_to_jwt`, which signs with `settings.SECRET_KEY`, and the local key is 18 bytes, so PyJWT 2.13.0 warns and `filterwarnings = error` fails the test. I did not check whether CI's `SECRET_KEY` is long enough. Check that before the test is pushed.
  - I temporarily reverted the one line to run the failing case, then restored it. The working tree is back to the fixed state (`git diff` shows the fix line).

  ### One thing the draft misses

  After the fix, a contract whose signers are all soft-deleted has `signers_count == signed_count == 0`, so it matches the `completed` folder and the `COMPLETED` workflow filter (and still matches `created` if no notification was sent). On master it shows as unsigned instead. Zero rows today, but a `annotation_signers_count__gt=0` guard, or a decision that this is acceptable, belongs in the fix.

  ### Recommendation

  - Drop "ship alone" and "count before shipping so CS can be told": both assumed live impact, and there is none.
  - Either fold the one-line fix and its test into the sibling perf change (`03_SDM_contracts_perf.md`, "GET /api/contracts runs 19 queries per contract"), or file it in SDM as a low-priority latent inconsistency. I'd fold it in.
  - If filed, the draft needs these edits: title to "…would count soft-deleted signers (latent, no production rows)"; replace the Impact section with the table above; add the all-signers-deleted edge case.

  ### Not done

  - No Linear ticket created (needs your explicit go-ahead, and the draft should change first).
  - Nothing committed or pushed. Fix and test remain uncommitted on master in the main checkout.
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: null
title: 'Verify and file ticket: Contracts folder and workflow filters count soft-deleted
  signers (stuck in pending)'
updated: 2026-11-12 12:31:47.404647
waiting_on: null
waiting_since: null
working_on: false
---

**Team:** SDM

**Context:** Correctness bug, not perf. One-line fix at contracts/views/api_views.py:691 with a test that fails on master. Ship alone. Count affected live contracts before shipping so CS can be told.

Source: dashboard latency audit, agent run 2026-11-09 (GTD item 2026-11-04T1957-dashboard-latency-audit...). Draft, fix diff, repro test and SQL dumps: backend/canary/tmp/dashboard_latency_repros/ (gitignored). Fixes and new tests are UNCOMMITTED on master in the main canary checkout. Audit page: https://claude.ai/artifact/QzNanTU2XKUkdEscaJYJUD. Excluded as already covered: chat/threads (PR #63670, SRE-1535), chat/messages (SRE-1745), check-in search (AD-10218 1.1).

---

## Ticket draft (04_SDM_contracts_soft_deleted_signer.md)

Team: SDM (SDM)
Title: Contracts folder and workflow filters count soft-deleted signers, so a contract with a deleted signer never reaches completed or countersigned
Labels: backend, bug
Related: the sibling perf ticket "GET /api/contracts runs 19 queries per contract"
---
## Problem

`contracts/views/api_views.py:691` annotates `annotation_signers_count=Count("signers")` without `filter=Q(signers__deleted_at=None)`. The sibling annotations at `:685-699` (signed count, countersigned count) do filter deleted signers. A contract that ever had a signer soft-deleted therefore never satisfies `signers_count == signers_signed_count`.

Misclassified by that comparison: the `completed` (`:538`), `countersigned` (`:550`) and `pending` (`:585-591`) folders, and the `SIGNATURE_DUE` (`:621`), `PAYMENT_DUE` (`:631`) and `COMPLETED` (`:641`) workflow filters. The contract stays in pending forever in the dashboard list.

## Reproduction

Test: `backend/canary/contracts/tests/views/test_contracts_list_soft_deleted_signer.py`. A contract with two client signers, one soft-deleted and the other signed, requested with the completed folder filter. On master the response is `[]`; expected `[<contract url>]`.

## Fix (one line, diff attached)

```python
annotation_signers_count=Count("signers", filter=Q(signers__deleted_at=None))
```

The test passes with the change. Existing contracts API view tests pass.

## Impact

Any hotel that removed a signer from a contract sees it stuck in the wrong folder and workflow state. Count how many live contracts have a soft-deleted signer before shipping, so CS can be told what moves.

+++ Agent notes

- Found while reading the list view for the dashboard latency audit (https://claude.ai/artifact/QzNanTU2XKUkdEscaJYJUD).
- Line numbers are from master on 2026-11-09.

+++