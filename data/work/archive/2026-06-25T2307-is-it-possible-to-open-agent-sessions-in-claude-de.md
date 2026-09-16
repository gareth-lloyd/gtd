---
area: null
completed_at: 2026-09-16 09:16:58.650228
contexts: []
created: 2026-06-25 23:07:59.351406
defer_until: null
due: null
energy: low
id: 2026-06-25T2307-is-it-possible-to-open-agent-sessions-in-claude-de
order: null
output: "## Agent run 2026-06-25T23:30 — research\n\n**Short answer: YES.** Both the
  Claude desktop app and the Claude Code CLI\nregister custom URL schemes you can
  fire from a script with macOS `open`.\nTwo distinct schemes exist (confirmed against
  official Anthropic docs):\n\n### Desktop app — `claude://`\nOpens / launches the
  Claude desktop app and navigates it. Relevant paths:\n- `claude://code/new?q=<prompt>&folder=<abs-path>`
  — opens a **new Claude\n  Code session in the desktop app**, pre-filled prompt +
  working folder.\n- `claude://cowork/new?q=<prompt>&folder=<path>&file=<path>` —
  Cowork session.\n- `claude://claude.ai/new?q=<prompt>` — new plain chat.\n- `claude://claude.ai/chat/<conversation-id>`
  — reopen a specific chat.\n- Params must be URL-encoded; `q` truncated to ~14,000
  chars. The app\n  prompts for confirmation before adopting an untrusted `folder`
  as cwd,\n  and auto-launches Claude if not already running.\n- Source: https://support.claude.com/en/articles/14729294-open-claude-desktop-with-a-link\n\n###
  CLI — `claude-cli://` (opens a terminal, NOT the desktop app)\n- Only path is `claude-cli://open`,
  plus query params:\n  - `q` — prompt to pre-fill (URL-encode; `%0A` for newlines;
  max 5,000 chars)\n  - `cwd` — absolute working dir (UNC/network paths rejected)\n
  \ - `repo` — GitHub `owner/name`; resolves to a local clone Claude Code has\n    seen
  before (else falls back to home dir). `cwd` wins if both given.\n- macOS: `open
  \"claude-cli://open?cwd=/path&q=review%20open%20PRs\"`\n- Requires Claude Code **v2.1.91+**.
  Handler auto-registers on first\n  interactive `claude` run (`~/Applications/Claude
  Code URL Handler.app`).\n  Disable via `disableDeepLinkRegistration: \"disable\"`
  in settings.json.\n- VS Code variant: `vscode://anthropic.claude-code/open` opens
  an editor tab.\n- Source: https://code.claude.com/docs/en/deep-links\n\n### Important
  caveats\n- **Prompt is pre-filled, NOT auto-sent.** Every scheme drops the text
  in\n  the input box and waits for the user to press Enter (a \"Prompt from an\n
  \ external link\" warning shows). So a deep link can't fully fire-and-forget\n  an
  autonomous agent run the way our current iTerm launch does — there's a\n  mandatory
  human keypress in the loop.\n- **No agent-teams / parallel-session targeting via
  deep link.** The\n  desktop Code tab is single-session; you can't launch a specific
  named\n  sub-agent or an agent \"team\" from a link. Feature requested upstream\n
  \ (github.com/anthropics/claude-code/issues/50585), not yet implemented.\n  (This
  last point came from a community-sourced agent summary — treat as\n  likely-true
  but unverified against official docs.)\n\n### Relevance to this GTD project\nOur
  `\U0001F916 agent` feature (agent_launch.py / launch_claude_session) currently\nspawns
  iTerm via osascript running `claude --permission-mode auto`. A\n`claude://code/new?q=<prompt>&folder=<working_dir>`
  deep link is a viable\nalternative that would open the session **inside the desktop
  app** instead\nof a terminal — cross-platform (no osascript), and `folder` maps
  cleanly to\nour project `working_dir`. Trade-offs vs today's approach:\n  - LOSE:
  auto-send / unattended start (deep link needs a human Enter), and\n    the `--permission-mode
  auto` flag (no way to pass CLI flags via the URL).\n  - GAIN: GUI surface, no terminal-emulator
  detection, Win/Linux portability.\nWorth a spike if we ever want a \"open in Claude
  Desktop\" launch option\nalongside the iTerm one. No code changed this run — research
  only.\n"
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: Is it possible to open agent sessions in claude desktop app by using deep links?
updated: 2026-09-16 09:16:58.650223
waiting_on: null
waiting_since: null
working_on: false
---