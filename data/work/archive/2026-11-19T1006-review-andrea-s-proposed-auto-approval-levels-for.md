---
area: null
completed_at: 2026-11-19 14:51:36.146641
contexts:
- consume
created: 2026-11-19 10:06:56.400728
defer_until: null
due: null
energy: medium
id: 2026-11-19T1006-review-andrea-s-proposed-auto-approval-levels-for
order: null
output: |
  ## Agent run 2026-11-19T12:47

  **Verdict: I would sign Yellow.** Level 1 is fine with two path removals. Level 2 should be split so the rubric runs in shadow before the merge rule changes. Nothing was posted anywhere; draft comments are at the bottom.

  ### Sources
  - Slack post, Andrea, 2026-11-18 23:34 EET, asks pod-enterprise to comment before end of week: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1795037698564479 (still no thread replies, one :joy: reaction)
  - Notion page "Auto-approval levels for Enterprise (ENT)": https://app.notion.com/p/canarytechnologies/Auto-approval-levels-for-Enterprise-ENT-41c8146861518137b62cc9754fffd63d (no comments or suggested edits yet; I did not read the rows of the sign-off table)

  ### What the page proposes
  - Level 1 (now): a `service` policy `enterprise-low-risk-paths`. The five pod-enterprise authors get a bot approval on low-risk ENT paths, about 10% of PRs. No birdline change.
  - Level 2 (next): an ENT risk rubric for the Approval Risk agent, plus a split of the birdline `enterprise` rule so `onboarding/plans/` and `configuration_providers/` get `author_counts: true`. Up to about 40%, only when the author requests a Macroscope review.
  - Level 3 (decide after four weeks): plans and providers added to the path policy, about 35% guaranteed.
  - Level 4 (not recommended): every single-owner ENT path except migrations.

  ### What I checked
  Checked against `origin/master` at 9fdbb464c6e (2026-11-19). The local `master` checkout is from 2026-10-30 and lacks most of these policies.
  - Confirmed: the policies it cites exist (`in-stay-paths`, `internal-tools-paths`, `staff-ops-paths`, `identity-service-paths`, `gateway-engineer-low-risk`, `gateway-engineer-non-critical`, `approval-risk`, `signal-review`) with the shapes described.
  - Confirmed: the birdline `enterprise` rule gates plans, providers, `sso/`, `permissions/constants/` and `membership_level_new.py` on a pod-enterprise approval with no `author_counts`.
  - Confirmed: pod-enterprise has exactly the five logins listed.
  - Confirmed: rubrics exist for kiosk, sdm, pms-gateway and eng-enablement, none for enterprise.
  - Not checked: the PR statistics (504 PRs, 48% no-comment approvals, 23% waiting over 24h, zero reverts, the week of 11-10 verdict counts).

  ### Concerns, most important first
  1. **Level 1 contradicts the Level 2 rubric.** The rubric rates "Salesforce or SaaSOptics writebacks" as High, but Level 1 puts all of `backend/canary/salesforce/` and `saas_optics/` in a `service` policy, which approves on path alone and never consults the rubric. Both hold write code outside `management/commands/`: `salesforce/services/push_hotel_support_ids.py`, `saas_optics/services/customer.py`, `saas_optics/services/transaction.py`, `saas_optics/views/dashboard/invoice.py`. Either drop both apps from Level 1 or exclude their `services/` and `views/`.
  2. **`rules_based_configuration/` is not obviously low-risk.** A wrong rule or binding misconfigures a whole cohort silently, which is the failure the rubric rates High for plans and providers. It also carries compliance rules (EU ID, the parked German retention rule). I would hold it for the Level 2 agent route.
  3. **Level 2 removes the last human from the highest-blast-radius code on thin evidence.** With `author_counts: true` plus a bot approval, a plan or provider PR merges with no human whenever the agent says safe. The evidence is one week: 12 verdicts, 11 safe. The rubric is six High bullets. Suggest shipping the rubric first, comparing verdicts to human reviews for two to four weeks, then doing the birdline split.
  4. **"No reverts" is the wrong safety measure for ENT.** ENT mistakes are fixed forward with a follow-up PR or a DB script, not a revert. The Level 3 gate ("no auto-approved PR needed a fix or a revert") has the same gap, and names no owner or method. Suggest counting follow-up fix PRs and ENT tickets traced to an auto-approved PR, with a named person doing the four-week read.
  5. **Level 2 coverage is optimistic.** 46 of 58 ENT PRs had no verdict that week, a verdict goes stale on any push, and the agent runs at most twice per PR. "Up to 40%" needs a habit change that only one member has today. Realistic coverage is probably nearer the Level 1 figure until then.
  6. **48% silent approvals does not prove review adds nothing.** Some review happens in Slack or pairing, and review is how the team sees each other's brand config. Worth asking what replaces that awareness (for example a weekly digest of auto-approved PRs).

  ### Smaller points
  - `gareth-lloyd` is not in the author list, so my own PRs (for example ENT-7726 in `rules_based_configuration/`) get nothing from any level. Decide whether to ask to be added or accept that. This is a personal call, not a flaw in the page.
  - Golem PRs are authored by `megolem` (for example PR #62682, https://github.com/canary-technologies-corp/canary/pull/62682), so the author condition keeps them out. Good, and worth stating on the page so nobody adds `megolem` later.
  - Level 1 includes `agent-plugins/claude-plugins/enterprise/` but excludes `skills/`, `prompts/`, `SKILL.md` and `CLAUDE.md`. What remains is mostly `commands/` (for example `work-ticket.md`), which also instructs autonomous Golem. The Gateway policy excludes all agent-instruction folders; `commands/` should probably join them.
  - Coverage for Level 2 ("up to 40%") is above Level 3 ("35% guaranteed"), which reads oddly in a table where each level includes the previous one.

  ### Draft Notion comment (not posted)
  > Yellow from me. Level 1 looks good with two changes: (a) drop `salesforce/` and `saas_optics/`, or exclude their `services/` and `views/`, because the Level 2 rubric rates their writebacks High and a service policy never consults the rubric; (b) hold `rules_based_configuration/` for the agent route, since a wrong rule misconfigures a cohort silently. For Level 2, can we ship the rubric first and compare its verdicts with our reviews for a few weeks before the birdline split? One week of 12 verdicts is thin for taking the human off plans and providers. Last, "no reverts" will not catch our failures because we fix forward. Could the four-week check count follow-up fix PRs and ENT tickets traced to an auto-approved PR, with a named owner?

  ### Open decisions for you
  - Sign-off colour (I suggest Yellow) and whether to post the comment above. The page asks "each Enterprise engineer" to sign; you are not in pod-enterprise, so a page comment may fit better than a table row.
  - Whether to ask for `gareth-lloyd` in the author list.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1795037698564479
tags:
- morning-gtd
- slack
time_minutes: 15
title: Review Andrea's proposed auto-approval levels for Enterprise (#epd-enterprise-engineers)
updated: 2026-11-19 14:51:36.145847
waiting_on: null
waiting_since: null
working_on: false
---

Andrea had Claude propose auto-approval configuration levels and put them in Notion to start the conversation. No replies yet.
https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1795037698564479