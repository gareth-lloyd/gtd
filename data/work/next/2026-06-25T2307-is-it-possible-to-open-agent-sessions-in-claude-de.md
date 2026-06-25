---
area: null
contexts: []
created: 2026-06-25 23:07:59.351406
defer_until: null
due: null
energy: low
id: 2026-06-25T2307-is-it-possible-to-open-agent-sessions-in-claude-de
order: null
output: |
  ## Agent run 2026-06-25T23:30 — research

  **Short answer: YES.** Both the Claude desktop app and the Claude Code CLI
  register custom URL schemes you can fire from a script with macOS `open`.
  Two distinct schemes exist (confirmed against official Anthropic docs):

  ### Desktop app — `claude://`
  Opens / launches the Claude desktop app and navigates it. Relevant paths:
  - `claude://code/new?q=<prompt>&folder=<abs-path>` — opens a **new Claude
    Code session in the desktop app**, pre-filled prompt + working folder.
  - `claude://cowork/new?q=<prompt>&folder=<path>&file=<path>` — Cowork session.
  - `claude://claude.ai/new?q=<prompt>` — new plain chat.
  - `claude://claude.ai/chat/<conversation-id>` — reopen a specific chat.
  - Params must be URL-encoded; `q` truncated to ~14,000 chars. The app
    prompts for confirmation before adopting an untrusted `folder` as cwd,
    and auto-launches Claude if not already running.
  - Source: https://support.claude.com/en/articles/14729294-open-claude-desktop-with-a-link

  ### CLI — `claude-cli://` (opens a terminal, NOT the desktop app)
  - Only path is `claude-cli://open`, plus query params:
    - `q` — prompt to pre-fill (URL-encode; `%0A` for newlines; max 5,000 chars)
    - `cwd` — absolute working dir (UNC/network paths rejected)
    - `repo` — GitHub `owner/name`; resolves to a local clone Claude Code has
      seen before (else falls back to home dir). `cwd` wins if both given.
  - macOS: `open "claude-cli://open?cwd=/path&q=review%20open%20PRs"`
  - Requires Claude Code **v2.1.91+**. Handler auto-registers on first
    interactive `claude` run (`~/Applications/Claude Code URL Handler.app`).
    Disable via `disableDeepLinkRegistration: "disable"` in settings.json.
  - VS Code variant: `vscode://anthropic.claude-code/open` opens an editor tab.
  - Source: https://code.claude.com/docs/en/deep-links

  ### Important caveats
  - **Prompt is pre-filled, NOT auto-sent.** Every scheme drops the text in
    the input box and waits for the user to press Enter (a "Prompt from an
    external link" warning shows). So a deep link can't fully fire-and-forget
    an autonomous agent run the way our current iTerm launch does — there's a
    mandatory human keypress in the loop.
  - **No agent-teams / parallel-session targeting via deep link.** The
    desktop Code tab is single-session; you can't launch a specific named
    sub-agent or an agent "team" from a link. Feature requested upstream
    (github.com/anthropics/claude-code/issues/50585), not yet implemented.
    (This last point came from a community-sourced agent summary — treat as
    likely-true but unverified against official docs.)

  ### Relevance to this GTD project
  Our `🤖 agent` feature (agent_launch.py / launch_claude_session) currently
  spawns iTerm via osascript running `claude --permission-mode auto`. A
  `claude://code/new?q=<prompt>&folder=<working_dir>` deep link is a viable
  alternative that would open the session **inside the desktop app** instead
  of a terminal — cross-platform (no osascript), and `folder` maps cleanly to
  our project `working_dir`. Trade-offs vs today's approach:
    - LOSE: auto-send / unattended start (deep link needs a human Enter), and
      the `--permission-mode auto` flag (no way to pass CLI flags via the URL).
    - GAIN: GUI surface, no terminal-emulator detection, Win/Linux portability.
  Worth a spike if we ever want a "open in Claude Desktop" launch option
  alongside the iTerm one. No code changed this run — research only.
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: Is it possible to open agent sessions in claude desktop app by using deep links?
updated: 2026-06-25 23:30:00.000000
waiting_on: null
waiting_since: null
working_on: false
---