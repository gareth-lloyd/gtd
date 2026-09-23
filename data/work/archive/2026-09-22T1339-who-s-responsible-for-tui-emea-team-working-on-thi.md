---
area: null
completed_at: 2026-09-22 13:52:45.358428
contexts: []
created: 2026-09-22 13:39:54.747186
defer_until: null
due: null
energy: low
id: 2026-09-22T1339-who-s-responsible-for-tui-emea-team-working-on-thi
order: null
output: |
  ## Agent run 2026-09-22T14:05:00+03:00

  **Short answer:** TUI is Isaac Sheahan's account (EMEA CS). Yes, the EMEA CS team is the team doing
  Twilio alphanumeric sender-ID registrations, and Isaac was already explicitly assigned TUI BLUE for the
  Spain (CNMC) version of this on Sep 17. Nobody has responded to Twilio's Austrian message yet and
  there is no Linear ticket for a TUI BLUE sender-ID registration in any country.

  **What the Twilio message is** (https://canarytechnologies.slack.com/archives/C079SQR30Q4/p1790018880170299,
  #ext-canary-tech-twilio, Morgan Hall @ Twilio, 2026-09-21): from **Oct 1, 2026** Austrian operators block
  unregistered alphanumeric sender IDs (error 21612, no fallback to long codes). Sub-account
  AC<redacted-twilio-sid>, sender ID "TUI BLUE", needs registering. Twilio offered to submit to
  the Austrian portal themselves if we give them the authorised representative's name + email + gov ID.
  **No thread replies as of this run.**

  **Who owns what**
  - **Isaac Sheahan (EMEA CS)** — TUI's CSM. Runs the weekly TUI sync, owns #tui (C06EVB6BPMX), and in
    #emea-cs on 2026-09-17 posted the Spain/CNMC sender-ID rollout and assigned himself "TUI BLUE, The Mora"
    (https://canarytechnologies.slack.com/archives/C099ES3HX8A/p1789640559318549). That thread has the
    customer email template + CustOps ticket template. Only Sam Stead has reported back in it so far;
    Isaac has not said whether he's emailed TUI for the docs.
  - **Rachel Kim** — Canary-side Twilio/sender-ID programme contact. Raised TUI BLUE + The Mora with Twilio
    for the France requirement on 2026-08-28 (https://canarytechnologies.slack.com/archives/C079SQR30Q4/p1787926974742599),
    asking whether one brand-level submission covers all properties. Thread ended with Twilio (jhrios)
    pointing at senderid-notify@twilio.zendesk.com; no resolution recorded in Slack.
  - **EMEA eng pod (James Saram, Martijn Dekker)** — on TUI for AI Voice / SIP (TUI BLUE Sylt) and Linear
    EMEA-* tickets. Not involved in sender-ID registration; that's a CS/CustOps process, not engineering.
  - **CustOps (Jolly Saracanlao / Cristhian Grijalva)** — execute the Twilio console registration once
    docs are in hand, via a CUSTOPS "Other" ticket per Isaac's template.

  **State of the registrations for TUI BLUE (AC<redacted-twilio-sid>)**
  - France: raised with Twilio Aug 28, no recorded outcome.
  - Spain (CNMC): assigned to Isaac Sep 17, no progress reported.
  - Austria: Twilio notice Sep 21, unanswered. Deadline Oct 1 (9 days).
  - Linear: no CUSTOPS/EMEA ticket mentions TUI BLUE sender ID or Austria/CNMC registration. Only TUI Twilio
    ticket is CUSTOPS-4541 (TUI BLUE Sylt number config, done Jul 30).
  - The same document set (proof of business, legal-rep gov ID, signed LOA) serves all three countries, so
    one ask to TUI covers Austria + Spain + France.

  **Suggested next step (not sent — needs your OK):** reply in the Twilio thread tagging Isaac and Rachel,
  e.g. "@Isaac @Rachel Kim this is the same doc set as the Spain/CNMC ask from last week — can we get
  TUI's authorised rep name/email to Twilio so they can file the Austrian one before Oct 1?" Or a one-line
  nudge in the #emea-cs Spain thread asking Isaac for status on TUI BLUE.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: who's responsible for TUI? emea team working on this?
updated: 2026-09-22 13:52:45.358420
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C079SQR30Q4/p1790018880170299