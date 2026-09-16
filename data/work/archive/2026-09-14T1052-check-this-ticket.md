---
area: null
completed_at: 2026-09-16 09:22:48.112269
contexts: []
created: 2026-09-14 10:52:18.192537
defer_until: null
due: null
energy: low
id: 2026-09-14T1052-check-this-ticket
order: null
output: |
  ## Agent run 2026-09-14T10:56

  **Verdict: nothing to do. Joshua's closing comment is correct, and you removed the code yourself.**

  Ticket: SDM-947 (https://linear.app/canary-technologies/issue/SDM-947/bug-authorizations-3-forms-are-created-by-default-instead-of-1). Opened by Ani in Aug 2023: new hotels got 3 auth forms (global Formstack + brand Formstack + Formweaver generic) instead of just Formweaver. Project: Formstack -> Formweaver. Assignee: Joshua Hart.

  - The linked comment (https://linear.app/canary-technologies/issue/SDM-947/bug-authorizations-3-forms-are-created-by-default-instead-of-1#comment-8b3a7678), from Joshua on 2026-09-11: "The AvailableFormPlan was removed at some point in the past three years." He moved the ticket from Backlog to **Done** at the same time.
  - You were probably notified because Joshua's 2023 comment @-mentioned you (and ypan). It asked whether brand-customised forms, especially the 9 Four Seasons templates, still needed spawning from onboarding.
  - Joshua's own fix, PR #9785 (https://github.com/canary-technologies-corp/canarytech_dev/pull/9785), was **closed without merging** on 2024-12-19.
  - The code was actually removed in **your** commit 919d790d559, [ENT-3791] "Make onboarding stages explicit and imperative" (#27914), on 2025-07-16. It deleted `backend/canary/onboarding/plans/available_form_plans.py`: `AddAvailableFormsPlan`, `BRAND_AVAILABLE_FORMS` and `GENERIC_AVAILABLE_FORM`.
  - Checked against local canary `master` (last commit 2026-09-09): `AvailableFormPlan` and `BRAND_AVAILABLE_FORMS` appear nowhere. The onboarding app no longer mentions Formstack or `AvailableForms`. It only sets the `has_formweaver_auth_or_contract_flow` flags.
  - Formstack code still exists elsewhere (authorization models, migration/backfill commands, views), but none of it runs during onboarding.

  Optional: reply on the ticket to say it was removed in #27914, so the record is exact. I haven't posted anything.
project: 2026-09-08-mobile
source_id: null
tags: []
time_minutes: 5
title: Check this ticket
updated: 2026-09-16 09:22:48.112259
waiting_on: null
waiting_since: null
working_on: false
---

https://linear.app/canary-technologies/issue/SDM-947/bug-authorizations-3-forms-are-created-by-default-instead-of-1#comment-8b3a7678