---
area: null
completed_at: 2026-09-16 09:14:58.738040
contexts: []
created: 2026-09-10 10:21:52.843393
defer_until: null
due: null
energy: low
id: 2026-09-10T1021-i-now-have-two-claude-accounts-ste-up-on-this-mach
order: null
output: |
  ## Agent run 2026-09-10T10:27:11

  Done: the GTD app now picks the Claude account per env, matching the `pclaude` convention.

  **What changed** (code commit ca41a207 on main, 595 backend tests pass, lint/pyright clean):
  - `EnvConfig` gains optional `claude_config_dir` (round-trips through config.yml).
  - iTerm agent launch (`launch_claude_session`) prefixes the command with `CLAUDE_CONFIG_DIR=<dir>` when set.
  - AI capture (`claude -p`) passes the same var in the subprocess env, so home captures also use the personal account.
  - Unset means default account, so the work env behaves exactly as before.
  - CLAUDE.md documents the convention under "Per-env Claude account".

  **Data change (not yet committed, picked up by next snapshot / Sync):**
  - `data/home/config.yml` now has `claude_config_dir: ~/.claude-personal`. Work config untouched.

  **Verified** by driving the real home/work configs through the service with osascript stubbed:
  - home: `CLAUDE_CONFIG_DIR=/Users/garethlloyd/.claude-personal claude --permission-mode auto ...`
  - work: `claude --permission-mode auto ...`

  **Caveats / things to decide:**
  - The desktop-app launch target (`claude://code/new` deep link) cannot carry an env var, so it always uses whichever account the Claude desktop app is signed into. If you launch home items via desktop, check which account that app holds.
  - `pclaude` also refuses to run inside ~/projects/canary. The launcher does not replicate that guard; a home project with `working_dir` under canary would still run with the personal account. Unlikely, so not added.
  - The blog approach (https://www.boxblinkracer.com/blog/claude-code-multi-account) is the same CLAUDE_CONFIG_DIR mechanism the zshrc `pclaude` function already uses, so nothing else on the machine needed changing.
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: I now have two claude accounts ste up on this machine. Home environment should
  always use the zshrc pclaude command to open claude. Work env should always use
  claude
updated: 2026-09-16 09:14:58.738031
waiting_on: null
waiting_since: null
working_on: false
---

https://www.boxblinkracer.com/blog/claude-code-multi-account