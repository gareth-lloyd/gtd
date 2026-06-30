---
area: null
contexts: []
created: 2026-06-30 12:15:53.063430
defer_until: null
due: null
energy: low
id: 2026-06-30T1215-check-eng-leads-doc-for-martijn-s-report-on-de-lun
order: null
output: |
  ## Agent run 2026-06-30T12:37

  **Task:** Find Martijn's report on De Luna at the Eng Leads meeting last Thursday (2026-06-25).

  **Caveat up front:** I could NOT locate a discrete "Eng Leads weekly meeting" Notion
  page with a 2026-06-25 De Luna entry. The current Eng Leads running notes appear to live
  in a Google Doc titled "Eng Leads"
  (https://docs.google.com/document/d/1SDdBDDeU6Ea8WZbNQng254LLXEANlQThBNjLWCgnypM) which
  is restricted from AI access ("ineligible to be used in generative AI contexts"), and the
  meeting-notes data source returned no eng-leads row for 6/24–6/26. So the literal
  page/report you asked for I can't read. If it's a Google Doc, you'll need to open it
  directly. Everything below is the De Luna substance I *could* find in Notion from that
  exact window — including your own note that this was raised at eng leads.

  **Martijn's De Luna account — your own "Martijn <> Gareth 1-1 journal", 6/30 entry**
  (https://app.notion.com/p/2e081468615180fb9418ee44c8a28b8d):
  - "Exploring different avenues. Axl is the one who needs to push next steps."
  - Concern that mis-communicated timelines are not being admitted to; we need the client to
    contact their PMS vendor.
  - Axl's manager is Nathan; Brad was involved from product (aware, but not his priority).
  - Path/blocker: excluded payment gateways we already integrate with — client has their own
    payment engine. **Manolo committed on executing payments.** Martijn explicitly
    **"mentioned over-committing in eng leads."**
  - Client has a contract with a CRS that could do payments, but that's excluded too.
  - Martijn found they had a contract for payments + PMS; we need credentials but don't have
    them. Request has been heard by the client but not the vendor — we need the customer to
    push, and Axl to push the customer.
  - 6/23 entry on the same page is blunt: "De Luna — disaster in the making."

  **Messaging Team Retro, 6/26** (https://app.notion.com/p/38b814686151804d8c07cdca9c2bc481):
  - Mati (🟢): "DeLuna incident wasn't great, but since payment stuff bought us time, I don't
    think it was stressful."
  - Sudarshan (lead) flagged "DeLuna / Sales commitment" under What could be better.
  - Gonza: "we should avoid a deluna situation in the future — maybe do a retro and figure
    out how we had a miscommunication between sales and eng on what features are actually
    implemented."

  **Related De Luna context (Voice/Neobookings track):**
  - Linear project "Voice AI: DeLuna <> Neobookings" — lead Marta Ochowicz Malarz, status
    Implementation, start 6/23, due 7/3:
    https://linear.app/canary-technologies/project/98876d5a-618d-45de-b27c-a906dd762264
  - "Deluna - Neobookings" (6/24): plan to send booking link instead of taking card over the
    phone / doing the payment integration:
    https://app.notion.com/p/38981468615180318928f65e29b47921
  - "Deluna Neobooking" (6/22): hotel client not currently blocking; focus on Neobookings +
    Subteo Pay: https://app.notion.com/p/387814686151807281bcf3f002f90cd8
  - "Kevin <> James: Voice AI" (6/23): De Luna manually pulled voice transcripts of failing
    calls to review/root-cause: https://app.notion.com/p/38881468615180a18a40f5da05542782

  **Bottom line:** The De Luna story Martijn would have reported is a sales/eng over-commitment
  on payment integration (Manolo committed to executing payments the client's stack can't
  support without vendor credentials we don't have), now being de-risked via a Neobookings
  booking-link approach while Axl pushes the client to push their PMS/payment vendor. If you
  specifically need the verbatim eng-leads notes, check the restricted "Eng Leads" Google Doc.
project: null
source_id: null
tags: []
time_minutes: 5
title: check eng leads meeting notion page for martijn's report on de luna (last thursday)
updated: 2026-06-30 12:37:28.969777
waiting_on: null
waiting_since: null
working_on: false
---