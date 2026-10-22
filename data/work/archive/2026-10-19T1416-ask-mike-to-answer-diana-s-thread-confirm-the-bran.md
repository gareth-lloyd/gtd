---
area: null
completed_at: 2026-10-20 14:01:54.548711
contexts: []
created: 2026-10-19 14:16:24.093409
defer_until: null
due: null
energy: null
id: 2026-10-19T1416-ask-mike-to-answer-diana-s-thread-confirm-the-bran
order: null
output: |
  ## Agent run 2026-10-20T10:00 (local)

  **Nothing left to ask Mike. He answered Diana's thread himself at 01:09 EEST on Oct 20, after this item was captured.** No message was drafted or sent.

  Mike's reply (https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792447754127599?thread_ts=1792399469.150039&cid=C0AN8AQ49UG), "settled in standup":
  1. No Other button for now.
  2. Wenjun to send the full-colour brand icons (may already have).
  3. Brands confirmed: Best Western, Wyndham, Marriott, Hyatt, IHG.

  State of the work as of this run:
  - STAFF-304 (https://linear.app/canary-technologies/issue/STAFF-304) moved to In Review on Oct 19 19:19 UTC. PR #138 (https://github.com/canary-technologies-corp/staff-app-react-native/pull/138) is no longer a draft.
  - The Other path is already out of the PR: commit 8de28c08 "Take the Other email path out of the brand selector" (Oct 19). Diana's Linear comment of Oct 19 18:19 UTC records the scope change.
  - The icon question is moot: commit 53263c8f (Oct 19) replaced the placeholders with the real brand marks rendered to 1x/2x/3x. I pulled the @3x PNGs from the branch and they are the colour brand marks (BW blue, Marriott red, Wyndham blue, World of Hyatt blue; IHG's mark is black by design). No monochrome fallback is needed.

  Loose ends still open on the ticket/PR, none of them blocking the ask in this item:
  - STAFF-304's Requirements > Other section and the "Other -> SSO email -> Next" acceptance criterion are now unmet by design. Diana asked in her Linear comment for them to be re-scoped to a follow-up; nobody has edited the ticket yet. Mike owns the ticket text.
  - Diana flagged the Hyatt asset is the "World of Hyatt" wordmark, not the plain HYATT mark; if the plain mark is wanted Wenjun needs to send that SVG.
  - PR "Not done yet": staging has no SSO application sid (device testing is production-only until Identity registers one), and design hasn't confirmed whether the outline "Sign in with SSO" button stays on the new password step. Also still to confirm with Mike/Identity that the org slugs (best-western, wyndham, marriott, ihg, hyatt) are the intended primaries with JIT provisioning on and a hotel mapping.
  - No end-to-end first-time BW user SSO sign-in on a device build yet. BWH conference starts Oct 26.
project: null
source_id: null
tags: []
time_minutes: null
title: 'Ask Mike to answer Diana''s thread: confirm the brand list and cutting "Other",
  and ship monochrome icons if colour ones aren''t ready.'
updated: 2026-10-20 14:01:54.548706
waiting_on: null
waiting_since: null
working_on: false
---

Diana's thread (Oct 19): https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792399469150039
Thread where Mike agreed to cut "Other" (Oct 16): https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1792141184559999
STAFF-304: https://linear.app/canary-technologies/issue/STAFF-304/staff-app-login-replace-scan-login-qr-with-an-sso-hotel-brand-selector
PR #138 (draft): https://github.com/canary-technologies-corp/staff-app-react-native/pull/138