---
area: null
completed_at: 2026-09-17 10:10:34.234994
contexts: []
created: 2026-09-16 19:31:41.535730
defer_until: null
due: null
energy: low
id: 2026-09-16T1931-workup-agent-sync-digest
order: null
output: |
  ## Agent run 2026-09-16T21:45+03:00

  **Sources**
  - Gemini notes email: https://mail.google.com/mail/u/0/#inbox/1a0ab0733ba7ed92
  - Full notes + transcript doc (owner Laura DeWald): https://docs.google.com/document/d/1GtLo6uum3q_SWjI9qxr3FgSSAw3Z9lQyP-x6sVUvxas/edit
  - Attendees who spoke: Blake Vanlandingham, Laura DeWald, Asher Davidson, Jason Flax, Matias Marco del Pont, Dylan Moradpour, Stephanie Barry. Gareth was invited but did not speak; nothing was assigned to Gareth.

  **Digest (32 min call, 2026-09-16 08:30 PDT)**

  1. SQL access for Workup via Canary MCP (Asher, ~00:01-00:11, 00:25-00:31)
     - Dev started last week. Blocker: the agreed Pomerium auth design is only on Pomerium main, not in a release. Workaround adopted: single token passed through to Django, authenticated in Django (same approach as Devon). Still authenticated, just not Pomerium JWT.
     - Late design feedback from Bernard on the edge design; Asher expects only minor changes.
     - ETA: "hopeful within the next few weeks". Sam is helping Asher.
     - Architecture: read-only SQL tool exposed through Canary MCP, restricted to Workup only. Controls are deterministic (table/column allowlists, no blanket queries, no password hashes / SMS verification codes / API creds) plus an LLM query reviewer. Security team is comfortable with the trade-off.
     - Jason pushed back on raw SQL vs preconfigured views. Dylan and Blake defended it: the long tail of one-off MCP tools was too costly (people asked, then didn't reuse for months), and raw SQL mirrors how engineers actually investigate (e.g. joining payment -> payment intent -> Stripe state with groundcover). Decision stands.
     - Blake: since Workup already has Snowflake access, events do NOT need to be a separate Canary MCP tool.
     - Asher to share the SQL design doc with Jason.

  2. Twilio as a data source (Matias, ~00:10-00:11)
     - Twilio logs are a frequently used secondary source for messaging triage. Only billing data reaches Snowflake; raw logs need the Twilio API (Twilio has an MCP).
     - Not a blocker, but needed to "complete the picture". Laura owns reaching out for access.

  3. Workup triage accuracy (Laura, ~00:12-00:22)
     - Judge model is fairly accurate; next-step accuracy is 16/43 (~23%) on the buckets.
     - Biggest miss: Workup suggests a code fix for tickets that humans then close as duplicates of an existing ticket. Likely causes: it stops once a code fix looks possible, and it may not search far enough back (duplicates were ~2000 issues older).
     - Matias's view: duplicates are rare (a few per week; last week's 7 were inflated by an incident that spawned ~5 tickets). Most effort should go to "expected behavior" / config-change tickets, which are the bulk: messaging tickets are mostly "why did the AI do X" (check logs, add KV item, tweak service ticket, close), and ~70% of Comscore tickets are scheduled-message start/end window checks.
     - Laura: bucket definitions make accuracy hard to measure (humans close unsupported requests instead of filing feature requests; Workup may be "right" but differ from the human).
     - Agreed focus: use Linear ticket history to find related/canonical tickets and reuse prior resolutions. Messaging already keeps canonical tickets for AI limitations / unsupported requests.
     - Common pattern Matias flagged: "messaging not working" tickets where Twilio was never configured; trivially answerable via SQL. Laura has an existing ticket to add messaging status to the hotel agent-context object; Blake wants that done regardless of SQL.

  4. Agent decomposition (Jason, ~00:22-00:25)
     - Jason suggested splitting Workup's broad investigate+triage duty into focused sub-agents. Laura: sub-agents already exist, the pipeline was recently refactored from a giant prompt into code, and Orbital may fit here. Laura and Jason to discuss; Blake framed this as forward-looking, not immediate.

  **Action items (as recorded; none for Gareth)**
  - [Asher] Share the SQL tool design doc with Jason.
  - [Laura] Reach out about Twilio log/API access requirements.
  - [Laura] Add a duplicate-ticket check before Workup suggests a code fix; investigate lookback window.
  - [Laura, Jason] Discuss decomposing Workup into focused sub-agents (Orbital).
  - [Laura] Add messaging status data to the hotel agent-context object (existing ticket).
  - [Laura] Progress the Django-side SQL integration (Blake's closing assignment).

  **Possible relevance to Gareth (not discussed on the call)**
  - The hotel agent-context messaging item maps to shared.agent_context providers in backend/canary (there is a backend:add-agent-context-provider skill). Worth checking whether Laura's ticket overlaps ENT messaging-config work.
  - The Twilio config gap Matias described ("Twilio never set up") is adjacent to the sms_phone normalisation issue already in memory; a hotel-level messaging-status check in agent context could surface both.
  - The read-only SQL tool decision affects how Workup handles ENT-style tickets; if the ENT triage playbook (agent-plugins/claude-plugins/enterprise/commands/work-ticket.md) assumes MCP tools only, it may need a note once the SQL tool lands.
project: null
source_id: null
tags: []
time_minutes: 5
title: workup agent sync call digest from email  - read transcript from today
updated: 2026-09-17 10:10:34.234984
waiting_on: null
waiting_since: null
working_on: false
---