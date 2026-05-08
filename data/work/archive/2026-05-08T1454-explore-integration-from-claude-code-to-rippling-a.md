---
area: null
contexts: []
created: 2026-05-08 14:54:10.183245
defer_until: null
due: null
energy: low
id: 2026-05-08T1454-explore-integration-from-claude-code-to-rippling-a
order: null
output: "## Agent run 2026-05-08T14:55\n\n**TL;DR:** Multiple Rippling MCP servers
  already exist. The path of least\nresistance is dropping the Bifrost open-source
  server into your Claude Code\nMCP config with a Rippling API token. ~5 min setup,
  no OAuth dance, read-only\non employee data.\n\n### Integration paths (ranked by
  effort)\n\n1. **MCP server, off-the-shelf (recommended)**\n   - `bifrost-mcp/rippling-mcp`
  — open source, 18 tools, bearer-token auth.\n     Install via `npx -y rippling-mcp-server`,
  set `RIPPLING_API_TOKEN`,\n     wire into `claude_desktop_config.json` (or Claude
  Code project\n     `.mcp.json`). Tools cover: company/departments/work-locations,\n
  \    employee lookup + search, teams/levels/custom-fields, leave balances\n     +
  requests + processing, group CRUD, company activity feed.\n   - `rocketsciencegg/rippling-mcp-server`
  — alternative OSS implementation.\n   - StackOne managed Rippling MCP — 37 actions,
  hosted, paid. Worth it\n     only if you want write coverage Bifrost doesn't have.\n\n2.
  **Custom MCP server** — build one if we need write actions Bifrost\n   doesn't expose
  (e.g. onboarding workflows, IT provisioning, app\n   assignments, payroll runs).
  Rippling Platform API v1 has these but\n   requires registering an app at developer.rippling.com
  and going\n   through OAuth2 (auth-code flow, per-tenant). Not worth it for\n   personal
  use; only worth it if Canary builds an internal agent.\n\n3. **Slash commands /
  skills wrapping curl** — quick hack for one-off\n   lookups. `~/.claude/commands/rippling-whois.md`
  that calls\n   `curl -H \"Authorization: Bearer $RIPPLING_API_TOKEN\" \\\n   https://api.rippling.com/platform/api/employees?...`.
  Fine for a\n   single query pattern; doesn't scale.\n\n### Auth notes\n\n- **API
  token** (Bifrost path): Rippling Settings → API Tokens → Create.\n  Scoped to issuing
  user's permissions. Easiest. No app registration.\n- **OAuth2** (developer portal):
  required for multi-tenant or App-Shop\n  distribution. Tokens scoped to one company
  tenant per flow.\n- Rate limits enforced via response headers — Bifrost server respects
  them.\n\n### What I'd actually use this for\n\n- Org chart lookups during 1:1 prep
  / hiring / cross-team triage.\n- \"Who's OOO this week\" before scheduling syncs.\n-
  PTO balance / request status without flipping to the Rippling UI.\n- Group/distribution-list
  membership audits.\n- Pulling org context for performance-review prep (already have
  a\n  `prep-review` skill — could augment with Rippling reporting structure).\n\n###
  Caveats / blockers\n\n- **Need a personal API token first.** Rippling admin (IT/People
  Ops at\n  Canary) may need to approve API token creation depending on policy.\n
  \ Worth checking with IT before assuming you can self-serve.\n- V1 employee endpoints
  are **read-only** — no write/update via Bifrost.\n- API token inherits issuer's
  permissions, so what an agent can see ==\n  what you can see in the Rippling UI.
  Probably fine for personal use.\n- Token = bearer secret. Don't paste into shared
  configs; keep in\n  `~/.claude/.env` or 1Password-backed env, not the repo.\n\n###
  Suggested next actions (for user to decide on)\n\n- [ ] Check Canary IT policy on
  Rippling API token creation.\n- [ ] If green-lit: install `bifrost-mcp/rippling-mcp`,
  wire into\n      `~/.claude.json` user-level MCP config (not the canary repo's\n
  \     `.mcp.json`, since this is personal).\n- [ ] Smoke test with `list_employees`
  / `get_company`.\n- [ ] Decide whether to extend `prep-review` and `gtd` skills
  to pull\n      Rippling org context.\n\n### Sources\n\n- https://github.com/bifrost-mcp/rippling-mcp\n-
  https://github.com/rocketsciencegg/rippling-mcp-server\n- https://www.stackone.com/connectors/rippling/mcp/\n-
  https://developer.rippling.com/documentation/developer-portal/rest-api/api\n- https://rippling.stoplight.io/docs/rippling-api/a310f900b0f84-api-reference\n"
project: null
source_id: null
tags: []
time_minutes: 5
title: Explore integration from claude code to rippling api
updated: 2026-05-08 15:55:12.000696
waiting_on: null
waiting_since: null
working_on: false
---