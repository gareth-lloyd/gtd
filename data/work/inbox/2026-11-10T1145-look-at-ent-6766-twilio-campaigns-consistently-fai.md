---
area: null
completed_at: null
contexts:
- react
created: 2026-11-10 11:45:30.273182
defer_until: null
due: null
energy: medium
id: 2026-11-10T1145-look-at-ent-6766-twilio-campaigns-consistently-fai
order: null
output: |
  ## Agent run 2026-11-10T12:53

  **Bottom line:** ENT-6766 is stale rather than untriaged. It has sat in Enterprise triage since 2026-07-02 with no owner, and the last comment is from 2026-07-28. Since then Messaging shipped half of the fix under a different ticket. The remaining half (a per-hotel legal-name line in the campaign description) is still not in code. I did not confirm whether BW campaigns are still being rejected at the July rate.

  **What the ticket asks for**
  - ENT-6766 (https://linear.app/canary-technologies/issue/ENT-6766/twilio-campaigns-consistently-failing-for-best-western), filed by Melissa Fairchild after this Slack thread with you: https://canarytechnologies.slack.com/archives/C08P0M47GPQ/p1782934789290359
  - Two changes: use Twilio's new campaign templates, and when the legal entity name differs from the hotel's public name, prepend a line such as "Due Di Mare Inc. is the legal name of Franklin Square Inn. Both brands are under the same ownership."
  - In that thread you said it needs a careful code change, should probably go via another team rather than Enterprise, and should be automated from hotel data with no manual input from the script runner.
  - Ownership was never settled. Andrea Bradshaw asked Justin Ligman and Rachel Kim to decide an owner (2026-07-09) and said she would schedule a chat (2026-07-16). Connor Swords then marked it blocked on CUSTOPS-4398 (2026-07-28). The label is still "Blocked: Other".

  **The blocker is gone**
  - CUSTOPS-4398 (https://linear.app/canary-technologies/issue/CUSTOPS-4398/enterprise-best-western-twilio-configuration) closed 2026-08-07. Cristhian Grijalva got the campaigns approved after 3+ manual resubmissions each.
  - Two details from it: adding the legal-name disclaimer alone was not enough, because Twilio then rejected the sample message. One hotel (bw-70304) was left on a toll-free number, which needs no campaign.

  **What has shipped since**
  - MSG-5620 (https://linear.app/canary-technologies/issue/MSG-5620/update-our-twilio-campaign-registration-script-to-have-new-content), requested by Rachel Kim and merged 2026-09-18 as PR #56889 by Rick Schieck, replaced the campaign description, consent flow text and sample messages.
  - The code is `TwilioService.create_a2p` in `backend/canary/messaging_integrations/services/twilio.py:1038`. It is still fully static: no legal-entity sentence, no hotel website, and no hotel name anywhere ("The hotel uses…", `<HOTEL>` placeholders). The copy Rachel supplied as "working" had all three personalised.
  - Glenn Santos commented on MSG-5620 on 2026-10-16 that the consent text and the Privacy Policy / Terms URL fields are "still not updated". Nobody replied, and the ticket is closed.
  - The Notion page linked from ENT-6766 (https://app.notion.com/p/3810ec4396f540b48ff5959dc58ef4ca) was last edited 2026-07-01 and still shows the older template, so it no longer matches the code.

  **Is it still happening?**
  - One confirmed case after the September copy change: CUSTOPS-6246 (https://linear.app/canary-technologies/issue/CUSTOPS-6246/failed-message-showing-error-30034-at-best-western-champions-forest), 2026-10-23. Best Western Champions Forest (bw-44784) was sitting on the Onboarding Queue sub-account because its own A2P campaign was never approved, and guests got error 30034. I could not tell whether that campaign was submitted before or after 2026-09-18.
  - I did not query Twilio or prod for campaign approval rates, so the current BW failure rate is unknown. The "4 of 5" figure is from July.

  **The Principle Hotel email is a different problem**
  - The 2026-11-09 failure (https://mail.google.com/mail/?authuser=glloyd@canarytechnologies.com#all/thread-f:1881424743774681024) is "Twilio registration data not found. Add an OnboardingValue with kind TWILIO_REGISTRATION_DATA". The hotel has no registration data loaded (entity name, EIN, address, GM contact), so the script stopped before any campaign was submitted.
  - Batch: https://www.canarytechnologies.com/manage/onboarding/cohorts/b72a0662-7a97-47bd-a119-6552cb2b3e2c/batches/e86d93f9-3c3f-4226-a15b-437e65affd66
  - It needs someone to add the registration data and rerun. It is not evidence for ENT-6766.

  **Feasibility of the remaining fix**
  - `TWILIO_REGISTRATION_DATA` already holds `entity_name` and `website` per hotel (`backend/canary/onboarding/configuration_providers/configs/twilio_registration.py:65`), so the legal-name sentence can be built automatically for script-onboarded hotels, as you wanted in July.
  - `create_a2p` has three callers (`hotels/twilio.py`, `twilio_interim_messaging.py`, `wyndham_connect_plus_service.py`), so the change touches all brands, not only BW. That supports Messaging owning it rather than Enterprise.

  **Suggested next step (nothing sent or changed)**
  - Move ENT-6766 to Messaging as a follow-up to MSG-5620, scoped to: personalise the description with legal entity, hotel name and website; resolve Glenn's 2026-10-16 comment; remove the stale blocked label. Rachel Kim and Rick Schieck are the people with context.
  - Before nudging, it is worth asking Cristhian Grijalva or Glenn Santos what the BW rejection rate has been since 2026-09-18. If it dropped, this is low priority; if not, the missing legal-name line is the likely cause.
  - Draft comment for ENT-6766, if you want to post it:
    "Picking this back up. CUSTOPS-4398 closed in August, so this is no longer blocked. MSG-5620 refreshed the campaign copy on 2026-09-18, but the description is still static: it has no legal-entity line, hotel name or website. The onboarding registration data already carries entity_name and website, so this can be automated. Since create_a2p is shared across brands, I think this belongs with Messaging as a follow-up to MSG-5620. @Rachel Kim @Rick Schieck does that work? @Cristhian Grijalva are BW campaigns still being rejected since the September change?"

  **Not done:** no playbook run (`/enterprise:work-ticket`), no Twilio or prod queries, no writes to Linear, Slack or Notion.
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-6766/twilio-campaigns-consistently-failing-for-best-western
tags:
- morning-gtd
- linear
- from-awareness
time_minutes: 20
title: 'Look at ENT-6766: Twilio campaigns consistently failing for Best Western'
updated: 2026-11-10 12:53:17.561621
waiting_on: null
waiting_since: null
working_on: false
---

In ENT triage with no priority set. 4 of 5 hotels in the last BW go-live batch failed; Twilio provided new templates. May need a nudge to get an owner. Related: The Principle Hotel configure_twilio onboarding failure email (2026-11-09).
https://linear.app/canary-technologies/issue/ENT-6766/twilio-campaigns-consistently-failing-for-best-western