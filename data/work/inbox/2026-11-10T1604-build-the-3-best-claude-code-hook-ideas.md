---
area: null
completed_at: null
contexts: []
created: &id001 2026-11-10 16:04:37.892895
defer_until: null
due: null
energy: null
id: 2026-11-10T1604-build-the-3-best-claude-code-hook-ideas
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: null
title: Build the 3 best Claude Code hook ideas
updated: *id001
waiting_on: null
waiting_since: null
working_on: false
---

From a 2026-11-10 session reviewing my workflow for hook applications.

1. **Hard denies for irreversible actions** (PreToolUse). Deny `gh pr merge`, `/merge` comments and Birdline queue commands (I merge manually). Deny any Salesforce MCP tool that writes; gate read SOQL behind an env var I set when I explicitly OK it. Also: block `git merge master` into a stacked PR whose base is not master (check `gh pr view --json baseRefName`).

2. **Rule injection on Write** (PreToolUse on Write). Root CLAUDE.md says `.claude/rules/` only loads when a matching file is *read*, so a new file pulls in nothing. Hook matches the target path against the rule globs and returns the rule text as additionalContext. Removes the "read the rule first" step.

3. **Pre-push gate** (PreToolUse on `git push`). Warn/block when: a changed service dir has not had `make check-fix` since last edit; views changed in canary/credential-manager but OpenAPI spec did not; branch mixes migrations with views/services (PR linter will reject); cookie-setting code changed but docs/security/cookies.md did not; PR body lacks a Linear ticket ref.

Existing precedent in repo: `.claude/hooks/block-production-access.py` and the pre-PR review gate on `gh pr create`. Wiring via the `update-config` skill.

Runner-up: PostToolUse lint on Edit/Write for feedback-memory conventions (hotel.country vs country_code, .all_objects on SoftDeleteModel, direct PortfolioHotel writes, AvailableForms auth gating, spaces in sms_phone).