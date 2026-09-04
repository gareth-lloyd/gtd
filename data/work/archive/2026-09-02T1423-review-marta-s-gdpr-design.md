---
area: null
completed_at: 2026-09-03 17:02:06.496017
contexts: []
created: 2026-09-02 14:23:22.130835
defer_until: null
due: 2026-09-03
energy: low
id: 2026-09-02T1423-review-marta-s-gdpr-design
order: null
output: |
  ## Agent run 2026-09-02T14:27:08+02:00

  Design doc: https://app.notion.com/p/canarytechnologies/GDPR-Country-based-default-retention-3ce8146861518059934ec78cf2f98777
  Linear: EMEA-350 (https://linear.app/canary-technologies/issue/EMEA-350/eng-design-gdpr-country-based-default-retention), status In Review, owner Marta.
  Grounded against code on branch glloyd/ent-7078 (canary sweep, gateway beat, account sync) and a deduped Snowflake count of live non-demo hotels in the EU region.

  ### Verdict
  Agree with the recommendation: resolve at read time on both sides from a shared country map, propagate country to the Gateway. The doc is clear and the ConformityService rejection is well argued. Six things need adding before approval; the rest are comments.

  ### Must address
  1. Explicit list, not environment (open thread with Marti). The data settles it: of ~545 live non-demo hotels in the EU region, ~135 are outside EU/EEA+UK (CH 21, TR 19, TH 15, NZ 14, PH 8, MY 7, IN 5, AE/BH/VN/KH 4 each, plus singles). Environment-based would over-apply to a quarter of the region. Suggest a new group in backend/shared/shared/geo/country/country_group.py: CountryGroup.EUROPEAN_UNION already exists; add EEA (IS, NO, LI) + UK as e.g. GDPR_SCOPE so both services import one list. Switzerland (21 live hotels, FADP not GDPR) needs a Legal call and should be named in the doc.
  2. Opt-out is a requirement, not a con. Business decision 4 allows "not deleting data at all", but option 1 says null = country default, so there is no way to express keep-forever. The doc needs an explicit precedence table per side: disabled override / numeric override / country default / not in scope. Suggest a tri-state (e.g. a retention mode enum next to pii_retention_days) rather than overloading null. Same question on the Gateway: is account.obfuscation_policy = an inactive policy an opt-out, or does null fall through to country?
  3. Gateway refactor is bigger than the doc implies. The beat iterates policy rows, not accounts (gdpr/beats/scheduled_obfuscation_service.py: for policy in ObfuscationPolicy.objects.filter(is_active=True) then Account.objects.filter(obfuscation_policy=policy)). GdprRun.policy FK, get_query scope by policy, the repair command and Snowflake deletion all key off a policy row. Read-time country resolution means inverting to a per-account loop and giving GdprRun a resolved window instead of a policy FK. Also ObfuscationPolicy rows are shared across accounts ("7 days" is one row for 2 accounts), so a CSM override means a new policy row per override, not editing the one the account points at. Worth spelling out.
  4. Rollout precondition missing. EMEA-350 calls out the hard-coded lag=7 days filter in pms-gateway gdpr/services/snowflake_deletion.py:72-76. Still there today. Any account on a 30-day window gets no warehouse cleanup, so pre-redaction guest copies stay in Snowflake. Must be generalised before any pilot account moves to 30 days. Same pattern in the Opera fetch exclusion. Neither is in the doc.
  5. Blank country_code. 3 live non-demo EU-region hotels have blank country_code; read-time resolution silently treats them as out of scope. Hotel.country_code is blank=True and its help text says it is for phone number formatting. It becomes compliance-load-bearing, so: sweep should report EU-region hotels with blank country, and the admin help text should say changing it changes deletion. Not-in-scope hotels should be logged per sweep so CS can answer "why is my data not deleted".
  6. Rollout gate needs a concrete design. Option 1 con says "needs a feature flag" and stops. Today null = not swept is the gate; read-time removes it. Propose: the country map itself is the rollout (a country is absent until Legal signs off, per point 4 in the doc's own business questions), plus a hotel-id cohort for the pilot. Whatever it is, the gate must be the same on both sides or CI/CO and PMS data go out of step.

  ### Comments
  - Propagating country to the Gateway is cheaper than described. Hotel.save() already flips gateway_account_needs_sync, cron_patch_accounts_in_gateway pushes via PMSGatewayService.update_account, which sends currency/timezone/is_demo. Add country to CreateAccountRequest/UpdateAccountRequest and the backfill is "set needs_sync on every hotel". No new mechanism. Account.country must be nullable (currency has a default; country must not).
  - "Obfuscated at the same time" (business decision 2) cannot be literally true. Canary sweeps by departure_date <= today - N once a day; the Gateway beat runs hourly, capped at 1000 rows per entity per run, with created_at shielding. Expect days of skew on a backlog. Soften to "same window" and keep the shared map in days only (the Gateway policy supports months/years, the Canary field is days, max 1827).
  - Ticket vs doc divergence. EMEA-350 scope says "driven by the ConfigurationRuleEngine developed by the Enterprise team". The doc rejects ConformityService for a per-country global default (single root tree per hotel, no catch-all root, independents get nothing). I think that assessment is right and the code map is the correct interim, with ConformityService reserved for brand-mandated retention. But Martijn wrote the ticket expecting the rule engine, so get that agreed explicitly and update the ticket scope.
  - Dashboard exposure (Marti thread, Marta agreed: greyed out, CSM-only change) is in the ticket requirements but not in the doc's scope section. Add it, or say it is a follow-up.
  - Category defaults: the doc lists ID docs / audit logs / messages then scopes them out. Fine, but say where those numbers will live so the shared map is shaped for them (category -> country -> days) rather than a flat country -> days that has to be reshaped later.
  - Strongly agree with the irreversibility note. Suggest the country list ships empty and each country is added only with a written Legal sign-off linked in the PR.

  ### Snowflake facts used
  EU region, CANARY_RAW.CANARY.HOTELS_HOTEL deduped per id, is_live and not demo: 545 hotels, 0 with pii_retention_days set. Top: GB 99, ES 63, IT 51, DE 35, CZ 26, FR 25, CH 21, TR 19.

  ### Follow-up 2026-09-02: General Rules doc
  Gareth asked whether Marta's design considers "Enforcing compliance with rules based configuration" (https://app.notion.com/p/canarytechnologies/Enforcing-compliance-with-rules-based-configuration-36581468615181359f2bce159fa804cc). It does not: no link, no mention of General Rules. Her rejection is of ConformityService as it exists today, which is accurate. That note (May 2026, draft, sketch PR #45775 https://github.com/canary-technologies-corp/canary/pull/45775 still open draft, nothing in main) proposes exactly the missing piece: a geo-only rule registry beside the brand trees, enforced cross-brand at startup with FINAL. Country-based retention is a textbook General Rule (countries -> value, brand-independent, legally owned). Two gaps if used here: General Rules as sketched are an enforcement check on brand trees, not a resolver, so independents with no root still need a resolution path; and the Gateway has no ConformityService, so the shared country map is still needed there. Suggested ask: Marta's doc should reference the note and say whether the code map is a stepping stone to General Rules or a permanent alternative.

  No external writes were made. Comments are drafted here only; say if you want any posted to the Notion doc.
project: 2026-07-20-gdpr
source_id: null
tags: []
time_minutes: 5
title: Review Marta's GDPR design
updated: 2026-09-03 17:02:06.496013
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/GDPR-Country-based-default-retention-3ce8146861518059934ec78cf2f98777?source=copy_link