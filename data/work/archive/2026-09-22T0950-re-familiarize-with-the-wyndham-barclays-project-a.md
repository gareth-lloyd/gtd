---
area: null
completed_at: 2026-09-22 14:20:04.454021
contexts:
- consume
created: 2026-09-22 09:50:30.757950
defer_until: null
due: 2026-09-22
energy: medium
id: 2026-09-22T0950-re-familiarize-with-the-wyndham-barclays-project-a
order: null
output: |
  ## Agent run 2026-09-22T10:30+03:00

  **Block review:** "Q3 Block 2 Review: Enterprise" is TODAY 2026-09-22, 15:00–15:45 EEST, SJ organising, Zoom https://canarytechnologies.zoom.us/j/8535381621 (attendees incl. Connor, Andrea, Blake, Ryan, Tincho, Lauta, Andrés, Wei). You have not RSVP'd. Calendar description asks for prior-month goal reviews in Notion + a stance on next-block goals.

  **Snapshot file: NOT READ.** Connor's image (Slack file F0C3EL685PU, https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1790017590754549) could not be fetched: SLACK_BOT_TOKEN lacks files:read (`missing_scope`) and the Playwright browser is not signed into Slack. Open it yourself before 15:00. Best inference on contents: the Enterprise Q4A project list (Linear label `26Q4A`, Enterprise team), which is what Connor/Blake would pre-read. That list today:
  - P-ENT-1656 Embed Wyndham Credit Card Application in Check-in Flow — Product Definition, P2/High, lead Ryan Rogers, target Q4 2026 https://linear.app/canary-technologies/project/embed-wyndham-credit-card-application-in-check-in-flow-808cd21ddec3
  - P-ENT-1648 Wyndham – Earn Points for Canary Check-in — Product Definition, no lead https://linear.app/canary-technologies/project/wyndham-earn-points-for-canary-check-in-7675f2105fe9
  - P-ENT-2357 IHG Scripting – Q4A 2026 — Planned https://linear.app/canary-technologies/project/ihg-scripting-q4a-2026-bca67c82a9ea
  - P-ENT-1806 Cross-region Auth & Above Property Dashboards — Eng Design, lead Andrea https://linear.app/canary-technologies/project/support-cross-region-auth-and-above-property-dashboards-da48fe9e2663
  - P-ENT-2359 Check-in V3: Enterprise Rollout and Backfill — Backlog https://linear.app/canary-technologies/project/check-in-v3-enterprise-rollout-and-backfill-49915fc05469
  - P-ENT-2358 Internal users manage portfolios in Manage — Planned; P-ENT-1956 Portfolio Reconciliation — Product Def; P-ENT-1936 Link email acct with SSO — Backlog; P-ENT-1911 SCIM for SSO — Paused

  ### Wyndham Barclays project — re-familiarisation

  **What it is.** Two capabilities at the payment step (step 3/3) of Wyndham Connect web digital check-in:
  1. Milestone 1 (PRD target Q3, clearly slipped): show cards saved in the guest's Wyndham Rewards wallet (Shiji = Wyndham's PCI vault / wallet-as-a-service; Canary already integrates with Shiji for the voice product) as selectable payment options, Wyndham co-brand card surfaced first; guest still enters CVV.
  2. Milestone 2 (Q4 target, Barclays dependency): "Apply for Wyndham Rewards Visa" CTA → JWE/JWS-encrypted Post-In redirect to Barclays-hosted application → Barclays tokenises the new card into the Shiji wallet → Post-Back JWT to a Canary RETURL with one of 8 decision codes (A/P/D/M/C/E/PN/PC) → approved card passed to PMS, no CVV. Non-members get enrolled in Wyndham Rewards as part of the application.

  **Sources.**
  - PRD (Connor, June 2026, still Draft): https://app.notion.com/p/canarytechnologies/PRD-Wyndham-Co-Brand-Credit-Card-in-Canary-Check-In-38781468615181ddb8c0ee253c0f7098
  - Kickoff recap 2026-09-14 "Wyndham Credit Card Offers": https://app.notion.com/p/canarytechnologies/Wyndham-Credit-Card-Offers-3db81468615180788705c9fac9f31600
  - Canary pitch deck (4 journeys, approval/denial flows): https://docs.google.com/presentation/d/1Cn5CopRNE79RRvNIN_i9diV0EMb99LWAut3XmpRM-AM/edit
  - Wyndham/Barclays requirements deck (do not share externally per Connor): https://docs.google.com/presentation/d/1Qf5fYDvNPZqNEWykT0qXP3ZTtExnNVV0/edit
  - Linear: P-ENT-1656 above. Only ticket: ENT-7486 "[Spike] Pre-eng design spike", 2 pts, Todo, Ryan, created by Andrea 2026-09-10 https://linear.app/canary-technologies/issue/ENT-7486/spike-pre-eng-design-spike. Members: Ryan, Tincho. No milestones, no docs.
  - #wyndham thread 2026-08-17 (Ani/Connor on Barclays timeline pressure): https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1786988752368909
  - Bear notes: nothing on this project.

  **Current state (as of today).**
  - Status "Product Definition". Kickoff with Payments pod + Arrivals/Departures happened ~2026-09-15. Ryan expected to lead eng design; Andrea and Ryan attended.
  - Wyndham is beta customer, built generically to extend to BW/IHG/Marriott/Hilton and other banks; BW and IHG conversations already started. Free to Wyndham; future brands revenue share (~$100/application, ~$150/approval).
  - Timeline: kickoff says no hard deadline, Q4 target, Q1 acceptable. Barclays wanted a September start and has a mid-Nov change freeze; Wyndham (Jen/Justin) asking for dates. Connor's stance (Aug 17): zero direct commercial upside, Justin must drive timeline not Barclays/Bryan; we shouldn't share more designs right now.
  - Cross-team dependencies: Check-in v3 (Arrivals/Departures; modular check-in this builds on), Payment Submitter (Payments pod; single payment interface), Bora's team guest-profile/card-reuse. Adobe content gateway supplies the offer creative (generic "credit card offer" content type) — note Content Gateway ENT-6692 is Blocked on Wyndham/Adobe access/contract.
  - Canary does not store card data; Shiji stays the vault. Longer-term idea: displace Shiji with Canary's own PCI vault.

  **Open questions worth raising in review / eng design.**
  - PCI scope: does receiving the Barclays post-back (Sijji token + expiry, no PAN) expand Canary's PCI DSS scope? Does the Wyndham PMS accept the Sijji token or does Canary need a dereference API? (PRD B6 + internal Q.)
  - Session recovery across the off-domain redirect (SESSION / CONFIRMATIONCODE), and how this works inside the Canary SDK WebView (follow-on phase).
  - Can Shiji's response distinguish a Wyndham co-brand card from other cards? (W2) Is there a Barclays cardholder flag to suppress the offer? (B5)
  - Barclays sandbox/QA access, JWKS key exchange, offerId, annual key rotation runbook ownership.
  - Unified CTA copy for members vs non-members; W1 behaviour when memberNumber is missing (PRD says suppress).
  - Staffing/lead is thin: one 2-pt spike, lead Ryan who also leads Golem triage, Managed Context and Content Gateway this block.

  **Adjacent Wyndham context.** Bryan M's 2026-08-26 #wyndham thread on Wyndham Connect upsell growth lists "Barclays card is another win to add to Wyndham Connect when we launch that" https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1787704062215709. Voice side (Val/Mason) references Barclay activity as a loyalty verification signal, unrelated to this project.
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1790017590754549
tags:
- morning-gtd
- slack
time_minutes: 30
title: Re-familiarize with the Wyndham Barclays project and pre-read Connor's snapshot
  before block review
updated: 2026-09-22 14:20:04.454016
waiting_on: null
waiting_since: null
working_on: false
---

Connor (group DM with Andrea): 'Would you mind re-familiarizing yourself with the Wyndham Barclays project? That's the main thing we're taking on' + snapshot file he pre-read with Blake. Block review this week.
https://canarytechnologies.slack.com/archives/C0B1Y5K9AMC/p1790017590754549