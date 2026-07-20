---
area: null
contexts: []
created: 2026-07-16 19:35:56.240615
defer_until: null
due: null
energy: low
id: 2026-07-16T1935-will-this-be-overwritten-by-wyndham-registration-c
order: null
output: |
  ## Agent run 2026-07-16T20:05:00+03:00

  **Short answer: yes — if the Wyndham reg card onboarding plan ever re-runs on this hotel, the custom fields get wiped. But nothing re-runs it automatically today.**

  **Context.** The Slack thread (https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1784219073780439) is Marta Ziaei asking about a Spanish Wyndham property (EU hotel 4503) whose Passport/ID capture Canary disabled a few months ago. Sebastian Cahill's answer: add the Spanish-police registration fields (document number, nationality, DOB) to the reg card via the form builder (example: gran-hotel-luna-de-granada23). The question is whether those manually-added fields survive the Wyndham registration card onboarding machinery.

  **What the onboarding plan does.** `WyndhamRegistrationCardProvider.perform_hotel_configuration` (backend/canary/onboarding/configuration_providers/wyndham/wyndham_registration_card_provider.py:286-358) ALWAYS rebuilds the schema from `WYNDHAM_DEFAULT_TEMPLATE`. For an existing card the ONLY thing it preserves is the hotel-policy markdown (extracted and re-inserted). Custom fields added in the form builder do NOT survive a re-run — they are silently replaced by the default template. So any re-run of `AddRegistrationCardPlan` with this provider on hotel 4503 overwrites the Spanish compliance fields.

  **Will it re-run?**
  - Onboarding plans run via onboarding script batches at onboarding time; hotel 4503 is already live, so nothing re-runs the reg card plan on a schedule.
  - The ID-capture disable itself came from a one-off script: PR #41679 "Script: Remove ID Capture from Wyndham Intl Check-In for Non-Compliant Countries" (Andrés Figueira, 2026-03-24, ENT-5708) — that script also changed `ADDITIONAL_GUEST_STEPS_BY_COUNTRY[SPAIN]` to NO_ID_COLLECTION_AND_ADDITIONAL_GUESTS. A similar future compliance sweep that goes through the provider WOULD clobber the custom fields.
  - Rules-based configuration / drift detection (Martin Rodriguez's work, currently dry-run) covers only scalar settings — `hotel.check_in_configuration.id_step` etc. in backend/canary/enterprise_wyndham/configs/wyndham.py (Spain is in WYNDHAM_NO_ID_AND_ADDITIONAL_GUESTS, id_step FINAL=DISABLED per ENT-5708). It does NOT track or enforce the reg card schema, so `apply_portfolio_settings`/drift remediation will not touch the added fields. It will keep ID capture disabled, which is what Spain wants anyway.

  **Caveats / follow-ups worth raising:**
  1. If the reg card fields are added for 4503, note it somewhere (KB / hotel notes): any future run of the Wyndham reg card provider on that hotel silently resets the card except the policy text. The provider could be extended to preserve custom fields the way it preserves policy markdown — currently it doesn't.
  2. The Notion source-of-truth doc "Registration card configuration" (https://www.notion.so/canarytechnologies/1d78146861518095830ad6923bda9163) is stale: it still lists Spain (and France, Italy, Netherlands, Portugal, etc.) as "Collect ID and Additional Guests", but the code has been no-ID for those countries since PR #41679. Worth updating since the code comment points to it as source of truth.
  3. Spanish police compliance likely needs these fields for ALL Spanish Wyndham properties, not just 4503 — if so, the right fix may be to add them to the Wyndham default template for Spain (in the provider) rather than per-hotel form-builder edits, which both scales and removes the overwrite risk.
project: null
source_id: null
tags: []
time_minutes: 5
title: Will this be overwritten by wyndham registration card onboarding plan
updated: 2026-07-17 13:07:45.860189
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1784219073780439