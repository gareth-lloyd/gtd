---
area: null
completed_at: null
contexts:
- react
created: 2026-11-13 09:54:28.454847
defer_until: null
due: null
energy: low
id: 2026-11-13T0954-reply-to-ishwar-re-bavarian-inn-intel-on-the-urlsc
order: null
output: |-
  ## Agent run 2026-11-13T10:07:16

  Nothing was sent. Draft reply for the DM with Ishwar (https://canarytechnologies.slack.com/archives/D07T5RZ3SKZ/p1794502101675639):

  > Thanks, that fits. urlscan only explains the first one: a single Bavarian link, scanned 20 Oct and opened 4 Nov. It only had a handful of our reservation pages in total, so it can't account for 20 Bavarian guests. Inntopia data would.
  >
  > One thing worth checking: is the guest on that 20 Oct link one of the Inntopia-compromised ones? If so, the urlscan submission may have come from the attacker, or a scanner on a compromised mailbox, rather than random leakage. urlscan shows where each scan was submitted from, which could be another indicator to pass to Inntopia.

  Shorter alternative if you only want to acknowledge:

  > Thanks, that fits. urlscan explains the first Bavarian link and the slugs, but not 20 guests at one hotel. Inntopia data would.

  What the reply rests on:
  - SJ's note and the 19-reply thread (https://canarytechnologies.slack.com/archives/C0CFU7HBZEK/p1794500508042429): Jim Engel says every affected guest with an email on file was also compromised through Inntopia; Greg confirmed the Bavarian lookups were direct hits; Greg says Bavarian is the only Inntopia property in the impacted set.
  - Your urlscan message (https://canarytechnologies.slack.com/archives/C0CFU7HBZEK/p1794351296770479): the Bavarian reservation opened on 4 Nov was submitted to urlscan on 20 Oct; 15 public scans in the last month, 7 of them reservation pages.
  - Ishwar already forwarded your urlscan message into SJ's thread, so the two findings sit side by side there. Nobody has yet said how they fit together.

  Not verified:
  - I did not open Greg's restricted spreadsheet, so I have not confirmed that all 20 Bavarian reservations came through the lookup, or which guest the 20 Oct link belongs to.
  - I did not query urlscan. The claim that it shows the submission source is from general knowledge of the site (public scans list submitter country and API/manual method).

  State of the thread since Ishwar's DM, in case it changes what you say:
  - SEC-1839 (https://linear.app/canary-technologies/issue/SEC-1839) tags direct-hit vs brute-forced and flags Inntopia; Greg added a "NonLookupExposures" tab.
  - SEC-1840 (https://linear.app/canary-technologies/issue/SEC-1840) covers sharing indicators only with Inntopia. Z planned to send IP ranges, user agents, request patterns and time window; SJ asked for a call first.
  - Sudarshan found no direct-hit pattern on Crowne and is still running the single-IP search across all hotels and regions.
project: null
source_id: https://canarytechnologies.slack.com/archives/D07T5RZ3SKZ/p1794502101675639
tags:
- morning-gtd
- slack
time_minutes: 10
title: 'Reply to Ishwar re: Bavarian Inn intel on the urlscan finding'
updated: 2026-11-13 10:07:16.586646
waiting_on: null
waiting_since: null
working_on: false
---

Ishwar forwarded SJ's note: Bavarian Inn (an impacted hotel) responded with intel; their COO Jim Engel leads the response and has notified their cyber insurer. He calls it "an interesting piece related to the urlscan thing you found".
https://canarytechnologies.slack.com/archives/D07T5RZ3SKZ/p1794502101675639