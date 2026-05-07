---
area: null
contexts:
- react
created: 2026-05-06 09:33:02.026732
defer_until: null
due: null
energy: medium
id: 2026-05-06T0933-triage-ent-6128-investigate-hotel-salesforce-oppor
order: 1
output: |
  ## Agent run 2026-05-06T16:15Z

  **Triage of ENT-6128** (Tincho, ENT Triage, Medium, no labels, created 2026-05-05).

  ### What the ticket asks
  Spike — not implementation. Investigate associating hotels with a Salesforce **opportunity ID** (in addition to / instead of account ID) to handle rebrand cases (e.g. Marriott → Stonebridge) without resorting to duplicate Salesforce accounts that SF's dedupe automation may silently delete. Affects MVW, Pyramid, Stonebridge. Onboarding-team-owned per Roland's Notion feedback #5. Related: ENT-5943 (auto-disable `has_tipping`).

  ### Repo signal Tincho may not have factored in
  The data layer already supports the proposal in large part:

  - `backend/canary/onboarding/migrations/0140_salesforceopportunity.py` — `SalesforceOpportunity` model exists with `salesforce_opportunity_id` (unique, 18 chars), `parent_opportunity_id`, FK `salesforce_hotel_account → SalesforceHotelAccount` (related_name `opportunities`). One-to-many account→opportunities is already modeled.
  - `onboarding_type` on the opportunity already encodes per-product/per-brand variants: `marriott_tipping`, `mvw_tipping`, `stonebridge_tipping`, `pyramid_tipping`, `wyndham_msa`, `ihg_msa`, etc. So per-opportunity onboarding metadata is in place.
  - `Hotel.salesforce_account_id` is wrapped in `deprecate_field(...)` at `backend/canary/hotels/models/company.py:23` — hotel-level account ID is already on a deprecation path; this ticket is the natural follow-up to settle what replaces it (or what supplements it).
  - `salesforce_account_id` is still actively read across `monitoring/`, `salesforce/`, `tmp/onetime/`, `tmp/repeatable/wyn/`, etc. — a non-trivial consumer surface to consider in option (b)/(c).

  ### Triage call
  - **Priority**: Medium is right. Recurring CS toil for rebrand-heavy enterprise portfolios; not user-facing degradation.
  - **Owner**: keep with Onboarding (Tincho/Roland). No reason to pull into ENT execution.
  - **Scope**: well-shaped as a research ticket. Acceptance criteria are clear. No labels, no project — Tincho may want to attach it to an Onboarding initiative if one exists.
  - **Build vs. don't**: don't pre-judge — the spike is the point. But my prior, given the data layer above, is option **(c)**: model the rebrand explicitly (e.g. opportunity becomes the unit for tipping/dashboard provisioning *without* fragmenting cross-product dashboards — the account remains the cross-product anchor, the opportunity is the per-contract slice). The existing `SalesforceOpportunity ↔ SalesforceHotelAccount` shape already implies this.

  ### Drafted Linear comment (NOT POSTED — needs approval)
  > Worth flagging that the data model is partially in place already: `onboarding.SalesforceOpportunity` (migration 0140) is keyed by `salesforce_opportunity_id`, FKs to `SalesforceHotelAccount` (related_name `opportunities`), and already carries the per-product onboarding metadata (`onboarding_type`, `go_live_date`, `deployment_segment`, etc.). And `Hotel.salesforce_account_id` is already wrapped in `deprecate_field`, so the hotel-level account ID column itself is on the way out. So the spike is mostly about: (1) which provisioning paths should switch from "lookup by account" to "lookup by opportunity," and (2) how to keep cross-product dashboards coherent when one account legitimately has two opportunities. Happy to pair on the writeup if useful.

  ### Action for me
  None — research ticket owned by Onboarding. No follow-up on my plate. Ready to archive once user confirms.
project: 2026-04-10T0840-ticket
source_id: https://linear.app/canary-technologies/issue/ENT-6128/investigate-hotel-salesforce-opportunity-association-for-rebrands
tags:
- morning-gtd
- linear
time_minutes: 15
title: 'Triage ENT-6128: Investigate hotel ↔ Salesforce opportunity association for
  rebrands'
updated: 2026-05-06 16:15:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

Tincho, ENT team Triage. https://linear.app/canary-technologies/issue/ENT-6128/investigate-hotel-salesforce-opportunity-association-for-rebrands