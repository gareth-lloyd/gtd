---
area: null
contexts: []
created: 2026-05-28 12:26:53.032849
defer_until: null
due: null
energy: low
id: 2026-05-28T1226-bw-settings-change-explore-whether-scripts-can-do
order: 3
output: |
  ## Agent run 2026-05-28T12:31:31+03:00

  ### Question (from thread, ENT-6111)
  Running `ChatSettingsPlan` against the BW cohorts would change more than the
  intended `escalation_candidate_scope` — it would also flip `has_ai`,
  `is_ai_responding_enabled`, and `repeat_notification_sound_until_read` back to
  BW onboarding defaults on ~78 live hotels. Melissa confirmed "keep current
  hotels config." Andres ran a one-off RW script for the immediate change (all
  1,247 BW live hotels). This task = explore a general fix: can the scripts
  detect whether settings were set before and avoid overwriting?

  ### Direct answer
  Not reliably with the current data model. The scripts CANNOT tell whether a
  field value was set by a human or by a prior onboarding run, because the chat
  settings model stores no provenance/history. A `has_ai = True` looks identical
  whether staff toggled it or onboarding wrote it.

  ### Why (what the code actually does)
  - `ChatSettingsPlan.execute()` —
    backend/canary/onboarding/plans/chat_settings_plan.py:18-86. For each field
    it does `if config.<field> is not None: hotel.chat_configuration.<field> =
    config.<field>`. The ONLY guard is "did the brand config provider supply a
    value?" — NOT "did the hotel already have a different value?" So whenever the
    BW provider supplies a value (it supplies all four), the plan overwrites the
    hotel's current value unconditionally.
  - The fields live on `chat.models.configuration.Configuration`
    (backend/canary/chat/models/configuration.py): `has_ai` (~L111),
    `is_ai_responding_enabled` (~L112), `repeat_notification_sound_until_read`
    (~L84), `escalation_candidate_scope` (~L99).
  - `Configuration` subclasses only `TimeStampedModel` — NOT `EventableModelMixin`
    and no django-simple-history. Verified: no audit/history table records
    field-level changes. So there is no source of truth for "was this manually
    changed?". (The only "audit" hits in chat/ are the unrelated AI-auditor
    feature.)
  - The BW provider (configuration_providers/best_western/chat_config_provider.py)
    populates all four fields, which is why a plan re-run clobbers manual edits.
  - The framework's only existing "don't touch" mechanism is field-level: a
    `None` in the `ChatConfig` dataclass
    (configuration_providers/configs/chat.py) means "skip this field." There is
    NO idempotency/skip-if-set/override-detection anywhere in the plan framework
    (base at onboarding/plans/base.py). Note: onboarding/CLAUDE.md calls plans
    "idempotent," but that only means re-applying the SAME config is safe — it
    does not mean manual overrides are respected.

  ### Two ways to solve it (they are different problems)
  Andres proposed "flags for specific subprocesses on each plan." Gareth asked
  "detect whether set before." These are distinct:

  Option A — SCOPE the run (recommended first move).
  Don't detect anything; make the targeted cohort/run touch ONLY the field it
  intends to change, leaving the rest `None`. The field-level `None = skip`
  support already exists; the only reason BW clobbers extra fields is that the BW
  provider sets all of them. Implement a scoped config provider (or a CUSTOM
  ScriptType variant) that emits only `escalation_candidate_scope`. Deterministic,
  low-risk, you only ever change what you declare. This is the precise fix for
  the ENT-6111 class of change and matches Andres's "subprocess flags" idea.

  Option B — DETECT prior manual changes and preserve them (general, but blocked).
  Requires provenance the model doesn't have today. Sub-paths:
    1. Add an audit trail (EventableModelMixin / simple-history) to Configuration,
       then skip any field a non-system actor previously changed. Most robust but
       heavyweight, and RETROACTIVELY BLIND — no history exists for changes made
       before it's added, so it wouldn't protect today's 78 hotels anyway.
    2. "Only overwrite if current == brand default." Cheap, no schema change, but
       cannot distinguish a deliberate set-to-default-value from an untouched
       default, and silently misbehaves when the intended new value equals the
       old default.

  ### Recommendation
  Lead with Option A (field-scoped plan runs / per-field subprocess flags). It
  directly prevents the silent-overwrite footgun, needs no schema change, and
  generalizes to the Wyndham/IHG asks Connor flagged. Treat Option B.1 (audit
  trail) as a separate, larger initiative only if there's a recurring need to
  bulk-reconcile while preserving arbitrary manual edits — and note it can't
  retroactively recover provenance. Avoid B.2 as a primary mechanism (ambiguous
  semantics).

  ### Pointers
  - Plan: backend/canary/onboarding/plans/chat_settings_plan.py:18-86
  - Config dataclass: backend/canary/onboarding/configuration_providers/configs/chat.py
  - BW provider: backend/canary/onboarding/configuration_providers/best_western/chat_config_provider.py
  - Model: backend/canary/chat/models/configuration.py
  - Wiring: backend/canary/onboarding/models/property_configuration_processes.py (ONBOARDING_TYPE_CONFIG)
  - No external writes made. Research only.
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: 5
title: 'BW settings change: Explore whether scripts can "do the right thing" as described
  in the thread'
updated: 2026-05-28 12:31:31.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1779958223770609?thread_ts=1779895878.594459&cid=C0B1MN8F869

Can the scripts detect whether these have been set before, and avoid overwriting changes?