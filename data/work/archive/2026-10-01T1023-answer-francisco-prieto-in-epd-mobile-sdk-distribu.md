---
area: null
completed_at: 2026-10-01 21:19:53.624296
contexts:
- react
created: 2026-10-01 10:23:58.697373
defer_until: null
due: 2026-10-01
energy: medium
id: 2026-10-01T1023-answer-francisco-prieto-in-epd-mobile-sdk-distribu
order: null
output: |
  ## Agent run 2026-10-01T15:05

  Nothing was posted. The draft reply below is for you to send or edit.

  ### Draft reply for the thread

  Thread: https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1790809950250929?thread_ts=1790809891.660649&cid=C09M5GRJPL2

  > Thanks Francisco, clear write-up.
  >
  > *Core:* +1 to C. It matches where Blake landed last week, with the same conditions (scrub, security check, docs stay gated). Two things in your doc are new since then, and Blake and Security should see them: the RN package is readable JS rather than a binary, and Maven Central can't be unpublished, so the scrub has to be a hard gate before the first release.
  >
  > *Vendors:* Y is the right target, with two things first:
  > • Before we write to the manufacturers, can we check the agreements we already hold? Romi mentioned the old SDK already shipped vendor libraries to customers, so the existing terms may answer X/Y/Z for some of them. @Mehul should know.
  > • Under Y, BLE hotels still need a credential, and Wyndham is on the BLE path this year. That puts the Annex B infra on the critical path for them. Which vendors does Wyndham need, and by when? I'd ask those first.
  >
  > Until we have answers I'd hold off putting vendor binaries on the releases page.

  ### What Francisco is asking

  His doc, "Mobile SDK distribution: what we have today and our options" (https://app.notion.com/p/3eb81468615181ffaa94d8ba32dd88e5), splits the question into two independent decisions and gives his pick for each. He tagged you, Diana, Blake and jcarnegie. There is no explicit question to you, and nobody has replied yet. The doc has no comments.

  - Decision 1, our core: A (shared password, manual download, as today), B (per-hotel credential, installed as a dependency), C (public on Maven Central, a public GitHub repo for iOS, and npm). He picks C.
  - Decision 2, the BLE vendor SDKs (ASSA ABLOY, dormakaba, Miwa, Onity, Salto): X (hotel gets the SDK from the manufacturer, we ship only our adapter), Y (we redistribute behind a per-hotel credential), Z (we redistribute freely). He picks Y and says the vendors accepting it is a guess.
  - The doc also lists 11 questions to put to each manufacturer in writing, and Annex B sketches the credential infra for B and Y: `sdk.canarytechnologies.com` on CloudFront, basic auth checked by a CloudFront Function.

  ### Why the draft says what it says

  - C is already close to agreed. In the 25 Sep thread (https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1790328396587869?thread_ts=1790328396.587869&cid=C09M5GRJPL2) Blake said he was comfortable going public, on these conditions: scrub customer names and internal identifiers, a Security double-check filed as a ticket against Platform, a clean-history iOS repo, and no documentation included. You agreed to the Security audit and asked Diana to tell Security the timeline.
  - Blake's comfort rested on "you can already extract the binaries from the app". The doc adds two cons that thread never covered: the React Native package is plain JavaScript, so the bridge source is readable, and Maven Central versions can't be corrected or deleted.
  - Y brings back per-hotel credentials for any hotel using BLE. Caitlyn said in the same thread that Wyndham work continues through year end, including BLE, and Wyndham is the customer Diana named as most urgent. So "no credentials to manage" holds only for non-BLE hotels.
  - Blake asked Francisco on 29 Sep to talk to Mehul Parekh about vendor redistribution. I found no Slack trace of that conversation.
  - The vendor code came from OpenKey. Francisco, 28 Sep: "most of the lines are BLE vendors code pasted from openkey" (https://canarytechnologies.slack.com/archives/C0A85HC8G3X/p1790608665465829). Romi said the old iOS SDK shipped custom builds with or without the ASSA library, distributed manually (https://canarytechnologies.slack.com/archives/C0A85HC8G3X/p1790693731440569?thread_ts=1790692337.371089&cid=C0A85HC8G3X). Existing agreements may therefore already cover redistribution. That "the old SDK" means OpenKey's is my inference; Romi did not name it.
  - The last line of the draft responds to Diana on 29 Sep: "at the moment with just adding the binaries into the release page will work" (same #eng-mobile thread). The doc says no hotel can get the vendor binaries today. Putting them on the releases page, behind the one shared password, would be redistribution before any vendor has answered. Francisco was also planning five `canary-sdk-ios-ble-<vendor>-dist` repos; Diana told him not to rush those.

  ### Not verified

  - Whether the Security ticket against Platform was filed. A Linear search for recent "SDK public" issues found nothing relevant, but that was one query, not a thorough check.
  - What the existing vendor agreements say. I did not look for the contracts.
  - Which lock vendors Wyndham needs for BLE, and the date.
  - The doc's claims about the current setup (shared docs password, iOS core zip at an open URL). The SDK repos are not in this monorepo, so I took these from the doc.

  ### Options if you want a different reply

  - Shorter: "+1 to C and Y. Before writing to the vendors, let's check the agreements we already hold with Mehul."
  - Drop the last line of the draft if you'd rather raise the releases-page point with Diana directly.
project: 2026-09-08-mobile
source_id: https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1790809950250929?thread_ts=1790809891.660649&cid=C09M5GRJPL2
tags:
- morning-gtd
- slack
time_minutes: 20
title: 'Answer Francisco Prieto in #epd-mobile: SDK distribution research'
updated: 2026-10-01 21:19:53.624281
waiting_on: null
waiting_since: null
working_on: false
---

He tagged me on his Notion research "Mobile SDK distribution: what we have today and our options", which covers two decisions. Wyndham and Best Western both vendor our binaries by hand today.
https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1790809950250929?thread_ts=1790809891.660649&cid=C09M5GRJPL2