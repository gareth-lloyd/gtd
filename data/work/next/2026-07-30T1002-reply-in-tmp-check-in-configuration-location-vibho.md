---
area: null
contexts:
- react
created: 2026-07-30 10:02:02.163557
defer_until: null
due: 2026-07-30
energy: medium
id: 2026-07-30T1002-reply-in-tmp-check-in-configuration-location-vibho
order: null
output: |
  ## Agent run 2026-07-30T13:10

  Read the full #tmp-check-in-configuration-location discussion (channel C0BKDAG8FMY).
  Context: Vibhor's message (https://canarytechnologies.slack.com/archives/C0BKDAG8FMY/p1785352659575199)
  answered your context questions — post-setup tweaks are frequent, CS needs a superset
  of hotel-user features, and he's OK with adminland if Canary staff get elevated access
  without extra hoops. Blake's directives (posted ~3h later, 2026-07-30 01:13 EEST) favor
  adminland as the single surface, impersonation default-disabled with allowlisted safe
  ops, and SAG for sensitive actions — which tensions directly with Vibhor's "no extra
  hoops" ask.

  DRAFT REPLY (not sent — needs your approval). Suggest posting as a channel-level
  message since the discussion is happening at channel level, not in threads:

  ---
  Thanks Vibhor — that answers the open questions from my side:
  • Post-setup tweaks are frequent enough that we should design for a low-friction CS path, not treat config as one-and-done.
  • CS needs a superset of what hotel users see.

  Combining that with Blake's directives, I think the *location* question is settled: the configurator lives in adminland — hotel users see the limited version, Canary staff see the superset — and /manage stays for internal-only operations.

  That leaves *access* as the one open tension. Blake's principles say impersonation is default-disabled with allowlisted safe operations, and SAG for anything sensitive; Vibhor's ask is no extra hoops for CS tweaks. These meet in one question:

  @Blake — would check-in configurator edits (field mappings, reg card setup, ID consent copy) count as "sensitive, SAG required", or could they be allowlisted as a safe operation? Some of it is guest-facing copy, which feels adjacent to the message-template case you flagged.

  If SAG is required, then Vibhor's cycle-time concern points at making the grant fast/automated (per your point about automating common use-cases) rather than weakening the gate.
  ---

  Note: the @Blake mention would need his Slack ID (ULMSUBGGM) formatted as <@ULMSUBGGM>
  when sending. Say "send it" (optionally with edits) and I can post it, or you can paste
  it into Slack yourself.
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C0BKDAG8FMY/p1785352659575199
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Reply in #tmp-check-in-configuration-location: Vibhor''s answers on configurator
  permissions'
updated: 2026-07-30 15:12:18.685681
waiting_on: null
waiting_since: null
working_on: true
---

Vibhor addressed my questions by name: CS/admin needs more access than hotel users; post-setup tweaks are frequent; OK with hotel-admin home if Canary users keep elevated access without extra hoops.
https://canarytechnologies.slack.com/archives/C0BKDAG8FMY/p1785352659575199