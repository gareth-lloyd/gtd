---
area: null
contexts:
- react
created: 2026-06-03 12:19:46.073998
defer_until: null
due: null
energy: medium
id: 2026-06-03T1219-follow-up-on-pms-8627-operaopi-tokenization-reject
order: null
output: |
  ## Agent run 2026-06-03T14:57 (local)

  Researched PMS-8627 across Linear, the Slack thread, the related ticket PMS-8647,
  and the pms-gateway codebase. No external writes made — research only.

  ### What's going on (root cause, confirmed)
  - **Property:** InterContinental Sydney Coogee Beach (SYDCB), an AU IHG pilot
    property on Opera V5 / OPI (Opera Kiosk). Sister report PMS-8647 is a second AU
    IHG property hitting the same "Opera System Error" on digital check-in pre-auth.
  - **Trigger:** On **May 27** a change to how VGS proxy routing is configured on the
    Canary side. Properties whose Opera host is a **private IP** began receiving **raw
    VGS tokens** (the `99…`-prefixed token, e.g. `9913709582770071047`) instead of the
    revealed PAN. Because VGS never detokenized, Opera/OPI forwarded the `99…` token to
    Global Blue, which rejected it ("Global Blue token starts with 1 for IHG; another
    token format is rejected, we have no record"). That is the GETPAN Error 06 /
    pre-auth System Error the property sees.
  - **Blast radius:** Yauheni's writeup says "almost all (700+) IHG properties were
    affected," not just the AU pilots.

  ### The fix that was applied
  - Yauheni applied a config change to the **VGS IHG proxy configuration**, adding the
    reveal **filter pattern** so tokens get detokenized again. On 2026-06-01 he marked
    PMS-8627 Done, citing PMS-8647 as confirmation the config change works. PMS-8647 is
    now **Done/completed**.

  ### Why it's NOT actually resolved (the live problem)
  - PMS-8627 was **reopened → back in Triage on 2026-06-02**, assignee **Yauheni
    Danchanka** (PMS Engineering). **SLA breaches 2026-06-04 03:31 UTC (~tomorrow).**
  - After the fix, the property **reposted** the card (res 49204732, and another
    reposted res d7b70378-…) and it **still failed** — "VGS token not replaced with the
    actual card number." So reveal is still not happening for this Opera Kiosk flow.
  - **Drew Delianides' key insight:** the reveal filter list is mostly **JSON paths**
    (`$.pan`, `$.account_number`, `$.reservations.reservationPaymentMethods[*]…`, etc.)
    plus one literal `CARD` regex. "If the payload isn't JSON it won't attempt any of
    the json paths. But the regex CARD is processed no matter the payload, even XML."

  ### Codebase verification (pms-gateway)
  - Filter patterns live on `VGSProxyConfig.filter_patterns` (JSONField) and are sent to
    VGS as the `X-VGS-FilterPatterns` header:
    `backend/pms-gateway/proxies/models/vgs.py` (~L42-53, `get_vgs_headers` ~L83-87).
  - IHG environments (`IHG_PRODUCTION`/`IHG_SANDBOX`) set `proxy_all_requests=True`
    (vgs.py ~L89-95), so every Opera request is routed through VGS.
  - Account → config link: `Account.vgs_proxy_config` FK
    (`backend/pms-gateway/gateway/models/account.py`).
  - **UpdateMethodOfPayment is SOAP/XML, not JSON.** Opera client builds a dict that
    zeep serializes to a SOAP envelope (`opera/client/client.py` ~L1082-1100); test
    confirms body is XML `<ns3:cardNumber>…` (`opera/tests/test_client.py` ~L2045-2051).
  - **Conclusion: Drew's XML-vs-JSON-path theory holds.** For the Opera Kiosk XML post,
    the JSON-path reveal patterns are silently skipped by VGS; only the raw `CARD` regex
    (VGS alias for `99\d{17}`) can match. That regex *should* match the 19-digit `99…`
    token — so if the post-fix config genuinely contains `CARD`, reveal ought to work,
    yet it still didn't for the reposted cards. That gap is the open mystery.

  ### Open questions worth driving (for Yauheni / payments)
  1. Does the **VGSProxyConfig actually attached to the SYDCB / AU-pilot accounts**
     contain the `CARD` pattern, or did the broad "700+ properties" fix touch a
     different config than the one these pilot accounts point to via FK?
  2. For the reposted-but-still-failing cards (res 49204732, d7b70378-…): is the
     outbound body still carrying a `99…` token to Opera (reveal not firing), or a
     revealed PAN that Opera/GB then rejects for a different reason? Datadog query in the
     ticket (`@request_fragment:UpdateMethodOfPayment @CTX_vgs_environment:ihg_production`)
     is the place to confirm which.
  3. Is `CARD` = `99\d{17}` the right alias for the token prefix actually in use, and is
     it definitely in the live filter list for this proxy route (Yauheni asked Drew this
     exact question on 2026-06-02 and it appears unanswered).

  ### Status / where it stands
  - Ticket is **Triage, unresolved, SLA-critical (breaches 2026-06-04 03:31 UTC)**, IHG
    escalating, heavily impacting ops. Latest action: Yauheni asked Bonnie (2026-06-02)
    to confirm whether *new* cards submitted today are also failing — awaiting property
    reply. Branch `glloyd/pms-8627-…` exists on this ticket (your name on it).
  - **No comments/messages were posted.** If you want to nudge the thread or drop the
    codebase finding (XML payload ⇒ JSON-path filters skipped ⇒ verify `CARD` is on the
    SYDCB account's config) into the Linear ticket, say the word and I'll draft it for
    your approval first.
project: null
source_id: https://canarytechnologies.slack.com/archives/C023K54M812/p1780268036482329
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 15
title: 'Follow up on PMS-8627: OperaOPI tokenization rejects for AU IHG pilot properties'
updated: 2026-06-03 14:58:54.209412
waiting_on: null
waiting_since: null
working_on: false
---

Bonnie: OperaOPI rejects Canary-retrieved cards (tokenization error) for a couple AU IHG pilot properties; IHG escalating, heavily impacting ops. https://canarytechnologies.slack.com/archives/C023K54M812/p1780268036482329