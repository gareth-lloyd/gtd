---
area: engineering
contexts: []
created: 2026-07-20 15:36:12.138116
defer_until: null
due: 2026-07-21
energy: medium
id: 2026-07-20T1536-review-this-document
order: null
output: |
  ## Agent run 2026-07-20T16:05

  Read the full Capability-Driven PMS Config TDD (TOOL-294, status REVIEW ME!):
  https://app.notion.com/p/canarytechnologies/Capability-Driven-PMS-Config-39181468615180238a31da976288eb14
  Cross-referenced against `backend/canary/rules_based_configuration/`.

  ### Answer: yes — and it's the strongest use case CONSISTENCY has had

  The doc's "Interaction with rules_based_configuration (MSA/GMS)" section discusses
  **only CONFORMITY** (ConformityService, apply_portfolio_settings, FINAL/FREE policy,
  Salesforce cohorts). It never mentions the CONSISTENCY rule layer
  (`rules_based_configuration/services/consistency.py`, 44 lines, 2 rules today in
  `check_in/configuration_rules/consistency_rules.py`). That's a gap, because the design
  creates exactly the failure mode CONSISTENCY exists to catch.

  **Why the merge needs cross-field validation:**

  1. **The 4-layer merge synthesises combinations nobody authored.** Each field resolves
     independently — `CAPABILITY_DEFAULT_RULES` predicates take only `frozenset[Capability]`
     and know nothing about sibling fields. So `integration_auto_post_to_pms` derives from
     `PRE_CHECKIN` while `..._passport_number` derives from `UPDATE_PASSPORT`. A vendor with
     UpdatePassport but not PreCheckin yields child-True / parent-False. (The doc's own prod
     table shows the parent at 68% and the children at 71% — I could not confirm whether
     that column is capability presence or current column state, so treat as suggestive, not
     proof. The predicates being independent makes it reachable regardless.) This matters:
     `kiosk/services/commit/commit.py:203,231` reads the passport sub-field with no parent
     check. Same shape for `addons.integration_push_purchases_to_charges` vs
     `addons.integration_enabled`.

  2. **Human overrides have no cross-field validation at all.** `HotelConfigFieldOverride.clean()`
     validates one field in isolation (type, choices, JSON round-trip). An IM can override
     the parent toggle off while the children stay derived True. Nothing catches it. The two
     existing CONSISTENCY rules already sit on this exact surface
     (`hotel.check_in_configuration.*`), so the vocabulary matches.

  3. **The design already reaches for a weaker version of this.** Its CI check is "each
     template value runs through the admin forms' `clean()`" — per-field and form-shaped.
     CONSISTENCY's boot-time pattern is the right shape: `ConformityService.finalize()`
     (`services/conformity.py:606-633`) enumerates every reachable setting combination in
     the group DAG and validates each, **raising at `AppConfig.ready()`** so the process
     refuses to start. The merge space here is finite and enumerable the same way —
     SUPPORTED_VENDORS x capability subsets x product flags x floor. Enumerating it in CI
     and running consistency rules would catch a bad constants map before deploy.

  ### Bug in the doc's coexistence rules (worth raising as a comment)

  The doc lists three coexistence rules, both naming only CONFORMITY sites. But **the
  CONSISTENCY evaluation sites read raw columns too** and will produce false warnings on
  active hotels:
    - `rules_based_configuration/signals.py:64` — admin-save warning banners
    - `services/hotel_config_health.py:153-164` — pre-go-live health report
    - `checks.py:7-29` — the Django system check
  Rule 1 ("ConformityService must read effective values via HotelConfig") needs widening to
  the whole framework, not just the conformity path.

  **Also unmentioned: a third parallel system.** `hotels/utils/pms_gateway_config_checks.py`
  (rendered in `hotels/admin/hotel.py:91`) already does config-field x PMS-capability
  coherence checks — literally "this toggle is on but the PMS lacks the capability", with
  remediation text. It reads raw columns via `CheckInConfiguration.objects.get(hotel=hotel)`,
  so it breaks identically on active hotels, and it overlaps conceptually with what
  CAPABILITY_DEFAULT_RULES now derives. Canary would have three cross-field config
  validators after this ships. Worth naming in the doc even if consolidation is out of scope.

  ### Caveats if you propose adopting CONSISTENCY

  - **Key vocabulary differs.** CONSISTENCY rules take a flat dict keyed by dotted paths
    rooted at `hotel.` (`hotel.check_in_configuration.x`); capability_driven_config keys by
    `(ConfigModel, field_name)`. Needs a trivial adapter, but it must be built.
  - **Package boundary.** `rules_based_configuration` is a canary app; the new code lives in
    `pms_gateway/capability_driven_config/`. `consistency.py` is a dependency-free registry,
    so importing it is cheap — or lift it to `backend/shared`. Note the doc's own precedent
    of CI import walls (the SlackService / `internal_support` problem in T15).
  - **Autodiscovery works out of the box**: `apps.py:22` picks up `configuration_rules/` in
    any installed app, so `pms_gateway/configuration_rules/consistency_rules.py` self-registers.
  - **Enforcement mode is a genuine addition.** Today CONSISTENCY is hard-fail only at boot;
    everywhere else it's warn-only, and `signals.py:83-89` swallows exceptions. Blocking a
    bad `set_override()` write is new behavior, not existing behavior.
  - **Boot enumeration won't cover the new rules for free** — it walks the conformity group
    trees only. Extending it to the merge space is the actual work item.

  ### Suggested next step

  Nothing was posted to Notion (no external writes made). If you want to raise it, the two
  comment-worthy items are (a) widen coexistence rule 1 from ConformityService to the whole
  framework incl. the consistency evaluation sites, and (b) consider CONSISTENCY rules +
  boot/CI enumeration as the merge-output invariant check, in place of the weaker
  "template values through admin `clean()`" CI check. Item (a) is a straight correctness
  gap; (b) is a design suggestion.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 15
title: review this document
updated: 2026-07-21 14:52:34.607513
waiting_on: null
waiting_since: null
working_on: true
---

https://app.notion.com/p/canarytechnologies/Capability-Driven-PMS-Config-39181468615180238a31da976288eb14?source=copy_link

Does this provide a potential use case for the rules_based_configuration CONSISTENCY enforcement rules?