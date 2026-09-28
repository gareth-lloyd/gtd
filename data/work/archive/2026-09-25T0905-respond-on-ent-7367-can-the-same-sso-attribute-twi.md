---
area: null
completed_at: 2026-09-25 11:21:54.226148
contexts:
- react
created: 2026-09-25 09:05:07.829341
defer_until: null
due: null
energy: low
id: 2026-09-25T0905-respond-on-ent-7367-can-the-same-sso-attribute-twi
order: null
output: |
  ## Agent run 2026-09-25 10:46:06.441699

  **Answer for Lautaro: no deliberate product reason. Safe to remove, but it is a small feature, not a one-line constraint drop.**

  Not posted to Linear. Draft comment is at the bottom; say "send it" and it goes on ENT-7367 (https://linear.app/canary-technologies/issue/ENT-7367/sso-setup-for-crystalbrook-collection). No existing Linear ticket covers lifting this limit (searched).

  ### Where the limit lives
  - `backend/canary/sso/models/organization_role_mapping.py`: `UniqueConstraint(sso_organization, source_attribute_value)` named `sso_role_attribute_unique_sso_organization`.
  - Added in `sso/migrations/0018_auto_20230808_2205.py` (Aug 2023), before portfolio roles existed (ENT-7160, Aug 2026). Back then one value could only ever mean one property role, so there was nothing to combine. Pre-restructure blame is lost, but nothing in the model, tests, or history records a reason beyond "one value = one role".
  - The CheckConstraint on the same model separately enforces "exactly one role field set per row", so a value needing property + portfolio role needs two rows, which the unique constraint forbids.

  ### Login already tolerates multiple rows per value
  - `SSOOrganizationService.map_and_assign_roles` (sso_organization.py ~700) buckets mappings into `defaultdict(list)` keyed by lowercased value and iterates every mapping in the list.
  - `get_portfolio_role_mappings` (~1107) does the same for portfolio roles, and `provision_portfolio_roles` iterates the list too.
  - The DB constraint is case-sensitive while login is case-insensitive, so `Manager` + `manager` rows already exercise that multi-mapping path today. The ENT-6966 service comments acknowledge such rows exist.

  ### Why dropping the constraint alone is not enough (3 spots assume one value = one role)
  1. `parse_hotel_roles` (~600, ~636): any `roles` value present in the portfolio-mappings dict is filtered OUT before hotel-role assignment. A value mapped to both would get the portfolio role and silently lose the property role. Needs to skip only values that map exclusively to portfolio roles.
  2. `map_and_assign_roles` logs `sso.provision_roles.unexpected_mapped_portfolio_role` at ERROR when it meets a portfolio mapping. Once (1) lets mixed values through, it should skip those quietly instead.
  3. The new dashboard editor `SSORoleMappingService.replace_role_mappings` (`sso/services/role_mapping.py`, ENT-6966, Sep 2026): `_reject_duplicate_attributes` returns 422 on a repeated value, and `_apply_entries` DELETES stored rows that collide on `group_key` at the next save. So even if admin created two rows, the customer's next dashboard save would wipe the second one. The API contract (one role per row keyed on value) and `SSORoleMappings.vue` / `packages/shared/schemas/sso/SSORoleMappings.ts` would need to become value -> list of roles, or key rows on (value, role).

  Suggested shape: replace the unique constraint with one on (org, value, mapped_role, mapped_default_role, mapped_portfolio_role, mapped_default_portfolio_role, mapped_portfolio_wide_property_role) or drop it and dedupe in service; fix (1)-(3); tests in `sso/tests/services/test_sso_organization.py` and `sso/tests/services/test_role_mapping.py`. Migration in its own PR per repo rules.

  ### For Crystalbrook now
  Andrés's workaround (ask IT to send an extra `roles` value for the above-property dashboard) is the right call and needs no code. Do NOT use the case-variant trick (`Group Director` -> property, `group director` -> portfolio): parse_hotel_roles would drop the property role, and the dashboard editor deletes the second row on save.

  ### Draft Linear comment (not sent)
  @lmena No product reason I know of. The limit is just the `(sso_organization, source_attribute_value)` unique constraint from migration 0018 (Aug 2023), which predates portfolio roles, so back then one value could only ever mean one property role.

  Fine to remove when there's time, but it's a bit more than dropping the constraint. Login already iterates every mapping per value (`map_and_assign_roles`, `get_portfolio_role_mappings`), so that side is ready. Three places still assume one value = one role:
  1. `parse_hotel_roles` filters out any value that has a portfolio mapping, so a value mapped to both would lose its property role.
  2. `map_and_assign_roles` logs an error when it meets a portfolio mapping; it'd need to skip quietly.
  3. The new role-mappings screen/API (ENT-6966) rejects duplicate values and deletes colliding stored rows on the next save, so the API contract would need to become value -> multiple roles.

  Worth a ticket. For Crystalbrook, asking IT for an extra roles value is the right call.
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-7367/sso-setup-for-crystalbrook-collection#comment-be59226e
tags:
- morning-gtd
- linear
time_minutes: 10
title: 'Respond on ENT-7367: can the same-SSO-attribute-twice mapping limit be removed?'
updated: 2026-09-25 11:21:54.226136
waiting_on: null
waiting_since: null
working_on: false
---

Lautaro (09-24): 'we can't map the same attribute two times... @glloyd do you know if there is a reason for this limitation or would it be ok to remove it when we have time?' Crystalbrook SSO; 3 new comments, bwai needs access sorted before training early next week.
https://linear.app/canary-technologies/issue/ENT-7367/sso-setup-for-crystalbrook-collection