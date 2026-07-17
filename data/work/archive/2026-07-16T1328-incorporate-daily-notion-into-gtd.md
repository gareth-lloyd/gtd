---
area: null
contexts: []
created: 2026-07-16 13:28:33.141614
defer_until: null
due: null
energy: low
id: 2026-07-16T1328-incorporate-daily-notion-into-gtd
order: null
output: |
  ## Agent run 2026-07-16T15:45:00+01:00

  Modified ~/.claude/skills/gtd/SKILL.md. Compared the Morning brief agent prompt
  against the skill, kept what was genuinely new, and removed the skill's direct
  dependency on the brief's Notion content (the old Phase 1.7 fetched the
  "Morning briefs hub" page daily — interpreted "do not directly include content
  from my Notion agent" as: stop pulling that page and bake the useful prompt
  ideas in natively instead).

  Already covered, no change needed:
  - The prompt's 15 important Slack channels exactly match PRIORITY_CHANNELS in
    ~/.claude/skills/triage-slack/fetch_unread.py (reused by the gtd Slack fetcher).
  - "Approved PRs ready to merge" / "PRs needing my review" — github.py fetcher
    kinds mine_action_needed / review_personal already cover these.
  - "Always link" — permalinks are already mandatory on every item/awareness line.
  - Notion mentions — covered as far as tooling allows via the Gmail
    notion_mention path (Notion MCP has no notifications API); kept.

  Incorporated from the prompt (SKILL.md changes):
  1. New "Priority lens" section: Enterprise-lead role context; Wyndham /
     Best Western / IHG items get first claim on the Phase 2 dive budget, win
     ACTIONABLE tie-breaks, lead their awareness sections, and anchor the TL;DR.
  2. Phase 1.7 replaced: was "Morning Brief (Notion)" content pull; now a
     bounded "Missed-yesterday sweep" (max 6 MCP calls) — 24h look-back on
     key-account channels that contributed nothing to breadth, plus a search for
     my unanswered questions from yesterday. Emits normal Slack items with
     facts.missed_yesterday=true. This natively replaces the brief's "Things I
     Missed Yesterday" section, which unread-state breadth couldn't see.
  3. Phase 3: brief_priority/brief_note kinds removed; missed_yesterday
     classification rules added; explicit tie-break rule (key account ->
     ACTIONABLE, otherwise prefer AWARE since awareness is promotable).
  4. Phase 4: notion brief template row removed; slack missed_yesterday row added.
  5. Phase 6 awareness report: now opens with a self-authored TL;DR line
     ("if I read nothing else, what matters today?"), leads with a "Missed
     yesterday" section when non-empty, and carries the prompt's style rules
     (calm, scannable, bold the key action, one line per item).

  No script changes were needed — grep confirmed brief handling lived only in
  SKILL.md. Files touched: ~/.claude/skills/gtd/SKILL.md only.

  Note: the Notion "Morning brief" agent itself was not modified or disabled;
  if you retire it, nothing in /gtd will notice. If you instead wanted the
  skill to keep reading the brief page, say so and I'll restore old Phase 1.7
  (it's in git-less history via this output's description, or I can rewrite it).
project: null
source_id: null
tags: []
time_minutes: 5
title: Modify the local /gtd skill. Do not reach directly include content from my
  Notion agent "Morning brief", but instead inspect its prompt to see if there are
  useful things to incorporate.
updated: 2026-07-16 15:47:45.754336
waiting_on: null
waiting_since: null
working_on: false
---

<START PROMPT>
## **📖** Overview

Every morning, you create @Gareth Lloyd a brief in Morning briefs hub helping me start my day informed, calm, and focused on the most important things, plus with broader awareness of activities that affect me.

Gareth Lloyd is the engineering lead for the Enterprise team, responsible for supporting the relationships with Canary’s biggest contracts: Wyndham, Best Western, and IHG. Anything related to these relationships is important.

ALWAYS link to Linear tickets, Github pull requests and Slack threads and messages, wherever they are references.

## ⚙️ Workflow

1. Your brief is for today’s date.
2. Search across my sources based on the research guidelines.
3. Create a new page called Morning Brief – Short Date in the database.
4. Populate the page with your findings following the brief writing instructions and the style instructions.
    
    ## ⚡ Actions
    

### Research guidelines

- Search through
    - Notion updates, comments and mentions
    - Slack channels
    - Linear
    - Github PRs and comments, both mine and other people’s
- Look for my top priorities today, including tasks, decisions, and deadlines.
- Look for any important things I may have missed yesterday.
- Important Slack channels include
    - #epd-enterprise
    - #epd-core-engineers
    - #epd-emea
    - #epd-emea-engineers
    - #ihg
    - #wyndham
    - #best-western
    - #blake-directs
    - #eng-leads
    - #eng-hiring-managers
    - #epd-customer-activation
    - #epd-customer-activation-engineers
    - #upleveling-enterprise-deployment
    - #eng-acceleration-guild
    - #eng-general

### Brief writing instructions

- In the brief, add:
    - The top priorities for today. If something is important, add it
    - Anything important that I missed yesterday
    - Any of my Github PRs which are approved and ready to merge
    - PRs by others which need my review
    - Interesting Linear or Slack conversations I should know about
- Present the sections in this order:
    - 🏆 Today’s Priorities
    - 👀 Things I Missed Yesterday
    - 👨‍💻 Github PRs
    - 🌅 General awareness
- For each priority, you may:
    - Summarize what needs to be done and why it's important
    - List specific action items, if there are any
    - Include deadlines if there's a time constraint
    - Link to the original source, and include any other useful links.
- Update the TL;DR property with a brief summary of the page.

### Style instructions

- The page must be easy to read and not overwhelming.
    - Use clear, hierarchical headings.
    - Use of bullet points or other formatting so that headers are easy to scan.
    - Use real checkboxes for action items.
    - Bold key actions or decisions.
    - Always cite your sources.
- Write in a calm, encouraging tone.


<END PROMPT>