---
area: null
contexts: []
created: 2026-05-08 14:54:10.183245
defer_until: null
due: null
energy: low
id: 2026-05-08T1454-explore-integration-from-claude-code-to-rippling-a
order: null
output: |
  ## Agent run 2026-05-08T14:55

  **TL;DR:** Multiple Rippling MCP servers already exist. The path of least
  resistance is dropping the Bifrost open-source server into your Claude Code
  MCP config with a Rippling API token. ~5 min setup, no OAuth dance, read-only
  on employee data.

  ### Integration paths (ranked by effort)

  1. **MCP server, off-the-shelf (recommended)**
     - `bifrost-mcp/rippling-mcp` — open source, 18 tools, bearer-token auth.
       Install via `npx -y rippling-mcp-server`, set `RIPPLING_API_TOKEN`,
       wire into `claude_desktop_config.json` (or Claude Code project
       `.mcp.json`). Tools cover: company/departments/work-locations,
       employee lookup + search, teams/levels/custom-fields, leave balances
       + requests + processing, group CRUD, company activity feed.
     - `rocketsciencegg/rippling-mcp-server` — alternative OSS implementation.
     - StackOne managed Rippling MCP — 37 actions, hosted, paid. Worth it
       only if you want write coverage Bifrost doesn't have.

  2. **Custom MCP server** — build one if we need write actions Bifrost
     doesn't expose (e.g. onboarding workflows, IT provisioning, app
     assignments, payroll runs). Rippling Platform API v1 has these but
     requires registering an app at developer.rippling.com and going
     through OAuth2 (auth-code flow, per-tenant). Not worth it for
     personal use; only worth it if Canary builds an internal agent.

  3. **Slash commands / skills wrapping curl** — quick hack for one-off
     lookups. `~/.claude/commands/rippling-whois.md` that calls
     `curl -H "Authorization: Bearer $RIPPLING_API_TOKEN" \
     https://api.rippling.com/platform/api/employees?...`. Fine for a
     single query pattern; doesn't scale.

  ### Auth notes

  - **API token** (Bifrost path): Rippling Settings → API Tokens → Create.
    Scoped to issuing user's permissions. Easiest. No app registration.
  - **OAuth2** (developer portal): required for multi-tenant or App-Shop
    distribution. Tokens scoped to one company tenant per flow.
  - Rate limits enforced via response headers — Bifrost server respects them.

  ### What I'd actually use this for

  - Org chart lookups during 1:1 prep / hiring / cross-team triage.
  - "Who's OOO this week" before scheduling syncs.
  - PTO balance / request status without flipping to the Rippling UI.
  - Group/distribution-list membership audits.
  - Pulling org context for performance-review prep (already have a
    `prep-review` skill — could augment with Rippling reporting structure).

  ### Caveats / blockers

  - **Need a personal API token first.** Rippling admin (IT/People Ops at
    Canary) may need to approve API token creation depending on policy.
    Worth checking with IT before assuming you can self-serve.
  - V1 employee endpoints are **read-only** — no write/update via Bifrost.
  - API token inherits issuer's permissions, so what an agent can see ==
    what you can see in the Rippling UI. Probably fine for personal use.
  - Token = bearer secret. Don't paste into shared configs; keep in
    `~/.claude/.env` or 1Password-backed env, not the repo.

  ### Suggested next actions (for user to decide on)

  - [ ] Check Canary IT policy on Rippling API token creation.
  - [ ] If green-lit: install `bifrost-mcp/rippling-mcp`, wire into
        `~/.claude.json` user-level MCP config (not the canary repo's
        `.mcp.json`, since this is personal).
  - [ ] Smoke test with `list_employees` / `get_company`.
  - [ ] Decide whether to extend `prep-review` and `gtd` skills to pull
        Rippling org context.

  ### Sources

  - https://github.com/bifrost-mcp/rippling-mcp
  - https://github.com/rocketsciencegg/rippling-mcp-server
  - https://www.stackone.com/connectors/rippling/mcp/
  - https://developer.rippling.com/documentation/developer-portal/rest-api/api
  - https://rippling.stoplight.io/docs/rippling-api/a310f900b0f84-api-reference
project: null
source_id: null
tags: []
time_minutes: 5
title: Explore integration from claude code to rippling api
updated: 2026-05-08 14:55:12.240269
waiting_on: null
waiting_since: null
working_on: false
---
