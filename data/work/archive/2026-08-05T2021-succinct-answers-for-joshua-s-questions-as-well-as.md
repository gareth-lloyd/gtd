---
area: null
completed_at: 2026-08-05 22:01:58.824370
contexts: []
created: 2026-08-05 20:21:55.591652
defer_until: null
due: 2026-08-05
energy: low
id: 2026-08-05T2021-succinct-answers-for-joshua-s-questions-as-well-as
order: null
output: |
  ## Agent run 2026-08-05T20:45:00+03:00

  Researched Joshua's thread (https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1785950349523259)
  against the rules_based_configuration code, the Notion design doc
  (https://app.notion.com/p/canarytechnologies/Rules-based-hotel-configuration-269814686151800f8812f8373d3f90e3),
  and prod (Groundcover). Draft reply below — NOT posted anywhere; review and post yourself.

  ### Verified facts

  - **Q1 — Portfolio vs Salesforce.** The two "models" play different roles. Source of truth
    for *which groups a hotel belongs to* is Salesforce-derived attributes (brand, parent
    brand, mgmt company, MSAs) fetched once and cached on `StoredHotelAttributes`
    (rules_based_configuration/services/hotel_attributes.py). The config trees
    (ConformityService) are keyed by those attributes. The `Portfolio` DB model in
    `apply_portfolio_settings` is only used to *enumerate member hotels*; expected values
    still resolve via HotelAttributes → ConformityService. Drift detection enumerates its
    cohort per MSA via `MSA_HOTEL_PROVIDERS` (currently only WYNDHAM_CONNECT_GMS →
    onboarding's Salesforce-derived `should_have_gone_live_according_to_salesforce`). So
    yes, both in use near-term, but groups are *logical* (attribute-defined, per the design
    doc); Portfolio rows are a convenience for enumeration and should converge on the same
    cohorts. The `/rollout` page (onboarding RolloutService, `ROLLOUT_RECIPES`) is a
    *different* system — staged go-live batches from Salesforce populations — unrelated to
    settings conformity despite the "recipes" naming collision.
  - **Q2 — cron_detect_drift is NOT running in prod.** Confirmed via Groundcover entities:
    no CronJob for it exists in any canary namespace (the only "drift" cron is
    credential-manager's unrelated `cm-drift-report`). The command is ready: dry-run by
    default, `--commit` persists to `StoredHotelAttributes.drifts`; first committed pass
    baselines per hotel so no alert flood; fails loud (no heartbeat) on partial failure.
    Turning it on = adding a k8s CronJob in the infra/ArgoCD config + a monitor on
    `detect_drift.new_drift`. And yes — detection only, no auto-fix by design; the write
    path is `apply_portfolio_settings` (deliberately human-invoked, dry-run first).
  - **Q3 — consistency rules.** `configuration_consistency_rule` is live at two enforcement
    points: (1) a Django system check that validates *all possible setting combinations* of
    the code-defined trees (CI/startup — this is the "linter" layer), and (2) a warn-only
    signal on Canary Admin hotel saves. It does NOT block writes yet, so it complements
    rather than replaces `.save()`/`.clean()` validation for now. Joshua is right that
    `payment_gateway_required_for_tokenization` is broken — `hotel.payment_gateway_config_id`
    doesn't exist (the real relation is `hotel.payment_gateway`, reverse OneToOne from
    PaymentGatewayConfiguration), so the rule can misfire/never fire. Needs fixing before
    anyone relies on it. Verdict: yes, start writing rules for new cross-setting invariants,
    keep hard blocking in model validation until the rules engine grows a blocking mode.

  ### Domain analysis for his oncall/standardization project

  Mapping his plan onto existing mechanisms:
  - Canonical settings package per brand ("recipes") → GroupAttributes tree definitions in
    code. PR + CI consistency check already validates internal coherence — exactly his
    PR-then-apply flow: update tree → CI → merge → `apply_portfolio_settings --dry-run` →
    apply → drift detector catches stragglers/later mutations.
  - Config linter → don't build a separate tool; add `configuration_consistency_rule`s +
    tree definitions. The system-check layer already lints codified config at CI time.
  - Existing audit tooling he may not have found: `audit_hotel_config`, `compare_hotels`
    management commands, and services `hotel_config_health.py`, `hotel_fleet_audit.py`,
    `hotel_comparison.py` in rules_based_configuration/services/.
  - **Gaps he'll hit:**
    1. ESA / Four Seasons / Drury have no cohort providers or tree definitions yet —
       `MSA_HOTEL_PROVIDERS` only has Wyndham Connect GMS. These are portfolios rather than
       MSAs, so either add portfolio-based cohort providers or extend the attributes model.
    2. His headline example — "canonical set of notif message templates for Four Seasons" —
       is *entity-shaped* data (template rows), not scalar `hotel.<attr>` settings. The
       system's "one setting value per hotel" constraint means templates don't fit today;
       that's the unbuilt "Refactor Named configurations" section of the design doc. This is
       the biggest scope question for his block plan.
    3. `apply_portfolio_settings` applies via raw `setattr` + `save()` — bypasses
       service-layer side effects, so settings whose changes require side effects (template
       creation, PMS re-sync, etc.) need care.

  ### Draft Slack reply (for Gareth to edit/post — not sent)

  > Answers, roughly in order:
  >
  > 1. *Portfolio vs Salesforce* — they're doing different jobs. Group membership is
  > attribute-based and Salesforce-derived (brand/parent brand/mgmt co/MSA, cached on
  > `StoredHotelAttributes`); the config trees are keyed off those attributes. The
  > `Portfolio` model in `apply_portfolio_settings` is just cohort enumeration — expected
  > values resolve the same way in both paths. So yes, both are in use, but the logical
  > groups (SF-derived) are canonical; Portfolio rows are a convenience that should converge
  > on the same cohorts. The `/rollout` page is a separate onboarding system (staged
  > go-live batches), not settings conformity — unfortunate naming overlap with "recipes."
  >
  > 2. *cron_detect_drift* — correct, it's not scheduled in prod yet (I checked: no CronJob
  > exists for it). It's ready — dry-run by default, `--commit` persists, first run
  > baselines so there's no alert flood. Turning it on is an infra CronJob + a monitor on
  > `detect_drift.new_drift`. And yes: detection only, no auto-fix by design. Your flow is
  > exactly the intended one — recipe change in code → PR/CI → `apply_portfolio_settings`
  > (dry-run, then commit) → drift detector flags anything missed or mutated later.
  >
  > 3. *configuration_consistency_rule* — yes, start hooking in for new cross-setting
  > invariants. It's enforced at CI time (system check over all tree combinations) and as
  > warn-only on admin saves; it doesn't block writes yet, so keep hard enforcement in
  > `.clean()` for now. And good catch on `payment_gateway_required_for_tokenization` —
  > `hotel.payment_gateway_config_id` doesn't exist (it's `hotel.payment_gateway`), so that
  > rule is broken as written. I'll get it fixed.
  >
  > One flag for your planning: your notif-template example is entity-shaped data, not a
  > scalar `hotel.<attr>` setting — the current system only covers scalars ("one setting
  > value per hotel"). Template/named-config packages are the unbuilt part of the design
  > doc, so worth scoping that explicitly for your block. Also ESA/Four Seasons/Drury need
  > cohort providers + tree definitions added (`MSA_HOTEL_PROVIDERS` only has Wyndham
  > Connect GMS today). Happy to pair on the first tree definition.

  ### Loose ends (user's call)

  - The broken `payment_gateway_required_for_tokenization` rule is a real bug worth a small
    fix PR (key doesn't resolve → rule dead/misfiring).
  - Tincho was pinged in-thread for the cron_detect_drift answer — the draft above covers
    it, so coordinate to avoid double-answering.
  - Asher was asked to share the visualization doc; not chased.

  ## Agent run 2026-08-05T21:35:00+03:00

  Re-read the thread; three replies landed since the first draft, which is now superseded:

  - Asher shared the visualization doc: https://pages.cnry.cloud/rules-based-config/
    (thread msg https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1785951662817529)
  - Martin (Tincho) fully answered Q2 (https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1785952940825859):
    cron_detect_drift is not scheduled — cron PR awaiting approval; he triggers manually
    while testing (dry-run in shell, or from Django admin which commits); read-only by
    design; remediation stays `apply_portfolio_settings`.
  - Martin on Q1 (https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1785953019997849):
    both paths read the same rules config, differ only in cohort selection; **convergence
    explicitly deferred to Gareth as a roadmap call**.
  - Martin on Q3 (https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1785954022775379):
    consistency rules are not part of drift detection — they run on config save + CI/system
    check; fix the key references first. (Accurate per my code read; the save-path check is
    warn-only, worth adding.)

  ### Recrafted draft Slack reply (for Gareth to edit/post — not sent)

  > Thanks Tincho and Asher — that covers the drift cron and the visualization. Filling in
  > the parts left to me:
  >
  > 1. *Roadmap call on Portfolio vs Salesforce* — Tincho's description is right: same
  > rules config, different cohort pickers. Direction-wise, the Salesforce-derived
  > attributes (cached on `StoredHotelAttributes`) are canonical for group membership —
  > the trees are keyed off them. The `Portfolio` model in `apply_portfolio_settings` is
  > just enumeration convenience, and I want the two to converge on attribute-defined
  > cohorts rather than maintaining both. So plan against the attributes/groups model;
  > don't build anything new on Portfolio-based enumeration. Also note the `/rollout` page
  > is a separate onboarding system (staged go-live batches) — unfortunate "recipes"
  > naming overlap with what you're planning.
  >
  > 2. *Should you hook into `configuration_consistency_rule` yet* — yes, for new
  > cross-setting invariants. One nuance on top of Tincho's answer: it enforces at CI time
  > (system check over all tree combinations), but the config-save path is **warn-only** —
  > it doesn't block writes yet. So keep hard enforcement in `.clean()`/`.save()` for
  > anything that must never be violated, and treat the rules as the linter layer until we
  > add a blocking mode. Good catch on `payment_gateway_required_for_tokenization` — the
  > key should be `hotel.payment_gateway`, not `hotel.payment_gateway_config_id`; we'll
  > fix that.
  >
  > 3. Two flags for your block planning:
  > • ESA / Four Seasons / Drury have no cohort providers or tree definitions yet
  > (`MSA_HOTEL_PROVIDERS` only has Wyndham Connect GMS) — and as portfolios rather than
  > MSAs they may need a portfolio-shaped provider, which dovetails with the convergence
  > point above.
  > • Your notif-template example is entity-shaped data (rows), not a scalar
  > `hotel.<attr>` setting — the current system only handles scalars ("one setting value
  > per hotel"). Template/named-config packages are the unbuilt "named configurations"
  > part of the design doc, so scope that explicitly. Relatedly, `apply_portfolio_settings`
  > applies via raw setattr+save, so settings needing side effects (template creation,
  > PMS re-sync) aren't covered today.
  >
  > Happy to pair on the first tree definition for one of your brands.

  ### Remaining loose ends

  - Fix PR for the broken consistency rule key (I offered "we'll fix that" in the draft).
  - Tincho's cron PR is awaiting approval — possibly yours; worth finding and reviewing it.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Succinct answers for Joshua's questions, as well as a quick analysis of his
  problem domaina nd appropriate mechanisms
updated: 2026-08-05 22:01:58.824363
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1785950349523259