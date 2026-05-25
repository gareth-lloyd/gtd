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
output: "## Agent run 2026-05-21T13:08:00\n\nRead Gmail thread 19e2bffa5b44b917 (17
  messages, May 15–20). You are CC'd\nthroughout, never on the To line. The active
  Canary owner was **Lautaro\nMena** (not Luis — likely a misread in the task title),
  who is OOO this\nweek and on May 15 said \"someone else from my team will continue
  this\nintegration in my place.\" Since May 18 the thread has been driven by\nCanary
  Concierge / support (Lyn Chua, Anna Hartwell, Anastasia Yudina,\nMarc) via ticket
  177929, with engineering fixing user-provisioning\nerrors as they're reported.\n\n###
  Where the thread sits (latest = Miles, 2026-05-20 13:59 UTC)\n\n- Miles set the
  cutover ask on **May 18**: target Go-Live **June 1**,\n  force SSO-only auth, and
  run a Teams meeting during cutover for instant\n  rollback. **No one from Canary
  has explicitly confirmed June 1 or the\n  cutover-call logistics yet.**\n- Support
  acknowledged the user-error reports and fixed the first five\n  users. Miles has
  since reported three more waves:\n  Aaron/Mackenzie/Ranj/Sierra, then Shawn McMahon/Kelly
  Miller/Gabriel\n  Hudson, then Sofia Jones/Lloyd Eksteen.\n- Miles's last open question:
  \"Any other insight you all can provide\n  here for my team or should they just
  keep trying and reporting when\n  it fails?\" — i.e., is there a deterministic way
  to identify which\n  users will fail before testing? No reply yet.\n\n### What's
  actually on your plate\n\nStrictly by To/From lines, nothing — support owns the
  ticket and Lautaro\nowns the integration. But two items deserve eyes-on while Lautaro
  is out:\n\n1. **Confirm June 1 cutover + schedule the rollback call.** Date\n   commitment
  to the customer that hasn't been formally returned by\n   anyone with authority.
  Worth a one-liner to Lautaro's backfill / CSM\n   to make sure it lands before he's
  back.\n2. **The systemic provisioning question.** Engineering keeps fixing\n   users
  one-by-one; Miles is asking whether there's a bulk/pre-flight\n   check. If there's
  a root cause (e.g. email mismatch between Entra\n   and Canary User), shipping a
  list or pre-cutover audit script beats\n   triage-by-email. This is the one item
  in the thread that needs\n   engineering thinking rather than support.\n\n### Suggested
  action (NOT taken — for your decision)\n\nLikely a short internal nudge, not an
  external reply:\n- Slack/email Lautaro's backfill + the CSM: \"June 1 cutover is
  on the\n  table for Archer/Lodgeworks. Make sure we confirm the date + book the\n
  \ rollback call, and that someone owns the user-provisioning sweep\n  before then.\"
  Converts this from a Gareth-reply task into a\n  coverage-check task, consistent
  with you being CC.\n- Nothing in the thread is explicitly addressed to you that
  requires a\n  direct external response.\n\nNo external messages sent.\n"
project: 2026-04-16T1210-unblock-team
source_id: gmail:thread:19e2bffa5b44b917
tags:
- morning-gtd
- gmail
time_minutes: 5
title: 'Reply to Miles (Lodgeworks/Archer SSO) re: integration cutover next steps'
updated: 2026-05-22 14:41:52.402052
waiting_on: null
waiting_since: null
working_on: false
---

Miles: 'This is working! Next steps: send link to field, draft cutover communication, schedule a time…' Luis Mena replied last; check whether anything is on my plate.