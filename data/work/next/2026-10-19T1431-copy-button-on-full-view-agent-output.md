---
area: null
completed_at: null
contexts: []
created: 2026-10-19 14:31:54.232532
defer_until: null
due: null
energy: low
id: 2026-10-19T1431-copy-button-on-full-view-agent-output
order: -1
output: |-
  ## Agent run 2026-10-19T14:34:44

  **Finding:** a Copy button already existed on the full view (added in 66ee8616, June) at the top-right of the "🤖 Agent log" panel. It was small, muted, labelled just "Copy", and scrolled out of view on long logs, so it was easy to miss.

  **Changes (commit 93f1eb09 on main):**
  - Button now reads "📋 Copy", with an aria-label and a tooltip ("copies the raw markdown").
  - The log panel header is sticky, so Copy stays at the top of the viewport while you scroll a long log.
  - New test in `frontend/src/AgentLogView.test.tsx`: clicking Copy writes the raw markdown to the clipboard, and the button is hidden when there's no log. Written red first, then green.
  - Frontend rebuilt; ran `make restart-service`. pytest passes (695), lint and tsc are clean.

  **Heads-up:** `frontend/src/WorkflowActions.test.tsx` has uncommitted edits that aren't mine (4 failing "uncomplete" tests, which look like red tests for the uncomplete-from-inbox/next item). I didn't touch or commit that file.
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: copy to clipboard button on full view agent output
updated: 2026-10-19 14:34:44.219856
waiting_on: null
waiting_since: null
working_on: false
---