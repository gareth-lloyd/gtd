---
area: null
contexts:
- consume
created: 2026-06-03 12:19:46.148899
defer_until: null
due: null
energy: low
id: 2026-06-03T1219-read-ent-6326-auto-response-rollout-testing-notes
order: null
output: |
  ## Agent run 2026-06-03T15:02:00

  Read Martin Rodriguez's local-testing writeup for ENT-6326 (posted 2026-06-02
  21:29 EEST, to Andrea). Slack thread has NO replies — just the parent message
  plus 3 attachments (ent6326_local_verify.py, ent6326_verify_b.py, a /manage UI
  screenshot). Reactions: raised_hands, telephone_receiver. The two .py scripts and
  the PNG could not be downloaded (Slack MCP is read-thread only, no file fetch), so
  this digest is from the message body, not the script source.

  ENT-6326 context (from Linear): "Template Auto-Response messages for pilot Best
  Western properties." Auto-response verbiage: "Thank you for contacting us. It
  appears our staff has not seen your message yet. If you'd like immediate help,
  please call our front desk at {Hotel Phone Number}..." Assignee Martin; High
  priority, In Progress; PR #46941; rollout starts with 100 BW properties before
  expanding. Project: "Enterprise Rollout: Best Western Auto-Response Template."

  Martin's four verification paths (all reported passing):
  - A — Calls the rollout handler directly. Confirms it: creates the auto-response
    rule, does NOT double-create, skips hotels with no web chat, and fills in the
    phone number correctly.
  - B1 — Runs through the normal service layer to confirm the plan -> handler
    wiring works.
  - B2 — Runs the whole batch flow with Salesforce faked, to confirm it behaves
    like a real rollout.
  - C — Manual /manage UI run: picked the recipe, confirmed, ran it, rule showed
    up on the hotel. (Screenshot attached.)

  Takeaways / open items for follow-up (NOT acted on):
  - Coverage looks solid across handler, service, batch, and manual layers. Key
    safety behaviors Martin explicitly verified: idempotency (no double-create) and
    skipping no-web-chat hotels — both directly relevant to the ticket's AC about
    not overwriting customized messaging.
  - Ticket AC also asks: how many hotels no longer match expected config, which
    drift is acceptable vs should be reset, and "make sure we don't overwrite any
    customizations." Martin's notes cover the rule-creation path but don't mention
    the customization-preservation / config-drift analysis — worth confirming that's
    handled (possibly in PR #46941) before the 100-property rollout.
  - If the script internals matter, open the two attached .py files directly in
    Slack (ent6326_local_verify.py = path A; ent6326_verify_b.py = paths B1/B2).

  No external writes made. Read-only research only.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1780424962087779
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 10
title: Read ENT-6326 auto-response rollout testing notes (Martin)
updated: 2026-06-03 14:59:28.149416
waiting_on: null
waiting_since: null
working_on: false
---

Martin's local-testing writeup for ENT-6326 auto-response (handler direct, service-layer, full batch w/ SF faked, manual /manage UI). https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1780424962087779