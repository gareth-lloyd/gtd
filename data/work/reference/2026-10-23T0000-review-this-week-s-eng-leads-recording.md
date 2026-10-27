---
area: null
completed_at: 2026-10-26 15:20:25.778618
contexts:
- consume
created: 2026-10-23 00:00:00
defer_until: null
due: null
energy: low
id: 2026-10-23T0000-review-this-week-s-eng-leads-recording
order: null
output: |
  ## Agent run 2026-10-26T14:29:25

  Source: Eng Leads, Thu 2026-10-22 (Zoom files in ~/Downloads/GMT20261022-155654_Recording.*: transcript.vtt, cc.vtt, newChat.txt, mp4). Agenda page: https://app.notion.com/p/canarytechnologies/Eng-Leads-dc605190ddef403da7f80cf620b4008a
  You don't appear as a speaker in the transcript. The meeting ended ~11 minutes early.

  ### Most relevant to you
  - **Sudarshan is demoing a "settings agent" at Huddle in two weeks (~Thu Nov 5/6).** He wants it in prod soon and is out next week. That overlaps with your Settings Assist / settings field guide work (Settings Assist Decision Review.pdf, 22 Oct, is in Downloads). Worth syncing with him before the demo.
  - **Python 3.11 → 3.14 straight bump (Alan Lee / SRE).** SRE expects its side done by end of October. Teams need to verify their dependencies; Alan may send a per-team checklist. Target merge date is **Nov 12** (it can move). 3.15 could be a fast follow.
  - **Code review iteration Q&A (Blake, follows his video).** The message: "not reviewing every line" is different from "no code review". Each team picks its own approval approach for now: Macroscope is the default but not required, any bot or a human click is fine, and there are no org-wide review skills yet ("mindset first"). Requests: put it in retros and overshare, including failures, in Acceleration Guild. Metrics they'll watch: PR count, throughput, creation→merge time, PR size, incidents, plus asking PMs "does your team seem faster?". Blake is working on the Macroscope budget with Daga and plans to turn Macroscope on for all repos. Aditya can't enable auto-approve on infra repos because the budget is allocated to canary.
    - Concerns raised: Yasmin said review's real value is knowledge transfer and architecture curation, not risk. Jordan said adoption will need repeated messaging. Joshua Hart (chat) said the risk is churn from changes outpacing customers. Matías (chat) suggested using the extra speed for product consolidation too.
    - Idea that might be useful for your team: Sudarshan wants a skill that posts "the 2–3 files worth reviewing" on each PR. Yasmin's pattern is to build a skill, share it, push adoption, and repeat.

  ### Other updates
  - **Sallyport:** Teleport is now fully replaced (the platform team cut over Wed 10/21). Aditya will record a Canary TV how-to. Report prod breakage to platform on-call.
  - **Birdline** (merge queue replacement) goes live **next Wednesday, Oct 28** (Z Lee). The design doc is linked on the Notion page.
  - **Loom → Canary TV** officially. File quality-of-life requests with the "send feedback" button, which opens GitHub issues; Andy is open to PRs if he merges them.
  - **Route 53 → Cloudflare** migration is close. It's waiting on one unresponsive customer and could start in 1–2 weeks.
  - **Check-in v3 migration** is 2–3 weeks behind (Dana), on purpose, to stay careful.
  - **Frontend metrics / Appcues / Amplitude** (Sudarshan): historically product-owned, and Amanda owned them alone. They are moving into the EE team (Z Lee). The current guidance is "talk to Ahn first". Andy thinks the data belongs in Snowflake. New Head of Product Ops: Felipe. Andy will meet him about operational health reviews.
  - **Team temperatures** are mostly green and better than 2–3 weeks ago. Garrett says the AI team is trending yellow because of concerns about product-org departures.
  - **People:** Elisha Nuchi joined to lead the Physical Access team and is onboarding with AD and Dana's teams. Navid is no longer in Eng Leads, so the Slack vs email norms topic was closed.
  - **Demos:** the Friday show-and-tell includes Sam (Workup asks questions when ticket info is missing), Jason Le Moyne (webchat quick replies), Laura (membership rewards) and possibly Ishwar (auto PR review). Meshack's demo is pushed. Blake wants more live showing and fewer slides.
  - Admin: the Eng Leads invite is missing its Zoom link for some people, and Andy will recreate the series.

  ### Possible follow-ups (not captured. Your call)
  1. Ping Sudarshan about his settings agent before the ~Nov 5 Huddle, to avoid duplicating Settings Assist work.
  2. Watch for Alan's Python 3.14 checklist and plan your team's verification before Nov 12.
  3. Decide your team's approach to code review approval, and possibly share it in Acceleration Guild.
project: null
source_id: null
tags: []
time_minutes: 30
title: Review this week's Eng Leads recording
updated: 2026-10-26 15:20:25.778424
waiting_on: null
waiting_since: null
working_on: false
---

Watch this week's Eng Leads meeting recording (meets Thursdays; recording usually posted Thursday evening/Friday).

transcripts in Downloads