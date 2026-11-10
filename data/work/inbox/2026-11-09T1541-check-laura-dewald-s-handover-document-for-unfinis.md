---
area: null
completed_at: null
contexts: []
created: 2026-11-09 15:41:50.651667
defer_until: null
due: null
energy: low
id: 2026-11-09T1541-check-laura-dewald-s-handover-document-for-unfinis
order: null
output: |
  ## Agent run 2026-11-09T16:05:00+02:00

  Source: Notion "Laura Parental Leave Coverage" (https://app.notion.com/p/4058146861518048b001e2fbf123e643), inline table "Responsibilities/Ownership", 18 rows, last edited 2026-11-03. 12 rows are checked "Handed off?", 6 are not. Nothing was written to Notion, Linear, Slack or GitHub in this run.

  Context that changes urgency: Laura posted in #epd-internal-tools-engineers today (2026-11-09 15:38 EET) that the baby came early and she is out now (no permalink captured; it is the top message in that channel today). The Nov 6 "team runs without Laura" date is therefore live and the 6 unhandled rows need owners this week.

  ### The 6 rows not marked handed off

  1. Canary Pages external sharing via magic links (row: https://app.notion.com/p/400814686151806ab83ec53478caa898). Status: build is finished. 15 of 16 project tickets Done; the last ten PRs (#182 to #190 in the cloudflare repo) merged on Nov 6. What is left:
     - TOOL-785 Launch external sharing on share.canarytechnologies.com (Todo, still assigned Laura) https://linear.app/canary-technologies/issue/TOOL-785/launch-external-sharing-on-sharecanarytechnologiescom. Needs: production custom-domain route, SHARE_COOKIE_SECRET via wrangler, robots.txt and favicon, curl checks in README, pilot page and customer (default: Nathan picks a QBR leave-behind), external-sharing Flagship flag on for the pilot manager only. Deploy is from a local checkout with no CI, so the pages/ subtree must match origin/main first.
     - TOOL-985 Stop domain allowlist entries from turning the sign-in caps into a lockout (Backlog, unassigned, created Nov 6 from pre-merge review) https://linear.app/canary-technologies/issue/TOOL-985/stop-domain-allowlist-entries-from-turning-the-sign-in-caps-into-a. One IP can burn a page's 200 daily sends in ~20 minutes and bounce Canary-branded mail to invented addresses.
     - Action: reassign TOOL-785 to Rami (named backup). Decide whether TOOL-985 lands before the pilot; my recommendation is to run the pilot with exact-address allowlist entries only and no domain entry, so TOOL-985 can follow. Ask Nathan for the pilot page and customer. Target: launch plan agreed before Q4B planning on Nov 19.

  2. Cloudflare repo ownership (row: https://app.notion.com/p/400814686151805ebcbff7b0a6bdafe1). Confirmed: no CODEOWNERS file anywhere in canary-technologies-corp/cloudflare. Of the 35 PRs merged since Oct 20, Laura authored 27; the others are Facundo (Dodo bot, 6), Adit (1), Dana (2). Open PR #198 by Facundo (Dodo webhooks) needs a reviewer https://github.com/canary-technologies-corp/cloudflare/pull/198. Top-level dirs: pages, zendesk-calls, linear-routing-stats, oncall-dashboard, dodo-pending-prs, linear-project-updates, pecking-order, people-db-rippling-to-notion-upload, slack-webhook-cron, voice-weekly-summary, windtrap.
     - Action: open a CODEOWNERS PR mapping pages/, zendesk-calls/, linear-routing-stats/, oncall-dashboard/ to the Internal Tools GitHub team, with the other dirs to their authors. Confirm at least one of Sam/Rami/Asher has Cloudflare wrangler deploy rights and the production secrets for pages, since deploys are manual. Ask Stephanie to own announcements for Pages.

  3. Zendesk Context app (row: https://app.notion.com/p/40581468615180f894c9d363917c58ee). Kevin is primary, Sam is to get admin. Open work still on Laura:
     - TOOL-789 Require hotel linking or N/A confirmation (Blocked, High, assigned Laura, no blocker recorded; Nensy asked for it on Oct 1) https://linear.app/canary-technologies/issue/TOOL-789/require-hotel-linking-or-na-confirmation-in-canary-context-app
     - Two stale draft PRs from June/July: canary#49686 Zendesk tickets modal on /manage/properties https://github.com/canary-technologies-corp/canary/pull/49686 and canary#48650 [TOOL-66] Comment on Linear issue when Zendesk ticket is closed https://github.com/canary-technologies-corp/canary/pull/48650
     - Action: reassign TOOL-789 to Kevin and find out what blocks it. Confirm Sam has Zendesk admin. Close the two drafts or hand them to Kevin explicitly.

  4. Orbital validation and testing (row: https://app.notion.com/p/400814686151809f8544d5d892c8d07c). Plan said "Sam validates with Laura before Nov 6". No evidence it happened: the only trace is Sam asking Laura on Oct 21 in #eng-alerts-internal-tools about a supabase db push error caused by separate migrations in orbital. No TOOL ticket exists. Jason said in #eng-acceleration-guild on Nov 8 that productionizing Orbital still needs "2 more weeks".
     - Action: ask Sam whether the validation happened. If not, treat it as a Q4B planning item on Nov 19, not a blocker, and ask Jason (backup owner) for a date when Workup can be installed as the first agent.

  5. On-call paging rules for Linear tickets (row: https://app.notion.com/p/40081468615180fa8c39dea3a470d826). Johannes (SRE) is primary, Sam backup. Evidence Johannes is already fielding it: Kevin asked him in #eng-alerts-oncall on Nov 4 to stop alerts firing on tickets already done and on tickets he escalated himself; James Morton noted on Nov 5 that Linear sends a webhook for High tickets from oncall. Related risk from the webhook row: on Sep 8 Linear auto-disabled the Canary webhook after a GitHub outage and urgent tickets missed Rootly for a week.
     - Action: confirm with Johannes that he owns the paging rules and knows the Sep 8 failure mode. File a TOOL ticket for Kevin's two bugs and assign Sam as code backup, since the rules live in the canary-side linear_agent code.

  6. Workup team enablement gate, LINEAR_AGENT_WORKUP_TEAMS (row: https://app.notion.com/p/4008146861518097b2e8d3337b4929cb). Blake decides, Stephanie logs, Sam flips. SDM is quietly enabled; Messaging is the only officially supported team; Arrivals/Departures has a PR waiting, blocked on Internal Tools. Linear: AD-8340 Workup agent for Arrivals and Departure (Backlog, Guido Percu) https://linear.app/canary-technologies/issue/AD-8340/workup-agent-for-arrivals-and-departure. No Slack discussion of the setting found.
     - Action: put "A/D enablement in Q4B?" on the Workup Agent Sync agenda (Wed 8:30 PT) for Blake to decide, and record the decision rule on the Notion row.

  ### Loose ends outside the table: Linear still assigned to Laura

  - TOOL-978 Workup: read an arrival report's header row (In Review). PR canary#63817 is APPROVED and unmerged https://github.com/canary-technologies-corp/canary/pull/63817. Action: Sam lands it via Birdline.
  - TOOL-955 Grant the Canary app role SES suppression list permissions (In Review) https://linear.app/canary-technologies/issue/TOOL-955/grant-the-canary-app-role-ses-suppression-list-permissions. Both PRs (canary#62762, canary-kubernetes#7258) are CLOSED unmerged, so the ticket state is stale. Action: cancel it, or reopen with a new owner; INFRA-673 and SRE-1611 style removals keep going through tickets until then.
  - In Progress on Laura: TOOL-906 (Groundcover templates scan all clusters), TOOL-914 (team classification misreads from the Oct 23 routing report), TOOL-773 (make gathering unskippable so Workup can move to Sonnet 5.5). Todo: TOOL-693, TOOL-718. Backlog High: TOOL-902. Action: reassign the three In Progress to Sam or move them to Backlog explicitly so the board is honest.
  - Row "Code review load" is checked but carries the note "Check codeowners": worth a look at canary CODEOWNERS for internal_support/ and the investigate plugin, so reviews land on Rami and Asher rather than Sam.

  ### Suggested order

  This week
  1. Reassign Laura's open TOOL tickets (TOOL-785 to Rami, TOOL-789 to Kevin, TOOL-978/906/914/773 to Sam or Backlog) and post the list in #epd-internal-tools-engineers.
  2. Land canary#63817 (TOOL-978).
  3. Decide TOOL-955: cancel or reopen.
  4. CODEOWNERS PR for the cloudflare repo; confirm wrangler deploy access for pages.
  5. Ask Sam about Orbital validation and Zendesk admin; ask Johannes to confirm paging ownership.

  Before Q4B planning, Nov 19
  6. External sharing launch plan: owner, pilot page and customer, TOOL-985 sequencing.
  7. Workup gate decision for Arrivals/Departures at the Wed sync.
  8. Tick the "Handed off?" boxes on the Notion table as each is resolved, so the page stays the source of truth.
project: null
source_id: null
tags: []
time_minutes: 5
title: check laura Dewald's handover document for unfinished items, and make action
  plan
updated: 2026-11-09 15:46:09.089099
waiting_on: null
waiting_since: null
working_on: false
---