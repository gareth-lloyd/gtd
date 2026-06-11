---
area: null
contexts:
- react
created: 2026-06-11 09:43:42.408448
defer_until: null
due: null
energy: low
id: 2026-06-11T0943-skim-lautaro-s-reworked-sso-onboarding-docs-and-gi
order: null
output: |
  ## Agent run 2026-06-11T14:05:00+03:00

  Skimmed all three docs from Lautaro's thread
  (https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1781122174466579):
  - Hub: https://www.notion.so/canarytechnologies/SSO-Onboarding-a40a4042b4504183a51a3785ac9e612f
  - CS Playbook: https://www.notion.so/canarytechnologies/37b814686151816fad1af44f8e67605c
  - Setup Guide: https://www.notion.so/canarytechnologies/329814686151811ba0e9c83835c89641

  Overall: big improvement. Role-based hub routing is clear, the new-vs-existing
  customer distinction is front and centre in both docs, and the "what a complete
  ticket needs" section directly fixes the triage pain. Specific feedback, roughly
  in priority order:

  1. **Slug selection has no owner or step.** Both docs warn "slugs are permanent —
     pick carefully" (CS Playbook blockers table; Setup Guide ACS/login URLs), but
     neither doc ever says who picks the slug or at which step. Should be an explicit
     input in Playbook step 2 or 3 and in the Setup Guide pre-setup checklist.
  2. **Setup Guide Section 6a assumes existing Canary users for testing** ("identify
     1-2 existing Canary users... linked to your SSO organization") — but new
     customers have no existing users by definition (fresh state, auto-provisioning
     on). Needs a new-customer variant (e.g. test users get JIT-provisioned, or
     are created first). Also "1-2" here vs "two test user emails" in the Playbook.
  3. **EU-host caveat is inconsistently applied.** Hub and Section 3b carry the
     "EU-hosted orgs use a different host" note, but Sections 6b and 7d print the
     literal `www.canarytechnologies.com/sso/login/<slug>` URL with no caveat —
     and 7d is the template customers will paste into staff comms.
  4. **Ticket spec vs Slack triage note mismatch.** Lautaro's Slack message says a
     complete ticket needs "property list, new vs. existing, roles/permissions",
     but Playbook step 2's ticket spec only lists properties + portfolio +
     new/existing (roles arrive later in step 4). Either add roles to the step-2
     ticket spec or adjust the triage expectation, otherwise triage will bounce
     tickets CS thinks are complete.
  5. **Name ID wording in Section 3a is confusing**: "your IdP sends the user's
     email or any other identifier as their unique identifier but the field needs
     to be `email`" — "or any other identifier" contradicts the troubleshooting
     table (Name ID must exactly match the Canary email). Tighten to: Name ID must
     be the user's email, format EmailAddress.
  6. **Case-sensitivity is easy to misread**: Section 4 says the `hotels` attribute
     *values* are case-insensitive, while a nearby callout says attribute *names*
     are case-sensitive. Correct, but worth one sentence making the name-vs-value
     distinction explicit since the blockers table only mentions names.
  7. Minor: `hotel_roles` is headed "colon-separated" but then allows `:`/`;`/`__`
     separators — pick one to recommend; Section 4 roles mapping table has an empty
     Permissions column; Playbook "flow at a glance" step 5 (Testing) has empty
     CS/Engineering cells; hub "Who does what" (6 phases) near-duplicates the
     Playbook table (7 steps) with different numbering — drift risk, consider
     keeping only one canonical; Playbook footer says "Owner: TBD".

  Not done (needs your call):
  - No reply posted to Slack (external-write rule). Happy to draft a reply to
    Lautaro's thread from the above if you want.
  - Monday session on SSO docs + SSO Diagnostics Tool: invite is in the same
    thread; no calendar action taken — accept/decline is yours.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1781122174466579
tags:
- morning-gtd
- slack
time_minutes: 15
title: Skim Lautaro's reworked SSO onboarding docs and give feedback
updated: 2026-06-11 14:44:05.998714
waiting_on: null
waiting_since: null
working_on: false
---

Lautaro reworked the SSO docs after two confusing customer integrations (hub + CS Playbook + Setup Guide) and @eng-enterprise asked for a skim. Also invited a Monday session on this + SSO Diagnostics Tool.
https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1781122174466579