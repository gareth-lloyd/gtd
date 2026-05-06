---
area: management
contexts:
- deep
created: 2026-05-06 09:33:02.029222
defer_until: null
due: 2026-05-06
energy: high
id: 2026-05-06T0933-review-ryan-s-wip-pre-production-hotels-eng-design
order: 1
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C08RELXN00M/p1778028161817529
tags:
- morning-gtd
- slack
time_minutes: 15
title: Review Ryan's WIP Pre-Production Hotels eng design (Notion)
updated: 2026-05-06 14:05:00.000000
waiting_on: null
waiting_since: null
working_on: true
output: |
  ## Agent run 2026-05-06T14:05Z

  Reviewed Ryan's WIP doc (Notion: Pre-Production Hotels, ENT-5912) against the
  canary codebase. Did NOT comment in Notion — review notes only, for Gareth to
  draft the response himself.

  Overall: the design is coherent and the salesforce-oriented direction is
  right. Ryan asked for "glaring omissions" — below are the items that look
  load-bearing and either missing or under-specified. Ordered roughly by
  blast radius.

  ### 1. The portfolio-mapping change is bigger than the doc claims (HIGH)

  Doc lists 5 call sites that propagate from
  `hotel_belongs_to_portfolio_by_identifier()`. Real count of code that gates
  on `Portfolio.Identifier.WYNDHAM` (and similar) and *bypasses* that service
  method is much larger. Sampled non-test, non-migration call sites:

  - `message_scheduler/services/utils.py:23` —
    `PortfolioHotel.objects.filter(hotel=spec.hotel,
    portfolio__identifier=Portfolio.Identifier.WYNDHAM).exists()`
  - `onboarding/services/salesforce_onboarding_fields.py:498` —
    `Hotel.objects.filter(portfolio__identifier=portfolio_identifier)`
  - `onboarding/services/rollout.py:109` —
    `live_qs.filter(portfoliohotel__portfolio__identifier=portfolio_identifier)`
  - `onboarding/services/vendor/wyndham_properties_batch_update_service.py:285,364`
  - `voice/services/booking.py:78,133`
  - `voice/skills/reservation_search.py:862`
  - `voice/livekit/utilities/agent_ability_checks.py:35`
  - `voice/livekit/agents/booking/agent.py:132`
  - `voice/services/default_voice_booking_template.py:15`
  - `voice/management/commands/onetime_update_wyndham_upsell_channel_number.py:52`
  - `message_templates/services/message_template.py:143`
  - `hotels/services/membership_level_new.py:388`
  - `onboarding/models/use_case.py:109,164`
  - `onboarding/services/master_service_agreement.py:11,17`

  The doc currently implies a single-method change "propagates" — it doesn't.
  Several of these are dict-key lookups (`{Portfolio.Identifier.WYNDHAM:
  WyndhamGuestJourneyMessageUseCases}`) where a service-method change is
  irrelevant; staging hotels just won't be in the dict.

  Ask Ryan to add an explicit audit step + decision matrix per call site:
  "should staging hotels match this gate (yes / no / parity-required)?" and
  list the resolution. Otherwise staging Wyndham hotels will silently lack
  Wyndham booking, voice, message-scheduling, and use-case behavior — defeating
  the parity goal.

  ### 2. IHG mapping is mis-aimed (HIGH)

  Doc proposes `STAGING_TO_PRODUCTION = {IHG_STAGING: IHG, ...}`. But IHG's
  *real* gate identifier is `IHG_PILOT`, not `IHG`. Production IHG hotels are
  added to BOTH (see `ihg_portfolio_provider.py:11,20`), and the bulk of
  IHG-specific behavior keys off `IHG_PILOT`:

  - `ihg_deactivate_hotel_provider.py:29` — IHG_PILOT
  - `ihg_remove_hotel_from_parent_brand_provider.py:63` — IHG_PILOT
  - `enterprise_ihg/services/ihg_reservation_data.py:32,50` — IHG_PILOT
  - `check_in/services/check_in.py:692,1490` — IHG_PILOT
  - `guest/services/membership_program.py:337` — IHG_PILOT in identifiers
  - `onboarding/management/commands/create_ihg_cohorts.py:27` — IHG_PILOT
  - `rollout_recipe.py:68` — IHG_PILOT

  Mapping `IHG_STAGING -> IHG` covers segmentation/tips/some loyalty paths but
  misses deactivation, reservation data, check-in, membership_program, and
  cohort logic. Either map `IHG_STAGING -> {IHG, IHG_PILOT}` (set, not single
  value), or have the staging IHG provider place hotels in IHG_STAGING +
  another internal staging-pilot identifier. Worth Ryan thinking through.

  ### 3. PMS Gateway UAT wiring deferred to "manual today" — biggest gap (HIGH)

  The dependency table marks "PMS Gateway UAT env wiring" as Manual today and
  moves on. This is the entire point of the project (a hotel pointing at a
  customer UAT PMS). The doc should at minimum:

  - Specify how the staging onboarding type configures the PMS connection to
    UAT (is there an `is_staging` on the PMS connection or a separate UAT
    endpoint pool? does staging onboarding pick a UAT PMS instance via a new
    SF field?).
  - Define what happens if the wiring is forgotten — does the staging hotel
    point at the production PMS by default? That would be catastrophic.
  - State who owns this and whether ENT or PMS Gateway team is on the hook,
    in this scope or follow-up.

  ### 4. SF account → onboarding-type guardrail (MEDIUM)

  Each staging hotel needs its own SF account, but nothing in the design
  prevents accidentally passing a *production* SF account ID into a staging
  batch (or vice versa). Suggest a guardrail in the staging onboarding type:
  reject SF accounts whose Name doesn't start with a staging marker, or
  require an SF custom field. Without this, sales-ops/admin error → a real
  hotel onboarded into the staging portfolio with `is_demo=True` and a
  `staging-` slug. Recoverable but ugly.

  ### 5. Slug-prefix enforcement is one-directional (MEDIUM)

  Doc enforces `staging-` prefix at staging onboarding time. It does NOT
  reject `staging-` prefix on production onboarding. A typo or copy-paste
  during prod onboarding → a prod hotel with a staging slug, which the SDM
  WASM plugin will then mishandle. One-line check in the production
  HotelInfoProvider would close this.

  ### 6. GoLivePlan skipped — side effects not enumerated (MEDIUM)

  Doc says GoLive is skipped because we don't want to activate staging
  hotels. But GoLive does more than flip `is_demo`: it sets `is_live=True`
  and unblocks downstream behavior (SMS via Twilio, payment gateway swap,
  etc.). Plenty of code paths likely branch on `is_live`. If staging hotels
  stay `is_live=False`, some test scenarios won't reproduce the production
  flow that customers want to validate. Ryan should list which features
  *cannot* be tested on staging hotels because of this and confirm that's
  acceptable.

  ### 7. Staging API credential lifecycle unspecified (MEDIUM)

  SDK example shows `app_staging_xxx`. `is_staging` already exists on
  ApplicationRecord (confirmed at `api_gateway/services/application_credential_service.py:30`).
  But the doc doesn't say:

  - Who/when creates the staging ApplicationRecord per hotel?
  - Is there 1 staging credential per staging hotel, or 1 per portfolio?
  - Is creation part of the staging onboarding pipeline, or out-of-band?
  - How do customers retrieve it?

  Without this, the SDK story remains "it'll work after SDM-4248" but skips
  the credential-issuance flow.

  ### 8. Notification side-effects beyond Twilio (MEDIUM)

  Doc only addresses Twilio (skipped). Other PII-bearing channels:

  - Guest-facing emails (booking confirmations, check-in invites) — staging
    hotels likely fire emails to whatever email is on the SF account /
    reservation. Need an explicit suppression strategy or env flag.
  - Outbound webhooks to PMS/CRS — UAT or prod targets?
  - Slack incident bots / on-call alerts triggered by staging hotel errors.

  ### 9. PortfolioService.add_hotels for the data migration (LOW but specific)

  Data-migration step says "migrate existing Wyndham pre-production hotels
  (3-5) to WYNDHAM_STAGING with staging- slug prefix". Codebase convention
  is that portfolio membership changes go through
  `PortfolioService.add_hotels()` / `remove_hotel()`, NOT direct
  `PortfolioHotel.objects.create/delete`. Worth calling out in the doc so
  whoever writes the migration follows the rule.

  ### 10. PUBLIC_PORTFOLIO_IDENTIFIERS side-effects under-explored (LOW)

  Adding staging identifiers to PUBLIC_PORTFOLIO_IDENTIFIERS isn't only a
  GrowthBook concern. The frozenset is also used by:

  - `hotel_staff/services/user_assignment_operation.py:42` — user assignment
    queries
  - `portfolios/services/portfolio.py:334,356` — portfolio lookups

  Behavioral diff for those callers should be confirmed, not just for
  GrowthBook. The doc considers and rejects a separate attribute partly on
  "the public set is already loose"; that's true but doesn't excuse skipping
  the impact analysis for the two non-GrowthBook callers.

  ### 11. Naming-suffix inconsistency (NIT)

  `WYNDHAM_STAGING_MSA`, `IHG_STAGING`, `BEST_WESTERN_STAGING_MSA`. Why does
  IHG drop `_MSA`? If it's because IHG isn't an MSA contract, fine — say so.
  Otherwise pick one convention.

  ### 12. Cron / Celery / batch-update interactions (LOW)

  `wyndham_properties_batch_update_service` (Wyndham property data sync)
  filters by `Portfolio.Identifier.WYNDHAM` to find hotels to update. Will
  it also pull/touch staging Wyndham hotels? Doc should make that decision
  explicit. Likely answer: staging hotels should be excluded so their config
  isn't overwritten by a Wyndham-feed run, but the staging providers don't
  currently exclude them.

  ### 13. Rollback / cleanup path (LOW)

  No mention of how to retire a staging hotel cleanly — does deactivation
  use the existing `wyndham_deactivate_hotel_provider`? If so, that provider
  early-returns on hotels not in `Portfolio.Identifier.WYNDHAM`
  (`wyndham_deactivate_hotel_provider.py:31`), so staging hotels can't be
  deactivated by it unless the mapping covers it.

  ### Things the doc gets right (worth saying so to Ryan)

  - Rejection of the dual-portfolio (staging+production) approach is correct.
    Filtering staging hotels out of every dashboard is a worse problem than
    the brand-parity-via-mapping problem.
  - Rejection of a separate canary staging environment is the right call,
    given the team's bandwidth.
  - Rejection of the "copy from existing hotel" path is well-justified —
    salesforce + standard onboarding pipeline is much closer to the
    production codepath, so staging hotels actually validate what we ship.
  - Decision NOT to add `is_staging` to the Hotel model and instead use
    portfolio membership is consistent with how `is_demo` and brand
    identifiers already work — good.
  - Skipping GoLive/Twilio/PaymentGateway plans is the correct minimal-mode
    set (just need to enumerate the trade-offs per #6).

  ### Suggested next-step for Ryan

  Two things would tighten this from WIP to ready-for-final-review:

  1. Replace the 5-line "propagates to call sites" claim with an actual
     grep-based audit, and a per-call-site decision (parity / exclude /
     skip). Same shape Section 1 above suggests.
  2. Make IHG_PILOT explicit in the staging mapping — it's the dominant
     IHG gating identifier, not IHG.

  Everything else is "address before merge" rather than "redesign."
---

Ryan posted WIP draft in Group DM 5/6 03:42 — wants eyes for glaring omissions before final draft. Notion doc: Pre-Production Hotels. Salesforce-oriented approach (no copy-from-existing). https://canarytechnologies.slack.com/archives/C08RELXN00M/p1778028161817529