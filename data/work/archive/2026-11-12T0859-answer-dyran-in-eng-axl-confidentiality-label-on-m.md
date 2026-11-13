---
area: null
completed_at: 2026-11-12 12:35:07.645527
contexts:
- react
created: 2026-11-12 08:59:20.829041
defer_until: null
due: null
energy: medium
id: 2026-11-12T0859-answer-dyran-in-eng-axl-confidentiality-label-on-m
order: null
output: |
  ## Agent run 2026-11-12T12:23

  Nothing was sent. Draft reply below for you to post in the thread
  (https://canarytechnologies.slack.com/archives/C04CYNNRUF9/p1794437454379649?thread_ts=1794437447.337209&cid=C04CYNNRUF9).

  ### Short answer

  Not today, but it is feasible. No report or download Canary produces carries a
  confidentiality label or footer, and there is no setting to turn one on. Adding
  one is engineering work, and how much depends on the file format.

  ### What I checked (canary repo, master)

  - Searched `backend/canary`, `backend/shared` and `frontend` for "confidential":
    no hits in any report, export, PDF or print code. The only matches are
    unrelated (French privacy strings, OAuth "confidential client", prompts).
  - There is no single export path to change. Downloads come from roughly 30
    separate places:
    - The Reports framework (`backend/canary/reports/`, see its README):
      scheduled and on-demand CSV/XLSX, delivered by email or SFTP. This is what
      Marriott's tips reports use, through about 20 providers in
      `backend/canary/tips/report_providers/group_specific_providers/`
      (`marriott_*`, `mvw_*`).
    - Per-product download views: authorizations export, check-out data report,
      tips disbursements, kiosk sessions and ID verification reports, voice call
      statistics and transcripts, staff user export, task management export,
      portfolio payment and integration summaries.
    - Frontend print views: `CheckInsPrint.vue`, `AuthorizationPrint.vue`,
      `ContractsPrint.vue`, `SalesBookingAuthformPrint.vue`.
  - Not checked: which of these Marriott properties actually have enabled, and
    whether report emails have a shared body template that could carry a label.
    I found no report email template under `reports/templates` (admin form only).

  ### Format matters

  - CSV has no footer. A label would be an extra row, which breaks anything that
    parses the file. Several Marriott tips reports feed payroll (ADP, UKG), so an
    extra row there is a real risk. For CSV the practical options are the file
    name or the body of the delivery email.
  - XLSX, PDF and print views can carry a real header or footer.

  ### Decision that is yours

  The questionnaire answer is a commitment, so pick the wording:
  "not supported" or "not today, can be added". The draft takes the second and
  commits to no date. Slack search found no earlier answer to this question.

  ### Draft reply

  > Hi Dyran, not today. Reports and downloads from Canary (CSV/XLSX exports,
  > scheduled emailed reports, printable views) don't carry a confidentiality
  > label or footer, and there's no setting to enable one.
  >
  > It is technically possible to add, with one caveat: CSV files can't have a
  > footer without breaking whatever ingests them, and some Marriott tips reports
  > go straight into payroll systems. For those, the label would have to go in
  > the file name or the delivery email. Excel, PDF and printed views can take a
  > proper footer.
  >
  > For the questionnaire I'd say: "Not currently. Canary can add a
  > confidentiality label to Marriott reports on request; the placement depends
  > on the file format." If Marriott has required wording or a list of the
  > reports they care about, send it over and we can scope it.
project: null
source_id: https://canarytechnologies.slack.com/archives/C04CYNNRUF9/p1794437454379649?thread_ts=1794437447.337209&cid=C04CYNNRUF9
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Answer Dyran in #eng-axl: confidentiality label on Marriott reports'
updated: 2026-11-12 12:35:07.645522
waiting_on: null
waiting_since: null
working_on: false
---

Marriott questionnaire (Data Protection and Retention): can we add a confidentiality label or footer to any reports containing Marriott data that can be produced or downloaded? cc Z. Open since Nov 11, no reply from me.
https://canarytechnologies.slack.com/archives/C04CYNNRUF9/p1794437454379649?thread_ts=1794437447.337209&cid=C04CYNNRUF9