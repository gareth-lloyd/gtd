---
area: null
completed_at: null
contexts: []
created: 2026-11-20 00:23:03.344784
defer_until: null
due: null
energy: low
id: 2026-11-20T0023-copy-quote-to-clipboard-marks-as-sent-and-prevents
order: null
output: |
  ## Agent run 2026-11-20T00:27

  **Cause.** In the quote rail, Copy quote to clipboard was gated by Send's
  draft-only rule (`sendReason`, from the Phase 4 quotation actions), in
  `frontend/src/features/quotations/QuotationDetailLayout.tsx`. The first
  copy calls `:mark-manually-sent`, which moves the quote to SENT, and that
  disabled Copy ("Only draft quotes can be sent."). The backend was never the
  problem: `record_quote_sent` is idempotent on SENT (GAP-081) and refuses
  only accepted and cancelled quotes.

  **Fix (committed, not merged).** Branch `fix/quote-copy-again`, worktree
  `.claude/worktrees/quote-copy-again`, commit 47e3f5c8. Copy now has its own
  gate: enabled on draft and sent, disabled on accepted and cancelled with
  "Already accepted or cancelled." I wrote two tests first and saw them fail
  (sent → enabled; accepted → disabled with that reason). All quotations tests
  pass (986/986), and eslint, prettier, tsc and the pre-commit hooks pass. The
  push hook (full test suite) has not run yet. Still to do: merge or ship to
  main, and a quick browser check.

  **Not changed: open questions for you.** You said "sent" is mostly not a
  useful status now that copy-and-paste is the main channel:
  - The rail's "Mark sent again" (Path A Send) button has the same gate, so it
    is never enabled on a SENT quote. It only emails, and copy-and-paste is the
    channel now, so I left it alone.
  - Each copy still marks the quote SENT, and each re-copy queues the Zoho
    push again (GAP-081 behaviour). That is probably right, since the re-copied
    quote may have changed. But if SENT now only means "copied at least once",
    is it still worth having, or should it be renamed or folded into draft?
    That is a product decision and needs a ticket or decision first.
  - Other things gated on draft-only still assume SENT means the email went
    out. Worth checking: what can still be edited on a SENT quote (unbranded is
    allowed).
  ## Agent run 2026-11-20 (follow-up)

  Explored the whole quote send flow (backend, frontend, design docs, legacy)
  and wrote it up as GAP-260 (docs only, uncommitted, in the
  `.claude/worktrees/quote-copy-again` worktree):
  `django_res_design/todo/gap-260-quote-shared-semantics.md` plus an INDEX row.
  The ticket keeps the flow but shows SENT as "Shared" (wire values unchanged),
  adds last_shared_at/by/path and an Activity entry per copy or email, and
  enables "Email again" (fixes BUG-071 S-64 for quotations). Part 0 is the
  Copy fix already on the branch (47e3f5c8).
  ## Agent run 2026-11-20 (ship)

  GAP-260 shipped to local main (not pushed). Commits 47e3f5c8 (Copy fix),
  c4195770 (ticket), c1e0246e (Unit 1: every copy or email records who and
  when plus an Activity entry; "Sent" now reads "Shared"; Email again really
  sends; 409 for guests with no email; repeat within 10s by the same person
  on the same channel ignored), 6cde4e76 (D-48, BUG-071 S-64 and
  REFACTOR-022 updated, ticket in done/), merge 0ed0c482. Full gate green:
  backend 11054 passed, frontend 5882/5884. The 2 failures were a
  RouteErrorBoundary timing flake that GAP-260 doesn't touch; that file
  passes on its own. Migrations 0059/0060 still need applying to the dev DB.
  Not yet looked at in the browser.
project: 2026-05-25-villa-collective
source_id: null
tags: []
time_minutes: 5
title: Copy quote to clipboard marks as sent and prevents copy again
updated: 2026-11-20 03:10:00
waiting_on: null
waiting_since: null
working_on: false
---