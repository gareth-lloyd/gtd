---
area: null
contexts: []
created: 2026-07-21 12:05:23.120983
defer_until: null
due: null
energy: low
id: 2026-07-21T1205-find-guest-profile-prd-from-kevin-li
order: null
output: |
  ## Agent run 2026-07-21T14:53

  **Found it — the "guest profile" PRD:**

  - **PRD: Guest Profiles** — https://app.notion.com/p/27681468615180f8a62eed8ae716b758
    - Best match. A full product requirements doc to let returning guests store
      personal info, ID, payment, and preferences in a secure Guest Profile for
      one-click / faster check-in.
    - Last edited ~2026-05-13 (~2 months ago).

  **Caveat on authorship:** Kevin Li's name is NOT in the page's metadata/properties,
  so I could not directly confirm he authored it. He shows up as a Canary product
  leader in adjacent search results, but treat "authored by Kevin Li" as unverified —
  worth a quick confirm with him or by checking the page's edit history.

  **Companion working docs (same feature):**
  - Guest Profiles / Guest Profiles (1) — https://app.notion.com/p/33e81468615180f6a3b5f12673d5182d
    (most recently edited 2026-07-16). Use the PRD above as canonical.

  **Key contents / decisions in the PRD:**
  - Unique identifier = Email + Name + hotel/brand; profiles stored at hotel level
    (brand/group level only with explicit buy-in).
  - Hotel/brand owns the data (controller); consent + MFA required at creation;
    profiles do NOT cross US/EU/APAC environment boundaries; no auto-linking of past
    reservations without explicit guest action.
  - MVP = guest-facing flow only, one brand/group, basic info + auto-fill + opt-in;
    staff UI and loyalty integrations are Phase 2+.

  **Open / TBD:** monetization, privacy/security, compliance (PCI, regional), and
  whether to integrate with PMS profiles. GTM proposed as a Capella-style pilot.

  Source: Notion (via notion-context skill).
project: null
source_id: null
tags: []
time_minutes: 5
title: Find guest profile PRD from kevin Li. GDPR consider
updated: 2026-07-21 14:53:48.713
waiting_on: null
waiting_since: null
working_on: false
---