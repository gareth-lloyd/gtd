---
area: null
completed_at: 2026-10-16 13:23:11.884381
contexts: []
created: 2026-10-15 20:19:16.741876
defer_until: null
due: null
energy: low
id: 2026-10-15T2019-absorb-thread
order: null
output: |
  ## Agent run 2026-10-16T12:45
  Thread: Aspire discovery-call prep and follow-up in #C04STT7UPRQ (https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1792081177515709). Started by Marta Ziaei on 2026-10-15. James Saram, nico and vibhor were tagged; Ani and Connor were cc'd. **You are not tagged and no action item names you.**

  **Context**
  - Aspire Hotels is a German group of about 60 hotels with very little front-desk staff. Two properties are live on Wyndham Connect (Canary). The rest use SciHot PMS and a third-party kiosk. Jen (Wyndham) is pushing them toward us.
  - It's competitive. Ani thinks the rival is Luca (https://www.luca-business.com/en), which already has a Vienna House by Wyndham story (Ani's thread: https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1792061110072159).
  - There's exec visibility: the owner is close to Dimitri (president of APAC/EMEA). They have 99+ unread Canary messages. Their 64 requests are now down to about 35.

  **Debate before the call**
  - Nico pushed back on Marta's question list. He didn't want to ask about eCommerce MIDs. His view: understand why they want charging at mobile check-in, mobile checkout and add-ons, sell our current approach, and don't interview them against our own requirements.
  - Nico also corrected one point: per-guest breakfast is one fixed charge sent to OHIP with frequency=daily, so it posts every day.
  - Both agreed not to push Aspire away by insisting on how we do things today.

  **Call outcome** (Notion notes: https://app.notion.com/p/canarytechnologies/Canary-Aspire-Hotels-Enhancement-Requests-Review-3fa8146861518116811dd93ab8cadc11)
  - **Payment at check-in:** Aspire collects full room + tax and uses Planet only (no Stripe). Planet "theoretically works" through a 100% deposit; Vibhor is confirming with payments. We recommend against forcing payment for each add-on. Add-ons should be charged to the check-in card, or a larger amount authorized upfront.
  - **Auto check-in + Opera payment collection** (card passed to Opera, Opera collects) was tested and doesn't work. Marta said a troubleshooting call with Jen, Manu and Lorraine was set for this morning (10-16), and a Gateway config update is probably needed. **This is the most engineering-relevant item and could touch PMS gateway/OHIP.**
  - **Mobile checkout folio:** already supported through OHIP auto checkout (Opera sends the folio).
  - **Company profile:** passing company details to an Opera company profile works today, and duplicate profiles are fine with Aspire. Company address fields need adding to the reg card. Conditional display is deferred to the conditionality work.
  - **Nationality-based ID capture:** being built. Target is dev/test done by end of year and an Aspire pilot in January. Singapore and LATAM also want it.
  - **Pin code in guest journey messages:** room number works now. Using the pin-code UDF in guest journey messages needs dev work.
  - **Per-guest pricing for upsells:** rolling out in November.
  - **Ticketing:** handled by the staff ticketing app. It's in the commercials, which are expected within a week.

  **Open actions (none are yours):** Vibhor on Planet requirements; Marta on the auto-checkout thread for Jen, message-history timeline and mockups from Connor, and the nationality-ID property list; Jen on reg-card company address and walking Aspire through payment options at Monday's meeting; a joint deep-dive session later; Manuel/Ani/Marta on the auto check-in + Opera payment issue.

  **Possible next step for you:** none needed. If you want to stay aware, check the outcome of the 10-16 auto check-in/Opera payment troubleshooting (gateway config) and who will build the pin-code UDF dev work.
project: null
source_id: null
tags: []
time_minutes: 5
title: absorb thread - Aspire hotels requirements call
updated: 2026-10-16 13:23:11.884374
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1792081244949419?thread_ts=1792081177.515709&cid=C04STT7UPRQ