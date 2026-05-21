---
area: null
contexts:
- react
created: 2026-05-21 09:29:44.762630
defer_until: null
due: 2026-05-21
energy: high
id: 2026-05-21T0929-reply-to-miles-lodgeworks-archer-sso-re-integratio
order: null
output: |
  ## Agent run 2026-05-21T13:08:00

  Read Gmail thread 19e2bffa5b44b917 (17 messages, May 15–20). You are CC'd
  throughout, never on the To line. The active Canary owner was **Lautaro
  Mena** (not Luis — likely a misread in the task title), who is OOO this
  week and on May 15 said "someone else from my team will continue this
  integration in my place." Since May 18 the thread has been driven by
  Canary Concierge / support (Lyn Chua, Anna Hartwell, Anastasia Yudina,
  Marc) via ticket 177929, with engineering fixing user-provisioning
  errors as they're reported.

  ### Where the thread sits (latest = Miles, 2026-05-20 13:59 UTC)

  - Miles set the cutover ask on **May 18**: target Go-Live **June 1**,
    force SSO-only auth, and run a Teams meeting during cutover for instant
    rollback. **No one from Canary has explicitly confirmed June 1 or the
    cutover-call logistics yet.**
  - Support acknowledged the user-error reports and fixed the first five
    users. Miles has since reported three more waves:
    Aaron/Mackenzie/Ranj/Sierra, then Shawn McMahon/Kelly Miller/Gabriel
    Hudson, then Sofia Jones/Lloyd Eksteen.
  - Miles's last open question: "Any other insight you all can provide
    here for my team or should they just keep trying and reporting when
    it fails?" — i.e., is there a deterministic way to identify which
    users will fail before testing? No reply yet.

  ### What's actually on your plate

  Strictly by To/From lines, nothing — support owns the ticket and Lautaro
  owns the integration. But two items deserve eyes-on while Lautaro is out:

  1. **Confirm June 1 cutover + schedule the rollback call.** Date
     commitment to the customer that hasn't been formally returned by
     anyone with authority. Worth a one-liner to Lautaro's backfill / CSM
     to make sure it lands before he's back.
  2. **The systemic provisioning question.** Engineering keeps fixing
     users one-by-one; Miles is asking whether there's a bulk/pre-flight
     check. If there's a root cause (e.g. email mismatch between Entra
     and Canary User), shipping a list or pre-cutover audit script beats
     triage-by-email. This is the one item in the thread that needs
     engineering thinking rather than support.

  ### Suggested action (NOT taken — for your decision)

  Likely a short internal nudge, not an external reply:
  - Slack/email Lautaro's backfill + the CSM: "June 1 cutover is on the
    table for Archer/Lodgeworks. Make sure we confirm the date + book the
    rollback call, and that someone owns the user-provisioning sweep
    before then." Converts this from a Gareth-reply task into a
    coverage-check task, consistent with you being CC.
  - Nothing in the thread is explicitly addressed to you that requires a
    direct external response.

  No external messages sent.
project: 2026-04-16T1210-unblock-team
source_id: gmail:thread:19e2bffa5b44b917
tags:
- morning-gtd
- gmail
time_minutes: 5
title: 'Reply to Miles (Lodgeworks/Archer SSO) re: integration cutover next steps'
updated: 2026-05-21 13:08:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

Miles: 'This is working! Next steps: send link to field, draft cutover communication, schedule a time…' Luis Mena replied last; check whether anything is on my plate.