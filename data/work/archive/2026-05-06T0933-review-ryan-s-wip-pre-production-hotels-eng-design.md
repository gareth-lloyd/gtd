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
output: "## Agent run 2026-05-06T14:05Z\n\nReviewed Ryan's WIP doc (Notion: Pre-Production
  Hotels, ENT-5912) against the\ncanary codebase. Did NOT comment in Notion — review
  notes only, for Gareth to\ndraft the response himself.\n\nOverall: the design is
  coherent and the salesforce-oriented direction is\nright. Ryan asked for \"glaring
  omissions\" — below are the items that look\nload-bearing and either missing or
  under-specified. Ordered roughly by\nblast radius.\n\n### 1. The portfolio-mapping
  change is bigger than the doc claims (HIGH)\n\nDoc lists 5 call sites that propagate
  from\n`hotel_belongs_to_portfolio_by_identifier()`. Real count of code that gates\non
  `Portfolio.Identifier.WYNDHAM` (and similar) and *bypasses* that service\nmethod
  is much larger. Sampled non-test, non-migration call sites:\n\n- `message_scheduler/services/utils.py:23`
  —\n  `PortfolioHotel.objects.filter(hotel=spec.hotel,\n  portfolio__identifier=Portfolio.Identifier.WYNDHAM).exists()`\n-
  `onboarding/services/salesforce_onboarding_fields.py:498` —\n  `Hotel.objects.filter(portfolio__identifier=portfolio_identifier)`\n-
  `onboarding/services/rollout.py:109` —\n  `live_qs.filter(portfoliohotel__portfolio__identifier=portfolio_identifier)`\n-
  `onboarding/services/vendor/wyndham_properties_batch_update_service.py:285,364`\n-
  `voice/services/booking.py:78,133`\n- `voice/skills/reservation_search.py:862`\n-
  `voice/livekit/utilities/agent_ability_checks.py:35`\n- `voice/livekit/agents/booking/agent.py:132`\n-
  `voice/services/default_voice_booking_template.py:15`\n- `voice/management/commands/onetime_update_wyndham_upsell_channel_number.py:52`\n-
  `message_templates/services/message_template.py:143`\n- `hotels/services/membership_level_new.py:388`\n-
  `onboarding/models/use_case.py:109,164`\n- `onboarding/services/master_service_agreement.py:11,17`\n\nThe
  doc currently implies a single-method change \"propagates\" — it doesn't.\nSeveral
  of these are dict-key lookups (`{Portfolio.Identifier.WYNDHAM:\nWyndhamGuestJourneyMessageUseCases}`)
  where a service-method change is\nirrelevant; staging hotels just won't be in the
  dict.\n\nAsk Ryan to add an explicit audit step + decision matrix per call site:\n\"should
  staging hotels match this gate (yes / no / parity-required)?\" and\nlist the resolution.
  Otherwise staging Wyndham hotels will silently lack\nWyndham booking, voice, message-scheduling,
  and use-case behavior — defeating\nthe parity goal.\n\n### 2. IHG mapping is mis-aimed
  (HIGH)\n\nDoc proposes `STAGING_TO_PRODUCTION = {IHG_STAGING: IHG, ...}`. But IHG's\n*real*
  gate identifier is `IHG_PILOT`, not `IHG`. Production IHG hotels are\nadded to BOTH
  (see `ihg_portfolio_provider.py:11,20`), and the bulk of\nIHG-specific behavior
  keys off `IHG_PILOT`:\n\n- `ihg_deactivate_hotel_provider.py:29` — IHG_PILOT\n-
  `ihg_remove_hotel_from_parent_brand_provider.py:63` — IHG_PILOT\n- `enterprise_ihg/services/ihg_reservation_data.py:32,50`
  — IHG_PILOT\n- `check_in/services/check_in.py:692,1490` — IHG_PILOT\n- `guest/services/membership_program.py:337`
  — IHG_PILOT in identifiers\n- `onboarding/management/commands/create_ihg_cohorts.py:27`
  — IHG_PILOT\n- `rollout_recipe.py:68` — IHG_PILOT\n\nMapping `IHG_STAGING -> IHG`
  covers segmentation/tips/some loyalty paths but\nmisses deactivation, reservation
  data, check-in, membership_program, and\ncohort logic. Either map `IHG_STAGING ->
  {IHG, IHG_PILOT}` (set, not single\nvalue), or have the staging IHG provider place
  hotels in IHG_STAGING +\nanother internal staging-pilot identifier. Worth Ryan thinking
  through.\n\n### 3. PMS Gateway UAT wiring deferred to \"manual today\" — biggest
  gap (HIGH)\n\nThe dependency table marks \"PMS Gateway UAT env wiring\" as Manual
  today and\nmoves on. This is the entire point of the project (a hotel pointing at
  a\ncustomer UAT PMS). The doc should at minimum:\n\n- Specify how the staging onboarding
  type configures the PMS connection to\n  UAT (is there an `is_staging` on the PMS
  connection or a separate UAT\n  endpoint pool? does staging onboarding pick a UAT
  PMS instance via a new\n  SF field?).\n- Define what happens if the wiring is forgotten
  — does the staging hotel\n  point at the production PMS by default? That would be
  catastrophic.\n- State who owns this and whether ENT or PMS Gateway team is on the
  hook,\n  in this scope or follow-up.\n\n### 4. SF account → onboarding-type guardrail
  (MEDIUM)\n\nEach staging hotel needs its own SF account, but nothing in the design\nprevents
  accidentally passing a *production* SF account ID into a staging\nbatch (or vice
  versa). Suggest a guardrail in the staging onboarding type:\nreject SF accounts
  whose Name doesn't start with a staging marker, or\nrequire an SF custom field.
  Without this, sales-ops/admin error → a real\nhotel onboarded into the staging portfolio
  with `is_demo=True` and a\n`staging-` slug. Recoverable but ugly.\n\n### 5. Slug-prefix
  enforcement is one-directional (MEDIUM)\n\nDoc enforces `staging-` prefix at staging
  onboarding time. It does NOT\nreject `staging-` prefix on production onboarding.
  A typo or copy-paste\nduring prod onboarding → a prod hotel with a staging slug,
  which the SDM\nWASM plugin will then mishandle. One-line check in the production\nHotelInfoProvider
  would close this.\n\n### 6. GoLivePlan skipped — side effects not enumerated (MEDIUM)\n\nDoc
  says GoLive is skipped because we don't want to activate staging\nhotels. But GoLive
  does more than flip `is_demo`: it sets `is_live=True`\nand unblocks downstream behavior
  (SMS via Twilio, payment gateway swap,\netc.). Plenty of code paths likely branch
  on `is_live`. If staging hotels\nstay `is_live=False`, some test scenarios won't
  reproduce the production\nflow that customers want to validate. Ryan should list
  which features\n*cannot* be tested on staging hotels because of this and confirm
  that's\nacceptable.\n\n### 7. Staging API credential lifecycle unspecified (MEDIUM)\n\nSDK
  example shows `app_staging_xxx`. `is_staging` already exists on\nApplicationRecord
  (confirmed at `api_gateway/services/application_credential_service.py:30`).\nBut
  the doc doesn't say:\n\n- Who/when creates the staging ApplicationRecord per hotel?\n-
  Is there 1 staging credential per staging hotel, or 1 per portfolio?\n- Is creation
  part of the staging onboarding pipeline, or out-of-band?\n- How do customers retrieve
  it?\n\nWithout this, the SDK story remains \"it'll work after SDM-4248\" but skips\nthe
  credential-issuance flow.\n\n### 8. Notification side-effects beyond Twilio (MEDIUM)\n\nDoc
  only addresses Twilio (skipped). Other PII-bearing channels:\n\n- Guest-facing emails
  (booking confirmations, check-in invites) — staging\n  hotels likely fire emails
  to whatever email is on the SF account /\n  reservation. Need an explicit suppression
  strategy or env flag.\n- Outbound webhooks to PMS/CRS — UAT or prod targets?\n-
  Slack incident bots / on-call alerts triggered by staging hotel errors.\n\n### 9.
  PortfolioService.add_hotels for the data migration (LOW but specific)\n\nData-migration
  step says \"migrate existing Wyndham pre-production hotels\n(3-5) to WYNDHAM_STAGING
  with staging- slug prefix\". Codebase convention\nis that portfolio membership changes
  go through\n`PortfolioService.add_hotels()` / `remove_hotel()`, NOT direct\n`PortfolioHotel.objects.create/delete`.
  Worth calling out in the doc so\nwhoever writes the migration follows the rule.\n\n###
  10. PUBLIC_PORTFOLIO_IDENTIFIERS side-effects under-explored (LOW)\n\nAdding staging
  identifiers to PUBLIC_PORTFOLIO_IDENTIFIERS isn't only a\nGrowthBook concern. The
  frozenset is also used by:\n\n- `hotel_staff/services/user_assignment_operation.py:42`
  — user assignment\n  queries\n- `portfolios/services/portfolio.py:334,356` — portfolio
  lookups\n\nBehavioral diff for those callers should be confirmed, not just for\nGrowthBook.
  The doc considers and rejects a separate attribute partly on\n\"the public set is
  already loose\"; that's true but doesn't excuse skipping\nthe impact analysis for
  the two non-GrowthBook callers.\n\n### 11. Naming-suffix inconsistency (NIT)\n\n`WYNDHAM_STAGING_MSA`,
  `IHG_STAGING`, `BEST_WESTERN_STAGING_MSA`. Why does\nIHG drop `_MSA`? If it's because
  IHG isn't an MSA contract, fine — say so.\nOtherwise pick one convention.\n\n###
  12. Cron / Celery / batch-update interactions (LOW)\n\n`wyndham_properties_batch_update_service`
  (Wyndham property data sync)\nfilters by `Portfolio.Identifier.WYNDHAM` to find
  hotels to update. Will\nit also pull/touch staging Wyndham hotels? Doc should make
  that decision\nexplicit. Likely answer: staging hotels should be excluded so their
  config\nisn't overwritten by a Wyndham-feed run, but the staging providers don't\ncurrently
  exclude them.\n\n### 13. Rollback / cleanup path (LOW)\n\nNo mention of how to retire
  a staging hotel cleanly — does deactivation\nuse the existing `wyndham_deactivate_hotel_provider`?
  If so, that provider\nearly-returns on hotels not in `Portfolio.Identifier.WYNDHAM`\n(`wyndham_deactivate_hotel_provider.py:31`),
  so staging hotels can't be\ndeactivated by it unless the mapping covers it.\n\n###
  Things the doc gets right (worth saying so to Ryan)\n\n- Rejection of the dual-portfolio
  (staging+production) approach is correct.\n  Filtering staging hotels out of every
  dashboard is a worse problem than\n  the brand-parity-via-mapping problem.\n- Rejection
  of a separate canary staging environment is the right call,\n  given the team's
  bandwidth.\n- Rejection of the \"copy from existing hotel\" path is well-justified
  —\n  salesforce + standard onboarding pipeline is much closer to the\n  production
  codepath, so staging hotels actually validate what we ship.\n- Decision NOT to add
  `is_staging` to the Hotel model and instead use\n  portfolio membership is consistent
  with how `is_demo` and brand\n  identifiers already work — good.\n- Skipping GoLive/Twilio/PaymentGateway
  plans is the correct minimal-mode\n  set (just need to enumerate the trade-offs
  per #6).\n\n### Suggested next-step for Ryan\n\nTwo things would tighten this from
  WIP to ready-for-final-review:\n\n1. Replace the 5-line \"propagates to call sites\"
  claim with an actual\n   grep-based audit, and a per-call-site decision (parity
  / exclude /\n   skip). Same shape Section 1 above suggests.\n2. Make IHG_PILOT explicit
  in the staging mapping — it's the dominant\n   IHG gating identifier, not IHG.\n\nEverything
  else is \"address before merge\" rather than \"redesign.\"\n"
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C08RELXN00M/p1778028161817529
tags:
- morning-gtd
- slack
time_minutes: 15
title: Review Ryan's WIP Pre-Production Hotels eng design (Notion)
updated: 2026-05-06 14:58:19.706575
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C08RELXN00M/p1778028161817529