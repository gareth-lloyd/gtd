---
area: null
completed_at: 2026-10-02 13:01:54.791752
contexts:
- react
created: 2026-10-02 11:12:14.688919
defer_until: null
due: null
energy: low
id: 2026-10-02T1112-reply-on-ent-7615-wyndham-scripting-change-for-ohi
order: null
output: |
  ## Agent run 2026-10-02T09:28:07Z

  Nothing posted. A reply is optional: Andrea's comment is addressed to Ryan, who is the assignee, and the ticket moved to Todo on 2026-10-01.

  **Thread state** (ENT-7615, https://linear.app/canary-technologies/issue/ENT-7615/wyndham-scripting-change-to-support-ohip-migration)
  - 2026-09-24 Andrea asked for your high-level thoughts.
  - 2026-09-30 You replied twice: prefer expanding the existing OnboardingValue kind; Gateway API changes are needed but are a simple mechanical change.
  - 2026-10-01 Andrea to Ryan: start with a lightweight design doc to communicate the changes to the Gateway team (https://linear.app/canary-technologies/issue/ENT-7615/wyndham-scripting-change-to-support-ohip-migration#comment-3a684796). No reply from Ryan yet.

  **What I checked in the code (master)**
  - Gateway already stores streaming credentials on the OracleOhip model: `streaming_app_key`, `streaming_client_id`, `streaming_client_secret` are required together, and `streaming_username`, `streaming_password`, `streaming_enterprise_id` are optional (`backend/pms-gateway/vendors/integrations/oracle_ohip/models/configuration.py:117-133`, validation in `clean_streaming_credentials` at line 558). So no Gateway model change or migration is needed.
  - The Gateway configuration API schema has no `streaming_*` fields (`backend/pms-gateway/vendors/integrations/oracle_ohip/schemas/configuration.py:15-38`). They can only be set in Gateway admin today. This is the Gateway API change from your second comment.
  - Canary has three places with no streaming fields: `OhipConfiguration` (`backend/canary/onboarding/configuration_providers/integrations_schemas/oracle_ohip.py:13`), `DynamicOhipValuesSchema` (`backend/canary/onboarding/services/pms_config.py:39`), and the Wyndham provider that builds the config (`backend/canary/onboarding/configuration_providers/wyndham/wyndham_pms_config_provider.py:163`).
  - Best Western reads the same `OHIP_CREDENTIALS_BY_CHAIN_CODE` kind (`backend/canary/onboarding/configuration_providers/best_western/pms_config_provider.py:179`), so any change to the kind's shape affects BW values too.
  - Not checked: whether `DynamicOhipValuesSchema` rejects unknown keys. If it does, the schema change must deploy before anyone adds `streaming_*` keys to an onboarding value. Also not checked: the onboarding value admin form (`backend/canary/onboarding/admin/onboarding_value.py`), which may validate the shape.

  **Recommendation**
  Reply with a short +1 that hands Ryan the touchpoints, and take a position on the shape: flat optional `streaming_*` keys on the existing kind, mirroring Gateway's field names. Option 1 as written in the ticket (nested fetch and streaming objects) would need every existing value rewritten or a parser that reads both shapes. Flat optional keys leave existing Wyndham and BW values valid with no data change, which answers your backward-compatibility concern.

  **Draft reply (not posted; reply under Andrea's comment)**

  > +1 to a short doc. The scope looks small, because Gateway already stores the streaming credentials on the OracleOhip model (`streaming_app_key`, `streaming_client_id`, `streaming_client_secret`, plus optional username, password and enterprise id). Two things are missing:
  >
  > 1. Gateway: the configuration API schema (`oracle_ohip/schemas/configuration.py`) doesn't accept the `streaming_*` fields, so they can only be set in admin today.
  > 2. Canary: `OhipConfiguration`, `DynamicOhipValuesSchema` and the Wyndham PMS config provider need to pass the same fields through.
  >
  > For the onboarding value, I'd add flat optional `streaming_*` keys to the existing kind rather than nesting fetch and streaming objects. Existing values stay valid with no data change, including Best Western's, which use the same kind.
  >
  > Happy to review the doc.
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-7615/wyndham-scripting-change-to-support-ohip-migration#comment-3a684796
tags:
- morning-gtd
- linear
time_minutes: 5
title: 'Reply on ENT-7615: Wyndham scripting change for OHIP migration'
updated: 2026-10-02 13:01:54.791744
waiting_on: null
waiting_since: null
working_on: false
---

Andrea to Ryan: 'let's start with a light weight design doc so that we can communicate the changes we're going to make with the gateway team'. Follows your two comments (prefer expanding the existing OnboardingValue kind; needs Gateway API changes). Addressed to Ryan, not you.
https://linear.app/canary-technologies/issue/ENT-7615/wyndham-scripting-change-to-support-ohip-migration