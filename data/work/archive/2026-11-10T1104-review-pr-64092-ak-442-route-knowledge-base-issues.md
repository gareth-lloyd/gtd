---
area: null
completed_at: 2026-11-10 15:53:25.300472
contexts:
- react
created: 2026-11-10 11:04:31.017955
defer_until: null
due: null
energy: medium
id: 2026-11-10T1104-review-pr-64092-ak-442-route-knowledge-base-issues
order: null
output: |-
  ## Agent run 2026-11-10T12:53:57

  Verdict: safe to approve, with one typo to fix and one scope point for the author to confirm. Nothing posted to GitHub; the draft comment is at the bottom.

  PR #64092 (https://github.com/canary-technologies-corp/canary/pull/64092) for AK-442 (https://linear.app/canary-technologies/issue/AK-442/update-issue-routing-for-ak-triage). Prompt and eval dataset only: instructions.txt (+21/-13) and dataset.yaml (+87/-11) under backend/canary/linear_agent/prompts/team_classification/. No Python changes.

  What I checked
  - The "no code change" claim holds. LinearTeam.AK = "ak", "Agent Knowledge" already exists (backend/canary/linear/constants.py:258), TeamClassificationOutput types team as LinearTeam, and IssueRoutingService.route_issue looks the team up by that label. "ak" is not in NON_ROUTABLE_TEAMS or TEAM_ROUTING_OVERRIDES.
  - CI is green. The only red check is "Birdline policy", which is just waiting for an approval and is not a gate.
  - No reviews or inline comments yet from matiasmarcodelpont or ramironieto.
  - Not done: I did not rerun team_classification_evals (the 506/510 figure is the author's), and I did not check that a LinearTeam row named "Agent Knowledge" exists in each prod region. If the row is missing, route_issue raises ValueError and the issue stays unrouted, so the failure is loud rather than a misroute.

  Points worth raising
  1. Scope differs from the ticket. AK-442 says KB *and* service ticket / ticket_gateway issues should go to Agent Knowledge. The PR sends live service ticket integrations to pms instead (third commit reverses the first). The basis is Matías's 2026-11-09 #epd-messaging message that ticketing gateway integrations are owned by another group (https://canarytechnologies.slack.com/archives/C05MRAL7ZDH/p1794244098441859?thread_ts=1794240161.915089&cid=C05MRAL7ZDH). I confirmed the message exists but did not resolve the user-group handle to PMS Engineering. Matías is a reviewer and moved the ticket to AK, so he is the right person to confirm; the ticket description (Kelly Waters, May) should be updated to match.
  2. Typo in the pms team description, instructions.txt line 26: "vendor connection errors.Handles all integration troubleshooting" is missing a space.
  3. Cases 101 and 164 look inconsistent. Both are "guest got a confirmation, nothing in the vendor, issue does not say whether the AI filed it". 101 expects pms with msg competing, per the new rule; 164 expects pms with no competing team. Either 164 should list msg, or the rule should say that "was working, stopped this week" removes the ambiguity. Likely source of flakiness later.
  4. Coverage gaps, optional: no Wyndham voice KB case (ak with ev competing), and HubOS/Knowcross are named in the prompt but have no case.
  5. Follow-ups the PR itself flags and leaves open: CODEOWNERS still gives /backend/canary/ticket_gateway/ to pod-messaging (CODEOWNERS:555); High/Urgent issues are still not auto-routed.

  Judgment calls I agree with: reading "anything involving knowledge base" narrowly (wrong answer goes to ak only when the issue points at the KB), keeping intent misreads and canned responses with msg, and keeping the AI's ticket decision with msg/vox/ev.

  Draft review comment (not posted)

  > Approving. Prompt and dataset only, and `LinearTeam.AK` already carries the "Agent Knowledge" name the router looks up, so no code change is needed.
  >
  > - AK-442 asks for service ticket issues to go to Agent Knowledge too; this sends live integrations to `pms`. @matiasmarcodelpont can you confirm that is what you want, and update the ticket text?
  > - `instructions.txt` pms description: missing space in "vendor connection errors.Handles".
  > - Cases 101 and 164 describe the same situation (guest confirmed, nothing in the vendor, unknown whether the AI filed it) but 101 expects `msg` competing and 164 expects none. Worth aligning one of them with the rule.
  > - Optional: a Wyndham voice KB case (`ak`, `ev` competing).
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/64092
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #64092: [AK-442] Route Knowledge Base issues to Agent Knowledge'
updated: 2026-11-10 15:53:25.300461
waiting_on: null
waiting_since: null
working_on: false
---

https://github.com/canary-technologies-corp/canary/pull/64092
Author: sudssm, branch claude/issue-routing-update-status-6732c3. Personally requested alongside matiasmarcodelpont and ramironieto.