---
area: null
completed_at: 2026-11-20 14:00:42.687163
contexts: []
created: 2026-11-19 22:47:56.891892
defer_until: null
due: null
energy: low
id: 2026-11-19T2247-explore-canary-atlas-philippe-s-work
order: null
output: |-
  ## Agent run 2026-11-20T13:08

  ### What it is
  "Atlas" is two things that share a name. Jason and Daga untangled this in #eng-orbital today (https://canarytechnologies.slack.com/archives/C0CJ7M5FQMQ/p1795171796487349).

  1. **Canary Product Atlas (the knowledge base) - Philippe Torbey, Head of Product Ops, owns and drives it.** Gurtej collaborates. Gurtej's framing: "a codified map of how the product works today and how it should work for a given customer, brand and enterprise nuance included", the product piece of a wider context layer. Kickoff post is the first message in #canary-product-atlas, 2026-11-05: https://canarytechnologies.slack.com/archives/C0CEURVDHGB
  2. **Atlas the agent - Jason Flax (Orbital / Engram).** A Slack bot (@atlas) that reads the knowledge base and answers questions, with Engram as its memory. Not Philippe's work.

  ### Philippe's work: the product-documentation repo
  Repo: https://github.com/canary-technologies-corp/product-documentation (created 2026-11-03, 91 PRs, 84 commits by Philippe, the rest by the canary-docs-writer bot).

  - A documentation agent (Claude Code in GitHub Actions, weekdays 13:37 UTC) reads canary at the **production-deployed commit** plus GrowthBook flag changes, triages what needs docs, and opens one PR per product with KB articles, reference sheets and weekly release notes. It never merges; people review everything. PM review requests go to the Linear PDOC team.
  - The repo is the source of truth. Notion is a generated mirror (Product Documentation: https://app.notion.com/p/40d814686151812caa6bf3140b1c8bb5); Zendesk comes later.
  - Trust rules in AGENTS.md: code decides behavior, PRDs decide intent, Slack is never a source. `decisions.yaml` holds answers people already gave, `feedback/log.yaml` logs every reviewer comment, and a monthly review turns patterns into rules.
  - Feedback sweep: every 2 hours for Linear PDOC, twice a day for Notion comments. Accuracy feedback from PMs/engineers is applied after a code check without review; others' feedback goes to a PM first.
  - Coverage now: Upsells (52 files), AI Voice (60), Digital Authorizations (32), Digital Contracts (26), Payments (12), plus platform and PMS integration pages. PMS is next (he was meeting Sharon on 11/20). He is asking which product to do after that.
  - Eval: answer the last 3 months of #product-questions from the KB only. Philippe got ~80% after regrading; Gurtej estimates today's bots (Claude tag, PMS capabilities bot, voice bot) at ~35%, target 95%.
  - Latest weekly update (2026-11-19) is the newest post in #product-ops-product-education-foundations: https://canarytechnologies.slack.com/archives/C0CA24DFS56 Full pipeline went live and runs daily this week.

  ### The parts that touch you (my read, not something anyone said)
  - **Wyndham brand page.** Started this week: `brands/wyndham.md` plus 8 sub-pages (PMS and payments, registration card and check-in, guest messages, upsells, AI voice, programs and lifecycle, ...), merged in PR #89 (https://github.com/canary-technologies-corp/product-documentation/pull/89). It is generated from `backend/canary/onboarding/configuration_providers/wyndham/`, `wyndham_definitions.py`, `wyndham_check_in_out_times.py` and GrowthBook rules for the Wyndham portfolio. Reviewer is Connor Swords; Philippe said he will review it with Connor and Dianna. It mirrors to a Notion database "Brand restrictions and configurations". Wyndham is the only brand so far; IHG, BW, Marriott would follow the same pattern.
  - **Overlap with your settings field guide.** His agent documents settings in dashboard/Django-admin names per product, from the code. Your field guide covers hotel config keys per model. Same source, different cut; nobody has connected the two.
  - **Overlap with Workup / enterprise KB.** The stated goal is that support, CS and agents get product answers from the Atlas. `changelog.yaml` records corrections with what the docs said before, so earlier wrong answers can be found.

  ### Open questions in flight (Jason's side)
  - Daga objected on 2026-11-19 to the Atlas agent crawling Slack/Notion/Linear/GitHub into one Supabase-hosted Engram (security sprint, no MFA, wide access) and asked whether pre-extracted facts scale: https://canarytechnologies.slack.com/archives/C0CJ7M5FQMQ/p1795113892500559
  - Where it stands today: crawlers paused, Atlas agent sits on top of Philippe's KB. agents #739/#743/#745 merged; #740, #742, #748, #752 wait on the Atlas decision (https://canarytechnologies.slack.com/archives/C0CJ7M5FQMQ/p1795169008092079).
  - Atlas bot test answers are in #temp-atlas-check (C0CL22AP42U); it cites product-documentation files directly.

  ### Channels
  - #canary-product-atlas (C0CEURVDHGB): the context-layer conversation, Gurtej/Philippe/Jason
  - #product-ops-product-education-foundations (C0CA24DFS56): Philippe's execution channel, weekly updates
  - #eng-orbital (C0CJ7M5FQMQ): Atlas agent / Engram engineering

  ### Not done
  I read the README, AGENTS.md, brands.yaml, products.yaml and the PR list. I did not read the Wyndham brand pages themselves or check them for accuracy, and I did not open the Notion mirror or the Customer education project doc (https://app.notion.com/p/canarytechnologies/Customer-education-3ec814686151813a9e02c65863b7b41e).

  ## Agent run 2026-11-20T13:50 - rules-based configuration and the Wyndham brand page

  Gareth's note: the Wyndham brand page should also take rules-based configuration into account. Checked against the docs repo at main and canary master.

  **Already there, partly.** Two of the eight area pages mention it:
  - `brands/wyndham/pms-and-payments.md` has a "Configuration rules" paragraph (line 220) listing values the rules lock and values only the save warning flags.
  - `brands/wyndham/registration-card-and-check-in.md` has one (line 216) covering check-in values, the ID rule by country and PMS posting.
  Both cite `enterprise_wyndham/configs/wyndham.py` in their agent-only blocks and describe the rules as "warn-only drift".

  **Gaps.**
  1. `brands.yaml` `code_paths` for Wyndham lists only the onboarding providers and `wyndham_definitions.py` / `wyndham_check_in_out_times.py`. `backend/canary/enterprise_wyndham/configs/` and `backend/canary/rules_based_configuration/` are not there, so a change to the rules alone does not send the page for a refresh.
  2. The `update-brand-page` skill never mentions rules-based configuration. Its sources are onboarding (section 1) and GrowthBook (section 3). The agent found the rules file by tracing, not by instruction, so the next brand page may miss it.
  3. The overview `brands/wyndham.md` and the other six area pages do not mention the rules. I did not check which of those areas the rules actually cover.
  4. Framing: the pages treat onboarding as what a hotel has and the rules as a side note about warnings. The rules file declares the expected config per group (Connect GMS, Connect GMS live, Connect Plus, EU region, US region, North America live, the ID-collection groups, all-inclusive), which is the "how it should work for this brand" statement the Atlas is after.

  **Draft feedback for Philippe (not sent).** Destination to choose: a PDOC Linear issue, or a reply in #product-ops-product-education-foundations.

  > The Wyndham brand page should treat rules-based configuration as a source alongside onboarding and GrowthBook. `backend/canary/enterprise_wyndham/configs/wyndham.py` declares the config Canary expects for each group of Wyndham hotels (by MSA, region, live status, ID-collection country), and `backend/canary/rules_based_configuration/` checks hotels against it. Two area pages already cite it, but only as a drift warning. Three changes would cover it: add both paths to Wyndham's `code_paths` in `brands.yaml` so rule changes refresh the page; add a step to the `update-brand-page` skill to read the brand's rules config and say, per setting, whether a rule expects it and for which group; and where onboarding and the rules disagree, flag it for review. Happy to walk through how the rules tree works.
project: null
source_id: null
tags: []
time_minutes: 5
title: explore canary atlas philippe's work
updated: 2026-11-20 14:00:42.687116
waiting_on: null
waiting_since: null
working_on: false
---