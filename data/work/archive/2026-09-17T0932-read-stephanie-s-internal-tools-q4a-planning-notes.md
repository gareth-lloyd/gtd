---
area: null
completed_at: 2026-09-17 17:18:16.588009
contexts:
- react
created: 2026-09-17 09:32:17.192232
defer_until: null
due: 2026-09-17
energy: medium
id: 2026-09-17T0932-read-stephanie-s-internal-tools-q4a-planning-notes
order: null
output: |
  ## Agent run 2026-09-17T11:37:22Z

  **BLOCKED on the actual doc — I could NOT read the Q4A page.** The Notion connector returns
  404 / object_not_found for
  https://app.notion.com/p/canarytechnologies/Planning-Internal-Tools-Q4A-Internal-Notes-3db8146861518171aab0dbfe1d5b53ca
  (tried URL and raw ID; it also doesn't appear in Notion search). Most likely the page is shared
  with you personally but not visible to the MCP integration. You still need to open it yourself
  (~15 min). Nothing below is from the Q4A doc — it is prep context assembled from adjacent sources.

  Slack message (https://canarytechnologies.slack.com/archives/D09Q1PTAMTR/p1789587177222649):
  Stephanie, 2026-09-16 22:32 EEST: "Sharing in advance of our 1:1 tomorrow" + link. No thread
  replies, no specific ask. The doc unfurl links "Linear — TOOL projects".

  ### Context 1 — previous block, Q3B notes (readable)
  https://app.notion.com/p/3b1814686151816cb470da06f103f965
  The Q4A doc almost certainly follows the same shape (Completed / In Progress / Upcoming /
  Discovery / Deprioritized / Team requests). Q3B themes:
  1. Decrease eng support dependency — AI Workup (next-step metric, Canary MCP SQL tool, accuracy,
     interactive investigations) and User Management (~78% of Oncall queue; scoped SAG type + trained L2).
  2. Onboarding automation — IHG AI Compendium, SAG Types, Check-in V3 onboarding, PMS Settings from
     PMS Capabilities.
  3. Support — country-based phone numbers, support web form, Hotel Support ID backfill.
  4. Canary Pages magic-link external sharing.
  Explicitly flagged for Q4A in Q3B Discovery: **Extend SAGs to Above Property** (portfolio-level
  grants; trigger = self-service SSO; "working with Enterprise")
  https://app.notion.com/p/3b98146861518123abafce6dfcfb17d0 — and Automate Voice Onboarding
  https://app.notion.com/p/3ac8146861518145bcbec2c8237b1a43.

  Items in the Q3B meeting notes that name you:
  - "Gareth Lloyd is a current blocker for design review" on Configure PMS Settings from PMS
    Capabilities (eng design https://app.notion.com/p/39181468615180238a31da976288eb14).
  - "Gareth Lloyd has provided an initial spec" for SAG Grant Types.
  - User-management approach was to be re-evaluated (approver wear-out + security risk; lean toward
    automating execution rather than training humans).

  ### Context 2 — TOOL Linear projects as of today (proxy for what carries into Q4A)
  Labelled 26Q4A already:
  - AI Workup: Interactive Investigations — Product Definition, Laura
    https://linear.app/canary-technologies/project/ai-workup-interactive-investigations-8e1ffa958fa5
  - Unify Onboarding & Add Products Code — Implementation, Rami (target was 2026-08-14, overdue)
    https://linear.app/canary-technologies/project/unify-onboarding-and-add-products-code-0cc00a3cbac7
  Q3B work still open, likely rolling over:
  - SAG Types — Implementation, Rami, target 2026-09-30
    https://linear.app/canary-technologies/project/support-access-grant-types-d2f3ff04096f
  - Canary MCP SQL Tool — Implementation, Asher, target 2026-09-30
    https://linear.app/canary-technologies/project/ai-workup-canary-mcp-sql-tool-72b25204de08
  - AI Workup: Accuracy — Implementation, Laura, target 2026-10-06 (~57% on July judged set)
    https://linear.app/canary-technologies/project/ai-workup-accuracy-1bfe6e72996f
  - Automate Check-in V3 Onboarding — Eng Design, Sam, target 2026-09-30
    https://linear.app/canary-technologies/project/automate-check-in-v3-onboarding-617b22ca4b48
  - Canary Pages magic links — Eng Design, Laura, target 2026-09-11 (passed)
    https://linear.app/canary-technologies/project/canary-pages-external-sharing-via-magic-links-58e24089d548
  - AI Compendium Improvements — Implementation, Asher
    https://linear.app/canary-technologies/project/ai-compendium-improvements-e5eafa889565
  - Enable Support to Manage Hotel Users — still Backlog, Stephanie
    https://linear.app/canary-technologies/project/enable-support-to-manage-hotel-users-2e268ccdba20
  - Intl Support country phone numbers — Backlog, target 2026-09-04 passed
    https://linear.app/canary-technologies/project/international-support-country-based-phone-numbers-95ee795699db
  Status changes worth noticing:
  - **Configure PMS Settings from PMS Capabilities — now Paused and relabelled 26Q4B** (updated
    2026-09-16). Design is now "gated read-time merge of layered defaults + overrides (HotelConfig),
    no per-hotel config writes; capability sync moves to Kafka".
    https://linear.app/canary-technologies/project/configure-pms-settings-from-pms-capabilities-092d8c80f510
  - Canceled: Support Web Form, Model Benchmark, Team Enablement via Knowledge Base.
  - New backlog: Onboarding Checklist (IHG-requested, portfolio/enterprise-configured, needs product
    definition) https://linear.app/canary-technologies/project/onboarding-checklist-84688150d000 ;
    Workup guest data handling (PII pseudonymization/erasure)
    https://linear.app/canary-technologies/project/workup-guest-data-handling-9dea5554cd38

  ### Likely 1:1 talking points (inferred, verify against the real doc)
  - Above-property SAGs and Onboarding Checklist both lean on Enterprise — what does she need from you?
  - PMS Capabilities paused to Q4B: is the design-review blocker on you still live, or moot?
  - User Management still in Backlog after the "re-evaluate approach" action — where did it land?
  - Several Q3B targets land 2026-09-30; how much of Q4A is rollover vs new?

  No external writes made (read-only Notion, Slack, Linear).

  ## Agent run 2026-09-17T11:52:00Z — deeper inference from Linear (Q4A doc still unread)

  Everything here is INFERENCE from TOOL-team Linear state, not the doc. Confidence noted per item.

  ### Signal: Stephanie groomed the board on 2026-09-16, hours before sharing the doc
  Projects touched that day: PMS Capabilities (-> Paused, 26Q4B), Interactive Investigations,
  Unify Onboarding, Hotel Support ID (-> Completed), Zendesk Context App (-> Completed), Intl phone
  numbers, MCP SQL Tool. Only two projects carry the 26Q4A label so far, so labelling is incomplete
  — the doc is likely ahead of Linear. Expect the block-planning meeting not to have happened yet
  (Q3B's was 2026-08-12; most Q3B targets are 2026-09-30).

  ### Probable Q4A shape
  **A. Rollover from Q3B (high confidence) — these will not finish by 09-30:**
  - SAG Types (Rami): ticketed 09-11 into ~20 issues; ~7 Done, 2 In Review, 1 In Progress, ~10 Todo
    incl. "Auto approve at request time" (TOOL-687
    https://linear.app/canary-technologies/issue/TOOL-687/auto-approve-at-request-time), requester
    binding (TOOL-677), google-group approver routing (TOOL-682), per-region leaders (TOOL-683).
    First type is CHECK_IN_CONFIGURATION — i.e. the Check-in V3 driver, not user-management.
  - Canary MCP SQL Tool (Asher): code exists, now blocked on infra/security plumbing — RDS Proxy
    user (TOOL-666), grant-applier cron (TOOL-667), Agent Vault egress (TOOL-665), Cloudflare Access
    bypass (TOOL-656), WAF NAT IPs (TOOL-664). Two security findings filed 09-16: mcp-server
    require-auth policy NOT enforced in prod (TOOL-704
    https://linear.app/canary-technologies/issue/TOOL-704/mcp-server-require-auth-authorizationpolicy-is-not-enforced-in-prod)
    and Django logging X-Mcp-Internal-Secret in cleartext (TOOL-703, High
    https://linear.app/canary-technologies/issue/TOOL-703/django-logs-every-x-request-header-in-cleartext-including-x-mcp).
    Mostly unassigned -> depends on Platform/Infra bandwidth. Likely a "team request" in the doc.
  - AI Workup Accuracy (Laura, target 10-06): has turned into an "Investigate plugin 2.0" rewrite
    (pipeline.py orchestrator, the loop, termination/debate gating, resolvers, posting gate in
    shadow). Bigger than the Q3B bullet implied.
  - Automate Check-in V3 Onboarding (Sam): slipped 09-04 -> 09-30 "due to IHG work", only now in
    Eng Design, "aligned with A&D timelines"
    https://linear.app/canary-technologies/project/automate-check-in-v3-onboarding-617b22ca4b48/activity#project-update-a1178b51
  - Unify Onboarding & Add Products (Rami): labelled 26Q4A, target 08-14 long passed.
  - Canary Pages magic links (Laura): still Eng Design past 09-11 target.

  **B. New for Q4A (medium confidence):**
  - AI Workup: Interactive Investigations — labelled 26Q4A, in Product Definition.
  - Extend SAGs to Above Property — named "next block — Q4A" in Q3B doc; no Linear project yet.
  - Enable Support to Manage Hotel Users — still Backlog with 26Q3B label, no work started; gated
    on SAG Types. Either slides to Q4A as the second SAG type or the approach is still unresolved.
  - Workup Staged Rollout to Eng-Routed Teams — summary literally says "revisit ~Q4A"; status Planned
    https://linear.app/canary-technologies/project/ai-workup-staged-rollout-to-eng-routed-teams-7ca5cf153530
  - Workup: Faster, Cheaper Runs — Planned, was deprioritized in Q3B.
  - Onboarding Checklist (IHG-requested, enterprise/portfolio-configured, "needs product
    definition") — Stephanie-led, created 09-03. Likely Discovery.
  - Workup guest data handling (PII pseudonymize/erase) — created 09-04, no lead. Compliance-driven.

  **C. Pushed out / dropped (high confidence):**
  - Configure PMS Settings from PMS Capabilities -> Paused, 26Q4B. Tier 1 100%, Tier 2 5%, Tier 4 13%,
    rest 0%. Your design-review blocker is moot for Q4A but will come back in Q4B.
  - Intl phone numbers -> on hold, offTrack, waiting on Support's research
    https://linear.app/canary-technologies/project/international-support-country-based-phone-numbers-95ee795699db/activity#project-update-7647b7b3
  - Canceled: Support Web Form, Model Benchmark, Team Enablement via KB.
  - Still paused: Gateway Config Events (ChangeTracker); Zendesk OAuth.

  ### What this means for you / Enterprise (why she likely shared it)
  - Two of the plausible new Q4A items sit on Enterprise ground: **above-property SAGs** (portfolio /
    management-group scoping, Wyndham-style enterprise approver scoping) and the **IHG Onboarding
    Checklist**. Expect asks for requirements, a design partner, or review time.
  - IHG work already displaced Check-in V3 automation once this block — worth asking what IHG
    demand she's planning around for Q4A (ties to ENT-6032 HotelKey pilot onboarding scripts).
  - SAG auto-approve (TOOL-687) is landing: check it matches the spec you wrote and the SOC 2
    framing from the Q3B meeting.
  - Team capacity looks like the real constraint: 4 engineers (Laura, Asher, Rami, Sam), each
    already carrying a rollover project; Asher was pulled off PMS Capabilities onto MCP + Compendium.

  ### Sharper questions for the 1:1
  1. How much of Q4A is genuinely new vs rollover, and what got cut to make room?
  2. Above-property SAGs: is it in, who is the Enterprise counterpart, and is self-serve SSO still the trigger?
  3. User management: did the "re-evaluate" action conclude — scoped SAG type + L2, or automation?
  4. MCP SQL tool: who owns the infra tickets and the two security findings (TOOL-703/704)?
  5. PMS Capabilities in Q4B: what does she need from you on the design review, and when?
  6. Onboarding Checklist: what exactly did IHG ask for, and who defines it?

  No external writes made (read-only Linear).

  ## Agent run 2026-09-17T12:21:59Z — ACTUAL Q4A doc read (supersedes the inference above)

  Doc: https://app.notion.com/p/3db8146861518171aab0dbfe1d5b53ca (last edited 2026-09-17 11:52Z,
  no comments/discussions). Linear Q4A view:
  https://linear.app/canary-technologies/team/TOOL/projects/view/q4a-d0024df01b68
  It is a short, list-style draft — no narrative, no priorities/themes section, no meeting notes
  yet (unlike Q3B). Read time ~5 min.

  ### What's in it
  **Completed:** IHG AI Compendium Onboarding (Rami); Workup Next-Step Metric (Laura, labels live on
  prod tickets); Workup Diagnosis-Quality Tracking (Laura); Hotel Support ID (Kevin); Zendesk
  Context App enrichment (Laura).
  **In Progress (all rollover from Q3B):**
  - AI Workup: Accuracy (Laura) — investigate plugin reworked into a closed-form pipeline
    (classify -> checks -> loop -> debate -> report). Phase 4 = 2.0.0 checks framework; Phase 5 = the
    loop; Phase 6 (future) = investigate-learn + fleet miner. Guide:
    https://pages.cnry.cloud/investigate-plugin-guide/
  - Canary MCP SQL Tool (Asher); SAG Types (Rami); Automate Check-in V3 Onboarding (no owner
    named in the doc; Sam in Linear); Canary Pages magic links (Laura); Unify Onboarding & Add
    Products (Rami).
  **Up Next:**
  - Onboarding Partial Activations — per-product "Set Live" in the automated flow so partial
    activations don't drop to manual; builds on Unify.
    https://app.notion.com/p/3cf81468615181da8893f52bfdfdf2d1
  - Zendesk OAuth Migration — Ready for Eng, cutoff Apr 2027 (was deprioritized in Q3B)
    https://linear.app/canary-technologies/issue/TOOL-387/zendesk-oauth-migration
  - AI Workup: Interactive Investigations (Laura).
  **For Consideration (the actual decisions to discuss):**
  - Productionize Implementation Team Pipeline AI App (**Atrium**) — whether/how Internal Tools
    takes it on. https://app.notion.com/p/38b8146861518015ac8ccb8a3e70c0e5
  - Onboarding Checklist — portfolio-inherited, required items read real system state,
    IHG-requested, "Needs validation". https://app.notion.com/p/3d081468615181a3b147db979d2d7df9
  - CS Skill Curation — CS publishes skills without GitHub (submit -> auto-checks -> curator ->
    Trove catalog / Cowork plugins). https://pages.cnry.cloud/cs-skill-curation/
  - Bulk Support Access Requests — one SAG request across many properties (Mid-Market bulk-change
    case). https://app.notion.com/p/3db81468615181528dfef27233da25c3
  **Ongoing:** AI Compendium Improvements (Asher) as a standing bucket.
  **Other Teams:** Default Language Plan -> EMEA onboarding pod; Automate Voice Onboarding split
  three ways (language -> EMEA, voice model + trunk IDs -> Voice team, script wiring -> Internal Tools).
  **Deprioritized:** Gateway Config Events; Workup Staged Rollout; Workup Faster/Cheaper;
  **Configure PMS Settings from PMS Capabilities — "on hold (design review / PMS-Gateway
  bandwidth); planned for Q4B".**
  **Team considerations:** "Atrium ownership" and "**Laura leave**".

  ### Where my Linear inference was right / wrong
  - Right: rollover list, Interactive Investigations, PMS Capabilities -> Q4B, Staged Rollout and
    Faster/Cheaper still parked, Onboarding Checklist as unvalidated candidate.
  - Wrong: **Extend SAGs to Above Property is NOT in the doc at all** (Q3B had promised it for
    Q4A). Closest thing is Bulk Support Access Requests, framed as Mid-Market, not Enterprise.
  - Silently missing vs Q3B: **User Management / Enable Support to Manage Hotel Users** (the ~78%
    of Oncall item — gone without a line), Intl Support phone numbers, Hotel Support ID backfill,
    Workup guest data handling (PII), and the Cost-to-Serve section.
  - New and not visible in Linear: Partial Activations, Atrium, CS Skill Curation, Bulk SAG.

  ### Observations for the 1:1
  1. **Laura leave is the biggest risk in the doc.** She owns Accuracy (mid-rewrite, Phases 4-5),
     Pages magic links, and the Up Next Interactive Investigations — i.e. all of Workup. Ask:
     dates, who covers, what pauses.
  2. **PMS Capabilities still lists "design review" as a hold reason** — that was you in the Q3B
     notes. Clarify whether anything is owed from you before Q4B or if it's purely Gateway bandwidth.
     Design: https://app.notion.com/p/39181468615180238a31da976288eb14
  3. **Above-property SAGs dropped, Bulk SAG added.** If Enterprise still needs portfolio-level
     grants (Wyndham approver scoping, self-serve SSO trigger), say so now; the two could be one
     design (multi-property grant) rather than two.
  4. **User management vanished.** It was the largest Oncall sink and the Q3B action was
     "re-evaluate". Ask whether it's dropped, waiting on SAG Types, or just unlisted.
  5. **Onboarding Checklist "needs validation"** — IHG-requested, so you're the natural validator;
     decide whether you want it and what IHG actually asked for.
  6. **Block is rollover-heavy with little themed narrative** — 6 in-progress carryovers for ~4
     engineers, one of whom is going on leave. Atrium + CS Skill Curation + Bulk SAG + Checklist
     can't all fit; worth asking what her own ranking is.
  7. Zendesk OAuth moving to Up Next with an Apr 2027 cutoff looks like filler relative to user
     management — reasonable to question.

  No external writes made (read-only Notion).
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/D09Q1PTAMTR/p1789587177222649
tags:
- morning-gtd
- slack
time_minutes: 15
title: Read Stephanie's Internal Tools Q4A planning notes before today's 1:1
updated: 2026-09-17 17:18:16.588003
waiting_on: null
waiting_since: null
working_on: false
---

Stephanie shared the Notion doc in advance of our 1:1 today.
https://app.notion.com/p/canarytechnologies/Planning-Internal-Tools-Q4A-Internal-Notes-3db8146861518171aab0dbfe1d5b53ca
https://canarytechnologies.slack.com/archives/D09Q1PTAMTR/p1789587177222649