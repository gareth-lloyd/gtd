---
area: null
completed_at: 2026-11-19 19:31:12.345094
contexts:
- consume
created: 2026-11-17 09:38:12.636089
defer_until: null
due: null
energy: medium
id: 2026-11-17T0938-reply-to-rami-re-resolution-agent-doc-and-flow-pag
order: null
output: |
  ## Agent run 2026-11-17T12:52

  **Nothing was sent.** I could not read either of the two things Rami linked, so there is no real review yet. Below: what blocked me, the context I did find, and a draft reply.

  ### What I could not read
  - Flow page (https://pages.cnry.cloud/resolution-flow/): redirects to the Cloudflare Access Google sign-in. Not readable without your browser session. No local or GitHub source found for it.
  - Notion "Resolution Agent" doc Rami linked (https://app.notion.com/p/canarytechnologies/Resolution-Agent-40781468615181a9831ed2f1dc81cea6): the Notion integration gets a 404 (not shared with it). The working notes call this page "Status and vision".

  ### Context I did find
  - Rami's two DMs (2026-11-16, 14:53 EET) are bare links with no text and no thread (https://canarytechnologies.slack.com/archives/D08CJ15NW21/p1794833626938459). No ask is stated; "for review" is an assumption.
  - Rami now runs Resolution Agent / Agent Assist after Laura's handover, and Settings Assist (building on Sudarshan's work) is the top block priority. Source: Granola summary of your Stephanie 1-1 on 2026-11-13 (https://notes.granola.ai/d/d874aebd-f0e6-401b-91fe-7bff30223c95). Summary only, not checked against the transcript.
  - Readable companion doc: "Resolution Agent — Working Notes & Planning" (https://app.notion.com/p/ca3064d7785d413da3707bddde3bd6a2), last edited 2026-11-11. It says the flow page covers "levels, tools, billing, knowledge" and holds the open questions, decisions, per-role jobs and ticket volumes.
  - Notion project row "Resolution Agent" (https://app.notion.com/p/4168146861518125ba4ae00d67f7ebd8): status In Discovery, page body blank. Sibling: "Resolution Agent: Settings Assist" (https://app.notion.com/p/40e81468615181b99cb3cd272a6cd760), not read.

  ### Points you could raise (from the working notes only, not the two linked artefacts)
  - **Fin or build is still open** (with Nensy). It decides most of the rest, so worth asking where it stands.
  - **Three open questions have no owner**: which actions the agent takes on its own plus guardrails and audit trail; how proactive it should be; how it knows which type of user is asking.
  - **Scope vs. block priority**: the notes cover 9 roles and about 60 jobs, while the block priority is Settings Assist. The P1 "Change" rows (auth forms ~167/mo, reg card ~79, upsells ~71, messages ~57, AI knowledge ~38) are the ones Settings Assist already covers. Worth asking what the first shipped slice is.
  - **"Refuses changes that aren't allowed"** (e.g. ID capture in Austria) needs a rules source. My inference: this is where your binding rules work (ENT-7726) plugs in; your 2026-10-30 Stephanie notes head a section "Binding Rules Engine and Resolution Agent".
  - **Workup as the shared diagnosis engine** (decision of 28 Oct). My inference: your Workup accuracy findings (errors cluster on "does Canary act / who acts") bear directly on escalation quality.
  - **Ticket numbers are sizes, not counts**: the notes say about 1 in 4 keyword-sorted tickets was mis-sorted and 1 in 5 could not be region-matched.

  ### Draft reply to Rami (not sent)
  Destination: DM with Rami, D08CJ15NW21.

  > Thanks for these. Before I go through them: what kind of feedback are you after, and by when? A general read, or specific decisions you want my view on (Fin vs build, which actions the agent can take on its own, first slice after Settings Assist)?

  Alternative if you would rather read first and reply with substance: open both links in your browser, and either paste the content into a follow-up run or share the Notion page with the Notion integration so a rerun can review them properly.

  ## Agent run 2026-11-18T14:05

  Follow-up asked: "rami has supplied an alternative doc. I can giv eyou access to pages"

  **Nothing was sent.** This run read all three artefacts in full and replaces the "points you could raise" list above with a review based on the actual content.

  ### What I read
  - Rami's follow-up DM, 2026-11-17 21:47 EET (https://canarytechnologies.slack.com/archives/D08CJ15NW21/p1794944863010029): the Notion page he first linked is Stephanie's private page; the public one is the working notes. He is not sure how Stephanie sees the two docs and suggests asking her. He still states no specific ask.
  - Flow page (https://pages.cnry.cloud/resolution-flow/), draft updated 11 Nov. The browser session got through Cloudflare Access without a prompt, so pages access now works.
  - Users and jobs page (https://pages.cnry.cloud/resolution-users/), draft 9 Nov. Companion to the flow page.
  - Working notes (https://app.notion.com/p/ca3064d7785d413da3707bddde3bd6a2), last edited 11 Nov, all toggles.
  - Still unread: Stephanie's private "Resolution Agent" page ("Status and vision"). Rami cannot share it.

  ### What the docs say, in short
  - Four levels running the same steps (gather, diagnose, fix, verify, reply, learn): 1 resolution agent, 2 Support + Workup, 3 On-call + Workup, 4 Eng pod. Each escalation carries what was gathered.
  - Settings Assist (live at /assist for staff, 75 setting areas) grows into level 1. The stated MVP is how-to questions alongside settings changes.
  - All levels answer from one product knowledge base written by Product Ops' documentation agent (prototype, AI Voice and Upsells only so far), possibly held in Engram.
  - Billing comes in as another ask: the agent reads and drafts, Accounting approves.
  - "What has to be true first": correct permissions, correct settings on live hotels, brand standards as checkable rules, country rules as checkable rules.

  ### Review points, strongest first
  1. **The prerequisites are the biggest work and have no owner or order.** "What has to be true first" lists four foundations, two of which are brand and country rules "held as rules a tool can check". Neither the page nor the notes say who builds them or which jobs are blocked until they exist. The open question "which jobs need country, brand or permission rules before they can ship?" sits with Nensy. My inference: this is the binding rules work (ENT-7726), and it is not named anywhere in the three docs. Worth offering as the rules source.
  2. **The "refuses changes that aren't allowed" claim rests on a check that may not exist.** The flow page says Settings Assist is safe because it "uses the same permissions and validation as the settings pages". The Austria ID capture example only works if the settings pages themselves block it. I did not check the code for that. If the pages do not enforce country rules today, the agent will not either.
  3. **The MVP and the priority table disagree.** The flow page calls how-to "the MVP". The notes' priority table puts five "Change" rows first, all already in Settings Assist (~412 tickets a month together). The how-to MVP depends on a knowledge base that covers only AI Voice and Upsells, while the notes' own gap table shows the high-volume how-to areas are undocumented (logins ~580, PMS sync ~256, auth forms ~167, tipping ~157, WhatsApp ~104). So a how-to MVP would answer little of real demand at launch. Ask which one ships first to hotel users.
  4. **Level 1 has no named diagnosis engine.** Levels 2 and 3 name Workup. Level 1 lists "Diagnose" and the flow page says it needs "diagnosis beyond reading settings: PMS state, logs, known issues", with no tool named. My inference from your Workup accuracy work: Workup's errors cluster on "does Canary act / who acts", which is exactly the escalate-or-fix decision at each level, so handoff quality depends on fixing that first.
  5. **Fin or build is open, but both pages assume build.** The notes list it as the first open question (with Nensy). The flow page presents Settings Assist growing into level 1 as settled.
  6. **Scope goes past resolution into new product.** The notes cover 9 roles and about 60 jobs, including drafting RFP replies, planning conferences, housekeeping assignments, bulk guest messaging and ordering QR cards. These are features, not support resolution. A cut line would help: what is in for the first release, and what is a later product bet.
  7. **Access recovery and before-login actions need a security review.** "Our old GM was the only admin" is verified by "signed in at the property, email matches the hotel's domain" and then goes to Support for one-click approval. Before login, the agent resends login links and 2FA codes. Credential updates go "through a secure form". These are account-takeover paths and no reviewer is named.
  8. **No success measure.** None of the three docs says how the agent will be judged (share resolved at level 1, time to resolve, wrong-change rate). "Shared tagging, so Learn has something to count" is listed as a later item.
  9. **Numbers do not line up across the docs.** Access is ~440 a month on the users page and ~580 in the notes' gap table (292 + 206 + 81 in the priority table). Automated payment emails are ~810 in one place and ~800 in another. The docs do say totals are sizes (1 in 4 keyword-sorted tickets was off), so this is tidy-up, not a blocker.
  10. **Billing is the largest category (~700 a month) but sits at P2**, read-only, with Accounting aiming at Q1. Fine if deliberate; worth confirming it is not on the Internal Tools pod's first release.
  11. **Portfolio changes are out of reach today.** The notes say Settings Assist works one hotel at a time; management company and brand jobs are marked "draft, for later".

  Possible link to your settings field guide work (my inference): the flow page wants "settings articles marking what the hotel, Canary GTM or Canary engineering controls". The field guide pipeline produces per-setting descriptions and could feed those articles.

  ### Draft reply to Rami (not sent)
  Destination: DM with Rami, D08CJ15NW21.

  > Read the flow page, the users page and the working notes. Good work, the levels model and the handoff carrying context are right. My main points:
  >
  > 1. "What has to be true first" is the largest piece of work and has no owner or order. Brand and country rules as checkable rules is what the binding rules engine is for. Let's talk about using it as the rules source.
  > 2. Settings Assist only refuses what the settings pages already refuse. Do the pages block the Austria ID capture case today? If not, the agent won't either.
  > 3. The flow page says the MVP is how-to, the priority table leads with settings changes. How-to depends on a knowledge base that covers Voice and Upsells only, and the top how-to areas aren't documented yet. Which ships to hotels first?
  > 4. What diagnoses at level 1? Workup is named at levels 2 and 3 only. Workup's weak spot is deciding whether Canary acts and who acts, which is the escalation decision.
  > 5. Access recovery, resending 2FA codes before login and credential updates need a security review before design goes further.
  > 6. I'd add a success measure and a cut line. Sales RFP drafting, event planning and housekeeping assignment are new product, not resolution.
  >
  > Is Fin vs build decided? The pages read as if it is.
  >
  > Happy to go through it on a call.

  ### Optional message to Stephanie (not sent)
  Rami suggested asking her how her private page relates to the working notes. Destination: DM with Stephanie.

  > Rami shared the Resolution Agent working notes and flow page for review. Your "Resolution Agent" Notion page is private. Is there anything in it I should read before I give him feedback, or are the working notes the current source?

  ### Not verified
  - Whether the settings pages enforce country or brand rules today (point 2).
  - Whether binding rules covers the cases the flow page needs (point 1). Both ENT-7726 links are my inference, not something the docs say.
  - The Granola context from the first run is still summary-only.

  ## Agent run 2026-11-19T18:10

  Follow-up asked: "draft reply to Rami, mainly saying "interesting" and adding anything else you tink valuable"

  **Nothing was sent.** Shorter draft that replaces the long one above. It adds two facts found after the review:
  - The knowledge base is the repo https://github.com/canary-technologies-corp/product-documentation (Philippe Torbey, created 3 Nov, last pushed 19 Nov), mirrored to Notion at https://app.notion.com/p/40d814686151812caa6bf3140b1c8bb5. It now has Authorizations, Contracts and Payments articles, so the flow page's "AI Voice and Upsells only" is out of date. Platform (7 files) and Integrations (5 files) are still thin.
  - Engram at Canary (https://github.com/canary-technologies-corp/engram-server) is one central service in us-west-2. Its README says shared team memory does not work yet, so "one memory agents can search" is not built.

  ### Draft reply to Rami (not sent)
  Destination: DM with Rami, D08CJ15NW21.

  > Interesting, thanks for sharing. I read the flow page, the users page and the working notes. The levels model with the handoff carrying context makes sense to me.
  >
  > A few things that might be useful:
  > - The "brand and country rules a tool can check" prerequisite is what I've been building with binding rules. Worth a chat before anyone starts on that separately.
  > - Philippe's knowledge base has moved on since the flow page was written. It now has Authorizations, Contracts and Payments as well as Voice and Upsells. Logins/access and PMS sync are still thin, and those are your biggest how-to volumes.
  > - Engram's shared memory isn't built yet (agents only write to their own graph), so I wouldn't plan the knowledge layer around it for now.
  >
  > Is there anything specific you want my view on?
project: null
source_id: https://canarytechnologies.slack.com/archives/D08CJ15NW21/p1794833626938459
tags:
- morning-gtd
- slack
time_minutes: 20
title: 'Reply to Rami re: Resolution Agent doc and flow page'
updated: 2026-11-19 19:31:12.345075
waiting_on: null
waiting_since: null
working_on: false
---

Rami sent two links with no text: https://pages.cnry.cloud/resolution-flow/ and the Resolution Agent Notion doc (https://app.notion.com/p/canarytechnologies/Resolution-Agent-40781468615181a9831ed2f1dc81cea6). Presumably for review.
https://canarytechnologies.slack.com/archives/D08CJ15NW21/p1794833626938459