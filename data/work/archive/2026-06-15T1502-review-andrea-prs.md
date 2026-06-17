---
area: null
contexts: []
created: 2026-06-15 15:02:51.711614
defer_until: null
due: null
energy: low
id: 2026-06-15T1502-review-andrea-prs
order: null
output: "## Agent run 2026-06-16T10:50Z — Review of Andrea's ENT-6490 PRs\n\nSlack
  ask (Andrea Bradshaw, #C0B1MN8F869, https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1781294771548779):\ntwo
  PRs for ENT-6490 (https://linear.app/canary-technologies/issue/ENT-6490),\nwants
  review — specifically any concerns about cleaning up inactive PMS vendors.\n\n-
  PR #47885 (https://github.com/canary-technologies-corp/canary/pull/47885) — base:
  enum + migration. **Already MERGED.** Nothing to review.\n- PR #47878 (https://github.com/canary-technologies-corp/canary/pull/47878)
  — the real review target. **OPEN**, 377 LOC. New `ConfigurePMSIntegrationCleanupForeignVendorsPlan`
  wired into IHG flow before CREATE.\n\n### Context\nIHG pilot batches fail \"Validate
  PMS Config\" with `pms_mixed_vendors`: the IHG provider only emits a HotelKey\nconfig,
  but the property already had a previous vendor (Opera/Autoclerk) on its Gateway
  account. The new plan\ninserts a CLEANUP stage (BASE → CLEANUP_FOREIGN_PMS_VENDORS
  → CREATE → VALIDATE → GOLIVE) that removes leftover\nforeign vendors. Orphaned leftovers
  (no enabled config) → cleaned; live leftovers (enabled config) → blocked with\n`pms_live_previous_vendor`
  for a manual PMS switch.\n\n### \U0001F534 BLOCKING — stale stack, needs rebase
  before merge\n#47878 has NOT been rebased since base #47885 merged to master (verified:
  branch head 9a587f8 does not contain\nmerge commit a8e31d38f43). It still carries
  the base's now-duplicate changes:\n  - The `CLEANUP_FOREIGN_PMS_VENDORS` enum line
  in `onboarding_script_batch.py` — already on master → merge conflict.\n  - Migration
  `0150_alter_onboardingscriptbatch_script_type.py` (deps on 0149). Master now has
  a DIFFERENT\n    `0150_alter_onboardingvalue_kind.py` (also deps on 0149), plus
  `0151_...` and `0152_alter_onboardingscriptbatch_script_type.py`\n    (the base
  PR's actual merged migration). So #47878's 0150 is a colliding migration number
  + sibling leaf node —\n    `makemigrations --check` / multiple-leaf-node failure
  in the onboarding app.\n  → Action for Andrea: rebase onto master and DROP both
  the enum line and the 0150 migration; they already landed via #47885.\n    The new
  plan/exception/flow-wiring/tests are the only things that should remain.\n\n###
  ✅ Core logic verified sound (re: her specific question on cleaning up inactive vendors)\n
  \ - `getattr(account, vendor.value)` config detection is consistent: every config-bearing
  `Vendor` value maps\n    exactly to an `Account` dataclass attr (hotelkey, opera,
  oracle_ohip, stay_n_touch, skytouch, synxis_crs, …\n    all cross-checked). No attribute-name
  mismatch that would silently miss a live vendor.\n  - 404 handling follows the existing
  convention in `configure_pms_integration_validate_plan.py` (HTTPStatus.NOT_FOUND,\n
  \   re-raises non-404). Network layer raises `requests.HTTPError`. Correct.\n  -
  `get_account(hotel)` called without use_cache → fetches fresh (default False) —
  right, avoids stale post-cleanup state.\n  - **Key de-risker:** `cleanup_rooms_and_account_validations`
  POSTs `/api/accounts/me/{vendor}/cleanup` — it clears\n    only rooms/room_types/blocks/validations,
  NOT the vendor's config/credentials row. So even a misclassified\n    \"orphaned\"
  vendor is NOT catastrophically destroyed; the integration config persists and room
  data re-fetches.\n    This substantially answers her \"any concerns about cleaning
  up inactive vendors\" worry — the blast radius is bounded.\n  - Live vendors (enabled
  config) are blocked, not cleaned; orphaned ones still cleaned even when another
  blocks\n    (loop continues, raises after). Idempotent / re-runnable as described.
  Good test coverage (8 plan tests).\n  - Nice new guard: `test_ihg_pilot_sequential_stage_children_have_labels`
  prevents the SCRIPT_TYPE_LABELS KeyError.\n\n### \U0001F7E1 Design points worth
  raising (non-blocking — these ARE the \"inactive vendor cleanup\" concern)\n  1.
  The \"foreign\" set spans the ENTIRE `Vendor` enum, not just primary PMS vendors.
  Auxiliary/secondary configs\n     (e.g. `canary_openapi`, `agora`) that legitimately
  coexist with a primary PMS would be treated as foreign —\n     cleaned if disabled,
  blocked if enabled. Harmless for the IHG-only wiring today (won't be present), but
  it's a\n     latent assumption if this plan is ever reused for a flow where a hotel
  runs a secondary integration alongside\n     its PMS. Consider scoping the allowlist
  beyond just the SYNXIS pair, or a comment documenting the assumption.\n  2. \"Orphaned\"
  = config absent OR `is_enabled=False`. A previous PMS paused/disabled mid-migration
  (config present\n     but disabled) is treated as safe-to-clean. Fine given cleanup
  spares credentials and validate would fail anyway,\n     but worth making the \"disabled
  config is intentionally cleaned\" decision explicit (the docstring implies it).\n\n###
  Verdict\nApprove the approach and implementation of #47878 — logic is correct, well-tested,
  follows conventions, and the\ncleanup blast radius is appropriately bounded (no
  credential deletion, live vendors blocked). The one true blocker\nis mechanical:
  rebase on master and drop the duplicate enum + migration that #47885 already merged.
  Optionally\naddress design point #1 (enum-wide foreign set) with a comment or tighter
  allowlist.\n\nNOTE: No comments posted to GitHub/Slack/Linear — review recorded
  here only, pending your call on how to deliver it.\n"
project: null
source_id: null
tags: []
time_minutes: 5
title: REVIEW Andrea PRs
updated: 2026-06-16 15:44:30.503685
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1781294771548779