---
area: null
completed_at: 2026-11-06 16:19:14.428006
contexts:
- react
created: 2026-11-06 10:24:22.078046
defer_until: null
due: null
energy: medium
id: 2026-11-06T1024-review-pr-63647-and-help-jordan-sterling-finish-th
order: null
output: |
  ## Agent run 2026-11-06T15:30 (local)

  ### Verdict on PR #63647 (https://github.com/canary-technologies-corp/canary/pull/63647)
  The two lines are correct and complete *for the catalog step*. Approve-able as-is, with one naming/locking suggestion below.
  - `Portfolio.identifier` has no `choices=` any more (backend/canary/hotels/models/portfolio.py:161), so adding an enum member needs no migration. Hyatt (#60494) set the same precedent.
  - The `TYPES_BY_IDENTIFIER` line is required: `test_types_by_identifier__covers_every_identifier` asserts the map covers every `Portfolio.Identifier`.
  - CI: everything green incl. `make test-backend`. The only red check is "Birdline policy", which is the review gate (no approval yet), not a code failure.
  - Not a migration PR, so no split needed.

  ### What Jordan still has to do (the enum entry creates nothing)
  1. **Create the Portfolio row in every region**: US/EU/AP prod + staging. Precedent is `backend/canary/api_gateway/management/commands/bootstrap_backfill_portfolios.py` (ENT-6937): a fixed identifier set, `PortfolioService.create_portfolio(hotel_slugs=[], ...)`, `--operator-email`, dry-run by default, `--commit` to write, idempotent. Easiest path: add `Portfolio.Identifier.CANARY.value` to that command's `_NEW_IDENTIFIERS` set (or copy the pattern into a sibling command) and have an engineer with prod shell access run it per region. This answers the open question in ID-144 ("who creates a portfolio and how is still open"): same way the `internal_*` and Conferma/HotelEngine rows were created.
  2. **Then run** `onetime_backfill_portfolio_type_assignments --commit` per region so the new row gets its type assignment. The command only assigns to rows that exist, so it must run after step 1.
  3. **Local dev**: ID-144 says `make up` should pre-create the Canary Website app + secret. The local portfolio row needs the same treatment or `ApplicationService.create` will point at a portfolio that does not exist locally. Check what `dev_set_up_sso.py` does for the Staff App's DEMO portfolio (it upserts the row) and mirror it.
  4. **Staff App scope creep**: the PR body says `canary` will own the Staff App. Today the Staff App's local application is pinned to `Portfolio.Identifier.DEMO` (`STAFF_APP_PORTFOLIO_IDENTIFIER` in backend/canary/sso/management/commands/dev_set_up_sso.py:51) and prod staff access is granted via `EPD_TEST_PORTFOLIO` in canary_staff_service.py:82. Moving the Staff App is a separate change with its own blast radius; keep this PR to the Website app and do not re-point those.

  ### On the security concern Gareth raised in the thread
  The design doc (https://app.notion.com/p/canarytechnologies/Global-Web-3c6814686151805b8a11f952998b7a6d) is explicit: "A Canary portfolio for our applications", i.e. an owner for first-party `applications` rows, not a hotel grouping. That matches the existing precedent of the hotel-less `internal_*` portfolios (internal_zendesk, internal_sales_booking_agent, ...). The access model makes a hotel-less portfolio safe:
  - An `ApplicationPrincipal` under it resolves hotels via `Hotel.objects.filter(portfoliohotel__portfolio__identifier=...)` (backend/canary/hotels/access_control/hotel_access.py:54-56), so zero hotels => zero hotels.
  - The Website app issues *user* tokens; `UserPrincipal` hotel scope comes from `companyhoteluser`, not from the application's portfolio. So the portfolio never needs hotels for the website to work.
  The risk is only that someone later adds hotels to a portfolio called "Canary". Two cheap mitigations to ask for in the PR:
  - Put `CANARY` in `CONTROLLED_BY_SCRIPTS_IDENTIFIERS` (same file as the PR's second change) instead of / in addition to `AD_HOC`. `Portfolio.is_admin_management_restricted()` then blocks hand-editing hotel and user membership in Django admin.
  - Make the label say what it is, e.g. `CANARY = "canary", "Canary (first-party applications, no hotels)"`, and a one-line comment on the enum member that it must never contain hotels. The identifier value `canary` can stay since ID-144 and the design doc already use it.

  ### Draft Slack reply for the thread (NOT sent; paste if you agree)
  https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1793928911698389?thread_ts=1793928911.698389&cid=C047K6WSUJY

  > Read the design doc, this is a portfolio that *owns applications* (Canary Website etc.), not hotels, so same shape as the `internal_*` portfolios from the ENT-6937 backfill. That's fine as long as it stays hotel-less: an app principal under it gets zero hotels, and the website's user tokens scope hotels by membership, not by the app's portfolio. Two asks on the PR: (1) put `CANARY` in `CONTROLLED_BY_SCRIPTS_IDENTIFIERS` so admin can't hand-add hotels to it, and (2) make the label say "first-party applications, no hotels" so nobody reads "Canary" as "every hotel".
  >
  > On "what else is there to do": the enum is just the catalog, it creates nothing. You still need the Portfolio row in each region (US/EU/AP prod + staging). Precedent is `bootstrap_backfill_portfolios` (`--operator-email`, `--commit`): add `canary` to its `_NEW_IDENTIFIERS` and run it per region, then run `onetime_backfill_portfolio_type_assignments --commit` so the row gets its type. Local dev needs the row too before `make up` can create the Website app against it. I'd keep the Staff App out of this PR, it's pinned to `demo`/`epd_test_portfolio` today and moving it is its own change.

  ### Not done
  - No comments posted to GitHub, Slack, or Linear. No approval submitted.
  - Did not run the test suite locally; relied on the green `make test-backend` CI run on the PR.
project: null
source_id: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1793928911698389?thread_ts=1793928911.698389&cid=C047K6WSUJY
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Review PR #63647 and help Jordan Sterling finish the portfolio identifier
  (#epd-enterprise)'
updated: 2026-11-06 16:19:14.427991
waiting_on: null
waiting_since: null
working_on: false
---

Jordan: "i tried to make a portfolio identifier today. i dont know everything that goes into making a portfolio identifier and may need help if there's more to do here". 2-line PR for the public MCP app's portfolio. Pecking Order: unassigned.
https://github.com/canary-technologies-corp/canary/pull/63647
https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1793928911698389?thread_ts=1793928911.698389&cid=C047K6WSUJY