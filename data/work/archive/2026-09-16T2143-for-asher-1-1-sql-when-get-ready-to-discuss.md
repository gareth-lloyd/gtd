---
area: null
completed_at: 2026-09-17 19:15:58.567318
contexts: []
created: 2026-09-16 21:43:28.520836
defer_until: null
due: 2026-09-18
energy: low
id: 2026-09-16T2143-for-asher-1-1-sql-when-get-ready-to-discuss
order: null
output: |
  ## Agent run 2026-09-17T15:27

  Sources: design doc "Canary MCP SQL Tool for Workup" (https://app.notion.com/p/3c8814686151808c8231f5997b870632, TOOL-562, status APPROVED, last edited 2026-09-16) and Workup Agent Sync (https://app.notion.com/p/3c281468615181a1a88fca0b5fea0b94), meetings of 08-26, 09-09 and 09-16.
  Coverage: I read the doc's goals, components, auth layer, alternatives, rollout, validation, open questions and revision log. I did NOT read lines covering the identity/database layer detail, data model, risks and load sections (roughly the middle third), nor the 31 comment threads beyond the 3 previewed. Read-only; nothing posted anywhere.

  ### Design in one paragraph
  `run_sql` MCP tool, Workup-only, POST to a new Django `RunSqlView`. The hard boundary is a least-privilege Postgres role `canary_mcp_ro` (grant manifest generated from a named blocklist, live grant check per region), READ ONLY transaction, named cursor for memory. On top: `;` byte rule, SELECT-only parse, no wildcards or whole-row reads, clamps (30s/120s, 100/1000 rows, 200KB), 6 req/min throttle plus 200k rows / 50MB daily quota in Valkey failing closed, intent-then-update `McpSqlQuery` audit row with 90-day retention, a Luna LLM judge and an EXPLAIN cost gate that both fail open. Env-var gated, dark by default, US first.

  ### Why the back and forth (auth has been redesigned three times)
  1. 08-26: design drafted by Laura and handed to Asher. Auth was Teleport app identities. Also a psycopg3 detour (TOOL-563): Django auto-switches driver, so they fell back to Django's raw path on psycopg2 with a `;` rule.
  2. 08-31: Security comment that SEC-587 (https://linear.app/canary-technologies/issue/SEC-587) and PR #54542 (https://github.com/canary-technologies-corp/canary/pull/54542) are removing the Teleport path because the forwarded JWT is never signature-checked. The design was standing on the path being deleted.
  3. 09-08 revision: "Auth is settled": Pomerium `bearer_token_format: jwt`. Doc officially approved 09-09.
  4. Then found that mode is not in any released Pomerium (merged to main 08-10, we run v0.33.0, no v0.34 tag or date). Settled auth was unbuildable.
  5. 09-15: Alina and Bernard approved "Option D" as temporary: static per-region bearer token on an unauthenticated `/workup/` Pomerium route, checked in an mcp-server ASGI middleware, identity `bot-workup` minted over the internal-secret channel, Django user-ID allowlist as the real authorization control. Four conditions. Write-up: https://pages.cnry.cloud/workup-machine-auth/
  6. 09-16: Bernard's second pass added nine more items after approval (throttle 30 to 6/min, data-modifying CTE, `_to_xml` family, audit row before execution, email-claim collision, Agent Vault header logging, blocklist prefix/named mismatch, name-pattern drift check). The 09-16 sync notes record this as feedback that arrived "later than expected".

  So the frustration looks legitimate: two of the three auth reversals came from outside (Security deleting Teleport, Pomerium not shipping the mode), and an APPROVED doc is still collecting review items.

  ### What still stands between Asher and Prod US
  - TOOL-665 (Platform): bring Workup into Agent Vault scope, plus Bernard's two checks (does it log request headers; can a non-Workup sandbox reach its admin/log surface with the shared proxy token). Blocks TOOL-656.
  - TOOL-656 (Platform/Security): path-scoped Cloudflare Access bypass for EKS egress. Blocks Prod US; without it the agent gets a 302.
  - TOOL-620 (Platform): Pomerium route in four values files, ESO entries, staging JWKS URL fix.
  - TOOL-637: Alina and Bernard re-review the diff in staging. This is a third Security gate and has no stated exit criteria.
  - TOOL-640: Prod US enablement, where the sandbox-origin proof and MITM CA trust test first run (no staging Workup sandbox exists, so first real end-to-end is in prod).
  - Asher-owned build: TOOL-635 middleware, TOOL-629 `bot-workup` migration, TOOL-621 agents-repo delivery gate, TOOL-619/625/626/631/633.
  - Sync estimate is "a few weeks"; Sam Kariu is helping. SQL is named the top Workup priority (triage accuracy is 16/43).
  - Note PR #54542 lands decoupled; whoever is second rebases. After it merges every non-Workup Overlord agent loses Canary MCP (EE-2046).

  ### Things I would raise or offer in the 1-1
  - Critical path is now mostly not Asher's: three Platform/Security tickets gate prod. Ask whether those have named owners and dates; this is where you can unblock rather than him.
  - Ask Security for a frozen launch-blocker list. "Approved with conditions" followed by nine new items and a staging re-review means approval is not a stable state. Agree what TOOL-637 must show, and that anything new after that goes to a post-launch list.
  - The doc itself has become a cost: 134k characters with a revision log restating the body. Every Security pass means re-reconciling it (Bernard's item 8 was purely doc drift against the blocklist page). Worth asking whether Asher can stop maintaining prose and track remaining items as tickets.
  - Scope check on the judge: it fails open, replaces no layer, needs Luna added to the prompt gateway, a new API key, ZDR confirmation and an in-region answer for EU/AP. The doc's own open question 5 asks whether it earns its latency. It was decided in the 08-26 sync, but it is the most separable piece if he needs to cut to land US sooner. Same for EXPLAIN gate thresholds (open question 4, no data until it runs).
  - Option D is explicitly temporary; phase 2 is TOOL-702 (https://linear.app/canary-technologies/issue/TOOL-702), blocked on a Pomerium release, with issuer and signing-key ownership open. Make sure that does not become a fourth auth rework that lands on him mid-build.
  - Residual he is carrying that someone should own with him: the static token is the identity, so containment to Workup sandboxes is Overlord convention (`sandboxes.agent_slug` gate plus pin tests), and the token transits Agent Vault's shared-token MITM proxy. Security accepted this; worth him hearing that the risk acceptance is shared, not his alone.
  - Side tickets surfaced: TOOL-703 (Django logs every X-* header in cleartext, including the internal secret; https://linear.app/canary-technologies/issue/TOOL-703) and TOOL-704 (mcp-server require-auth AuthorizationPolicy not enforced; https://linear.app/canary-technologies/issue/TOOL-704).
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Review SQL design and Auth situation in advance of Asher 1-1
updated: 2026-09-17 19:15:58.567311
waiting_on: null
waiting_since: null
working_on: false
---

He's frustrated on SQL MCP access back and forth

Angle: Your'e doing somethign real and powerful, and let's be honest: dangerous. It's cool!

Thank you for working through these things. c

https://app.notion.com/p/canarytechnologies/Canary-MCP-SQL-Tool-for-Workup-3c8814686151808c8231f5997b870632?source=copy_link

https://app.notion.com/p/canarytechnologies/Workup-Agent-Sync-3c281468615181a1a88fca0b5fea0b94?source=copy_link