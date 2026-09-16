---
area: null
completed_at: null
contexts: []
created: 2026-09-16 09:22:55.134253
defer_until: null
due: null
energy: low
id: 2026-09-16T0922-meeting-with-joshua
order: null
output: |
  ## Agent run 2026-09-16T10:05:00

  ### TL;DR

  SDM's "config linter" is Workstream C of the Q3 Block 2 project *SDM Oncall Efficiency* (https://linear.app/canary-technologies/project/sdm-oncall-efficiency-config-linter-config-cleanup-brand-profiles-eb744cdaff74). Joshua Hart wrote the plan and every ticket; Luiza Manhães (project lead) wrote every PR, with Joshua as reviewer and design partner on each. They deliberately plugged into Enterprise's rules-based configuration engine (warn-only contract, green-lit with Gareth's team 8/5) instead of building their own linter. Four of six tickets are merged; two PRs are open and awaiting review. Milestone "Config linter running with first rule set" is at 75%, target 2026-09-17.

  ### Why (their intention)

  - Roughly 40% of SDM oncall over 6 months was configuration-driven, not code defects (~24% closed with no code fix, ~19% config-change requests). Proposal: https://app.notion.com/p/3ae814686151807884fdc88c83df5240 (not readable via the Notion connector this session; page 404s for the integration).
  - Goal: catch invalid authorization/PMS config combinations where config is edited and at go-live, so misconfigured hotels warn before they generate an outage ticket. Everything is warn-only; no blocking mode is scheduled.
  - Umbrella ticket SDM-4862 (Joshua, In Review): https://linear.app/canary-technologies/issue/SDM-4862. Joshua's 8/27 "plan-vs-reality" check split it into SDM-4989..4993 and reshaped the plan: reconcile with Gareth's stale draft #42860 first; no capability tree exists so "gateway can't do auth-only" becomes a consistency rule plus a separate ask to Enterprise; go-live re-check builds on Enterprise's existing HotelConfigHealthService (#47463) rather than new validation; the surfacing signal must also fire from the AuthorizationConfiguration admin.

  ### What landed on master (merged)

  1. **SDM-4989 — land ENT-5030's rules, rebased** PR #55352 (https://github.com/canary-technologies-corp/canary/pull/55352), merged 2026-09-09. Supersedes Gareth's draft #42860 (https://github.com/canary-technologies-corp/canary/pull/42860). Lands 6 check-in + addons rules and registers AddonsConfiguration in CONFIGURABLE_MODELS. Review dropped the two deposit-slot rules (coupling doesn't exist in code) and re-keyed the tokenization rule onto real settings keys. Confirmed autodiscovery registers rules with zero explicit imports.
  2. **SDM-4992 — surface rules from AuthorizationConfiguration admin + activate 4 dormant checkers** PR #54997 (https://github.com/canary-technologies-corp/canary/pull/54997), merged 2026-09-10. Two engine changes: consistency rules now run for every hotel (not only hotels with a brand conformity tree) and over the full settings-key universe; drift stays tree-only. AuthorizationConfiguration admin saves now trigger checks. The four dormant card-posting capability checkers in hotels/utils/pms_gateway_config_checks.py are live. Fixed the inert tokenization rule.
  3. **SDM-4990 — authorization rules, batch 1** PR #55498 (https://github.com/canary-technologies-corp/canary/pull/55498), merged 2026-09-14. Creates authorization/configuration_rules/ with 3 rules: post_to_pms_flags_consistent (auto-post flags require hotel-level PMS flags), advanced_fraud_flags_in_sync (ID/amount verification require the advanced-fraud gates), deposit_slot_required_for_pms (7 slot-requiring PMSes warn when payment posting is on and both slot sources are empty — the real cause behind the runbook incidents Gareth's deposit-slot rules were guessing at). Ticket's 4th rule ("no live forms in demo mode") deliberately dropped: it is a data-state claim, not a settings claim.
  4. **SDM-4993 — config health check at demo→live flip** PR #55050 (https://github.com/canary-technologies-corp/canary/pull/55050), merged 2026-09-14. The "Set hotel(s) live" admin action runs HotelConfigHealthService after each successful flip; issues render as hotel-named admin warning banners plus a structlog event for Groundcover. Offline (no Salesforce fetch on the request path), never blocks the flip. Direct call from the admin action rather than a new signal (Joshua's review call).

  Master now has 9 autodiscovered consistency rules: 3 addons, 3 check-in, 3 authorization. Surfacing points: Hotel admin save, AuthorizationConfiguration admin save, demo→live admin action. Enterprise's PA-800 (#54914/#54915, Tyler Slateman) separately added a sweep-all-hotels command and structured audit events on the same engine.

  ### Open PRs (awaiting review)

  - **SDM-4991 — charge-only gateway backs an authorization tier** PR #55833 (https://github.com/canary-technologies-corp/canary/pull/55833), open since 2026-09-09, reviewers FannLuo/jwhart91. Fixes NexiConfig.CAPABILITIES (it falsely declared AUTHORIZE_* for years; two Nexi hotels lost the product in Feb, SDM-4174/SDM-4171). Adds a gateway-capability check on the Hotel admin page: tokenize-but-no-hold gateway warns naming the templates that still enable the hold; charge-only gateway warns unless authorization_tier is payment_only. Lives on the admin checker surface, not the rules engine, because rules can't see capabilities or FormTemplate rows. Heads-up: the declaration fix activates two dormant guards for Nexi hotels (FormTemplate.clean blocks hold features; missing_authorizing_vendor logging).
  - **SDM-5039 — declare rule keys + skip on ANY_NON_NULL** PR #56000 (https://github.com/canary-technologies-corp/canary/pull/56000), open since 2026-09-10, reviewers abrad/jwhart91. Ticket filed by Gareth (https://linear.app/canary-technologies/issue/SDM-5039). Rules declare keys=; a new Django system check E002 fails CI on a nonexistent key (pyrefly silently stops enforcing large Literal unions, so static-only didn't work). Tree validation skips rules reading a key valued ANY_NON_NULL. Measured 0 live hotels in any region flagged by the tokenization rule, so the legacy-gateway exemption was resolved by data rather than code.

  ### Asks they've filed to Enterprise

  - ENT-7488 (Luiza, Triage): expose hotel.gateway.capabilities.* and hotel.pms.capabilities.* as settings keys so the SDM-4991 check can move into the rules engine. https://linear.app/canary-technologies/issue/ENT-7488. Notes PMS capabilities are already local (Hotel.pms_capabilities M2M), gateway capabilities are the new half, and both need a derived/computed-key mechanism. Suggests a one-time sweep of vendor CAPABILITIES declarations against implementations.
  - Related Enterprise backlog they lean on: ENT-6097 Part 2 (capability keys), ENT-7113 (scope FINAL rules by region/capability), ENT-7103 (severity/explanation on rule errors — their messages carry full remediation text as a workaround).

  ### Adjacent SDM work feeding the same goal

  - SDM-4866 gatherer PR #54261 (merged 2026-09-03): gather-sdm-authorizations-context investigate gatherer runs the registered config rules for a ticket's hotel (Workstream B, Workup).
  - SDM-4865 (Workstream D, open PRs #56354/#56369): merging the split-brain advanced-fraud flag pair, which the advanced_fraud_flags_in_sync rule currently polices.

  ### Observations for the meeting

  - Joshua's design stance throughout: trace every rule premise to the code path it claims (they removed two of Gareth's original rules on that basis), keep the engine warn-only, prefer direct calls over signals when there's one sender/receiver, and keep capability-dependent checks on the admin checker surface until Enterprise ships capability keys.
  - Things Gareth's team owns that unblock them: review on #56000 (abrad) and a triage decision on ENT-7488; ENT-7103 severity/explanation.
  - The Notion proposal and "Engineering notes — A" toggle were not readable this session; worth opening before the meeting for the nine outage-shaped tickets in §1.2.

  ### What they need from Gareth (checked 2026-09-16)

  1. Review PR #56000 (SDM-5039, Gareth's own ticket). Joshua approved; abrad only commented; jordan-canary also requested. SDM-4862 is marked blocked by SDM-5039, so this is the last gate on the milestone.
  2. Triage ENT-7488 (capability settings keys). Sitting in Enterprise Triage since 2026-09-09; it is ENT-6097 Part 2 (Gareth's ticket, still Todo) plus gateway capabilities. Not blocking them, but SDM-4991's engine-side deliverable waits on it.
  3. Confirm or refute the two deposit-slot rules dropped from ENT-5030 in #55352. Luiza's note: "if Gareth's incident says otherwise, they can return with a code citation."
  4. Workstream E co-build: Four Seasons and ESA brand profiles plus template/named-config packages, offered by Gareth's team 8/5. Milestone at 6%, target date 2026-09-03 already passed.
  5. Review turnaround: SDM-4862 expected slow Enterprise review while the drift project was paused. A named reviewer for SDM PRs touching rules_based_configuration would help.
  Correction to the section above: ENT-7103 (explanation messages) is Done since 2026-09-10 and ENT-7113 is Deployed since 2026-09-14, so neither is an open ask. Whether ENT-7103's explanation field reaches ConfigurationConsistencyError (not just ConfigSpec drift rules) is worth confirming.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Joshua Hart and Luiza Manhães have been working on rules-baed configuration
  consistency checks for SDM
updated: 2026-09-16 14:53:26.210083
waiting_on: null
waiting_since: null
working_on: false
---

Gather their work (PRs and already merged to main) and create a high level overview of their intentions and outcomes.