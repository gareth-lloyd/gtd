---
area: null
completed_at: 2026-10-29 14:26:52.618679
contexts:
- react
created: 2026-10-28 11:10:00.626333
defer_until: null
due: null
energy: low
id: 2026-10-28T1110-reply-to-ian-clark-re-capability-bot-pmsexpert-age
order: null
output: "## Agent run 2026-10-29 14:08:09\n\nSource: Ian's DM (https://canarytechnologies.slack.com/archives/D071KNA6UQ1/p1793109375373269)
  links https://github.com/canary-technologies-corp/agents/tree/main/overlord/src/agents/pmsexpert.
  Read from origin/main @ 634d7a60 (2026-10-29). Your local ~/projects/canary-agents
  checkout is stale (Sep 24) and has no pmsexpert dir; I did not pull it.\n\n### TL;DR\nThe
  \"capability bot\" is the **PMS Expert** Slack agent (slug `pmscapabilities`, bot
  U0AEBAKLMPS) in the overlord agents server. It answers colleagues' questions about
  Canary's PMS integrations (what a PMS supports, what that means for a product, partner/Open
  API onboarding, project status) by fanning out to four read-only researcher sub-agents
  (code, Notion KB, Linear, Groundcover), then writes a short non-engineer answer
  with a source line. It also runs a feedback loop (\U0001F44D/\U0001F44E, corrections,
  nightly miner, weekly review by Ian) that edits the KB. Ian built it alone; all
  PMS-114xx commits, Oct 23–29, so it's ~1 week old and still under active rollout.\n\n###
  Overview\n- **Triggers** (routing.ts): @-mention, DM or API call -> always answers
  in-thread. Plus unprompted top-level posts in #product-questions (C01V4NYTQRH) ->
  go through a cheap **gate** LLM (gate-prompt.md) that says YES/NO on \"is this a
  PMS-capability question?\". It says NO to bugs, one-hotel problems, tasks, announcements,
  mobile key/brand/POS questions. Edits are ignored so it never answers twice.\n-
  **Politeness:** if the gated post @-asks a human who isn't a PMS owner, it waits
  15 min and stays quiet if anyone replied or reacted. If the post asks another bot,
  it stays out.\n- **Coordinator** (agent.ts + expert-prompt.md, max 10 steps) calls
  researcher tools, each a sub-agent with its own prompt and 20-step budget (subagents.ts):\n
  \ - `askCode`: code search plus the `pmsCapabilities` tool (an hourly-cached capability
  matrix in overlord/src/tools/pms-capabilities). Treated as the most authoritative
  for \"is it implemented\".\n  - `askKnowledgeBase`: PMS Gateway Notion KB (quirks,
  flags, vendor docs, contacts)\n  - `askLinear`: projects, owners, roadmap. Read-only
  is enforced in code: mutations are refused.\n  - `askGroundcover`: production logs,
  for \"what does the vendor actually send\" and \"do live customers use it\"\n  If
  it runs out of steps, a no-tools \"write-up\" call builds the answer from the findings
  gathered so far.\n- **Answer style:** about 100 words, plain English, Yes/No only
  for yes/no questions, readable setting names with admin page links, Linear links,
  one source sentence (\"Verified in the codebase.\"). It never speculates on timelines,
  makes commitments, repeats commercial details or diagnoses live hotel problems;
  those get pointed to a ticket or an owner.\n- **Owners** (owners.ts): code, not
  the model, turns `@name` into a Slack ping, and only for listed PMS owners, so the
  bot can't ping random people.\n- **Playbooks** (playbooks/*.md): per-topic answer
  checklists the agent reads on demand. Topics: project-status (owner Mal), feature-request,
  new-integration, open-api, roadmap/certification, vendor-access (docs, sandboxes,
  contacts).\n- **Feedback loop** (FEEDBACK-LOOP.md; feedback*.ts, reactions.ts, miner.ts,
  correction-judge.ts, review-queue.ts, disputes.ts, digest.ts, apply.ts):\n  - Every
  answer is logged to Supabase (`pms_expert_answers`).\n  - A \U0001F44E privately
  asks the reactor what was wrong.\n  - Replies such as \"that's wrong, Mews posts
  to folio 1\" are recorded as feedback and get a fixed thank-you.\n  - A nightly
  miner has an LLM judge read thread replies for corrections and drafts items into
  a Notion \"PMS Expert Review\" DB.\n  - Ian gets a weekly DM digest and decides
  each item. Approved items either become \"Learned notes\" under the KB root (indexed
  hourly) or **dispute** a bad KB entry, which hides it from answers until it is edited.\n-
  **Cost tracking:** spend is summed across the gate, coordinator and sub-agents and
  logged per answer.\n\n### Examples (what it would do)\n1. \"@PMS Expert does Mews
  support posting payments to the folio?\" -> askCode + askKnowledgeBase in parallel
  -> \"Yes, … except … (KB quirk). Verified in the codebase and the PMS Gateway Knowledge
  Base.\"\n2. Unprompted post in #product-questions: \"Can upsells post charges back
  to the PMS for hotels on arrival reports?\" -> gate YES -> \"No. Upsells from an
  arrival report cannot post back to the PMS…\"\n3. \"What's the status of the HotelKey
  integration?\" -> project-status playbook -> askLinear -> linked Linear project,
  its lead, the project Slack channel, current status with the date of the latest
  update, and the target date only if Linear records one.\n4. \"Do we integrate with
  <unknown PMS>? Customer wants it.\" -> new-integration playbook -> says it's unsupported,
  explains the request route, names the owner. It makes no commitment.\n5. \"Hotel
  X's reservations aren't syncing\" -> gate NO (a bug or one-hotel problem), so it
  stays silent. If @-mentioned directly, it declines to diagnose and points to a ticket.\n6.
  \"Which RoomBoss fields come from the Registration Card?\" -> no leading \"Yes\":
  \"RoomBoss receives these Registration Card fields: …\"\n7. Thread reply \"this
  was about mobile key, not PMS\" -> recordFeedback -> fixed thank-you -> goes to
  the miner and Ian's weekly review.\n\n### Relevance to you / possible reply angles\n-
  Overlap with your agent-context and settings field guide work: it answers \"what
  does a PMS support\" from code plus a capability matrix, and has the same KB-plus-review-loop
  shape. The weekly human review gating KB changes may be worth borrowing.\n- Draft
  ack (NOT sent): \"Thanks Ian, read through pmsexpert. Nice shape: gated #product-questions
  with the 15-min traction wait, read-only researcher sub-agents, and the miner ->
  review -> KB disputes loop. Is the pmsCapabilities matrix generated from Gateway
  code, or maintained by hand?\""
project: null
source_id: https://canarytechnologies.slack.com/archives/D071KNA6UQ1/p1793109375373269
tags:
- morning-gtd
- slack
time_minutes: 10
title: summarize what pmsexpert agent link is and does
updated: 2026-10-29 14:26:52.618675
waiting_on: null
waiting_since: null
working_on: false
---

Answering your request for a TLDR on the "capability bot", Ian sent agents/overlord/src/agents/pmsexpert. Read it and acknowledge.
https://canarytechnologies.slack.com/archives/D071KNA6UQ1/p1793109375373269

Give me a tldr, an overview and some examples