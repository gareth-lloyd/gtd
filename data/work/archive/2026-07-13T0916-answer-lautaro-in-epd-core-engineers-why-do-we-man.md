---
area: null
contexts:
- react
created: 2026-07-13 09:16:05.858920
defer_until: null
due: null
energy: medium
id: 2026-07-13T0916-answer-lautaro-in-epd-core-engineers-why-do-we-man
order: null
output: |-
  ## Agent run 2026-07-13T11:41:45

  Researched Lautaro's question (thread: https://canarytechnologies.slack.com/archives/C08RJU9Q7FV/p1783711241606869?thread_ts=1783710660.786259&cid=C08RJU9Q7FV). His actual question, refined in the thread: besides SSO, is anything preventing ESA from managing users themselves via the Above Property Dashboard, and why did we start managing them internally?

  ### The answer (well documented in Notion)

  **1. Hard technical blocker: org-level flag.** All ESA-Azure properties (~552 hotels) sit on SSO Organization 379 "ESA (Azure)", which has `disable_user_creation_from_settings = True`. The hotel serializer surfaces this flag (backend/canary/hotels/utils/api/serialize_hotel.py:218) and adminland hides the Add Staff button when it's set (frontend/adminland/src/views/HotelStaff/HotelStaffTablePage.vue:36). It's org-level with NO per-hotel override, so no ESA property or admin can self-serve regardless of role. Only Canary staff can add users (the User Data Import tool bypasses the block only for @canarytechnologies.com creators). Doc: "Adding Staff to an SSO Franchise Property (ESA): Self-Serve Is Disabled, Add Canary-Side" (https://app.notion.com/p/38781468615181adab92f45c35419291).

  **2. Why it was set up this way: ESA corporate wanted centralized control + the SSO migration stalled mid-flight.** ESA is transitioning from u/pass to Azure SSO, but their IdP is NOT sending roles or hotels in the SAML assertions, so auto-provisioning is impossible — Canary took on provisioning for both new and existing users as an interim measure. Corporate user requests also require explicit approval from Keely Wilson (ESA corporate); franchise properties are exempt from that approval but still hit the org flag. Docs: "ESA User Management Process" (https://app.notion.com/p/18f814686151803a8f35cd49d43d075a), "ESA Support Guide (User Access)" (https://app.notion.com/p/27781468615180389d9dc973bf765862).

  **3. Do they have anyone on their side?** Keely Wilson is the ESA-side contact and is supportive, but per the SSO transition pre-work notes, "ESA — we could be 90 before they turn on their integration" (https://app.notion.com/p/canarytechnologies/SSO-Transition-Pre-work-Tuesday-30a814686151804ba9e5d774d39ba154). Also, many "ESA" requests are actually third-party management companies (Aimbridge, HSM Hospitality, ESA Management — see ENT-6847/ENT-6848) whose staff aren't in ESA's directory, and would need manual creation even after SSO goes live.

  **4. What would let them self-serve:**
  - (a) ESA finishes the SSO setup on their end and sends roles + hotel site codes in assertions → @extendedstay.com users auto-provision (management-company users stay manual).
  - (b) Flip `disable_user_creation_from_settings` on org 379 — but that's org-wide across all ~552 hotels, not per-hotel. ENT-6581 (https://linear.app/canary-technologies/issue/ENT-6581) is the structural request for exactly this (franchises managing their own Logins). Caveat: existing ESA staff hold legacy GLOBAL roles ("Staff"/"Manager", hotel_id=None) via manual PropertyRoleGrants, which the settings self-serve flow and the import tool can't assign — so role cleanup/migration would be needed too.

  ### Draft Slack reply for Lautaro (NOT posted — needs your approval)

  > Two reasons:
  >
  > 1. Self-serve is deliberately off: ESA's SSO org (379, ~552 hotels) has `disable_user_creation_from_settings=True`, which hides the Add Staff button. It's org-level, no per-hotel override. Details: https://app.notion.com/p/38781468615181adab92f45c35419291
  >
  > 2. ESA is mid-migration to Azure SSO, but their IdP doesn't send roles/hotels, so we can't auto-provision — we manage users manually in the meantime, with Keely Wilson approving corporate requests. We're waiting on ESA to turn on their side. Process: https://app.notion.com/p/27781468615180389d9dc973bf765862
  >
  > Letting them self-serve means flipping the org flag (that's https://linear.app/canary-technologies/issue/ENT-6581) plus cleaning up legacy roles. Note management-company staff (Aimbridge, HSM) aren't in ESA's directory, so they'll stay manual even after SSO.

  ### Posted
  Reply posted to the thread with user approval on 2026-07-13: https://canarytechnologies.slack.com/archives/C08RJU9Q7FV/p1783932410805929?thread_ts=1783710660.786259&cid=C08RJU9Q7FV
project: null
source_id: https://canarytechnologies.slack.com/archives/C08RJU9Q7FV/p1783711241606869?thread_ts=1783710660.786259&cid=C08RJU9Q7FV
tags:
- morning-gtd
- slack
time_minutes: 10
title: 'Answer Lautaro in #epd-core-engineers: why do we manage ESA users internally?'
updated: 2026-07-13 11:47:30.000000
waiting_on: null
waiting_since: null
working_on: false
---

Lautaro asked why we manage ESA (Extended Stay America) users internally / whether anything prevents them self-serving via Above Property Dashboard; Laura deferred to me or Blake (Jul 10). Related triage: ENT-6847/ENT-6848 (Add ESA users).
https://canarytechnologies.slack.com/archives/C08RJU9Q7FV/p1783711241606869?thread_ts=1783710660.786259&cid=C08RJU9Q7FV

Search notion for relevant ESA documentation