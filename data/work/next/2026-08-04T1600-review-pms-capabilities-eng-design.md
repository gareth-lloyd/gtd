---
area: null
completed_at: null
contexts:
- deep
created: 2026-08-04 16:00:16.245615
defer_until: 2026-08-17 09:00:00
due: null
energy: high
id: 2026-08-04T1600-review-pms-capabilities-eng-design
order: 7
output: |
  ## Agent run 2026-08-04T16:00

  In-depth review of the doc (read 100%) with 4-agent code verification against the canary repo.

  ### The concrete proposals
  1. Engine extensions: pms + capabilities_all/absent predicate dimensions, live HotelAttributes dims, fallback root (iterated last), parent-based child registration, derived enterprise_parent_brand_ids() exclusion, derived managed-field set, key-aware tie-breaking + boot guard (D2).
  2. Non-enterprise tree: root defines nothing; 9 capability groups (weight 20) + CloudBeds vendor group (weight 30); all FREE; expected value total = override -> derived -> Django default (D18); the 17 v1 fields.
  3. Writer (materialize) inside sync_gateway_state: strict healing (D1), ConsistencyService validation, exactly one attributed event per write with write_reason (D21); kill switch = rollout flag stops writer, drift keeps watching.
  4. Overrides: set_override sole write path; admin edits auto-create override rows via per-field reason confirmation page (D4); FINAL rejected.
  5. Observation history gates activation; latest occurred_at is the override boundary (D3/D6/D19/D20); PMS migration supersedes manual config wholesale.
  6. Drift generalization: NON_ENTERPRISE_ACTIVATED (heal+alert, deliberately ignores rollout flag) + NON_ENTERPRISE_LEGACY (report-only, drives Phase B). Enterprise unchanged (FINAL-only, no writer).
  7. Model move into rules_based_configuration; retire GLOBAL_CONFIG_DEFAULTS/CAPABILITY_DEFAULT_RULES/PMS_CONFIG_OVERRIDES/DEFAULTS_VERSION; retire webhook + gateway crons after Kafka parallel run.
  8. ChangeTracker attribution extension as writer prerequisite.

  ### Doc vs code — what checks out
  Remarkably accurate: 17 fields exist w/ claimed defaults; Capability enum exactly 64; SUPPORTED_VENDORS={CLOUDBEDS}; PRODUCT_FLAG_BY_MODEL exists; override/observation models merged w/ append-only + canonical-JSON clean() (pms_gateway/capability_driven_config/models.py:71,188); drift V1 exactly as described (drift.py:138 final_only=True, cron merged 2026-07-30, single Wyndham cohort); enterprise trees confirmed incl. BW narrow root. The two claims justifying the hardest engine work are real constraints: _get_tree_during_setup (conformity.py:686) raises on >1 overlapping root (so parent-based registration is required), and drift is hardwired to MSA (so cohort generalization is new).

  ### Material divergences
  1. sync_gateway_state + T6 producer + real T7 consumer are NOWHERE in the repo (no branch/PR found) despite "implemented and in review". Writer's host doesn't exist; Lane 1 is the critical path.
  2. ChangeTracker risk overstated: contextvar attribution already exists (request_context_middleware.py: change_source_context, user_context; source="other" fallback confirmed). Only new: RULES_WRITER enum value + write_reason plumbing.
  3. pms_payment_slot_identifier is NOT in check_in CONFIG_FIELDS -> ChangeTracker emits nothing for it; breaks D21 unless added. Also the only field defaulting to None.
  4. Nullable booleans (passport/dob/nationality: null=True, default=False): NULL != False means noisy legacy drift reports + writer flipping NULLs.
  5. "Existing dotted-path mapping utility" doesn't exist as a utility — duplicated across 5 sites; consolidation is unlisted work.
  6. Key-aware weights partially exist already (per-setting weights in Wyndham config); D2's delta is only the disjoint-key allowance + boot guard. CannotBreakTiesError is dead code; real error is InvalidConformityTreeError.
  7. Fallback root fights TWO guards: register_root mutual-exclusivity (doc acknowledges) AND GroupAttributes.__post_init__ rejecting empty predicates (doc doesn't).
  8. pms-auto-config flag doesn't exist; PMS_CAPABILITY_DRIVEN_CONFIG already generated in Features (no call sites) — T10 partially done.
  9. try_fetch_hotel_attributes doesn't exist; the fetch has a write side effect (creates row, calls Salesforce).
  10. ConsistencyService has exactly 2 rules (check_in only) — thin validation net. D4 has no save_model-level confirmation precedent; sketch's ValidationError in save_model would 500.

  ### Assessment of my three critique points (refined)
  1. Weight-collision relaxation: objection targets the wrong delta — differing weights on overlapping keys is the EXISTING engine mechanism, not new. D2's delta (disjoint-key weight sharing) can't cause precedence surprises; real cost is the invariant becoming non-locally-checkable (reviewer trusts the boot guard). "Explain" tooling largely exists (config visibility/comparison views, tree viewer). But D2 is recorded as settled — flag at sync if it needs adjudication.
  2. Fallback root vs enterprise carve-out: STANDS. enterprise_parent_brand_ids() is derived from registered roots so cannot exclude a brand with no root; only defense is the placeholder-root convention (process, not code). Plus BrandId silent-None loophole: unknown brand -> parent_brand_id None -> most permissive branch. Ask for: alert/refuse stamping on activation of any hotel with a non-None parent_brand_id outside the derived set; make placeholder-root a checked gate.
  3. Write precedence: doc DOES specify it for v1 (override -> derived -> default; boundary dormancy D3; overrides enforced by healing D17; enterprise partitioned; drift never writes). The real gap is the merged-system endgame: enterprise write precedence (scripts vs future drift-writes vs override table) is explicitly punted — and that is exactly the sync question Asher aimed at me. Reframe as: "v1 internal precedence is well-specified; the write-precedence contract for the enterprise half must be designed before enterprise writes exist."

  Doc: https://app.notion.com/p/canarytechnologies/Capability-Driven-Config-Drift-Detection-3b18146861518073a23dd5241ddc8b6b

  ## Agent run 2026-08-05T13:45

  Follow-up pass covering what the first run didn't: the sync doc, the Slack thread, and verification of the Lane-1 "in review" claim against Linear/GitHub.

  ### Sync doc (read in full + both comment threads)
  https://app.notion.com/p/canarytechnologies/Sync-on-PMS-capabilities-driven-configuration-3ac8146861518007b0f8e4fd9d5c416e
  - Resolved: 1 system not 2; columns stay authoritative (no reader migration); non-enterprise only (enterprise keeps scripts, revisit later); keeping Kafka/observation pipeline, HotelConfigFieldOverride, capability predicates, admin layer-provenance improvements; reusing tree-based rule resolution from drift detection.
  - BOTH standing critique points are explicit open "Q:"s in the doc — they ARE up for adjudication, not settled:
    1. D2 weight relaxation: doc asks whether raising an error only when two nodes share config keys AND weights (allowing disjoint keys / differing per-key weights) eliminates the z-index problem. Prior-run refined position applies: the delta itself is safe; the cost is the invariant becoming boot-guard-checked rather than locally readable.
    2. Fallback root: doc asks "This will catch any enterprise brands not in the tree already. Is that okay?" Answer prepared in prior run: No — enterprise_parent_brand_ids() is derived from registered roots so can't exclude a brand with no root; ask for alert/refuse-stamping on activation of any hotel with non-None parent_brand_id outside the derived set, placeholder-root as a checked gate, and note the BrandId silent-None loophole.
  - Question aimed directly at Gareth: "when will drift-detection writes be implemented?" — Asher wants to collaborate or take the lead; ownership to be decided in block planning.
  - Open Q: is CloudBeds the right first target? (data: https://pages.cnry.cloud/pms-setup-automation-numbers). A comment (likely from Gareth) asked to add this question.
  - Misc/process: Asher raises the approve→reject→approve→reject churn (Ian, then Gareth, after dev started); floats an eng channel for design-doc executive summaries. Julius(?) commented "This was a miss on my part. I should have recommended a reviewer higher up the chain."
  - Next steps recorded: in-depth eng-design review by Gareth(?) + Enterprise team; block planning decides ownership; project channel; Asher to compare capabilities across PMSes + check non-check-in/booking capability support; PMS Platform (Juan) owns config/capability targeting accuracy; work with product teams per config.

  ### Lane 1 "implemented and in review" — verified, still not visible anywhere
  - TOOL-425 (T6 gateway producer) and TOOL-426 (T7 consumer + sync_gateway_state) are both In Progress since 2026-07-21, assigned to Asher, ZERO PR attachments (https://linear.app/canary-technologies/issue/TOOL-425, https://linear.app/canary-technologies/issue/TOOL-426).
  - Asher has zero open PRs in the canary repo; no branch matches tool-425/426 or pms-account-changed. Only T3 landed: PR #50591 (https://github.com/canary-technologies-corp/canary/pull/50591) + #50588 (https://github.com/canary-technologies-corp/canary/pull/50588), Kafka schemas/plumbing, merged 2026-07-21.
  - Yet both ticket descriptions contain "(review finding, fixed)" annotations — a review happened somewhere invisible (local/AI/unpushed). Worth asking Asher directly where the T6/T7 code lives; it is the writer's host and the critical path.
  - TOOL-425/426 descriptions are extremely detailed and largely consistent with the design doc (producer hook placement, partition key = hotel_uuid, observe-service idempotency, enabled_at gating, cron-heals-lost-events). No new divergences spotted from the ticket text.
  - Related context: Julius has open prototype PR #50352 "Prototype: per-account capability overrides" (https://github.com/canary-technologies-corp/canary/pull/50352) — a gateway-side take on overrides, worth reconciling with the canary-side HotelConfigFieldOverride design.

  ### Main doc edited after the first review
  Last edit 2026-08-04T20:51Z (prior run read it ~15:00Z). No comment threads on the doc. Couldn't diff the exact change; the visible lane structure now maps 1:1 to Linear tickets (TOOL-425/426/430/433 "in progress"/reworked), so the edit looks like lane/ticket restructuring, not a substantive design change. Note the doc still says T6/T7 "implemented and in review" while the tickets say only "in progress".

  ### Slack thread — no substantive discussion
  https://canarytechnologies.slack.com/archives/C0AMJPBUH60/p1785803212077869
  Just the doc-share (meeting prep for the Aug 5 sync), cc's, Julius reporting the first link was private, and Asher fixing permissions (noting the "engineering" Notion group is stale at 37 people).

  ### Suggested talking points for the sync (not sent anywhere)
  1. Answer Asher's writes-timing question: reframe per prior run — v1 internal precedence is well-specified; the enterprise-half write-precedence contract must be designed before enterprise writes exist; decide ownership in block planning.
  2. Concede D2 relaxation with the boot-guard caveat; hold firm on fallback-root guards (concrete asks above).
  3. Ask where T6/T7 code actually lives — nothing is pushed, and the doc's "in review" claim is unverifiable.
  4. Raise the prior run's unclaimed divergences that affect the writer: pms_payment_slot_identifier missing from check_in CONFIG_FIELDS (breaks D21), nullable booleans (NULL vs False drift noise), GroupAttributes.__post_init__ rejecting empty predicates (second fallback-root guard).
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 30
title: Review PMS capabilities eng design
updated: 2026-08-13 15:24:20.135872
waiting_on: null
waiting_since: null
working_on: false
---

Asher's superseding eng design for TOOL-294: capability-driven config inside rules_based_configuration (fallback root, strict-healing writer in sync_gateway_state, override rows, two-tier drift). CloudBeds v1.

Doc: https://app.notion.com/p/canarytechnologies/Capability-Driven-Config-Drift-Detection-3b18146861518073a23dd5241ddc8b6b
Sync doc: https://app.notion.com/p/3ac8146861518007b0f8e4fd9d5c416e
Slack thread: https://canarytechnologies.slack.com/archives/C0AMJPBUH60/p1785803212077869?thread_ts=1785803212.077869&cid=C0AMJPBUH60