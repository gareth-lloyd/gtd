---
area: null
contexts:
- react
created: 2026-07-01 08:29:45.614078
defer_until: null
due: null
energy: medium
id: 2026-07-01T0829-answer-leandro-andrea-do-onboarding-scripts-use-lo
order: null
output: |
  ## Agent run 2026-07-01T15:40 (research; nothing sent)

  **Answer to Leandro's question ("are you currently using LOCKED to prevent
  admin-level changes so CS can't bypass it in the UI?"): No — there is no lock
  today. Nothing currently prevents CS from editing these fields in the UI.**

  ### What the FINAL/FREE (Leandro's "LOCKED") concept actually is
  - The framework is the `rules_based_configuration` app. Field states live in
    `OverridePolicy` (`rules_based_configuration/services/conformity.py:27` —
    `FINAL = "final"`, `FREE = "free"`).
  - FINAL/FREE **is** in active use, e.g.:
    - `enterprise_best_western/configs/best_western.py` (BW GMS membership vendor/kind/level = FINAL)
    - `enterprise_ihg/configs/ihg_pilot.py` (dozens of check-in/check-out settings = FINAL, some = FREE)
  - BUT FINAL ≠ a UI/admin lock. FINAL only controls **override precedence inside
    the config rules hierarchy**: a setting an ancestor group marks FINAL cannot be
    overridden by a *descendant group* in the tree. This is validated only at
    config-authoring time in `ConformityDiamondTree.finalize()`
    (conformity.py:517-541, "after FINAL override policy has been defined by an
    ancestor"). It says nothing about whether a human can edit that field on a hotel.

  ### Why it does NOT stop CS today (the key points for Leandro)
  1. The only place rules meet a live hotel is
     `ConformityService.validate_hotel_on_save` → wired via the `hotel_admin_saved`
     signal (`rules_based_configuration/signals.py:31`). Its own docstring says:
     **"Does not block saving (warn mode)."** It only emits "Configuration drift"
     `messages.warning(...)` — never blocks the save.
  2. That signal is fired from **exactly one place: the Django admin**
     (`hotels/admin/hotel.py:2024`). It does NOT fire from the CS-facing product
     dashboard. So when CS edits a field in the normal product UI, the drift check
     doesn't even run — no warning, no block.
  3. Onboarding scripts/plans just write plain editable hotel fields via normal
     `.save()` (e.g. `onboarding/plans/chat_settings_plan.py`). They set no
     read-only/locked flag. On re-run a plan overwrites drift back to the expected
     value (some plans instead skip). That reactive reset (next script run) is the
     only real "enforcement" — there is no preventive lock.

  ### Bottom line to relay
  - **No lock exists.** FINAL governs hierarchy override precedence at config-authoring
    time; the conformity/drift check is warn-only AND Django-admin-only. CS can freely
    change rule-governed fields in the product UI with nothing stopping them.
  - This matches Andrea's recollection ("we can use the final/free to better control
    that, but I don't think we take advantage of that right now" — msg 19:09).
  - If the goal is to actually prevent CS bypass, that enforcement must be built —
    e.g. wire `ConformityService.hotel_conforms` / the consistency checks into the
    product save path to *block* (not warn), and restrict which fields CS can edit.
    Leandro already floated this ("rules expose a method to check consistency... we
    could use that to prevent changes if we need to, it's a matter of prioritization").

  ### Refs
  - Slack group DM thread: https://canarytechnologies.slack.com/archives/C0B4QD01GP8/p1782836057103019
  - Notion (Leandro's design): "Check-In V3 Configuration"
    https://www.notion.so/canarytechnologies/Check-In-V3-Configuration-365814686151808c805efb429b821412
  - Notion (rules enforcement note): "Enforcing compliance with rules-based configuration"
    https://www.notion.so/canarytechnologies/Enforcing-compliance-with-rules-based-configuration-36581468615181359f2bce159fa804cc
  - Connor is named as the ENT PM in-thread (for the product-prioritization question).

  NOTE: I did not post anything to Slack. Draft reply is above — send if you want.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0B4QD01GP8/p1782836057103019
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Answer Leandro & Andrea: do onboarding scripts use LOCKED/final to prevent
  admin/UI field edits?'
updated: 2026-07-01 16:30:55.066133
waiting_on: null
waiting_since: null
working_on: false
---

Group DM — Andrea deferred to 'Gareth's knowledge' on free/locked. Leandro needs to know if LOCKED is used to prevent admin-level changes so CS can't bypass it in the UI. https://canarytechnologies.slack.com/archives/C0B4QD01GP8/p1782836057103019