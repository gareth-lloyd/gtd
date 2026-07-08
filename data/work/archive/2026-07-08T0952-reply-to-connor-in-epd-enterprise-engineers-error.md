---
area: null
contexts:
- react
created: 2026-07-08 09:52:43.577371
defer_until: null
due: null
energy: low
id: 2026-07-08T0952-reply-to-connor-in-epd-enterprise-engineers-error
order: null
output: |
  ## Agent run 2026-07-08T10:20 (research + drafted reply — NOT posted)

  Thread: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1783439627731099?thread_ts=1783438349.025529&cid=C0B1MN8F869
  Origin ticket: ENT-6768 (IHG SSO "No Hotel Access" — Prairie Crest Calgary Airport onboarded with numeric SF "Unique Hotel ID" 13404 instead of alphabetic InnCode YYCAP). https://linear.app/canary-technologies/issue/ENT-6768 — this was Gareth's ticket, now Deployed.

  ### Connor's actual question (to @Andrea @Andres @Gareth)
  "We know IHG InnCodes should be 5-digit alphabetic (not numeric). Do you think we should throw an error when we see a 5-digit numeric for IHG? …or generally see an id from Salesforce that doesn't match the customer's convention?" Wyndham/BW are always 5-digit numeric. Andrea suggested adding it to the hotel-brand-change flow and alerting when the value didn't change during a brand transition. Andres: validate/strongly-type data by brand where possible.

  ### Codebase findings (backend/canary)
  - There is currently NO format validation on IHG InnCodes. IHG providers only check not-empty (`is_field_empty`) + normalize (`.strip().lower()`), then use the value to build the slug (`ihg-{inn_code}`) and the SSO hotel id. A 5-digit numeric like `13404` is accepted and produces `ihg-13404` + a broken SSO id — exactly the ENT-6768 failure.
    - `backend/canary/onboarding/configuration_providers/ihg/ihg_sso_provider.py:13-31`
    - `backend/canary/onboarding/configuration_providers/ihg/ihg_hotel_info_provider.py:10-27` (`generate_ihg_slug`)
    - `backend/canary/onboarding/configuration_providers/ihg/hotel_association_id_provider.py:14-25`
    - Model: `backend/canary/hotels/models/hotel_association_id.py:21` (`IHG_INN_CODE`), identifier is a plain `CharField(max_length=1024)` with no constraint.
    - Source of the value: Salesforce "Unique Hotel ID" (`SF_FIELD_UNIQUE_HOTEL_ID`).
  - We ALREADY enforce the INVERSE for Wyndham/Best Western: `fix_numeric_id(raw_id, min_length=5)` requires a 5-digit numeric and raises otherwise. Clean precedent to mirror (inverted) for IHG.
    - `backend/canary/onboarding/configuration_providers/config_utils.py:12-24`
    - `backend/canary/onboarding/services/salesforce_hotel_account.py:351-360` (raises `InvalidHotelIdentifiers`)
    - Error plumbing lives in `backend/canary/onboarding/exceptions.py` (e.g. `ERROR_IHG_INN_CODE_NOT_SET` at :153; "5 digit numeric" messaging at :303/:307/:336/:445).
  - Note: existing IHG SSO tests treat digit-containing codes as valid (`ABC123`, `HOTEL-123`) but none is purely-numeric. Safe rule is "reject if all-digits (`^\d{5}$`)", NOT "must be alphabetic" — needs data-team confirmation that no legitimate IHG property has an all-numeric InnCode before making it a hard block.
  - The InnCode stays in `canary` (SSO + slug + association); it does NOT flow into pms-gateway as a hotel identifier, so any check belongs in canary onboarding / brand-change, not the gateway.

  ### My recommendation (the substance of the reply)
  1. Yes — worth adding, and cheap. It's symmetric to what we already do for Wyndham/BW. Best home: the IHG onboarding config providers (or an onboarding pre-run check) + Andrea's brand-change flow, failing loud with a clear error rather than silently building `ihg-13404`.
  2. Be honest about coverage: an all-numeric guard catches the cross-brand paste where formats differ (a numeric Wyndham/BW id landing in an IHG field — i.e. ENT-6768). It does NOT catch a wrong-but-valid-format IHG code, nor Wyndham-id-in-BWH-field (both numeric), as Connor already noted. Format validation is a cheap first line, not a complete solution.
  3. Rule should be "reject all-digits" not "require alphabetic" (avoid blocking a legit numeric IHG code if any exist) — confirm with data team; could ship as a warning first, harden to a hard error once confirmed.
  4. Andrea's "alert when the id didn't change during a brand transition" is a good complementary heuristic — catches the forgot-to-update case regardless of format. Worth doing alongside.
  5. The only thing that catches a valid-format-but-wrong code is reconciling the InnCode against IHG's real property directory (does it resolve to an actual IHG hotel?). Heavier lift; flag as the real upstream fix. Connor is already chasing the Salesforce-entry angle with Stacy — that's the best place to stop it at source.

  ### DRAFTED Slack reply (NOT posted — needs your approval to send)
  > Yeah, I'd add it — it's basically the mirror of what we already do for Wyndham/BW, where we force a 5-digit numeric id (`fix_numeric_id`). Today IHG InnCodes get zero format validation: we accept whatever's in the SF "Unique Hotel ID" field and build the slug/SSO id straight off it, which is exactly how 13404 slipped through and produced `ihg-13404` in ENT-6768.
  >
  > A couple of caveats so we're clear on what it buys us:
  > - The rule should be "reject if it's all digits", not "must be alphabetic" — worth confirming with the data team that no real IHG property has an all-numeric InnCode before we make it a hard block (can ship as a warning first, harden once confirmed).
  > - It only catches cross-brand mismatches where the formats differ (a numeric Wyndham/BW id in an IHG field — i.e. this case). It won't catch a wrong-but-valid IHG code, or a Wyndham id sitting in a BWH field, like you said.
  >
  > For placement I'd put the check in the IHG onboarding config providers + the brand-change flow so it fails loud during config. +1 to Andrea's "alert if the id didn't change during a brand transition" as a complement — that catches the forgot-to-update case regardless of format. And the only thing that catches a valid-but-wrong code is reconciling the InnCode against IHG's actual property list, which is a bigger lift — the highest-leverage fix is still stopping it at the SF entry point (what you're chasing with Stacy).

  Not sent. If you want it posted, say the word and I'll post it (or you can paste/edit).
project: null
source_id: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1783439627731099?thread_ts=1783438349.025529&cid=C0B1MN8F869
tags:
- morning-gtd
- slack
time_minutes: 10
title: 'Reply to Connor in #epd-enterprise-engineers: error on 5-digit numeric IHG
  InnCode?'
updated: 2026-07-08 15:10:47.336749
waiting_on: null
waiting_since: null
working_on: false
---

Connor: IHG InnCodes should be 5-digit alphabetic (not numeric). 'Do you think we should throw an error when we see a 5 digit numeric for IHG?' Directed at @Andrea @Andres @Gareth.
https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1783439627731099?thread_ts=1783438349.025529&cid=C0B1MN8F869