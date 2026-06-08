---
area: null
contexts: []
created: 2026-06-05 16:07:58.369715
defer_until: null
due: null
energy: low
id: 2026-06-05T1607-catch-up-on-eng-leads
order: null
output: |
  ## Agent run 2026-06-05T16:16

  Searched Notion (+ connected sources) for the Eng Leads meeting of 2026-06-04.

  **What exists:** The "Eng Leads" page is a recurring *living hub*, not a
  per-date note — there is no standalone June-4 transcript or recording. The
  June-4 content lives in linked databases that were edited that day (last
  edited 2026-06-04, owned by Blake Vanlandingham).
  - Eng Leads hub: https://app.notion.com/p/dc605190ddef403da7f80cf620b4008a
  - Critical items DB: https://app.notion.com/p/1fb81468615180048306dc365d20c653
  - "OCR Rewrite?" discussion: https://app.notion.com/p/3598146861518064b67fd14fe0ccf188

  **Meeting summary (June 4):**
  - Standing agenda ran: Friday Demos, hires/departures, team temperature,
    Critical Items (high-risk changes, tiger teams, cross-pod deps, enterprise
    rollouts), then discussion.
  - Discussion topic "OCR Rewrite?" was covered and marked Done.
  - High-risk infra reviewed: deprecating the nginx pod (route traffic straight
    to Django to cut 503s); EKS 1.36 rollout slated Mon Jun 8; Groundcover
    maintenance Jun 19.

  **Decisions / leanings:**
  - OCR / ID verification: leaning away from an all-in Incode deal toward
    pay-per-use; VisionKit on kiosk tested well by Jason (not a firm decision).
  - Datadog to be fully sunset in favor of Groundcover by mid-June.

  **Action items:** None with explicit owners recorded on the page beyond
  marking "OCR Rewrite?" Done.

  **Open threads:**
  - Wyndham segmentation — [6/4] no update, slated a week or two out.
  - Protel additional-guest sync still unreliable (cross-pod).
  - Enterprise rollouts in flight: ESA multi-reservation generic links (400 corp
    sites target 6/1, franchise 7/1), Check-In V3, Room Ready IHG.

  **Not found:** a standalone June-4 transcript/recording; the Records DB
  surfaced no June-4 entry.
project: null
source_id: null
tags: []
time_minutes: 5
title: catch up on eng leads meeting 20260604
updated: 2026-06-05 16:24:05.864940
waiting_on: null
waiting_since: null
working_on: false
---

search notion for notes or transcripts
https://app.notion.com/p/canarytechnologies/328814686151804588fae86f1fb42c87?v=32881468615180cf9f08000caf331759&source=copy_link