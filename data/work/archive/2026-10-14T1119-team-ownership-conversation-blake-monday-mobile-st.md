---
area: null
completed_at: 2026-10-19 14:59:43.626829
contexts: []
created: 2026-10-14 11:19:45.583086
defer_until: null
due: 2026-10-19
energy: low
id: 2026-10-14T1119-team-ownership-conversation-blake-monday-mobile-st
order: 1
output: |
  ## Agent run 2026-10-19T14:15

  Prep brief for the Blake 1:1 (Mon 19 Oct). Sources: Diana 1:1s on 7 Oct and 14 Oct, the Blake Directs meeting on 13 Oct, Connor 1:1s on 5–6 Oct (the 5 Oct note is empty), the Caitlyn 1:1 on 1 Oct, the Stephanie Barry call on 16 Oct, the mobile sprint standup on 16 Oct, and Slack. Four items in the body have changed or were wrong; they are flagged ⚠️.

  ### ⚠️ Corrections to the body
  - **Accessibility facts.** The body says "Stephanie's 1:1 on Oct 15: Level Access contract runs to March 2027, web VPAT target Nov 13". I could not find this anywhere.
    - The 16 Oct call (https://notes.granola.ai/d/29079fc9-1798-478e-8210-563a6d642e36) was with **Stephanie Barry**, who said her team isn't involved. The web VPAT moved from Amanda to **Stephanie Fernandez**, in Z's org.
    - The target is **Nov 14**, not Nov 13. It is Level Access's "conservative estimate" (Amanda, #rfp-accor-digitalkey, 25 Sep) and is **not in the Accor contract**. Jean-Charles confirmed that in #eng-enablement on 6 Oct: https://canarytechnologies.slack.com/archives/C09D2A5LYN9/p1791289152687849?thread_ts=1791272376.107829&cid=C09D2A5LYN9
    - I found no source for "March 2027". Don't cite it unless you have it from somewhere else.
  - **Nathan's scope: partly answered.** On 16 Oct you told Diana that Connor said Nathan starts on the main enterprise workstreams and "might extend to enterprise mobile over time" (https://canarytechnologies.slack.com/archives/D0AFZUT5DCH/p1792148522262729). Blake said on 13 Oct that Nathan "will also help drive mobile roadmap". These two answers differ in emphasis, so pin it down with Blake.
  - **Mobile PM hire: Diana's interviews were a mix-up.** On 14 Oct Jason asked #eng-hiring-managers to swap Diana in for him on "mobile product interviews". On 16 Oct Diana said she had only mentioned that the position exists. Connor confirmed they are looking at candidates. Bree left in July and a product director was planned as her backfill (https://notes.granola.ai/d/aee94f39-4d33-4eca-bfd4-2063df50a7aa). Whether this mobile PM role is that backfill is still unknown.
  - **David app transfer: moving.** You nudged Blake, David and Z on 16 Oct, and David replied to Z. No need to raise it.

  ### Proposed agenda (most important first)

  **1. Who sells mobile? (the PM gap)**
  - Blake said on 13 Oct that Caitlin is "TPM-style, not a true PM" and that her move to Tipping exposes the mobile PM gap rather than creating it (https://notes.granola.ai/d/6e3be9bf-2577-457d-927a-318f20699685). Connor has made the same point twice: Caitlin is strong on current detail and weak on vision (Wyndham gating, feature flags).
  - Diana on 16 Oct: the team can cover the operational side, but "I'm scared no one is selling the mobile product work to customers" (https://canarytechnologies.slack.com/archives/D0AFZUT5DCH/p1792148955409539).
  - Ask: is the mobile PM role a dedicated mobile hire or Bree's backfill? What is the timeline? Until someone is hired, who owns the mobile roadmap: Nathan, Connor, or Caitlin at reduced scope?

  **2. Who owns StaffApp product and engineering?**
  - Messaging and Team Chat have no PRDs, and Rachel asks for work informally. Team Chat stalled because the "Figma" was a vibe-coded prototype (Diana, 7 Oct: https://notes.granola.ai/d/795b9f6f-7d72-433e-8f03-9832a67e196d). SJ also pushed back on Team Chat at block planning and asked for impact data (Caitlyn 1:1, 1 Oct: https://notes.granola.ai/d/e8982053-efd3-490e-9656-bd9abd9c02da).
  - The F&B ordering request adds to StaffApp work, and mobile devs are confused about whether StaffApp work is theirs. Your view on 1 Oct, which Caitlyn shared: StaffApp and the guest SDK are separate products and should have separate codebases, with shared infrastructure staying with mobile.
  - Backend: James leaves this week. Rafa has a backend background with some Flutter and no React Native, so this also leaves a React Native gap (Blake raised that himself on 13 Oct). Ishwar is interim lead but not hands-on. Mike's roadmap needs backend work.
  - Ask: does StaffApp move to Staff Ops long term? Who replaces James, and is a hire planned? Until then, which team takes Mike's backend asks into block planning?

  **3. Guest app (the new OpenKey "V5")**
  - Blake told you on 13 Oct that it blocks every new MobileKey customer from onboarding to the new OpenKey. It has stalled since June: Jason built an iOS prototype, there is no Android version, Debbie did the designs, and Caitlin owns it on paper.
  - Your open action from 13 Oct: get a briefing on its current state from Jordan. Not done yet, as far as I can see.
  - Ask: who owns it? Does it get a slot in the next block, and at the expense of what?

  **4. Caitlin's capacity**
  - Caitlin is on Tipping plus mobile now that Quinn has left. Next week she is also on IHG monitoring and alerting before the mid-Nov scale-up, plus the Wyndham upsells sign-off (standup, 16 Oct: https://notes.granola.ai/d/7b0bc068-7a94-44cf-be04-bcf87bf29496).
  - Diana is taking over Linear and cycle planning and spends 2–3 hours every morning on questions (14 Oct: https://notes.granola.ai/d/d0de2936-cdf1-44f8-a66a-8c3413970e56).
  - Ask: is Blake comfortable that the dual role works through IHG's scale-up and Best Western's conference? Blake said Diana will need confidence in it.

  **5. Accessibility: settle the steer**
  - On 7 Oct you told Diana to prioritise commercial work, so accessibility gets deferred. Diana then paused it on 14 Oct.
  - On 13 Oct Blake said it should **not** be deprioritised: retesting takes 30+ days, and IHG may push for it even though Accor no longer needs it.
  - On 6 Oct, in #eng-enablement, Blake had concluded the Mobile SDK was not needed for Accor, and Daga flagged the web Nov 14 date as very tight.
  - Your instructions to Diana and Blake's steer conflict. Ask: start the mobile SDK backlog now because of the lead time, or wait for an IHG ask? If now, who owns the mobile ACR with Level Access? Jason and Diana were named on 21 Sep.

  ### Smaller items (only if there's time)
  - Connor's MOB-1325 asks to record a source (web or SDK) on records so Omni can split by it. Diana will write a short engineering design. FYI only.
project: 2026-09-08-mobile
source_id: null
tags: []
time_minutes: 5
title: Plan team ownership conversation blake monday mobile staff ops
updated: 2026-10-19 14:59:43.626819
waiting_on: null
waiting_since: null
working_on: false
---

Ownership
  - Messaging in StaffApp: who's the PM? Caitlin coordinates, Rachel and the messaging team ask for work informally, and  nobody writes PRDs. Team Chat is paused until there are requirements and a design.
  - Nathan's scope: does it cover enterprise mobile (Wyndham, IHG, Best Western)? Does it cover the guest app?
  - Guest app: stalled since June. Caitlin owns it on paper but keeps pushing it back. There's an iOS prototype (Jason's) and no Android version. If new OpenKey customers can't be onboarded without it, it needs an owner and a slot in the next block.
  - Mobile product lead hire: Diana was asked to interview for it. Is it backfilling Bree, and how does it fit with    Nathan?

  Capacity
  - Caitlin on Tipping as well as mobile: Diana is worried about her bandwidth. Diana is taking over Linear and cycle planning, which pulls her further from IC work.
  - StaffApp backend: James leaves next week. Rafa is still ramping up, and Mike's roadmap needs backend work. Is a hire
    planned, or does mobile absorb it?

  Accessibility
  - Diana has paused it, citing your earlier point that Accor's scope is small. Confirm your steer: start the mobile
    backlog work now because of the lead time? Bring the facts from Stephanie's 1:1 on Oct 15: the Level Access contract
    runs to March 2027 and the web VPAT target is Nov 13.



Sources to check: diana 1-1 last week, connor 1-1s over last month
Caitlyn 1-1s