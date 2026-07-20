---
area: null
contexts: []
created: 2026-07-15 15:19:03.600215
defer_until: null
due: null
energy: low
id: 2026-07-15T1519-find-examples-of-technical-debt-due-to-fixing-shor
order: null
output: |
  ## Agent run 2026-07-15T16:05:00+01:00

  Researched via codebase sweep, git-history sweep, Linear, and Bear notes. Strongest
  examples of tech debt created by short-term fixes for EMEA clients, ranked:

  ### 1. Travelodge (UK) demo — hardcoded creds, auth bypass, "temporary" endpoint (STILL LIVE IN CODE)
  A rushed OHIP demo left: committed demo passwords in git
  (backend/pms-gateway/vendors/integrations/oracle_ohip/views.py:24-119, e.g.
  `_DEMO_PASSWORD = "Tr@v3lodge-Demo!..."`), mirrored Basic-auth headers in
  backend/canary/front_desk/services/front_desk_service.py:240-249 and
  front_desk/services/admission/pms_line_items.py:29-32; gateway secret-key auth
  bypassed for these paths (gateway/middleware/middleware.py:33-37); hardcoded EU
  gateway URL `.../temporary-travelodge-payment-for-demo/...` and hotel slug
  `travelodge-london-central-city-road87`; no rollback safety ("reservation stays
  checked in and needs manual cleanup"). All gated only by
  "TODO: remove after the demo". Security-relevant, worth acting on.

  ### 2. Grecotel (Protel pilot) — densest hotfix/debt cluster, May–Jul 2026
  - Hardcoded Grecotel-only name-override hack from ID scan: commit 54d177ec610
    (AD-7603, PR #44875, self-described "Single-hotel hack" with `remove_after=2026-08-01`),
    fully reverted 12 days later by e489877b233 (PR #45936, -354 lines).
  - Forced-marketing-consent "TEMPORARY" flag keyed to hotel_code 4556: commit
    0c7a341cbb0 (PR #47937, hotfix), removed 10 days later by a761d77b32d
    (PMS-9027 https://linear.app/canary-technologies/issue/PMS-9027, PR #48711).
  - Same-day auto-merged hotfix chain on consent (AD-7850, PRs #48829, #48854).
  - create_guest 60s-budget hotfix (PMS-8654
    https://linear.app/canary-technologies/issue/PMS-8654) whose proper
    generalization is still open backlog (PMS-8700
    https://linear.app/canary-technologies/issue/PMS-8700).
  - AD-7750 (https://linear.app/canary-technologies/issue/AD-7750) literally plans a
    "dirty fix for the immediate case" on add-guest updates with improvements as followup.
  - Ghost guest rows from the urgent PMS-9248 check-in fix needed a separate cleanup
    (PMS-9274 https://linear.app/canary-technologies/issue/PMS-9274).
  - Whole "Grecotel Hardening" Linear project exists to pay down pilot-era debt
    (https://linear.app/canary-technologies/project/fc2b1eba-8a9a-40eb-9f55-88c9f2e4a211).
  - Grecotel-specific signature-step schema baked into check-in (AD-7707, PR #46236).

  ### 3. Booking.com messaging (EMEA-heavy OTA) — polling architecture band-aids
  10-min message age cutoff shorter than the ~20-min poll cycle silently lost messages;
  fix was to bump the magic number to 30 min plus a one-off backfill command
  (CC-2809 https://linear.app/canary-technologies/issue/CC-2809, commit 0bbd6ce84ac,
  PR #49373). Underlying polling fragility remains (poller re-skips the same messages
  forever for disabled-config hotels — CC-2801
  https://linear.app/canary-technologies/issue/CC-2801); real fix is the Push API
  migration project (CC-2832).

  ### 4. Mews (EMEA PMS) — language + payment shortcuts
  - Room-type localization picks the alphabetically-first language
    (`sorted(...)[0][1]`) to unblock the Best Western Mews rollout — wrong for exactly
    the multi-locale European hotels (vendors/integrations/mews/rest/reservations.py:883-898,
    TODO: RES-5228).
  - PCI-Proxy/Datatrans production URL committed with `# TODO: is this a correct
    production url?` above it (mews/client.py:797); env-keyed push URLs + routing keys
    hardcoded in source, justified by "follows existing integrations" — the
    anti-pattern is self-propagating (mews/client.py:60-68).

  ### 5. Opera — "for now" currency assumption in payment push
  Payment amounts pushed with no currency because "there doesn't seem to be an obvious
  way to send the currency to Opera right now"; copy-pasted in two services
  (payment_links/services/payment_link_pms_operations.py:199-203 and
  authform/services/pms_operations.py:865). Wrong-currency postings for any EMEA hotel
  whose Canary and Opera currencies differ.

  ### 6. Regulatory (GDPR) one-offs instead of abstractions
  - onetime_wyndham_disable_id_capture_gdpr.py hardcodes the "GDPR-affected" country
    list — and gets it wrong (includes CL and TH). Every regulatory change becomes
    another one-off script.
  - Shiji right-to-be-forgotten handled via a special "Anonymised"-trigger compensating
    pipeline because PII already written to historical Delta payloads can't be erased
    by a normal re-load (PMS-8705, commit becfc368755, PR #46947).

  ### 7. EMEA check-in v3 rollout pressure
  - OCR compatibility gate deliberately dropped to unblock wave-4 migration
    (EMEA-283, commit 3b227afe821, PR #46001 — tests renamed from "skipped" to
    "migrates_without_blocker").
  - `@isolate` wrapped around ID-form PMS pushes so failures never block the flow —
    swallow-failures band-aid instead of fixing push errors (EMEA-293, PR #47234).
  - Additional-guests resync fix landed behind a feature flag after a revert
    ("Remove locking" → "Revert, adopt the feature flag") (EMEA-295, PR #46521).

  ### 8. Per-PMS special-casing of Italian/Spanish/German PMSes
  - Immobinet (IT): per-integration CSV field override (`Codice esterno` vs interno),
    PMS-7538, PR #40948; Agenzia phone mapping later collided in the same parser
    (EMEA-298, PR #46537).
  - Sihot (DE): capability gaps papered over as silent no-ops/assumptions (guest
    refresh returns guest unchanged; currency assumed when absent) instead of using
    the Capabilities framework.
  - Ulyses (ES): Spanish relation-type translations hardcoded per-PMS via hotfix
    (AD-7829, PR #48082).
  - Market Segment attribute shipped ungated then hidden behind a hand-maintained
    27-entry hardcoded UNSUPPORTED_PMS blocklist (STAY-3501, commit ff8f8d61936,
    PR #48466, "No feature flag").

  ### Cross-cutting observations
  - pms-gateway's own rules say "never special-case a vendor / use Capabilities", yet
    EMEA integrations (Protel, Mews, Sihot, OHIP/Opera) accumulate exactly those
    special cases — the strategic-pilot + oncall-SLA pressure visibly overrides the
    architecture rule.
  - Repeat idioms marking deliberate debt: `remove_after=`, `# TEMPORARY`, `@isolate`,
    auto-merged "[Hotfix]" PRs, and "Hardening" Linear projects created after pilots.
  - Bear notes corroborate the org-level cause: Voice was "not GTM ready for EU…
    Feels like beta testing in EMEA" (Bear: "James saram"); EMEA pod under-resourced
    vs demand, GDPR/localization routing ad hoc (Bear: "Martijn Dekker", "EMEA pod").
  - Adjacent non-EMEA example of the same pattern, if useful for a broader narrative:
    Kalahari r60 stopgap `amadeus/kalahari_hack.py` (PR #49300, "Time-boxed hack").

  Suggested next actions (not taken): (1) ticket the Travelodge demo leftovers —
  committed credentials + auth bypass deserve prompt removal/rotation; (2) if this is
  for a doc/talk, Grecotel is the best end-to-end case study (pilot → hotfixes →
  revert → Hardening project).
project: null
source_id: null
tags: []
time_minutes: 5
title: Find examples of technical debt due to fixing short term problems for EMEA
  clients
updated: 2026-07-17 12:07:03.539024
waiting_on: null
waiting_since: null
working_on: false
---