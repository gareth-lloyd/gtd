---
area: null
contexts:
- react
created: 2026-05-29 11:43:03.820126
defer_until: 2026-06-01 09:00:00
due: null
energy: medium
id: 2026-05-29T1143-review-pr-46624-ent-6179-wyndham-staging-providers
order: null
output: |
  ## Agent run 2026-05-29T13:05

  Reviewed PR #46624 (ENT-6179, rrgrs). +330/-0, 5 files. Top of a 3-PR stack
  (on #46621/#46618). Verified diff against HEAD 1d03ed9 and compared the new
  WYNDHAM_STAGING_MSA config stage-by-stage against WYNDHAM_MSA.

  VERDICT: Looks solid. No blocking bugs. The mirror is faithful and the three
  intentional drops are correctly applied. A few clarifying questions worth
  raising with Ryan before/at approval (none are hard blockers).

  ### What I verified
  - **Mirror is faithful.** BASE_CONFIGURATION_NEW plan list matches WYNDHAM_MSA
    exactly except ConfigurePaymentGatewayIntegrationPlan dropped; providers
    swapped only for HotelInfo/Portfolio/PMS. Stage graph correct: CONFIGURE_TWILIO
    and GOLIVE stages removed, terminal_stage moved GOLIVE→CONFIGURE_ROOM_UPGRADES,
    next_stages updated consistently (base no longer points at CONFIGURE_TWILIO;
    room_upgrades no longer points at GOLIVE). EnableMsaProductsPlan still runs in
    base config, so dropping the GOLIVE re-run is harmless. pre_start_checks kept.
  - **Providers correct.** StagingWyndhamHotelInfoProvider prepends `staging-`
    after super() sets the wyndham-{site_id} slug; inherits overwrite=True; no
    double-prefix risk (super re-derives slug each instantiation).
    StagingWyndhamPMSConfigProvider rewrites SphConfiguration.environment_configuration
    to "Wyndham Staging" via dataclass replace; OHIP raises NotImplementedError.
    StagingWyndhamPortfolioConfigProvider emits only WYNDHAM_STAGING.
  - **Enums/types exist on-branch** (parent PRs): Portfolio.Identifier.WYNDHAM_STAGING,
    OnboardingType.WYNDHAM_STAGING_MSA.
  - **Tests sound by inspection.** stub_pms_secrets/stub_onboarding_plan_data
    signatures match the kwargs used; SynXis vs OPERA vendor resolution traces
    correctly to the asserted outcomes. PR claims 292 passing + pyright/ruff clean.

  ### Questions / things to confirm with Ryan (non-blocking)
  1. **SphCrsConfiguration NOT rewritten for staging.** The SYNXIS branch of the
     parent adds BOTH SphConfiguration and SphCrsConfiguration. The staging
     provider only rewrites SphConfiguration; SphCrsConfiguration keeps
     environment="Wyndham" (production CRS) + production creds. Confirm staging
     SynXis hotels are meant to keep the production CRS environment, or whether
     the CRS row also needs a staging variant.
  2. **IDS_NEXT falls through silently.** StagingWyndhamPMSConfigProvider only
     branches on OPERA (raise) and SYNXIS (rewrite). An IDS_NEXT Wyndham hotel
     would silently emit an unmodified PRODUCTION IDSNextConfiguration. If IDS_NEXT
     isn't in scope for staging, consider raising NotImplementedError (mirroring
     the OHIP guard) so the gap is loud rather than silently pointing a staging
     hotel at prod IDS Next.
  3. **Non-swapped providers stay production.** SSO (WyndhamSsoProvider),
     MembershipGateway, GuestJourney, Chat all still use production providers for
     staging hotels. Most likely intended per the design doc (only portfolio/
     hotel-info/PMS needed staging variants), but worth a one-line confirm —
     membership gateway registering a staging hotel against prod is the notable one.
  4. **is_demo dependency.** Dropping ConfigurePaymentGatewayIntegrationPlan relies
     on the hotel being created with is_demo=True (Stripe test keys). That flag is
     set outside this PR (mgmt command / parent). Just flagging the coupling.

  ### Minor
  - OHIP branch runs the full production OHIP path in super().__init__ (secret
    fetch + OhipConfiguration build) before raising NotImplementedError. Harmless
    (it raises) and hard to avoid since self.vendor is only set inside super(), so
    fine to leave — noting for completeness.
  - ad_hoc_stages omitted means no UPDATE_PMS_CONFIGURATION / PRE_POPULATE_RESERVATIONS
    for staging hotels via this entry point. Fine for the creation-only scope, and
    those use the production WyndhamPMSConfigProvider anyway.

  No code changes made. No comments posted to GitHub (would need explicit approval).
  If you want, I can draft an inline PR comment with questions 1 & 2.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/46624
tags:
- morning-gtd
- github
- from-awareness
time_minutes: 20
title: 'Review PR #46624: ENT-6179 Wyndham staging providers + wire WYNDHAM_STAGING_MSA'
updated: 2026-05-29 12:47:00.075330
waiting_on: null
waiting_since: null
working_on: false
---

Top of rrgrs's stack (stacked on #46621 / #46618). First brand wired end-to-end for staging hotel creation. https://github.com/canary-technologies-corp/canary/pull/46624