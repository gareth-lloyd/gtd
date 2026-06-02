---
area: null
contexts: []
created: 2026-05-29 12:16:13.010735
defer_until: null
due: null
energy: low
id: 2026-05-29T1216-rules-based-configuration-models-hotel-attributes
order: null
output: |
  ## Agent run 2026-06-02T10:31:30Z
  Created Linear ticket ENT-6393 (Enterprise team, Backlog, 0 Points, "Starter" label) — approved by user in session.
  https://linear.app/canary-technologies/issue/ENT-6393

  Verified the two issues against the code before writing the ticket:
  1. Wrong import source — hotel_attributes.py:7 does `from onboarding.testing import ManagementCompanyId`.
     Canonical definition is `canary.salesforce_ids.ManagementCompanyId` (salesforce_ids.py:205); onboarding.testing
     only re-exports it (onboarding/testing.py:17). The same file already imports BrandId from canary.salesforce_ids (line 6).
  2. Type-only usage — `ManagementCompanyId` is used solely in the annotation `management_company_id: ManagementCompanyId | None`,
     so it belongs under `if TYPE_CHECKING:`. Plain @dataclass with no `from __future__ import annotations`, so the fix should add
     future annotations (or stringify) when moving the import behind the guard.

  Ticket includes problem statement, fix, and acceptance criteria. No code change made — this task was scoped to writing the ticket.
project: null
source_id: null
tags: []
time_minutes: 5
title: rules_based_configuration/models/hotel_attributes.py
updated: 2026-06-02 13:33:47.132073
waiting_on: null
waiting_since: null
working_on: false
---

importing management comany id from wrong place
Also should only be imported if typechecking

Write this up as a 0 point Enterprise backlog ticket. Make sure it has the starter label