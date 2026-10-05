---
area: null
completed_at: 2026-10-05 10:01:24.180362
contexts:
- consume
created: 2026-10-05 00:00:00
defer_until: null
due: null
energy: low
id: 2026-10-05T0000-review-friday-s-show-tell-recording
order: null
output: |
  ## Agent run 2026-10-05T10:00:00+01:00

  Source: ~/Downloads/GMT20261002-145716_Recording.transcript.vtt (EPD show & tell, Fri 2026-10-02, ~66 min, 4 demos + SJ on equity/comp). Kelly's web-chat testing demo was bumped to next week.

  ### 1. Ramiro (Romi) — IHG Core onboarding-script slowdown fixed [07:50-13:30]
  - Batch on 21 Sep took ~40 min (first to last run ~1 hr); all hotels onboarded but slow. Claude-generated Gantt chart showed ~50% worker time idle while runs queued.
  - Three root causes fixed: (a) the Wyndham Connect Plus WhatsApp/Meta rate-limit delay was applied as a single group to every onboarding run, so runs could not fan out across workers; now one group per run, WCP delay retained; (b) IHG Core AI compendium extraction ran via on_commit before the hotel actually existed, so it failed to find the hotel; (c) OOM kills, fixed by Infra giving more memory and better worker scaling.
  - Result: ~40 min down to ~4 min. Andrea gave Romi a shout-out for owning it end to end. Only IHG Core was affected because only it has the AI compendium step.
  - Relevance for Gareth: this is the shared enterprise onboarding-script infra; worth confirming the ent-monitor checks still reflect the new per-run grouping.

  ### 2. Leandro (Leo) — Check-in V3 configurator (Arrivals & Departures) [13:40-27:20]
  - New settings-app UI replacing Django-admin edits for check-in flow config. Sits on Check-in V3 / guest_experience app / shared step framework (evolved from kiosk; goal is to move kiosk and authorizations onto it too).
  - CS can now: edit step wording + translations; add/remove form fields from a shared "catalog" (fields defined once by CS, propagate to web and kiosk; data model unchanged, still schema form); configure ID and payments buckets. Gateway/payment internals stay Django-admin only. Backed by audit logs in Manage > Activity.
  - Rollout: live on Vibhor's test hotel; ~700 hotels already on V3; plan is to enable for a few, let implementation team tweak, then general rollout. Property managers get wording/translation editing only; field creation (needs PMS mapping) is CS-only via a special permission.
  - Questions: Nico worried about letting hotels reorder steps (we are better placed to optimise the funnel; e.g. signature conversion 70%->20%). Leo: reordering not built yet; could add rules or keep shape changes CS-only. The "Greek hotel needing signature at end" example is the Grecotel/Caramel pilot. Meshack asked whether config changes should propagate into an in-flight session (sensitive on card step); Leo: changes propagate to any unsubmitted step, submissions snapshot their schema; guardrails possible, taken offline.

  ### 3. Franco — Sales Coordinator Chrome extension for RFP marketplaces [27:40-37:30]
  - Chrome extension scrapes Cvent (wizard-style) RFP pages step by step, feeds the LLM, surfaces Delphi function-room availability/rates and PMS room availability in one panel, auto-creates a Canary RFP thread, and (via Joshua's work) creates and incrementally updates a Delphi inquiry.
  - "Answer library" (knowledge-base extension to sales-agent config) drafts responses to Cvent's free-text additional questions; well received by beta customers.
  - Auth via staff login / staff JWT. One adapter per marketplace, rest generic; next targets are MeetingBroker and others, but needs vendor logins (Rachel). Rachel: fastest-responding properties win the booking, so this is the sales team's main time sink. Kevin Li flagged the pattern as reusable for any system we lack an integration for.

  ### 4. Asher — Live read-only SQL MCP tool for Workup [37:30-53:10]
  - Flow: Workup -> Sallyport -> MCP server -> Django -> Postgres read replica. Gates in order: caller throttle, Workup-only allowlist + run ID, request-size cap, SELECT-only parse, Django preflight blocklist of tables/columns/functions (better errors than Postgres), DB presence check, grant-drift "ratchet" (runs if Postgres grants are stricter than code, blocks if looser until deploy), daily per-agent quota, EXPLAIN plan-cost gate (1M), LLM judge on query + plan for perf and security, then run, charge quota, return.
  - Grants generated from code, run on every migrate and a 3-hourly cron; CI errors on new encrypted/secret-looking columns until explicitly allowed or denied. ~900 tables fully granted, ~200 column-by-column, ~60 fully denied, ~400 columns denied, 57 exfiltration-capable functions blocked. Everything audited (who, run ID, literal-masked query, fingerprint, tables, outcome, judge reasoning, cost, rows); denied attempts also logged.
  - First 2 days: 22 Workup tickets, 7 used the tool, 44 queries, 32 returned data, ~4 s each (judge dominates). Wins: confirmed contracts V3 flag went live without backfill; found a hotel with no Twilio number. Misses: misread dead data twice; judge vetoed a nested-loop query at 10% of the cost gate (too strict); LLM wrote wrong column names twice.
  - Blake: wants to open the tool beyond Workup, eventually to CS, as confidence grows. Relevant to the Workup/TypeSafe experiments: tickets needing live data should now be getting more definitive answers.

  ### 5. SJ — equity and compensation [53:10-69:10]
  - Admits Canary under-communicates equity value out of fear of over-promising; historically over-achieved almost every year.
  - Last round (early 2025): under $40M CARR, investors paid ~$25/share. Now $103M CARR after the IHG deal (proper $100M celebration coming). Linear extrapolation ~$50/share less 10-12% dilution; "those are facts on spreadsheets, not opinions". ~90% growth this year, 91% last year, planning similar next year.
  - Carta $5 figure is the strike/FMV (409A, valid 12 months, expires around 1 April), negotiated far below investor price as a deliberate team advantage; not the sale value.
  - Refresh grants' one-year cliff is a retention tool, not short-changing; acknowledges the feedback.
  - Variable comp (5-10% of EPD salary): monthly/quarterly objectives caused stress and rigid sprint planning; company metrics (CARR, churn) feel disconnected; Q3 likely under 100%. Re-evaluating whether variable should exist at all, not reducing salary. DMs open.
  - Q&A: early exercise not considered yet, SJ will think about it. Liquidity: early team (4-5+ yrs) sold small portions in Series B/C/D secondaries; intention to repeat at a Series E. IPO not imminent. Financing is opportunistic, years of runway. Garrett's "do we need a new big bet for 90% next year" deferred to a separate session ("a little bit, but not necessary").

  ### Possible follow-ups for Gareth (not actioned)
  - Check whether Workup's new run-SQL tool changes anything in the Workup/TypeSafe backtest assumptions (judge's blind pass still code-only?).
  - Ask Leo how the configurator interacts with rules-based configuration / ENT-7726 binding rules, since both now claim ownership of "config that shapes the flow".
  - Grecotel signature-at-end requirement is now a named driver for form splitting in the V3 configurator; worth linking in the pilot notes.
project: null
source_id: null
tags: []
time_minutes: 30
title: Review Friday's show & tell recording
updated: 2026-10-05 10:01:24.180354
waiting_on: null
waiting_since: null
working_on: false
---

Downloads -> 
GMT20261002-145716_Recording.transcript.vtt