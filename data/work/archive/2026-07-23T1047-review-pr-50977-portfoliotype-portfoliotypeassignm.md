---
area: null
contexts:
- react
created: 2026-07-23 10:47:01.714655
defer_until: null
due: null
energy: medium
id: 2026-07-23T1047-review-pr-50977-portfoliotype-portfoliotypeassignm
order: null
output: |
  ## Agent run 2026-07-23T11:20:00

  Reviewed PR #50977 (https://github.com/canary-technologies-corp/canary/pull/50977, ENT-6873
  https://linear.app/canary-technologies/issue/ENT-6873) via three parallel review agents
  (general code, type design, test coverage), cross-checked against the Typed Portfolios design
  doc (https://app.notion.com/p/canarytechnologies/Typed-Portfolios-Design-Doc-37481468615181b6b94bd569ba782491).
  NOTHING was posted to GitHub — findings below; a draft review comment is at the bottom
  awaiting your approval to post.

  **Verdict: approve after one fix (or an explicit "intended") — the PR is otherwise clean.**

  ### The one substantive finding
  `EventMeta.ancestor_field = None` in portfolio_type_assignment.py should almost certainly be
  `ancestor_field = "portfolio"`. Portfolio is itself an EventableModelMixin, so the mixin
  supports rolling assignment events up under the portfolio's event lineage. As written, every
  audit event for a type assignment is rootless — it won't associate with the portfolio it
  changed, which defeats the ticket's stated reason for adding the mixin ("type changes drive
  business rules, so they get an audit trail"). The DevicePlacement precedent (also
  ancestor_field=None) doesn't apply: its FK target HotelDevice is NOT eventable, and it
  overrides get_event_ancestors() to hop to the hotel; this model does neither.

  ### One question worth asking
  on_delete=PROTECT vs the design doc's §1 sketch, which used CASCADE. PROTECT matches the
  PortfolioHotel precedent, but once ENT-6874 backfills a type onto every portfolio, no
  portfolio will be deletable without manually clearing its assignments first. Probably fine
  (deletion friction on portfolios may even be desirable), but worth confirming it's a
  deliberate deviation from the doc.

  ### Non-blocking suggestions
  - Consider an explicit `id = models.BigAutoField(primary_key=True)` — VERIFIED: global
    DEFAULT_AUTO_FIELD is AutoField (canary/settings/base.py:396) and HotelsAppConfig doesn't
    override, so hotels tables default to int PKs; but 58/127 apps default to BigAutoField and
    legacy AutoField apps have an established per-model opt-in pattern (e.g.
    chat/models/ai_message_tool_call.py:22, task_scheduler/models/scheduled_task.py:30).
    Counterweight: this table is portfolios × types (thousands of rows max), so int overflow
    is unreachable — pure nit.
  - stub_portfolio heads-up: there are TWO stub_portfolio helpers, and the existing
    hotels/tests/models/test_portfolio.py imports the OTHER one (portfolios/testing.py), which
    was NOT extended with types=. Follow-up test authors may reach for the wrong helper.
    Also the extended helper's docstring doesn't mention the new types param, and the types=
    path has zero callers on this branch (dead until the follow-up PR) — a one-line smoke test
    would make it self-verifying.
  - Optional: CheckConstraint(type__in=PortfolioType.values) — choices= only bites under
    full_clean(), which objects.create() (incl. the stub itself) never calls; the DB accepts
    any <=64-char string.
  - The structural/functional split exists only as comments; a frozenset constant would make it
    branchable — though the design doc deliberately defers the rules registry, so optional.

  ### Verified clean (no action)
  - Migration 0756 head is free (master is at 0755); migration matches model; new-table
    constraint needs no concurrent build.
  - migration_files_only linter: compliant — testing.py adds 5 lines, under the 20-line exemption.
  - No admin registration is correct: explicitly deferred to ENT-6886 per ticket/design doc.
  - Zero committed tests matches direct precedent (#50784 DevicePlacement/0755 shipped
    test-free); test-coverage agent rates this non-blocking; real coverage obligation lands on
    the follow-up feature PR.
  - Design-doc cross-check: structural-type exclusivity, has_type(), backfill, and invariant
    enforcement are all deliberately deferred (ENT-6874/6875/6877/6878) — agents' questions on
    those are answered by the doc, not defects here.
  - Field annotations ([PortfolioType, PortfolioType]) match the repo rules-doc example;
    codebase is genuinely mixed (370 [X,str] vs 165 enum-getter) so no change requested.
  - Failing CI check "Non-blocking / Playwright E2E Tests (Shard 4/4)" is non-blocking and
    unrelated to a schema-only change.

  ### Draft GitHub review comment (NOT posted — approve to send)
  ---
  Looks good overall — clean mirror of PortfolioHotel and the migration is textbook. One thing
  I'd like resolved before merge, one question, and a couple of optional nits:

  1. **EventMeta.ancestor_field** — should this be `"portfolio"` rather than `None`? Portfolio
  is itself eventable, so the framework will roll assignment events up under the portfolio's
  lineage for free. With `None`, type-change audit events are rootless and won't associate with
  the portfolio they modified — which was the stated reason for adding EventableModelMixin.
  (DevicePlacement uses `None` only because HotelDevice isn't eventable, and it overrides
  `get_event_ancestors()` to compensate.)

  2. **PROTECT vs the design doc's CASCADE sketch** — deliberate? Fine either way (it matches
  PortfolioHotel), but after the ENT-6874 backfill every portfolio will have assignments, so
  portfolio deletion will always require clearing type rows first.

  Nits (non-blocking): (a) new tables in legacy AutoField apps usually opt into
  `id = models.BigAutoField(primary_key=True)` (see chat/task_scheduler/internal_support
  models) — admittedly academic for a table this small;
  (b) `hotels/tests/models/test_portfolio.py` imports the *portfolios* `stub_portfolio`, which
  didn't get `types=` — worth extending/consolidating in the follow-up so test authors don't
  fork; (c) the `types` param isn't in the stub docstring; (d) optional
  `CheckConstraint(type__in=PortfolioType.values)` since `choices=` doesn't bind at the DB.
  ---

  Next step is yours: say the word and I'll post the draft (as-is or edited) to the PR.

  ## Agent run 2026-07-23T11:35:00 — ancestor_field finding verified against framework code

  Traced the full chain at Gareth's request; the finding is CONFIRMED:
  - Dispatch: dispatch_event() attaches model_object.get_event_ancestors() (event/services/event.py:594);
    with ancestor_field=None the chain is empty (eventable_model_mixin.py:77-84).
  - Storage: each ancestor becomes an EventRelatedObject(relation=ANCESTOR,
    object_uuid=portfolio.uuid) row (event/services/event.py:330-338, 362-378).
  - Query: EventService.find_events(object_uuid=...) and fetch_events() filter
    EventRelatedObject by object_uuid with NO relation filter (event.py:644, 700-713), so
    ANCESTOR rows surface in the portfolio's event feed exactly like TARGET rows.
  With ancestor_field="portfolio", type-assignment events appear in the portfolio's event feed.
  With None, a type-REMOVAL event's only lookup key is the deleted assignment row's uuid —
  gone from the DB, so the audit event is effectively undiscoverable.
  Caveats: Event.portfolio_id (set only if dispatch passes portfolio=) serves direct
  portfolio_id queries but not the standard object-feed API; hydration also consumes ANCESTOR
  rows (message_scheduler/events/scheduled_message_sent.py:22), so the fix helps there too.
  Conclusion: recommend ancestor_field = "portfolio" — finding upgraded from "confirm intent"
  to a straightforward change request.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/50977
tags:
- morning-gtd
- github
- from-awareness
time_minutes: 20
title: 'Review PR #50977: PortfolioType + PortfolioTypeAssignment models (Andrea)'
updated: 2026-07-23 13:36:46.237430
waiting_on: null
waiting_since: null
working_on: false
---

Andrea asked "review plz" in her EOD. PortfolioType TextChoices enum + through-model with (portfolio, type) unique constraint; migration hotels/0756. ENT-6873.
https://github.com/canary-technologies-corp/canary/pull/50977