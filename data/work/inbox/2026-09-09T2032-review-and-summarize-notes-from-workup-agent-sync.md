---
area: null
completed_at: null
contexts: []
created: 2026-09-09 20:32:21.164388
defer_until: null
due: null
energy: low
id: 2026-09-09T2032-review-and-summarize-notes-from-workup-agent-sync
order: null
output: |
  ## Agent run 2026-09-09T20:40+03:00

  Source: Gemini auto-notes email "Notes: Workup Agent Sync, Sep 9, 2026" (https://mail.google.com/mail/u/0/#inbox/FMfcgzQhWLRLZThCSkWfbRPCfkNJXMhS). Full notes doc: https://docs.google.com/document/d/1i-IOhiSYeRAbePmuEb51IfIaaxGOw2rhwz95pnkk7KM/edit?tab=t.igx3j47u2zax
  Context: the Sep 2 occurrence was cancelled by Laura DeWald for the all-hands, so this covers ~2 weeks of work.

  ### Summary

  **Platform / plugin progress (last 2 weeks, 45 commits merged)**
  - Next-step judge deployed. Definitions being refined to separate "configuration" actions from "operations" actions.
  - Tool outputs now persisted so runs can be replayed for evals.
  - Zendesk API token errors for gatherers fixed.
  - Investigate plugin split into core + bindings, with a new pipeline added.
  - Laura removed all Devin-related skills from the repo (notes say "Devon"; almost certainly Devin).

  **MCP SQL tool (Asher)**
  - Design approved, build underway.
  - Read-only only, reachable exclusively through the workup agent. Write access explicitly deferred.
  - Overlord auto-records MCP outputs, with size limits that drop oversized payloads.
  - Non-blocking LLM judge added as a second verification layer on query/explain results.
  - Bot auth via bearer tokens validated by Pomerium and Django.
  - Code ownership moved to Internal Tools.

  **Action items**
  - Laura DeWald: send the "comms core checks" PR to Monty for review once ready.
  - Nothing assigned to Gareth in these notes.

  ### Things worth watching
  - The config-vs-operations action definition refinement will shape what the next-step judge allows; worth a look if you have opinions on the boundary.
  - SQL tool being read-only and workup-agent-only is a deliberate blast-radius choice; write access is a future decision, not a plan.

  ### Attendees (calendar RSVPs for Sep 9; actual attendance not recorded)
  - Accepted: Laura DeWald (organizer), gidler, jseporaitis, sbarry, nauzina, mmarcodelpont, adavidson
  - Declined: jbueno, bvanlandingham
  - No response: dmoradpour, glloyd (optional)
  - Agenda: https://app.notion.com/p/canarytechnologies/Workup-Agent-Sync-3c281468615181a1a88fca0b5fea0b94
project: null
source_id: null
tags: []
time_minutes: 5
title: review and summarize notes from workup agent sync
updated: 2026-09-09 20:50:35.781825
waiting_on: null
waiting_since: null
working_on: true
---

https://mail.google.com/mail/u/0/#inbox/FMfcgzQhWLRLZThCSkWfbRPCfkNJXMhS