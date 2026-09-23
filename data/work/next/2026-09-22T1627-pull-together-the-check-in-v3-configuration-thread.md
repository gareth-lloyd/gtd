---
area: null
completed_at: null
contexts:
- deep
created: 2026-09-22 16:27:43.984283
defer_until: null
due: 2026-09-23
energy: high
id: 2026-09-22T1627-pull-together-the-check-in-v3-configuration-thread
order: null
output: ''
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 90
title: Pull together the check-in v3 configuration threads and propose country-based
  (general) rules
updated: 2026-09-23 09:29:05.323681
waiting_on: null
waiting_since: null
working_on: false
---

Captured 2026-09-22 from a Slack/Linear/code sweep on rules-based configuration for check-in v3. Companion to the existing item on the 2026-08-11 V3 migration/ownership call (gaps #1-#6).

## The ask for this item

Pull the threads below into one proposal for **country-based (general) rules for check-in configuration**, and decide where it lands: Enterprise mechanism + legal-owned rule contents, or folded into A&D's v3 configurator. Bring it to Andrea, Lea, Dana, Vibhor, Marta.

## State of play: how A&D is rolling out v3

- **Migration, not configuration, is the mechanism.** Guido's `guest_experience/services/v3_migration.py` derives the v3 Flow from Configuration + RegistrationCard + Incode + has_addons, then flips `checkin_version=v3` and `rollout_check_in_v2_level=stable`. Routing is client-side on that field. Reg card is consumed verbatim as one step's JSON.
- **Rollout by wave, run by Guido.** 2026-08-11 call agreed: migrate 100-200, flip model default to v3, migrate the rest. Andrea offered the Enterprise rollout framework and withdrew it as overkill. As of 2026-09-17 Guido had migrated 153 hotels that week incl. 50 Wyndham (on top of 28 earlier). Additional guests entered the wave model 2026-09-02 (AD-8332), so Wave 2 non-NA hotels are in scope.
- **Lea's workstream is the configurator, not the rollout.** Facade over existing check-in config, single read/write interface, no data-model change. Product told A&D in June not to touch flow generation. Lea's pipeline: `onboarding/rules -> populate config -> flow_generation consumes persisted config`. Figma thread 2026-08-11/12 (David Champeil, Lea, Vibhor) settled: platform-shared settings live in central config, per-step settings on the step. Conditional logic inside the flow (ID types by nationality) explicitly kept out: "without having to design the whole rules engine thing". Vibhor has no model yet for conditional alternate steps across platforms.
- **Sync is push + pull.** Signals re-derive the flow; `reconcile_hotel_v3_flow` exists for drift but nothing schedules it. AD-8324 (Guido, backlog) covers a neighbouring drift case.

## Rules-based configuration: where it entered and where it landed

- 2026-05-15/19: gave Lea `rules_based_configuration` as current thinking, plus the compliance doc and a Loom. Lea shared the v3 configuration problem statement and the RBC PRD.
- 2026-06-30/07-01 (group DM with Andrea + Lea, C0B4QD01GP8): Lea asked whether FINAL/FREE locking is enforced in Django admin so the configurator can't let CS bypass enterprise constraints. Answer: not today. Posted "Enterprise-aware Django admin: lock rules-controlled Hotel fields read-only". **Agreed outcome:** enforcement of locked fields is a future Enterprise roadmap item; no UI restrictions needed in the configurator now. Lea also asked whether the rules consistency-check could block invalid combinations; left as prioritisation.
- 2026-07-01: stated the principle that onboarding calls a pod-owned config service with typed intent, never hand-writes pod-owned fields. Lea: A&D has no such service; Vibhor's PRD assumed the opposite. Lea agreed with the shape, suggested LOCKED/FREE arrive as args.

## Dana's pushback

- May (migration thread, C04STT7UPRQ): asked for a migration *service* with an API boundary rather than a management command, so Enterprise scripts call it on the client's schedule. Dana agreed to add one before migrating beyond the first few. Service exists; the command still drives it.
- 2026-08-06/07 (six-person DM, C0BNGM6R3UJ): restated the ask as an intent-based check-in configuration service. Dana: "Why would you guys be taking a hotel to v3? Our plan is to run the migration to v3, just like we did with v2." Dana wants config/reg-card changes to auto-update the v3 flow; will build v2->v3 migration service for Enterprise to call for Wyndham/BW/IHG.
- 2026-08-11 call: A&D owns migration; Enterprise informed on timing. Stephanie relayed my scripting-ownership position and Vibhor accepted it. Dana named two cases to cover (net-new hotels; existing customers newly enabled) with "we will coordinate" and no owner.
- **Dana's frame never engaged with the compliance question.** It is about who runs the migration, not what configuration a v3 hotel is allowed to have per country. A&D's derivation takes Configuration on trust.

## The compliance doc (the path to country-based rules)

https://app.notion.com/p/canarytechnologies/Enforcing-compliance-with-rules-based-configuration-36581468615181359f2bce159fa804cc

- Proposes **general rules**: brand-agnostic legal floor, scoped by country/region only, declared once via existing type-safe `.define()` with `OverridePolicy.FINAL`, plus a Django startup check (E002) that walks every brand tree and fails boot on a conflicting resolved value.
- Names the gap: FINAL is intra-tree and trees are brand-scoped. Wyndham's GDPR no-ID rules lock id_step / additional_guests_* only inside the Wyndham tree; IHG/BW aren't forced to match; independents get nothing.
- Explicitly targets check-in v3: "as flexible as the AD team wants; the startup check guarantees no configuration over- or under-collects against the law." Gives a principled home for Vibhor's ID-type-by-nationality problem without A&D building a rules engine in the flow.
- Doc's own caveat: if v3 makes one ruleset span all portfolios, general rules fold into that resolver.
- Open risks: partial country-set overlap only checked at terminal group; no negative scopes ("EU except X"); recommend keeping WYNDHAM_NO_ID_* as belt-and-braces first rather than moving them.
- **Status: designed, sketched, not started.** Draft PR #45775 open since 2026-05-19, no updates, nothing on master. No Linear ticket. 2026-09-02 Marta Ochowicz posted GDPR country-based default retention design in #epd-emea-engineers and asked if RBC should become the engine for all hotels; I said yes, could build quickly, nothing started.

## Live gaps this proposal should either cover or explicitly defer

1. Onboarding cannot set `checkin_version=v3`: `CheckInConfigurationUpdates` has no field (still true on master 2026-09-17). Dana's 2026-09-10 thread gave new-hotels-on-v3 to Enterprise; Guido supplied the values and said new hotels also need a Flow created. No ticket on either team. Bulk Wyndham migration is already running, so every new Wyndham/BW hotel lands on v2 meanwhile.
2. Existing customers newly enabled on check-in: no v3 path at all.
3. Wyndham `ADDITIONAL_GUEST_STEPS_BY_COUNTRY` is exactly the per-brand duplication general rules would replace; as Wave 2 relaxes the blocker, the bare `V3MigrationBlocked` from pre_save becomes the failure mode on plan re-runs.
4. FINAL enforcement in admin / configurator (agreed roadmap item, unscheduled).

## Key links

- Group DM Andrea/Lea: https://canarytechnologies.slack.com/archives/C0B4QD01GP8
- Six-person DM incl. Dana: https://canarytechnologies.slack.com/archives/C0BNGM6R3UJ
- Figma/configurator thread: https://canarytechnologies.slack.com/archives/C0A5Z7LE5AL/p1786481451916029
- New hotels on v3 thread: https://canarytechnologies.slack.com/archives/C029BPP02H0/p1789058358455499
- Marta GDPR thread: https://canarytechnologies.slack.com/archives/C0AB9E7AE59/p1788330939315209
- Sketch PR: https://github.com/canary-technologies-corp/canary/pull/45775
- Lea's Check-In V3 Configuration doc: https://www.notion.so/canarytechnologies/Check-In-V3-Configuration-365814686151808c805efb429b821412
- Related: ENT-6639 (BW created on v1, fixed June), AD-8324 (flow drift), AD-8332 (Wave 2 in wave model)