---
area: null
contexts: []
created: 2026-07-08 13:10:36.798525
defer_until: null
due: null
energy: low
id: 2026-07-08T1310-find-recording-of-internal-tools-and-take-notes
order: null
output: |
  ## Agent run 2026-07-08T15:45:00

  ### TL;DR
  There is NO separate video/AI recording of a "July 7" Internal Tools Q3A planning
  meeting in Notion, the Meeting Notes Index, or Google Drive/Gemini. The single
  canonical Notion artifact for the Internal Tools Q3 Block A (Q3A) plan is the doc
  below. It embeds a meeting-notes block, but that recording is dated **June 30**
  (a leadership framing session) and contains only rough manual notes — no AI
  transcript. July 7 appears only as a "Planning meeting debrief" line in Gareth's
  1-1 journals, i.e. the meeting happened but wasn't captured as its own recording.

  ### Primary artifact (the plan)
  - **Planning - Internal Tools - Q3A (Internal Notes)**
    https://app.notion.com/p/38f81468615180b7abf6c50c43271dc6
    (last edited 2026-07-07; owned by the Internal Tools pod: Stephanie Barry (PM),
    Laura DeWald (Lead Eng), Kevin Cormier, Asher Davidson, Sam Kariu, Rami Nieto)
  - **Internal Tools pod Q3A Linear view:**
    https://linear.app/canary-technologies/team/TOOL/projects/view/q3a-f54bf2ac5f3c
  - **Internal Tools Pod Home:**
    https://app.notion.com/p/32781468615180708a7ac0c563d7ea3e

  ### Where the "recording" question lands
  - The doc's "Meeting Summary and Next Steps" toggle has an embedded Notion
    meeting-notes block, but its meeting date is **2026-06-30**, and it holds only
    scratch notes (COGS/gross-margin/share-price framing with SJ & AJ — a strategy
    session, not the pod planning walkthrough). Fetching with include_transcript=true
    returned no transcript/summary for that block.
  - The only Zoom recording linked anywhere in the doc is the **Atrium** (Implementation
    pipeline app) demo walkthrough — NOT the planning meeting.
  - The July 7 meeting itself surfaces only as "July 7, 2026 — Planning meeting debrief"
    in the **Andrea <> Gareth 1-1 journal**
    (https://app.notion.com/p/3568146861518006b9daf302fb27807c) and a "Q2 planning /
    July 7" note in the **Martijn <> Gareth 1-1 journal**
    (https://app.notion.com/p/2e081468615180fb9418ee44c8a28b8d).
  - Searches that came up empty: Notion meeting notes filtered to created >= 2026-07-06;
    personal meeting-notes data source (empty for all of July); Google Drive "Notes by
    Gemini" for Internal Tools/Planning on 2026/07/07. NB "Q3 Block 1 - internal review"
    (07-06, has a full transcript) is the **EMEA pod**, a different team — not this.

  ### Notes on the plan content (from the doc)
  Mission: Internal Tools builds the tooling, automation, and AI behind onboarding,
  configuration, and support — automating routine work and equipping support,
  implementation, integration, and triage engineers.
  Goals: activate revenue faster, reduce churn, grow Canary without scaling internal
  headcount at the same rate. Metric framing: support spend / live ARR; time-to-activate.
  Themes: (1) Property Lifecycle — onboarding, config, transitions & deactivations;
  (2) Support & Diagnostics; (3) Access & Controls; (4) User Management (not prioritized).

  Released: Properties Page + Manage restructure; create INT/migration tickets from
  Properties Page; set expansion opp live from Properties Page; ChangeTracker config-change
  visibility; AI-Generated Compendium (~156 hrs saved first month); edit F&B on live hotels;
  Mobile Key Figma demos; Canary Pages (host internal HTML/JS); Salesforce Opportunities
  refactor; Feature Request intake option; AI Workup end-to-end PMS investigation; Beta
  Support Access Requests (SAP); above-property roles clarity; Allowed IP shows current IP.

  In Progress: Auto-Config PMS Features (Cloud Beds v1); Automated Hotel Creation from
  Salesforce; Zendesk Context App user/hotel enrichment; Hotel Support ID.

  Upcoming: Unify Onboarding & Add Products code; show hotel-related Linear tickets on
  Property Page; edit upsells for an expansion; add products + user access for expansions;
  automate registration-card setup by country (EMEA); AI Workup expansion to GMS/Comms +
  reliability & observability.

  Discovery: productionize Go-Live Checklist app; productionize Atrium (Implementation
  pipeline AI app); deactivating properties (~473 transitions/yr: 70% mgmt / 28% brand /
  2% both); Omnibar search; Salesforce as source of truth (+ view hotel Zendesk tickets).

  ### Recommendation for the user
  If you specifically wanted a *July 7* recording, it doesn't appear to exist as its own
  Notion/Drive recording — likely the July 7 session was a live walkthrough of the plan
  doc and wasn't separately recorded. Options: (a) treat the plan doc above as the
  artifact; (b) check whether the July 7 meeting had a Zoom/Gong recording under the
  organizer's account (I could not find one in the connected sources); (c) tell me who
  organized it and I can look again.
project: null
source_id: null
tags: []
time_minutes: 5
title: find recording of internal tools q3 block A planning meeting . Meeting took
  place tuesday 7th july. Should be in notion
updated: 2026-07-08 15:45:00.000000
waiting_on: null
waiting_since: null
working_on: false
---