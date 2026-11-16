---
area: null
completed_at: null
contexts:
- react
created: 2026-11-16 10:10:20.350604
defer_until: null
due: null
energy: medium
id: 2026-11-16T1010-answer-stephanie-barry-in-group-dm-block-planning
order: null
output: |
  ## Agent run 2026-11-16T12:11:42Z

  Nothing was sent. A draft reply is below, waiting for your go-ahead or edits.

  ### What is being asked

  - Stephanie's list of five block-planning candidates: https://canarytechnologies.slack.com/archives/C0CHDN04Y68/p1794556805220889
  - Her follow-up naming you: https://canarytechnologies.slack.com/archives/C0CHDN04Y68/p1794585563975099. She says your work "would likely be the underlying infrastructure" for item 2 and that she looped you into "that conversation".
  - "That conversation" is a second group DM (you, Vibhor, Sebastian, Stephanie, Philippe) that she added you to at the same time: https://canarytechnologies.slack.com/archives/C0CH93V7WBT/p1794500585101659. Sebastian pitches the internal Guest Data Compliance Hub (42 countries) as the content source for automatic check-in setup by country and asks for a 30-minute call before block planning closes. You have not replied there either.
  - Item 2's actual question: "main automation and infrastructure is built now. Can EMEA EPD just keep adding countries from here and connect it to the hub?"
  - James, Sebastian and Philippe all agreed with the priority order. Sebastian calls item 2 "super high prio" and wants to talk to Vibhor about v3 config options. Stephanie said item 1 may not fit in the block.

  ### What I found

  - The "automation and infrastructure" in item 2 is not yours. It is Sam Kariu's Internal Tools project, Automate Check-in V3 Onboarding (https://linear.app/canary-technologies/project/automate-check-in-v3-onboarding-617b22ca4b48). Phase one is 100% done. Phase two (country definitions) is 68%: base provider TOOL-872 and monitoring TOOL-873 are Done; Italy TOOL-874, Spain TOOL-875 and UK TOOL-876 are In Review, each gated on content approved by EMEA CS.
  - A country there is one `CountryDefinition` in `backend/canary/onboarding/configuration_providers/country/base.py`: ID step, `id_document_*` settings, additional-guest, retention and purge settings, plus the catalog fields it adds. It applies to new non-enterprise hotels at onboarding, and TOOL-873 monitors live hotels against it. It does not use `rules_based_configuration`.
  - Your ENT-7726 stack is not underneath any of that today. #59047 (https://github.com/canary-technologies-corp/canary/pull/59047) is ready for review; #59059, #61725, #61724 and #63320 are drafts. PR 5, the part that writes country defaults at hotel creation, is not started and is blocked on deferred decisions 3 and 5 in your plan. It covers `hotel.*` settings only, not catalog fields or registration card content.
  - The overlap is the settings half of a country definition (ID step, retention). Your plan's long-term goal is to move that kind of config out of onboarding scripts into rules. The hub already records "legal status" and "Canary default" per field, which is the same split as your binding rules and conventions.
  - One thing to watch, not in the draft: your first law rule (#61725) limits `id_step` and `id_step_with_ocr` on the EU scope minus Italy and Spain. Italy and Spain definitions cannot clash with it, but any later EU country definition taken from the hub could set a value your rule forbids, and your boot checks only compare rules against brand trees, not onboarding country definitions.

  ### Draft reply

  Destination: the block-planning group DM, C0CHDN04Y68, as a new top-level message (nobody threads there).

  > Sorry for the slow reply. On #2, from the side of what I'm building:
  >
  > Yes, EMEA can keep adding countries on what Sam built, and it shouldn't wait for my work.
  >
  > • Sam's country definitions are the thing to add countries to today. A country is one definition: its check-in settings plus the fields it adds to the catalog. Italy, Spain and the UK are in review and waiting on approved content, which is what Sebastian's hub supplies. So the work left per country is mostly content and sign-off, not engineering.
  > • What I'm building (binding rules and country conventions in rules-based configuration, ENT-7726) is not underneath that yet. The first PR is in review and the rest are drafts, so nothing writes to a hotel yet. It also only covers hotel settings, not catalog fields or registration card content.
  > • Where the two meet: country definitions reach new non-enterprise hotels at onboarding. Mine is meant to cover every hotel, brand hotels included, and it separates "the law requires this" (checked and reported) from "a sensible default for this country" (written when the hotel is created). Long term I'd expect the settings half of a country definition (ID step, retention) to move into rules, with the fields half staying in onboarding.
  >
  > One ask that costs little now: when you agree the format for pulling countries from the hub, keep the hub's split between legal status and Canary default for each setting. That's the split I need, so the same data can feed both later without a rewrite.

  Optional last line, only if it is your view (I could not confirm it from anything you wrote): "On priority, #2 looks high value and cheap to me, since the engine is built and the blocker is content. No strong view on the others."

  ### Decisions for you

  1. Send the draft as is, edit it, or drop it.
  2. Whether to include the priority line. The draft otherwise gives no view on items 1, 3, 4 and 5.
  3. Whether to also answer in the other DM (C0CH93V7WBT). Sebastian's request for a 30-minute call is still open there, and Sam is not in either DM although the work is his.

  ## Agent run 2026-11-16T13:00:48Z

  The draft above is superseded. It contradicts what you told Stephanie in your 1-1 on Friday 2026-11-13 (https://notes.granola.ai/d/d874aebd-f0e6-401b-91fe-7bff30223c95), which I had not read when I wrote it.

  What the transcript shows you said:
  - The next step on guest data compliance is you, because your rules system generalises to it.
  - The hub matrix is the kind of content that could feed the rules, be set on hotels automatically, and get drift detection.
  - You want something to show before block planning on Thursday 2026-11-19; most of the code is there and needs sign-off.
  - You asked whether this then would not become an Internal Tools block project. Stephanie agreed: a couple of urgent countries on the current infrastructure is fine, but not much more until it is settled where the per-country data lives.
  - You said you would get back to her Monday or Tuesday with context, and that you would pull the threads together and respond.

  ### Revised draft reply

  Same destination: C0CHDN04Y68, top-level.

  > Sorry for the slow reply. On #2, as I said to Steph on Friday, I think the next step here is mine.
  >
  > • Short term: if a country is urgent, adding it on Sam's country definitions is fine and cheap. I wouldn't make "keep adding countries" a block project yet, though.
  > • Why: I'm building rules in rules-based configuration where a country's requirements are stated once, starting with ID collection and GDPR retention. Hotels get them set automatically, and we get a report when a hotel drifts. Sebastian's hub matrix is the content that should feed that, so I'd rather settle where the per-country data lives than hand-write each country twice.
  > • Where it is: most of the code is written, the first PR is in review and the rest are drafts. I'm aiming to have something to show before block planning on Thursday.
  > • Limit: it covers hotel settings (ID step, retention and similar). The registration card fields a country adds stay with Sam's onboarding work.
  >
  > One ask for now: keep the hub's split between legal status and Canary default for each setting. That's the split the rules need.

  Still for you to decide: send, edit or drop; and whether this message also counts as the "Monday or Tuesday context" you promised Stephanie, or she gets a fuller note separately.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0CHDN04Y68/p1794585563975099
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Answer Stephanie Barry in group DM: block-planning priorities and check-in
  V3 in more countries'
updated: 2026-11-16 15:00:48.000000
waiting_on: null
waiting_since: null
working_on: false
---

Stephanie added me to the DM (Sebastian, James, Philippe) because item 2, check-in V3 in more countries, would sit on what I'm building. She wants priority/impact input before block planning; everyone else has replied. Open 2 days, no reply from me.
https://canarytechnologies.slack.com/archives/C0CHDN04Y68/p1794585563975099