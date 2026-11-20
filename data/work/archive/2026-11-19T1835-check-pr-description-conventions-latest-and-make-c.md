---
area: null
completed_at: 2026-11-20 14:10:27.998408
contexts: []
created: 2026-11-19 18:35:59.343218
defer_until: 2026-11-19 21:39:00
due: null
energy: low
id: 2026-11-19T1835-check-pr-description-conventions-latest-and-make-c
order: null
output: |-
  ## Agent run 2026-11-20T13:06:47

  ### Current PR description conventions
  Canonical source: the `dx:pr-description` skill, `agent-plugins/claude-plugins/dx/skills/pr-description/SKILL.md`, now at version 11. Last behavioral change: 2026-10-28, "[EE-2656] Add Risk and revert to PR descriptions", PR #61721 (https://github.com/canary-technologies-corp/canary/pull/61721).

  - Pick the form first. Self-evident diff: 1-2 plain sentences, no headings. Otherwise the full shape. Judge self-evidence, not size (a 2-line bug fix takes the full shape).
  - Full shape, visible part: ticket link, `## Why`, `## What`, `## What I verified`. Optional `## Reviewer heads-up` (rare). Visible part stays under 180 words.
  - New since October: `## Risk and revert`, only when risk is High (money, access, credentials, durable data, external messages, PMS writes, devices, shared contracts, infra). Exact labels `**Risk: High.**` and `**Revert:**`; tools parse them. Low and medium risk PRs omit the section.
  - Depth goes in folded `<details>` blocks. Fixed names: `Why these decisions`, `Caveats and what's not here`, `Risk and revert details`. No invented reasoning, no placeholders or N/A.
  - "What" carries intent, not a file or artifact inventory. "What I verified" is grouped by behavior or risk, not one item per test; routine CI checks are omitted; gaps go in as `Not verified: <thing> — <reason>`.
  - Never write a ticket link from memory.
  - Every body ends with a `<!-- canary-pr-meta ... -->` comment rendered by `pr_meta.py render` (never hand-written), and must pass `pr_meta.py validate <body-file>` before `gh pr create --draft --body-file` / `gh pr edit --body-file`.

  ### Hook: written and tested, NOT installed
  The auto-mode classifier refused my write to `~/.claude/hooks/`, so I did not install it or touch `~/.claude/settings.json`. The script is at:
  `/Users/garethlloyd/projects/plans/pr-description-hook/require-pr-description-skill.py`

  What it does (PreToolUse on Bash, fails open):
  - Only acts inside a checkout that contains the skill's `pr_meta.py` (canary and its worktrees). Other repos are untouched.
  - Denies `gh pr create` with no `--body-file`, with inline `--body`, with `--fill`, or with stdin body, and tells Claude to invoke `dx:pr-description`.
  - With `--body-file`: denies if the file lacks the `canary-pr-meta` comment or the skill's validator reports an ERROR (the errors are passed back to Claude).
  - Same checks for `gh pr edit` when it sets a body. `gh pr edit` for title/labels, `gh pr create --web`, and `gh pr view` pass.
  - Bypass for one call: `PR_DESC_HOOK_SKIP=1 gh pr create ...`.

  Tested with 18 simulated hook payloads (allow and deny cases, subdirectory cwd, non-canary cwd, malformed JSON); all behaved as intended. Not tested in a live session, since it is not installed.

  Known gaps: the GraphQL `updatePullRequest` fallback is not gated; an unreadable body file is allowed through; a `cd` inside the command is not followed when resolving a relative body path.

  To install:
  1. `mkdir -p ~/.claude/hooks && cp ~/projects/plans/pr-description-hook/require-pr-description-skill.py ~/.claude/hooks/`
  2. Add to `hooks.PreToolUse` in `~/.claude/settings.json`:
     `{"matcher": "Bash", "hooks": [{"type": "command", "command": "python3 ~/.claude/hooks/require-pr-description-skill.py", "timeout": 10}]}`
  3. Start a new session (or review via `/hooks`).

  Alternative: ship it in the dx plugin beside `pre_pr_review_gate.py` so everyone gets it. That needs a PR, a plugin version bump and an opt-in decision; not done.
project: null
source_id: null
tags: []
time_minutes: 5
title: check pr description conventions latest, and make claude hook to write pr descriptsion
updated: 2026-11-20 14:10:27.998397
waiting_on: null
waiting_since: null
working_on: false
---