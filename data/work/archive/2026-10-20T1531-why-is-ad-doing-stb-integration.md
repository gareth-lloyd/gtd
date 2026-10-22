---
area: null
completed_at: 2026-10-21 10:06:34.547020
contexts: []
created: 2026-10-20 15:31:09.369440
defer_until: null
due: null
energy: low
id: 2026-10-20T1531-why-is-ad-doing-stb-integration
order: null
output: |
  ## Agent run 2026-10-21T10:15
  **Short answer:** AD got it because A&D owns the STB/EVA code, and the
  ticket landed there by default. Nobody decided "AD owns STB onboarding".
  The work is now almost entirely ops/config, not engineering.

  **How AD-8319 got to AD** (https://linear.app/canary-technologies/issue/AD-8319/voco-orchard-singapore-stb-integration)
  - 2026-08-07: Angela Wu (APAC CS) filed it. 2026-08-11: Sharon Hales asked In-Stay for help with the new JWKS upload process.
  - Nobody picked it up for 3 weeks (Angela bumped it on 08-26 and 09-01). 2026-09-01: Sharon asked Becca, then "Moving to A&D - @mjeffery you did the original integration".
  - Dana Levine (A&D) took it on 09-02. Infra uploaded the JWKS (INFRA-669, INFRA-674). Dana ran the test transaction on 09-23. Status is In Review.
  - Open item: on 10-14 Dana offered to send Angela the creds to go live.
  - AD-8320 Wyndham Singapore (https://linear.app/canary-technologies/issue/AD-8320/wyndham-singapore-stb-integration) has the same shape: Angela filed it 09-01, it went through three triage states (bounced between teams), went to Dana, and is In Review.

  **Are the related tickets all AD?** Engineering tickets are AD; infra pieces went to Cloud Infra/Platform.
  - AD: AD-6222 JWT flow (Dana, Done), AD-6588/AD-6721 Secrets Manager (Done / Backlog, Dana), the Tablet Reg kiosk STB step (Bruno, AD-87xx), the Kiosk GTM staff override (Federico, AD-9135 family), AD-10234 block v3 migration for STB hotels (Guido, Done 10-06).
  - Infra: INFRA-441, INFRA-669, INFRA-674, PLAT-3663, PLAT-3698 (JWKS URLs, Aditya Menon).
  - QA: QA-297/298 (Canceled).
  - **None are on an APAC team board.**

  **Slack / Notion**
  - Dana posted in #epd-apac on 2026-10-06 (https://canarytechnologies.slack.com/archives/C0AJ29WQEF2/p1791312731358199): a self-serve guide now exists, so APAC CS can onboard STB hotels without engineering. Dana also asked whether APAC eng can take on **check-in v3 STB support**. **No replies.**
  - Guide: "Setting Up a Hotel for STB/EVA" (https://app.notion.com/p/5269a86e9cca4d6f86dd1a2351c5a2f6). Older docs: "Guide: STB/EVA implementation" (https://app.notion.com/p/361814686151802e8699d692fe5d0453) and the design doc "STB/EVA Integration on Kiosk" (https://app.notion.com/p/31e814686151806db781ceaa8d4b08b9).
  - Martijn's DM on 10-20 (https://canarytechnologies.slack.com/archives/D0A2UR1AMD1/p1792496399759259) says the 2 STB tickets should go to APAC and calls it "teams too protective of their domain". The history doesn't support "protective": AD took the tickets after nobody else would, and Dana is actively trying to hand off.

  **Suggested framing back to Martijn:** AD-8319/8320 are nearly done and should close out with Angela via the self-serve guide. The real open ownership question is v3 STB support, which Dana already offered to APAC eng on 10-06 with no answer. That is the thing to assign.

  **Flag:** Angela's 2026-09-21 comment on AD-8319 has the hotel's STB prod password in plaintext. Consider asking for it to be deleted.
project: null
source_id: null
tags: []
time_minutes: 5
title: Why is AD doing STB integration
updated: 2026-10-21 10:06:34.547012
waiting_on: null
waiting_since: null
working_on: false
---

https://linear.app/canary-technologies/issue/AD-8319/voco-orchard-singapore-stb-integration

Check related tickets - are they all with AD team?

Any discussion on slack or notion?