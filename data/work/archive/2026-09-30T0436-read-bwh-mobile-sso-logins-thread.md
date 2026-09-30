---
area: null
completed_at: 2026-09-30 13:50:31.952255
contexts:
- react
created: 2026-09-30 04:36:30.044160
defer_until: null
due: null
energy: medium
id: 2026-09-30T0436-read-bwh-mobile-sso-logins-thread
order: null
output: |
  ## Agent run 2026-09-30T13:30:00
  Read the thread (28 replies, 2026-09-28/29) and the resulting Linear ticket. Note: the thread does NOT mention Jason from BWH logging in with SSO; that claim in this item's body must have come from elsewhere.

  **Question Mike Hu asked:** do BWH SSO users have to log in on web before mobile SSO works? Context: BWH conference starts Oct 26 and Mike wants max staff-app signups there.

  **Answer (Renan S Moreira, Lauta):** yes. Brand-new users must log in via web first. It is a backend limitation: with no existing user record, the backend cannot tell from an email whether the person should be routed to SSO. The app itself does not block anything (Diana Perez Afanador).

  **Connor's persona split (rough guess):** ~60% already logged in on web (served today), ~20% have BWH SSO but never logged in on web (blocked), ~20% not yet provisioned in BWH IdP (provision at conference, then same as bucket 2). Caitlyn noted the 60% is likely lower for owners specifically, and BWH owners are often the GM.

  **Options discussed:**
  - Pre-create Canary users from a BWH attendee list (name + email). Lauta: feasible but prefers a reusable solution.
  - QR code that deep-links the staff app straight into the BW SSO login flow (Lauta's suggestion). Mike and Connor prefer this; Mike sees it as a precursor to QR magic-login for staff generally.

  **Decision:** QR approach chosen. Linear STAFF-257 (https://linear.app/canary-technologies/issue/STAFF-257/open-best-western-sso-in-the-staff-app-via-qr-code), Staff Ops, High, status Triage, assigned to Diana Perez Afanador (possibly plus a mobile eng). Target: next cycle (~1 week). Requirements: QR downloads the app if not installed, deep-links if installed, plus fallback direct URLs for sales. Open question: separate QRs for iOS vs Android? Caitlyn flagged Diana is also on push notifications this week and wants to sanity-check priority.

  **Relevance to me:** none direct. The backend limitation (unknown email cannot be routed to SSO) is the real gap; the QR is a workaround that sidesteps the email step. Nothing asked of Gareth in the thread.

  Thread: https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1790612702904389?thread_ts=1790612702.904389&cid=C0AN8AQ49UG
project: null
source_id: https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1790612702904389?thread_ts=1790612702.904389&cid=C0AN8AQ49UG
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 15
title: Read BWH mobile SSO logins thread
updated: 2026-09-30 13:50:31.952249
waiting_on: null
waiting_since: null
working_on: false
---

Mike Hu in #epd-staff-app: thread on mobile SSO logins for BWH, 28 replies. Jason from BWH was able to log in with SSO.
https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1790612702904389?thread_ts=1790612702.904389&cid=C0AN8AQ49UG