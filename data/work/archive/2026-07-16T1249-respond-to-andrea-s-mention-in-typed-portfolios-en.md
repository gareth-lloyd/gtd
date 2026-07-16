---
area: null
contexts:
- react
created: 2026-07-16 12:49:55.810858
defer_until: null
due: null
energy: low
id: 2026-07-16T1249-respond-to-andrea-s-mention-in-typed-portfolios-en
order: null
output: |
  ## Agent run 2026-07-16T15:05:00+01:00

  **What the mention is:** Andrea added you to the *Reviewers* property of "Typed Portfolios — Eng Design"
  (https://app.notion.com/p/39e814686151813484e1e10c84e4324f) — that's what generated the @mention email.
  There is no comment to reply to: the page has zero discussions (checked incl. resolved) and the inline
  Review table is empty (no reviewer has responded yet). Doc status is "REVIEW ME!". You are the first of
  5 reviewers. This is a review request, not a question.

  **What I did:** Read the full doc and verified its key claims against the codebase (backend/canary).
  Nearly everything checks out — model conventions, MSA_PORTFOLIO_IDENTIFIERS really holding parent-brand
  identifiers (so the ENT-6882 correction is right), the ENT-6887 customer-supplied-identifier gap is real
  (CreateChildPortfolioRequestSchema.identifier, portfolios/views/portfolio.py:80), the Blake/canary_staff
  permission note is accurate.

  **Findings for the review (1 real gap, 2 questions, 1 nit):**

  1. GAP — `PortfolioService.delete_portfolio` will start raising `ProtectedError`. Portfolio is
     HARD-deleted (not SoftDeleteModel), and delete_portfolio (portfolios/services/portfolio.py:148-184)
     works by manually deleting every PROTECT-related child row before portfolio.delete() at :172.
     PortfolioTypeAssignment on PROTECT (right choice, matches PortfolioHotel) must be added to that
     cleanup block — otherwise every leaf-portfolio delete breaks the moment the backfill guarantees
     ">=1 type per portfolio". Not in the doc's Error Cases section; should be added there and to
     ENT-6873/ENT-6878 scope.
  2. QUESTION — APD derivation may over-match: explo_customer_token is set inside create_portfolio via
     ExploService.get_or_create_explo_customer_for_portfolio (portfolios/services/portfolio.py:245). If
     that runs on all creation paths, token presence would type nearly every portfolio
     ABOVE_PROPERTY_DASHBOARD in the ENT-6874 backfill. Check token distribution in the dry run.
  3. QUESTION — hierarchy-cap location: today's one-level cap is enforced in add_hotels
     (portfolio.py:411), not at creation/parenting time. ENT-6879's type-aware nesting rules should state
     explicitly that they also run where parent is set, else illegal nesting only surfaces on add_hotels.
  4. NIT — doc says "~40 call sites" of hotel_belongs_to_portfolio_by_identifier; grep finds 55 non-test
     references. ENT-6881's audit number should be the source of truth.

  **Drafted response for Andrea (NOT posted — needs your approval).** Two-part response:
  (a) a page comment with the findings, (b) a row in the inline Review table
  (Person: you, Status: your call — I'd suggest "Approved" since #1 is a scope addition, not a design
  change; "Needs Revision" if you want the doc amended first).

  Draft comment text:

  > Reviewed — design looks solid and matches the codebase. One real gap plus smaller notes:
  >
  > 1. **`PortfolioService.delete_portfolio` will start raising `ProtectedError`.** Portfolio is
  > hard-deleted, and `delete_portfolio` (`portfolios/services/portfolio.py:148`) manually deletes every
  > PROTECT-related child row before `portfolio.delete()`. `PortfolioTypeAssignment` on PROTECT (right
  > choice — matches `PortfolioHotel`) needs adding to that cleanup block, otherwise leaf-portfolio
  > deletion breaks once the backfill guarantees every portfolio has ≥1 type. Suggest adding to the Error
  > Cases section and ENT-6873/ENT-6878 scope.
  > 2. **APD derivation may over-match.** `explo_customer_token` is set inside `create_portfolio` via
  > `ExploService.get_or_create_explo_customer_for_portfolio` — if that runs for all creation paths,
  > token presence types nearly everything `ABOVE_PROPERTY_DASHBOARD`. Worth checking against actual
  > token distribution in the ENT-6874 dry run.
  > 3. **Hierarchy rules at parenting time?** The current one-level cap lives in `add_hotels`, not at
  > creation. If ENT-6879's type-aware nesting rules also run where the parent is set, say so explicitly.
  > 4. Nit: I count 55 non-test references to `hotel_belongs_to_portfolio_by_identifier`, not ~40 —
  > doesn't change the plan; ENT-6881's audit is the source of truth.
  >
  > Spot-checked the rest: `MSA_PORTFOLIO_IDENTIFIERS` really does hold parent-brand identifiers (ENT-6882
  > correction is right), the ENT-6887 identifier gap is real, and the canary_staff/Blake permission note
  > is accurate.

  **Next step (yours):** say "post it" (I can add the comment + Review-table row via Notion MCP), or edit
  the draft first. Links: doc https://app.notion.com/p/39e814686151813484e1e10c84e4324f · Linear project
  https://linear.app/canary-technologies/project/portfolio-typing-60798dba32e0
project: null
source_id: https://mail.google.com/mail/u/0/#inbox/19f678b60efa141c
tags:
- morning-gtd
- gmail
time_minutes: 10
title: Review Typed Portfolios — Eng Design (Andrea added you as reviewer)
updated: 2026-07-16 14:58:16.512187
waiting_on: null
waiting_since: null
working_on: false
---

Andrea Bradshaw added you to the Reviewers property of the Typed Portfolios eng design doc (Jul 15, 11:50 PM) — the @mention email was the reviewer-request notification, not a comment. You are the first of 5 reviewers; doc status is "REVIEW ME!" and no reviewer has responded yet. Design landed; ENT-6873–6887 ticket batch created.

Remaining action: approve/edit the drafted review response (see output below) and post it — a page comment with findings plus a row in the doc's inline Review table.

Doc: https://app.notion.com/p/39e814686151813484e1e10c84e4324f
Linear project: https://linear.app/canary-technologies/project/portfolio-typing-60798dba32e0