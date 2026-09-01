---
area: null
completed_at: null
contexts: []
created: 2026-08-31 13:12:32.944759
defer_until: null
due: null
energy: low
id: 2026-08-31T1312-review-eng-design
order: null
output: |
  ## Agent run 2026-08-31T13:19

  **Source:** Asher's Slack post 2026-08-27 in #eng-design (https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1787843117696999), asking Blake + Bernard to review.
  **Doc:** Canary MCP SQL Tool for Workup — https://app.notion.com/p/canarytechnologies/Canary-MCP-SQL-Tool-for-Workup-3c8814686151808c8231f5997b870632 (Linear TOOL-562, status "REVIEW ME!")
  **Seed blocklist (separate doc, the artifact Security reviews):** https://app.notion.com/p/3c681468615181d2be85ff5f38d7ab26
  **Prior art:** Dylan's stalled PR https://github.com/canary-technologies-corp/canary/pull/51853

  ### State of play (as of reading)
  - Blake (bvanlandingham) has reviewed: "I'm happy with the direction here. Only minor comments. Excited to get this unblocked!" Left 7 threads, all minor/non-blocking.
  - Bernard's (Security) review is still pending — he is the gate, and the seed blocklist is explicitly waiting on him.
  - Blake also filed EE-1959 off the back of it (MCP servers should be opt-in per agent):
    https://linear.app/canary-technologies/issue/EE-1959/agents-mcp-servers-should-be-opt-in-per-agent-nothing-installed-by

  ### My read: approve the direction
  Genuinely strong design — better evidenced than most TDDs we circulate. Three things stand out as real engineering rather than assertion: the measured 25MB vs 443MB named-cursor-vs-buffered memory comparison, the `;` byte-test verified against a live Postgres 15.3 (`U&'\003b'`, `E'\073'`, `chr(59)`), and the psycopg3 dead-end written up so nobody re-derives it (Django's `try: import psycopg / except: import psycopg2` means you cannot scope psycopg3 to one module). The security model is right: the Postgres role is the boundary, everything above it is defence in depth, and the doc says so plainly.

  I would not block it. Below is what I'd raise, ordered by how much I'd push.

  ### 1. I'd cut the LLM judge from v1 (would push hard, non-blocking)
  The doc's own Open Question #5 is "what the judge is worth", and by its own construction the judge (a) can only veto, (b) fails open, (c) "can be removed without weakening the boundary". That is the definition of something that is not a security control. Meanwhile two of the eight listed risks — "the judge blocking legitimate work" and "latency" — exist *only* because of it, and it adds build tasks (Luna onto `ai.prompt_gateway`, a new API key), a new monitor (judge-unavailability, which is silent by construction), and a model round-trip on every query for a tool whose whole point is unblocking investigation speed.

  The stated justification is that the coverage sweep found 182 sensitive columns the first blocklist missed. But Blake spotted the hole in that argument in-thread: on a `SELECT *` the judge cannot see column names either, so it does not actually cover the case it is being bought for.

  My suggestion: ship v1 with the deterministic layers plus the EXPLAIN plan gate (cheap, deterministic, real), run the weekly audit review, and add the judge only if the review shows the blocklist actually missing things in practice. Cheaper v1, one less failure mode, and the decision then gets made on evidence — which is what the doc says it wants everywhere else.

  ### 2. The `SELECT *` decision is in the comments but not in the doc (would raise before Bernard signs off)
  Blake and Asher converged in-thread on rejecting `*` outright rather than letting it bounce off a permission-denied. The doc body still describes the old behaviour ("On a column-blocked table, `SELECT *` fails with permission denied... The fix belongs in Workup's prompt guidance"). That is a security-relevant behaviour change, not an editorial one, and it materially improves the blocklist story: with `*` banned the app-layer pre-flight can enumerate every named column against the blocklist instead of leaning on Postgres's "permission denied for table <t>", which never names the column. Pull it into the body — Bernard should be reviewing the version that has it, and the doc should carry Asher's own caveat that this rests on sqlparse and is therefore usability + defence in depth, not a boundary.

  ### 3. The Django-layer access control's root of trust is a hand-created DB row (this is the one I'd want fixed)
  Verified in `backend/canary/canary_mcp/auth.py:86-89`: `TeleportJwtAuthentication` resolves the Django user by `email__iexact` first and only falls back to `username`. The new SQL allowlist (`CANARY_MCP_SQL_ALLOWED_USERNAMES`) keys on username. The doc acknowledges "nothing in the repo seeds the bot user rows" and makes creating `bot-workup` per region a manual build task.

  So the Workup-only guarantee at the Django layer rests on three unversioned, manually-created rows in three regional databases. That is a weaker standard than the design applies to everything else — the grant manifest is checked in with CI asserting it matches the app blocklist; the bot users should get the same treatment. Ask: a checked-in idempotent management command or data migration creating them with an unusable password, no groups, no permissions, and a **blank** email (so the email-first branch can never resolve a human onto them), plus the binding test the doc already promises.

  ### 4. `MCP_DJANGO_URL` routing is bigger than "blocks enablement, not the build" (Open Question #1)
  Two things the doc states but under-weights. First, the recommended interim (point `MCP_DJANGO_URL` at `django-admin`) moves *every* MCP tool onto that pool, not just this one — that is a blast-radius change for existing MCP consumers arriving as a side effect of a Workup bridge tool, and it still puts the `MCP_SQL_*` credentials on pods serving the admin UI. Second, the end state (dedicated MCP Django deployment) is described as "Nobody has filed this ticket."

  I'd want that decision made *before* the build lands, not before enablement, and the platform ticket filed now with an owner and an ETA. Otherwise this is the thing that holds a finished tool dark for weeks — and the doc has no fallback if platform picks option 2 and deprioritises it.

  ### 5. The Teleport name-match guarantee needs a pin test (small, high value)
  The doc flags that the whole Teleport layer holds because `run_sql` fails to match `^(read|get|list|search|query|describe|fetch|view).*$` in `coding-agent-mcp`, and that renaming it to a read-verb would silently grant it to every coding agent. Correctly identified — but left as prose. That is a three-line test: assert the registered tool name does not match that regex. Closes a silent privilege-escalation path for essentially nothing.

  Separately, the doc's side finding that `^canary-mcp.*$` in `coding-agent-mcp` matches *app* names rather than tool names and "has matched nothing since June" is a live finding about production access config. That deserves its own ticket regardless of whether this project ships — worth knowing whether something is currently over- or under-permissioned as a result.

  ### 6. Two smaller factual gaps
  - **Availability list is missing the event DB.** The design makes the audit write synchronous and fail-closed ("if the audit write fails, the request fails"). Correct call — but the Availability risk enumerates MCP server, Django, Valkey, read replica and the role, and omits the event DB, which is now a hard dependency of every query.
  - **"Fast kill" may not be immediate.** Rollback claims revoking `canary_mcp_ro`'s LOGIN "stops execution immediately without a deploy". Postgres checks LOGIN at *connect* time, not per statement, so any already-established session survives it. With `CONNECTION LIMIT 5` and short-lived connections this is probably fine in practice, but Security will lean on this control — worth verifying against the actual connection lifecycle (and noting `REVOKE` on the grants, or `pg_terminate_backend`, as the genuinely immediate kill).

  ### Claims I checked against the repo
  - "First throttled view in canary" — holds. No `throttle_classes` / `DEFAULT_THROTTLE_RATES` / `*RateThrottle` anywhere in `backend/canary`.
  - "sqlparse already pinned as a direct dependency" — holds (`backend/canary/uv.lock`, specifier `==0.5.4`).
  - Email-before-username auth resolution — holds, `backend/canary/canary_mcp/auth.py:86-89`.
  - The GET-only CI test does catch subclasses — holds. `uses_mcp_auth()` in `backend/canary/canary_mcp/tests/test_mcp_auth_read_only.py:52` uses `issubclass(...)`, so the planned POST-permitting `TeleportJwtAuthentication` subclass will be seen by the scan and does genuinely need the named exception. The exception-list approach is sound.

  ### Suggested next step (nothing sent anywhere)
  Nothing has been posted to Notion or Slack. If you want to leave this as a review, points 2, 3 and 4 are the ones worth Asher seeing before Bernard signs off; 1 is a judgement call worth voicing but not worth blocking on; 5 and 6 are cheap adds. Say the word and I'll draft comment text for you to edit and post yourself.
project: null
source_id: null
tags: []
time_minutes: 5
title: Review eng design.
updated: 2026-08-31 15:06:08.985693
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C0AL1T2H43V/p1787843117696999

Directive from Blake: don't over-sanitize.