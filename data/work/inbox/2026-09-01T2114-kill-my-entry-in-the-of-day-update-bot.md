---
area: null
completed_at: null
contexts: []
created: 2026-09-01 21:14:52.867451
defer_until: null
due: null
energy: low
id: 2026-09-01T2114-kill-my-entry-in-the-of-day-update-bot
order: null
output: |
  ## Agent run 2026-09-02 11:15:26.751247

  **Found the source.** The "End-of-Day Update" bot (Slack app B0B1NDRHU4T, DM channel D0B21TC8AUS) is the `slack-webhook-cron` Cloudflare Worker in https://github.com/canary-technologies-corp/cloudflare. It runs every 30 minutes and DMs each person in a hard-coded roster at their configured local time.

  Your entry, `slack-webhook-cron/src/index.ts` line 146 under `EPD_ENTERPRISE`:
  https://github.com/canary-technologies-corp/cloudflare/blob/main/slack-webhook-cron/src/index.ts#L146

      "glloyd@canarytechnologies.com": "20:00 - Africa/Nairobi",

  It was added in PR #83 (https://github.com/canary-technologies-corp/cloudflare/pull/83) by Andres Figueira in Feb 2026 as part of the enterprise roster.

  **Prepared, not pushed.** Local branch `glloyd/remove-glloyd-from-eod-bot` in the scratchpad clone at
  `/private/tmp/claude-501/-Users-garethlloyd-projects-canary/e65eceda-8705-4faf-8de6-132d7420a6f7/scratchpad/cloudflare`
  with one commit (2904d8f) that deletes that single line. Diff is the one-line removal only.

  **Convention in that repo:** small roster-edit PRs straight to `main` (e.g. #129, #130, #110). There is no GitHub Actions deploy; `package.json` has `"deploy": "wrangler deploy"`, so after merge someone with Cloudflare access must run `pnpm deploy` (or `npx wrangler deploy`) inside `slack-webhook-cron/`. Laura DeWald (ldewald) is the most active maintainer and merged most recent PRs. Until it is deployed the DMs will keep arriving even after merge.

  **Needs your approval (outbound writes):**
  1. `git push -u origin glloyd/remove-glloyd-from-eod-bot`
  2. `gh pr create` with title "slack-webhook-cron: remove glloyd from EOD roster" and body:
     "Removes my entry from the EPD_ENTERPRISE end-of-day update DM roster. I no longer want the 20:00 EAT reminder. Needs a `wrangler deploy` of slack-webhook-cron after merge."

  Say "yes, push and open the PR" and I will do both. Alternative that skips the bot entirely: Slack > the End-of-Day Update app DM > mute, but that only hides the message; the worker still sends it.

project: null
source_id: null
tags: []
time_minutes: 5
title: kill my entry in the  of day update bot
updated: 2026-09-02 11:15:26.751247
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/D0B21TC8AUS/p1788282023218869

there's a github repo, I think it's scripts for cloudfront workers or something like that which I have an entry in, and it sends these. I no longer want them