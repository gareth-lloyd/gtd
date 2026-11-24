---
area: null
completed_at: 2026-11-23 17:25:36.250300
contexts:
- consume
created: 2026-11-23 09:30:58.819616
defer_until: null
due: null
energy: medium
id: 2026-11-23T0930-read-blake-s-security-sprint-announcement-and-work
order: null
output: |
  ## Agent run 2026-11-23T14:45

  **Bottom line: Enterprise owes nothing specific yet.** No project, ticket or deadline has been assigned to Enterprise (or any pod). Blake assigns security projects to pods as they are identified, and those items "trump everything". The live open question is the one you already put to Andrea today (https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1795437073984889) — no reply yet.

  ### What Blake's post says
  Thread: https://canarytechnologies.slack.com/archives/C05K3SM1EDC/p1795187960994519?thread_ts=1795187960.994519&cid=C05K3SM1EDC
  - Security Sprint to close all known or potential gaps; it will require product changes and is *the* top priority for EPD.
  - Pods will need to deprioritize other work as security projects are identified.
  - Blake coordinates which projects are prioritized and which pods take them. He was also due to cover it at the start of Show & Tell.
  - Also posted to #eng-announce; Andrés forwarded it to #epd-enterprise-engineers with no discussion (https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1795188272039199).

  ### The 5 replies (nothing directed at Enterprise)
  - Tyler: already has an audit ticket for Tipping, TIP-5662 "Audit tipping endpoints" (https://linear.app/canary-technologies/issue/TIP-5662/audit-tipping-endpoints) — In Progress, delegated to Golem, with an endpoint-audit PDF attached.
  - Luke asked Blake and Z whether there is a process or skill for investigating security holes per domain with Claude; unsure how prescriptive to be. No real answer given.
  - Z: trying to get Mythos access to investigate.
  - Tyler: many endpoints fail basic OWASP Top 10 checks, so start there. Z agreed.

  ### Notion page (https://app.notion.com/p/41d81468615180d8954acfc34ae5b3b2)
  - Premise: assume frontier-level agent swarms will target Canary; security by obscurity is dead; even small leaks (email/phone exfiltration) will be exploited; controls must restrict first and notify humans to undo.
  - Goal: identify and quantify every risk worth finding, then close those Blake and SJ deem necessary. In scope: anything that could make media or a customer say "Canary got hacked", including AWS/GitHub/Slack access and malware on staff machines, and risks baked into how the product works today.
  - Game plan: log issues in one central place; the sprint team ("Falcon") fixes ticket-sized items directly; project-sized fixes go to product pods and outrank everything.
  - Team: Blake (coordinating), Security (Z, Greg, Alina), Andy, Yauheni, Charles, Chris Carter. Nobody from Enterprise.
  - The page does not yet link the "centralized location" for issues, and gives no end date.
  - Sub-page "Security Sprint: Ideas" (https://app.notion.com/p/41e814686151805fa7cccf6a03b7834f), 4 items so far: login behind Cloudflare Turnstile; hotel IP identification as a foundation; rotating our credentials against external systems (Piotr's suggestion); check-in / checkout / stay links should expire and then require MFA.

  ### Where Enterprise is likely to be pulled in (my inference, not stated anywhere)
  - **Credential rotation against external systems** — brand/PMS integration credentials (e.g. Wyndham OHIP) sit close to Enterprise.
  - **Guest link expiry + MFA** and **Turnstile on login** — product changes that brand customers and SSO/SDK flows (e.g. the Wyndham SDK) would feel; Enterprise would probably own customer comms and brand-specific exceptions even if another pod builds it.
  - **Hotel IP identification** — enterprise hotels on brand networks/VPNs are the likely edge cases.

  ### Other sprint tickets seen so far
  - AD-11034 "[Security Sprint] Tailscale Auth Key is visible on the public internet" (https://linear.app/canary-technologies/issue/AD-11034/security-sprint-tailscale-auth-key-is-visible-on-the-public-internet) — AD, Triage, unassigned.
  - SEC-2022 "Restrict /canary-admin access to Cloudflare WARP" (https://linear.app/canary-technologies/issue/SEC-2022/restrict-canary-admin-access-to-cloudflare-warp) — In Review. Worth watching: affects anyone using canary-admin for enterprise support work.

  ### Possible next actions (your call)
  - Wait for Andrea's answer on how this filters down to the team.
  - Optionally get ahead of it the way Tyler did: an endpoint audit of Enterprise-owned surfaces (rules_based_configuration, enterprise_* apps, SSO) starting from OWASP Top 10, and feed findings to Blake's central list once its location is known.
  - Expect block-planning priorities (Settings Assist etc.) to be bumped if Enterprise is handed a security project.

  Not checked: the eng leads transcript you mentioned (not in Granola), and what Blake said at Show & Tell.
project: null
source_id: https://canarytechnologies.slack.com/archives/C05K3SM1EDC/p1795187960994519?thread_ts=1795187960.994519&cid=C05K3SM1EDC
tags:
- morning-gtd
- slack
time_minutes: 20
title: Read Blake's Security Sprint announcement and work out what Enterprise owes
  (#epd-general)
updated: 2026-11-23 17:25:36.250295
waiting_on: null
waiting_since: null
working_on: false
---

@here from Blake, Nov 20: a Security Sprint to close all known or potential gaps, "Important: this will require product change". Notion: https://app.notion.com/p/canarytechnologies/Security-Sprint-2026-Q4-41d81468615180d8954acfc34ae5b3b2 . I have not read the full post or the 5 replies.
https://canarytechnologies.slack.com/archives/C05K3SM1EDC/p1795187960994519?thread_ts=1795187960.994519&cid=C05K3SM1EDC