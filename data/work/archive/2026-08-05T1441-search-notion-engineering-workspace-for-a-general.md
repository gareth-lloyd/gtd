---
area: null
completed_at: 2026-08-06 12:57:28.888935
contexts: []
created: 2026-08-05 14:41:09.003687
defer_until: null
due: null
energy: low
id: 2026-08-05T1441-search-notion-engineering-workspace-for-a-general
order: null
output: |
  ## Agent run 2026-08-05T15:05:00

  Searched Notion (AI search across the workspace) for a directory of technical-system
  descriptions. Verdict: there is NO company-wide "how our systems work" directory —
  only pod-level knowledge bases. Best fit found:

  **Recommended home: Core knowledge base** (database under Pod Homepages > Enterprise)
  https://app.notion.com/p/32081468615180609ecef6d3f6399d86
  - Has Category options including "Permissions", "Authorization", and
    "Rules-based configuration" — exactly the taxonomy for this doc — plus a
    "New doc" template.
  - Existing sibling docs: "Permissions System: Architecture and Usage Guide",
    "Users can only assign a role if they have all the permissions on that role",
    "How to Safely Add New Permissions: Rollout Impact Assessment".

  Related pages worth linking from the new doc:
  - Permissions System: Architecture and Usage Guide (verified against codebase
    2026-03-11; covers access-vs-permissions split, role/grant model, gating views):
    https://app.notion.com/p/32081468615181aeb6e0e70d17ed3b43
    (supersedes the older "Permissions System" page:
    https://app.notion.com/p/4d154ff31bc44e0aaf559aee34ee31b0)
  - Rules Browser: Above-Property UI for Rules-Based Configuration (nearest existing
    rules-based-config doc; links the Rules-based configuration PRD):
    https://app.notion.com/p/37c81468615181be923cec1df122e5fd
  - Request Framework hub (Requests/Responses/Authorization child pages) exists but
    lives under personal "Projects > Misc Project Notes", not a shared directory:
    https://app.notion.com/p/37381468615181de8c31dacd9b08546c

  Suggested next action: create the Rules Based Permissions overview in the Core
  knowledge base with Category "Rules-based configuration" (or "Permissions"),
  cross-linking the Architecture and Usage Guide and the Rules Browser doc.
  No Notion writes were made.
project: null
source_id: null
tags: []
time_minutes: 5
title: Search Notion engineering workspace for a general directory of descriptions
  of current features and systems.
updated: 2026-08-06 12:57:28.888922
waiting_on: null
waiting_since: null
working_on: false
---

E.g. "this is how our permissions system works", or "this is our request auth framework" or "this is our background worker queue" system.

I.e. technical "features" not product features. 

Idea is to find a natural home for a document overviewing Rules Based Permissions framework.