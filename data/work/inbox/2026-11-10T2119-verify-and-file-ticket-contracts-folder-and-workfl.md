---
area: null
completed_at: null
contexts: []
created: &id001 2026-11-10 21:19:47.811416
defer_until: null
due: null
energy: null
id: 2026-11-10T2119-verify-and-file-ticket-contracts-folder-and-workfl
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: null
title: 'Verify and file ticket: Contracts folder and workflow filters count soft-deleted
  signers (stuck in pending)'
updated: *id001
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