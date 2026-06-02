---
area: null
contexts:
- consume
created: 2026-05-31 07:53:13.184601
defer_until: null
due: null
energy: low
id: 2026-05-31T0753-read-archer-sso-handover-doc-lauta-pto-may-june
order: null
output: "## Agent run 2026-06-02T14:21:54\n\nRead the Archer SSO section of Lauta's
  handover doc + the Slack thread that announced it.\nSources: Slack thread C08RJU9Q7FV
  / 1779993073.788129 (Lauta, 2026-05-28) and Notion\n\"\U0001F510 SSO Integrations
  — Handover (Lauta PTO, May–June 2026)\" (page 36181468...dfe0c).\n\n### TL;DR —
  Archer cutover already executed (doc is slightly behind reality)\nThe doc targets
  the force-SSO cutover for \"June 1 via a live call\". The Slack thread shows it\nactually
  happened around then:\n- 2026-05-29: Lauta ENABLED JIT user provisioning (`jit_provision_users=True`)
  on Archer SSO\n  org 940 (the open decision in the doc was resolved → ON).\n- 2026-06-01:
  Andrea Bradshaw DISABLED password login (`disable_password_login=True`) for the\n
  \ org and emailed the enterprise; asked Ryan (U07N0CW4108) to watch for errors that
  day.\nSo as of today (2026-06-02) Archer is SSO-only with JIT provisioning on. The
  live action item\nis just monitoring the Datadog tail for fallout — note JIT being
  ON carries the documented risk\nthat a new hire who already has a Canary account
  under a *different* email gets a fresh empty,\npermission-less account (merge only
  happens on exact NameID=email match).\n\n### Datadog query (the thing Lauta pinned)\nLive
  tail of error-level POSTs to the Archer SAML ACS endpoint:\n```\n@method:POST @url_name:saml-acs
  @path:\"/sso/saml/acs/archer\" -status:(warn OR info)\n```\nStream view, count agg,
  sliding window. This + the \"SSO Login Attempts\" table on the org's\nadmin page
  are the two places to read failure reasons.\n\n### Archer config (for reference)\n-
  Linear: ENT-6164 (reopened 2026-05-28 for cutover). Slug: `archer`. IdP: Microsoft
  Entra\n  (Azure AD), SAML 2.0. Auth-only — no role mapping / no auto hotel assignment.\n-
  SSO org admin: /canary-admin/sso/organization/940/change/\n- 7 properties in the
  org: Archer Tysons(2536), Redmond(2535), New York(2534), Burlington(2533),\n  Florham
  Park(2532), Austin(2531), Napa(1316). Users on @archerhotel.com / @lodgeworks.com.\n-
  Prior incidents (root-caused & resolved 2026-05-26): (1) 2 hotels missing from the
  SSO scope;\n  (2) 3 users with duplicate Canary accounts (kimberly.lopez / issac.zelaya
  / jordan.medeiros\n  @archerhotel.com) — consolidated, should re-test. 12 users
  affected May 18–26; details in\n  Zendesk #177929.\n- Troubleshooting a failed login,
  check in order: email domain → user exists & is_active →\n  user's hotel is one
  of the 7 → no duplicate account.\n- Contacts: customer IT POC Miles Patterson (Zendesk
  #177929); coordinator Wafa Kacem;\n  Canary CS Marc Javillonar / Tim Asuncion; support
  Justin Blose / Jacob Jones.\n\n### Doc also covers (FYI, not in scope of this task
  but worth knowing)\n- Hyatt (ENT-6185, Connor Swords): sandbox+prod orgs 973/974
  created, BLOCKED on Hyatt IdM\n  returning metadata XML; 3 pilot hotels not yet
  attached. Gareth = escalation, confirmed SAML\n  over OIDC.\n- Caesars (no Linear
  ticket; Okta/SAML, orgs 907/908): sandbox metadata+role mappings loaded,\n  no hotels
  attached, waiting on customer testing. CSM Dianna Kertz; Andrea shadowing.\n\nAction
  for me: nothing required — cutover is done and owned (Andrea executed, Ryan monitoring).\nJust
  be aware I'm the named SSO escalation for Hyatt + Caesars during Lauta's June 1–5
  PTO.\n\n## Agent run 2026-06-02 — Datadog check (ran the pinned query)\n\nRan `@method:POST @url_name:saml-acs @path:/sso/saml/acs/archer` over the last 5 days.\nVolume: 1423 info (successful logins), 7 warn, 10 error. The warns share the same trace_ids\nas the errors, so the 10 error lines = ~8 distinct failed requests, reducing to 3 underlying\nissues — none an active system fault:\n\n1. jason.wade@lodgeworks.com — \"New user tried to log in but user provisioning is not enabled\"\n   (HTTP 500), May 29 ~15:05–15:06 UTC. This was BEFORE Lauta flipped jit_provision_users=True\n   later that day; enabling JIT is exactly the fix. No recurrence after. RESOLVED.\n2. archerallisonknight — cannot_record_login_no_hotel, one occurrence May 29 21:01 UTC.\n3. archerjenaeliaiga — cannot_record_login_no_hotel, retried 5x on cutover day June 1\n   (16:51 → 18:28 UTC). SSO auth succeeds but the user has no hotel association in the org,\n   so login cannot be recorded → effectively locked out. This is the doc's documented failure\n   mode (the user-hotel-in-org check).\n\nHealth verdict: last error/warn was June 1 18:28 UTC; nothing since (~17h clean as of this run),\nwith successful logins continuing (latest info June 2 03:22 UTC). Cutover is stable; no code\nerrors post-JIT.\n\nOnly possible loose end: confirm someone (Ryan/Andrea, who were monitoring) attached\narcherjenaeliaiga to one of the 7 hotels — that user was still failing at end of cutover day.\nEverything else is clean.\n"
project: null
source_id: https://canarytechnologies.slack.com/archives/C08RJU9Q7FV/p1779993073788129
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 15
title: Read Archer SSO handover doc (Lauta PTO May/June)
updated: 2026-06-02 14:31:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

Lauta updated the SSO Integrations Handover doc for his PTO; Archer SSO section + Datadog query.
https://canarytechnologies.slack.com/archives/C08RJU9Q7FV/p1779993073788129