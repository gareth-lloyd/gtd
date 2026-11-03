---
area: null
completed_at: 2026-11-02 15:00:02.727066
contexts: []
created: 2026-10-30 15:13:09.650404
defer_until: null
due: null
energy: low
id: 2026-10-30T1513-structured-input-in-settings-assist
order: null
output: |
  ## Agent run 2026-11-02T14:50
  **Short answer: partly. The agent cannot present an arbitrary form to collect input before it acts. It has two narrower forms of structured input.**

  Worktree: ~/projects/canary-settings-assist, branch `codex/settings-assist` (Sudarshan Muralidhar, head 211d86f3aac, 2026-10-22).

  1. **Clarification = single-choice buttons only.** The LLM's output model `SettingsDecision` (backend/canary/settings_agent/agent/types.py) has `kind` = clarification|read|proposal|handoff|unavailable, plus `question: str` and `choices: list[str]`. `ClarificationCard.vue` renders the question and one outlined button per choice. Clicking a button sends the choice text back as the next chat message. It has no fields, types, multi-select or validation, and the user can type free text instead.
  2. **Proposal review = typed, schema-driven editor.** When the agent proposes a change, each prepared operation carries an `editor_schema` (JSON Schema). `PlanItemEditor.vue` and `editorSchema.ts` render real controls from it: inputs, selects, enums, nested objects, arrays, `oneOf`/`anyOf` variants and optional-field collapse. The user edits the proposed values and `revise(plan.id, revision, operations)` posts them back, then approves. This is form-like structured input. But the capability provider defines the schema (capabilities/contracts.py), not the agent. It only appears after the agent has already prepared a proposal with draft values. It edits a proposed save; it does not ask the user to fill in missing information.

  So the pattern "the agent needs X, Y and Z, so it shows a form" is not supported directly. The closest way to get it is for the agent to propose a change with placeholder or best-guess values and let the user fix them in the plan editor. The other route is a sequence of single-choice clarifications. To add a real "ask with form" step, a new decision kind (or a `fields`/`input_schema` on clarification) would need to reuse the existing editorSchema/PlanItemEditor renderer. Most of the frontend for that already exists.

  Not run: I did not launch the app or eval suite. This is from reading the code only.
project: null
source_id: null
tags: []
time_minutes: 5
title: structured input in settings assist
updated: 2026-11-02 15:00:02.727060
waiting_on: null
waiting_since: null
working_on: false
---

Does Sudarshan's work, checked out locally in a worktree, let the settinsg assist agent take structured input by presenting a form to the user?