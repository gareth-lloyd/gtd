---
area: null
contexts: []
created: 2026-05-20 13:34:09.320491
defer_until: null
due: null
energy: low
id: 2026-05-20T1334-understsand-this-pr
order: -23
output: "## Agent run 2026-05-20T13:45:00\n\n**PR #45841** — \"PMS-8437: swap OHIP
  onboarding from proxy hardcode to vgs_proxy_config_slug\"\nAuthor: Drew Delianides
  | Branch: drew/pms-8437-canary-ohip-slug-swap → master\n9 files, +276/-19, currently
  OPEN.\n\n### What it does (one-liner)\nMigrates BW + Wyndham OHIP onboarding away
  from writing the legacy\n`OhipConfiguration.proxy=\"vgs-production\"` string, to
  instead populating\n`Account.vgs_proxy_config` (an FK) via a new `vgs_proxy_config_slug=\"production\"`\nkwarg
  on the gateway create/update account call.\n\n### Phase context\n- **Phase 1** (PR
  #45810, already merged): added the `vgs_proxy_config_slug`\n  field on the gateway's
  `CreateAccountRequest` / `UpdateAccountRequest` plus\n  the resolver that turns
  the slug into an FK.\n- **Phase 2** (this PR): wire canary onboarding to actually
  send the slug.\n- **Phase 3** (separate branch `drew/pms-8437-deprecate-ohip`):
  remove\n  `OhipConfiguration.proxy` and the `OracleOhip.proxy` column. Gated on
  a\n  backfill check and one real onboarding cycle exercising the new path.\n\n###
  Plumbing\n`PmsIntegrationConfig.vgs_proxy_config_slug` (new optional field, default
  None)\n  → `PMSGatewayService.get_or_create_account` / `update_account` kwarg\n
  \ → existing `CreateAccountRequest` / `UpdateAccountRequest` field\n  → gateway
  resolves slug to `vgs_proxy_config` FK.\n\n### Who sets the slug\n- BW provider:
  `VGSProxyConfigSlug.PRODUCTION` only when `vendor == Vendor.ORACLE_OHIP`\n- Wyndham
  provider: `VGSProxyConfigSlug.PRODUCTION` only when `vendor == Vendor.OPERA`\n  (the
  IDS_NEXT and SYNXIS branches stay None).\n- IHG: untouched (no OHIP integration).\n-
  All other providers default to None — leaves existing gateway value alone.\n\nLegacy
  `proxy=\"vgs-production\"` strings are removed from both BW and Wyndham\nOHIP config
  builders in the same PR.\n\n### Deploy-safety story\nField defaults to None at every
  layer (canary config dataclass, gateway service\nkwargs, request dataclass, gateway
  marshmallow schema `allow_none=True`).\n- Old canary → new gateway: kwarg just defaults
  to None, fine.\n- New canary → old gateway (mid-deploy lag): slug not on the wire,
  fine.\n- No DB migrations.\n\n### Files touched (9)\n- `onboarding/configuration_providers/best_western/pms_config_provider.py`
  — set slug for ORACLE_OHIP; drop legacy `proxy=`\n- `onboarding/configuration_providers/wyndham/wyndham_pms_config_provider.py`
  — same pattern for OPERA branch\n- `onboarding/configuration_providers/configs/pms_integration.py`
  — add `vgs_proxy_config_slug: str | None = None`\n- `onboarding/plans/configure_pms_integration_create_configuration_plan.py`
  — forward slug to both create/update calls\n- `pms_gateway/services/pms_gateway.py`
  — new `vgs_proxy_config_slug` kwarg on `get_or_create_account` + `update_account`\n-
  4 test files — new asserts that slug is forwarded; legacy `proxy` field is None
  on OHIP configs\n\n### Risk read\nLow. The new field is purely additive and defaults
  to None everywhere. Old\n`OhipConfiguration.proxy` column still exists and still
  gets written to by\nthe gateway-side resolver (until Phase 3). Behavior on rollback
  is identical.\nReviewer should mostly sanity-check that:\n1. BW + Wyndham OHIP are
  the only providers that set the slug (true — IHG\n   wasn't touched because no OHIP
  there).\n2. The slug only fires on the right vendor branch in each provider (it
  does —\n   guarded on `Vendor.ORACLE_OHIP` and `Vendor.OPERA`).\n3. The post-deploy
  backfill check is real: `Account.objects.filter(type=\"oracle_ohip\", vgs_proxy_config__isnull=True).count()
  == 0` before Phase 3 ships.\n\n### Why Drew tagged you / why this is in inbox\nLikely
  just for awareness — there's no review request from you on this PR;\nit's a Drew/PMS
  area change. The event link\n(#event-25731181843) is the PR event timeline, not
  a specific comment thread\npointing at you. Probably worth a skim and clear unless
  you want to weigh in\non the Phase 3 plan.\n"
project: null
source_id: null
tags: []
time_minutes: 5
title: Understsand this PR
updated: 2026-05-20 14:29:43.898675
waiting_on: null
waiting_since: null
working_on: false
---

https://github.com/canary-technologies-corp/canary/pull/45841#event-25731181843