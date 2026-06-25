---
area: null
contexts: []
created: 2026-06-19 00:28:55.584315
defer_until: null
due: 2026-06-23
energy: low
id: 2026-06-19T0028-operationaloze-decision-review
order: null
output: |
  ## Agent run 2026-06-24T20:37

  Built the idea as a Claude skill + a thin command wrapper. Both are live now
  (the skill appears in this session's available-skills list).

  ### What I shipped
  - **Skill**: `~/.claude/skills/decision-review/SKILL.md` — the full mechanics.
    Invokable as `/decision-review` and auto-surfaces on phrasings like "decision
    review this PR" / "what choices are in this PR".
  - **Command**: `~/.claude/commands/decision_review_of.md` — `/decision_review_of <PR>`,
    matching your existing `*_review_of` family (brutal/nice) for muscle memory. It
    just delegates to the skill.

  ### How it operationalizes the idea
  The skill reframes review from "hunt bugs in lines" to "adjudicate the choices the
  author made." Five phases:
  1. **Acquire** — resolve target (PR # via `gh`, branch diff, or working diff) + read
     the ticket/intent (a decision is only judgeable against intent).
  2. **Extract decisions** — pull every choice with a real alternative, tagged by kind
     (structural / contract / data-migration / behavioral / dependency / tradeoff /
     scope / test-strategy / naming). Explicitly *excludes* mechanical/forced changes so
     the agenda isn't noise. Each decision gets: what was chosen, the alternative,
     why it matters, **reversibility** (one-way vs two-way door), and an **implicit?**
     flag for decisions the author made without noticing — the highest-value finds.
  3. **Order** — exactly your ask: build the dependency DAG, present roots first
     (rejecting a root prunes its now-moot descendants), tie-break within a tier by
     reversibility (one-way doors first), batch trivia into one final item.
  4. **Walk one at a time** — fixed card format separating CHOSE / INSTEAD OF / RESTS ON
     / SUPPORTS / "My read", then **stops** for a verdict (accept · reject · discuss ·
     flag) before advancing. Reject upstream → offers to skip moot downstream items.
  5. **Ledger** — final verdict table; flagged items drafted as comments but never
     posted without explicit approval.

  ### Design choices I made (so you can push back)
  - **Skill, not just a command**: a skill carries the "mechanics of review" knowledge
    and auto-triggers; the command is a thin discoverable alias. Distilled the structure
    from the gtd SKILL.md (phase separation), the pr-review-toolkit `review-pr` command
    (aspect taxonomy, aggregation), and your `brutal/nice_review_of` commands (PR-as-arg,
    local-only, never touches GitHub).
  - **Reversibility (one-way vs two-way door) is the primary prioritization axis** within
    a dependency tier — that's the lever that makes "which decision deserves scrutiny"
    objective rather than vibes.
  - Kept it a judgment tool, not a linter: it's told NOT to manufacture concern on sound
    decisions and NOT to invent decisions for a mechanical PR.

  ### Try it
  `/decision_review_of <PR#>` or `/decision-review` on a branch with a diff. Single most
  likely tweak after a real run: the card format in Phase 4 (too verbose vs too terse).

  Not done / open: haven't dry-run it against a live PR yet — the real test is whether the
  dependency ordering feels right on a chunky PR. Suggest trying it on your next sizeable
  review and tuning the card + the "collapse trivia" threshold.
project: 2026-04-16T1348-ideas
source_id: null
tags: []
time_minutes: 5
title: Operationaloze decision review
updated: 2026-06-24 20:37:12
waiting_on: null
waiting_since: null
working_on: true
---

The idea is: PR review should be reconceptualized as decision review. 
The agent should read the PR and carefully parse out the decisions contained therein

Then it should present them to you in a carefully decided order based on the internal dependencies among hte decisions, allowing you to consider them one by one. 

Create a Claude skill or command that is aware of the mechanics of review to operationalize this. Learn from other skills and try to distill somethign that will work.