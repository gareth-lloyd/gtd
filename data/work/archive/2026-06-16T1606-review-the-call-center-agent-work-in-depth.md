---
area: engineering
contexts:
- deep
created: 2026-06-16 16:06:32.609636
defer_until: null
due: null
energy: high
id: 2026-06-16T1606-review-the-call-center-agent-work-in-depth
order: 3
output: |-
  # Call Center Agent Work — In-Depth Review

  Reviewed two engineering designs and the live PR state on `master`. Bottom line: the **dispatch seam was front-loaded and merged cleanly** (good), but the cost has shifted to the **agent base layer**, where Wyndham and Can Calco are being built as two divergent implementations in parallel.

  ## Design docs

  - **Design 1 — Call Center Conversational Routing** (VOX-3131, Voice team): https://www.notion.so/canarytechnologies/Call-Center-Conversational-Routing-3738146861518094b4f2e7a75491c56d
  - **Design 2 — Can Calco CallCenterAgent** (EMEA team): https://www.notion.so/canarytechnologies/Can-Calco-CallCenterAgent-3728146861518033b09bf8e0d67520d6

  ## What the two designs are

  **Design 1 (Voice).** Replace Wyndham's DTMF phone-tree IVR with a conversational entry agent: caller speaks naturally, the agent infers intent and routes to an automation, a specialist sub-agent, or a human team. Calls stay hotel-free (`Call.hotel = None`). Delivers `Experience.entry_agent_type` + a registry-backed dispatch, a shared `CallCenterBaseAgent`, `WyndhamCallCenterAgent`, and a pre-recorded language-select entry agent. **Note:** mid-review amendments (2026-06-09) reversed core decisions — dropped `IVRScript`/`IVRNode`-driven routing and the original two-dimensional dispatch (`entry_agent_type` mode + `CallCenter.agent_key`), collapsing to a single `entry_agent_type` field and moving routing logic in-code.

  **Design 2 (EMEA).** First non-Wyndham customer on the same foundation: one Spanish line serving 6 Mallorca hotels, KB-grounded answers scoped per property, booking links sent post-call by SMS/WhatsApp, and **never transfers** (fallback is a documented email/WhatsApp contact). Explicitly scopes the dispatch mechanism, the agent base class, nullable `crs_account_uuid`, and KB hosting as "Voice-team-owned — we plug in."

  ## Overlap assessment

  Deliberate, layered reuse — **not** a competing implementation. Can Calco is strictly downstream of Voice's foundation. The collision risk lived entirely in the items Can Calco listed as "out of scope, Voice owns it," which were open questions rather than frozen contracts: the base-agent interface, nullable `crs_account_uuid`, the dispatch field, and a net-new KB-on-`CallCenter` story (Design 1 has no KB story at all — "Wyndham has no KB").

  ## The core risk of simultaneous development

  Under commercial pressure both were built at once. The danger was that the *consumer* (Can Calco) was being built against a *platform* that was unbuilt and whose interface the doc had **mis-specified** — Can Calco assumed a `CallCenterAgent` base with `prompt(self, ud)` / `tools_for_intent(self, intent)` overrides, which does **not** match the codebase's real livekit idiom (`instructions=` kwarg, module-level `@function_tool()` functions, `update_tools()` / `update_instructions()`, handoff by returning an agent).

  ## What the code actually shows (live PR state)

  My first code check ran against a **stale worktree branch** (`worktree-portfolio-analytics-agent`); `master` had advanced well past it. Corrected picture:

  **Already merged to master**
  - `Experience.entry_agent_type` (free-text `CharField`, validated in `clean()` against an `EntryAgentType` `TextChoices` enum) — migration `0147`.
  - `voice/livekit/call_center/experience_agents.py` — the `EXPERIENCE_AGENTS: dict[EntryAgentType, Callable[[], Agent]]` registry (currently **empty**, with a commented example for the Can Calco key).
  - Worker dispatch: `EXPERIENCE_AGENTS.get(entry_agent_type)`.
  - Session/worker/post-call refactor (VOX-3022) and admin support.

  **Open / started work (PRs)** — repo `canary-technologies-corp/canary`:
  - Voice foundation:
    - #48011 — VOX-3299, transfer tool + telephony foundation (**DRAFT**): https://github.com/canary-technologies-corp/canary/pull/48011
    - #45741 — VOX-3028, IVR agent: https://github.com/canary-technologies-corp/canary/pull/45741
  - EMEA / Can Calco:
    - #47842 — Add `CanCalcoCallCenterAgent` + 4 tools + prompt + tests: https://github.com/canary-technologies-corp/canary/pull/47842
    - #48046 — Register Can Calco Agent (wires it into `EXPERIENCE_AGENTS`): https://github.com/canary-technologies-corp/canary/pull/48046
    - #47543 — [Part 2b] Resolve Twilio subaccount creds for call-center webhooks (EMEA-289): https://github.com/canary-technologies-corp/canary/pull/47543

  ## Two projected risks were actually mitigated

  1. **The hard seam was front-loaded.** `entry_agent_type` + the `EXPERIENCE_AGENTS` registry + worker dispatch landed first, on `master`, cleanly. Both teams plug into a real, merged contract — exactly the right de-risking move.
  2. **Can Calco self-corrected off the fictional API.** PR #47842 does **not** use the doc's imaginary `prompt()/tools_for_intent()` base. It subclasses livekit `Agent` directly with the real idiom (`instructions=`, `tools=[]`, `on_enter` → `update_tools`, `generate_reply`) and documents why: *"deliberately NOT a BaseAgent subclass… owns its tool set outright."* The no-transfer guarantee is thereby made structural — no transfer tool is ever registered.

  ## Where the real debt now sits

  1. **No shared `CallCenterBaseAgent`.** Can Calco went fully standalone with its own `CanCalcoCallState`; Voice's #48011 is still building the shared `CallCenterAgentUserData` + transfer foundation that Wyndham will sit on. The "thin subclass of a shared base" model both docs promised does not exist. Result: multilingual handling, post-call turn naming, state, and tool registration get implemented twice and will drift.
  2. **Deferred reconciliation.** Can Calco's own comment: swapping `CanCalcoCallState` for the foundation call-center userdata "is a one-line change" — but it isn't done. Two state models for call-center calls coexist.
  3. **Untested registry contract.** The registry is a zero-arg factory (`Callable[[], Agent]`). That works for Can Calco (all kwargs defaulted) but is unproven against Wyndham's need to inject per-call experience/call-center context at construction; Wyndham will likely have to read from session userdata in `on_enter` instead.
  4. **No-transfer guarantee is conditional.** It holds **only** while Can Calco stays off the shared base — in direct tension with any later consolidation onto #48011's foundation, which bundles the transfer tool.
  5. **Live sequencing / import-ordering dependency.** Can Calco can't be exercised end-to-end until #47842 (agent) + #48046 (register) + #47543 (Twilio) **and** Voice's #48011 foundation all land, roughly in that order. #48046 imports the agent module at registry-load time — the doc's "import it or the registry is silently empty → `worker.get()` returns `None` → calls fall through" footgun is now a real dependency.

  ## Suggested follow-ups

  - Decide explicitly whether Can Calco stays standalone or converges onto `CallCenterBaseAgent`; if it converges, re-establish the no-transfer guarantee structurally rather than by staying off the base.
  - Land the `CanCalcoCallState` → `CallCenterAgentUserData` reconciliation rather than leaving it as a "one-line change" IOU.
  - Prove the `EXPERIENCE_AGENTS` factory signature against Wyndham's context-injection path before #48011 leaves draft.
  - Verify registry import-wiring (AppConfig.ready / module import) so the registry isn't silently empty at worker start.
  - Confirm KB ownership: `call_center` FK on the KB entry model + `owner=CallCenter` / `property_tag` in `KnowledgeBaseSearchService` are net-new and not in Design 1's scope.

  *(Review based on the two Notion designs and open PRs as of 2026-06-16.)*
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 30
title: Review the call center agent work in-depth
updated: 2026-06-25 12:59:15.044947
waiting_on: null
waiting_since: null
working_on: false
---