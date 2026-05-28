---
area: null
contexts: []
created: 2026-05-27 19:56:03.080514
defer_until: null
due: null
energy: low
id: 2026-05-27T1956-marriott-sitch
order: -1
output: |
  ## Agent run 2026-05-28T08:48Z

  **The sitch (ENT-6255 — Courtyard By Marriott Cleveland Independence, hotel 11697):**
  Jacob Jones pinged you + Andrea (comment 606df030): "property appears deactivated,
  not migrated to franchise property. can you assist?" with a screenshot.

  **Bottom line: nothing is broken — the system behaved exactly as you designed it
  in ENT-6117.** There is no automatic "migrate in place" for Marriott. The ratified
  fresh-hotel path is: deactivate/archive the OLD managed hotel (keep it for
  tipping/audit history + portfolio analytics), strip its Salesforce ties to free the
  SF Account, then CS creates a BRAND-NEW franchise hotel via the SFDC Onboarding App.
  "Appears deactivated, not migrated" is the expected intermediate state.

  **Andrea already gave the correct answer** (comment e5f3b96c): a new property must be
  created from a new opportunity; the dashboard can't be reused (preserve Marriott
  managed analytics); users can no longer log in via SSO (managed-only). This matches
  ENT-6117 scope precisely.

  **Andrea's script run is verified-correct** (comment 6705c747, script batch
  3a798200): name → "(Marriott-managed, archived)", slug → "...-marriott-managed",
  still in marriott + atlas portfolios (deliberate, per Taylor Kirchwehm 2026-05-08),
  association IDs removed, active unchecked, tip config can_be_tipped=false + payment
  gateway empty. All five runbook outcomes hit.

  **What you actually need to do:** essentially nothing technical — Andrea has it.
  Your @mention is for confirmation. Optional reply drafted below if you want to close
  the loop. NOT posted (needs your approval).

  **Worth flagging (systemic):** This is the 2nd Marriott managed→franchise ticket from
  Jacob in a row (also ENT-6252) where CS expected an in-place migration. The
  "CS must create a new hotel via the SFDC Onboarding App once the SF Account is freed"
  step is the recurring confusion point. Consider making that step louder in the KB
  runbook ("Marriott Owned-to-Franchised Hotel Transition") so the next handoff doesn't
  re-open as "looks deactivated, did it break?".

  ---
  **DRAFT reply (not posted — approve before sending):**

  > @jacobjones confirming Andrea's right — this is working as designed. For Marriott
  > there's no in-place migration: we deactivate/archive the old *managed* hotel (kept
  > for tipping + analytics history) and the SF Account is now freed, so the next step
  > is for CS to spin up a fresh *franchise* property via the SFDC Onboarding App from a
  > new opportunity. The old dashboard intentionally can't be reused, and the franchise
  > users won't use Marriott SSO. Once the new hotel exists, GM admin access gets sorted
  > there (see ENT-6252 for the account-merge side).
project: null
source_id: null
tags: []
time_minutes: 5
title: marriott sitch
updated: 2026-05-28 12:04:37.521286
waiting_on: null
waiting_since: null
working_on: false
---

https://linear.app/canary-technologies/issue/ENT-6255/managed-to-franchise-transition#comment-606df030