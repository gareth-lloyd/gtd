---
area: null
contexts: []
created: 2026-05-07 20:45:23.646871
defer_until: null
due: null
energy: medium
id: 2026-05-07T2045-re-review-ryan-pre-prod
order: -4
output: '## Agent run 2026-05-08T14:00 — re-review of v3


  Reviewed: Pre-Production Hotels design doc (Notion 35881468...22a8), v3 dated 2026-05-06.

  Linear: ENT-5912. Project: ea3f26bc... (Configure Pre-Production Environment for
  Wyndham).


  ### Status of my v2 comments

  Both incorporated cleanly:

  - **Entry point**: v3 abandons "staging hotel has its own SF account" entirely (Connor
  confirmed marketing won''t allow staging in SFDC). New `OnboardingService.onboard_staging_hotel_from_production_hotel()`
  creates a fresh Hotel without `SalesforceHotelMetadata`, reuses prod hotel''s `sfdc_account`
  for plan-data, delegates to `run_plans_on_hotel()`. Also dropped `OnboardingScriptBatchAdmin`
  path in favor of a `create_staging_hotel` management command (Connor framed usage
  as "spikey" / EPD-managed). Right call.

  - **Portfolio-scoped staging API credentials**: Adopted as proposed. New nullable
  FK `Portfolio.staging_application_record`, `bootstrap_staging_portfolio` mgmt command,
  defense-in-depth credential-vs-portfolio check on requests. `create_staging_hotel`
  refuses to run if the portfolio credential isn''t populated — clear ordering.


  ### v3 additions worth noting

  - **OHIP environment separation now in scope (Chunk 2)**, modeled on PMS-7177. Wyndham''s
  existing dummy-hotel-codes workaround for OHIP Sandbox / SPH Test Location is what
  Connor said broke things; doing the OHIP env work removes that workaround. Right
  time to do it. PMS-Gateway team should review for pattern consistency with PMS-7177.

  - Doc''s "Alternative solutions" section is well-reasoned; explicitly explains why
  dual-portfolio membership and per-hotel credentials were rejected.


  ### New flags / things I''d raise on v3


  1. **Blast-radius audit on `hotel_belongs_to_portfolio_by_identifier()`**: doc lists
  5 call sites that propagate brand behavior to staging. That''s not an inventory
  — it''s the touched call sites for booking/segmentation. Need a grep audit of all
  `Portfolio.Identifier.WYNDHAM` / `IHG` / `BEST_WESTERN` references and decide per-call-site
  whether staging-equivalence is desired. Risk areas: any flow that contacts external
  customer systems on a "production brand" check (loyalty submissions, analytics push,
  marketing) — staging hotels point PMS at UAT but may still call non-PMS prod endpoints
  if gated only on portfolio identifier. The doc''s mitigation ("`is_demo=True` and
  separate portfolio") only helps where downstream code reads those fields.


  2. **OHIP inbound webhook routing**: doc says "exact disambiguation mechanism (URL
  prefix vs. payload field) confirmed during implementation". Push to nail down before
  Chunk 2 starts — depends on whether OHIP supports per-env webhook URLs. If it doesn''t,
  payload-based disambiguation may be the only option and that affects model design.


  3. **`is_demo=True` is doing a lot of implicit work** ("uses Stripe test keys, excluded
  from some prod flows"). Worth a similar audit to (1): grep `is_demo` and confirm
  every call site does the right thing for staging hotels (which are a stricter subset
  than demo hotels). Some "demo" gates may not be appropriate for staging; some staging-specific
  behavior may not be covered by `is_demo`.


  4. **SF-account write-back risk**: prod hotel''s `sfdc_account` is read for plan-data
  construction. Need to confirm none of the "Runs with SF data (same)" plans *write*
  back to the SF account as a side-effect — otherwise the staging onboarding mutates
  prod SF state. Skipped plans (Twilio, PaymentGateway, GoLive) are obvious; the long
  tail of "all other plans" is not audited in the doc.


  5. **Drift / refresh acknowledgment is thin**: command is idempotent (errors if
  staging hotel exists), and "automated refresh" is explicitly out of scope. Fine
  for v1 — but should call out that drift between prod and staging configuration is
  a known operational gap, with a manual remediation path (teardown + rebuild). Otherwise
  the first time prod config changes meaningfully, ops will be surprised.


  6. **Chunk ordering: IHG migration in Chunk 1, IHG providers in Chunk 6**: data
  migration sets `identifier=''ihg_staging''` on existing portfolio 3764 in Chunk
  1, but `StagingIhgPMSConfigProvider` etc. don''t land until Chunk 6. Between those,
  IHG staging hotels are in a portfolio with no working create-flow. Fine if no creation
  happens in that window, but the dependency should be explicit (or move the data
  migration to Chunk 6).


  7. **OHIP unique-constraint migration**: "add nullable FK → backfill → set non-null
  → change unique constraint" is the right shape, but the unique-constraint change
  is the risky step. Worth confirming `OracleOhip` table size and whether the constraint
  swap needs a maintenance window or `CONCURRENTLY` strategy.


  8. **Credential blast radius vs rotation**: portfolio-scoped credential is good
  ergonomics, but a leak = all staging hotels of that brand. For UAT-pointed, `is_demo=True`,
  no real reservation data this is probably fine — but worth a one-liner stating the
  threat model is accepted, plus rotation procedure (presumably re-run `bootstrap_staging_portfolio`
  and tell customer to swap key).


  9. **Defense-in-depth check perf**: per-request "hotel''s portfolio has a `staging_application_record`
  matching the validated credential" loads portfolio memberships on the hot path.
  Confirm the existing auth/slug-resolution flow already loads this, or note the caching
  strategy.


  10. **Operator UX once volume grows**: doc estimates 5–50 staging hotels per brand.
  The "optional adjacent admin work" (Hotel changelist filter for staging hotels)
  probably needs to be in scope — at 50 hotels, EPD search needs to know how to find
  them.


  11. **`create_staging_hotel` failure modes underspecified**: what happens if the
  production slug refers to a hotel with no `PRODUCTION_TO_STAGING` mapping (e.g.,
  Marriott)? Should error clearly. Worth a line in success criteria.


  ### Recommendation

  v3 is in good shape — design is implementable as written. The flags above are mostly
  audit/scope items, not architectural blockers. Suggest:

  - Block on (1), (2), (4) before Chunk 1/2 start (they may shift scope).

  - Defer (3), (5), (6), (7), (8), (9), (10), (11) to be addressed inline during implementation
  or as doc clarifications.


  ### Next action

  Decide whether to post these as Notion comments on the design doc, raise async with
  Ryan in Slack, or batch into a synchronous review. I have NOT posted anything to
  Notion or Linear — drafting only. Awaiting your call.

  '
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 15
title: RE-review Ryan pre-prod
updated: 2026-05-08 14:30:39.638494
waiting_on: null
waiting_since: null
working_on: true
---

https://linear.app/canary-technologies/issue/ENT-5912/engineering-design-for-pre-production-wyndham-environment