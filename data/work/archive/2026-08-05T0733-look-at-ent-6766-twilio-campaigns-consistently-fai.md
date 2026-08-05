---
area: null
completed_at: 2026-08-05 13:59:53.740081
contexts:
- react
created: 2026-08-05 07:33:38.169250
defer_until: null
due: null
energy: medium
id: 2026-08-05T0733-look-at-ent-6766-twilio-campaigns-consistently-fai
order: null
output: |
  ## Agent run 2026-08-05T10:38:23Z

  Ran the enterprise work-ticket playbook (read-only diagnosis; nothing posted anywhere).

  ### Headline
  - GTD framing said "urgent-priority", but the Linear ticket has **No priority set** and has sat **unassigned in Triage since Jul 2** (https://linear.app/canary-technologies/issue/ENT-6766/twilio-campaigns-consistently-failing-for-best-western). The ownership question (Andrea/Justin/Rachel, Jul 9-16) was never resolved.
  - Impact is real and ongoing: per Melissa on CUSTOPS-4398 (Jul 28), "pretty much every twilio campaign fail for BW even after Criss resubmits multiple times"; properties are being parked on the temporary onboarding Twilio account, blocking hosted numbers and efficient go-lives. 4 of 5 recent go-lives had failed campaigns.
  - **New info since the ticket was filed** (CUSTOPS-4398, Cristhian, Aug 4): adding the legal-name disclaimer did NOT fix approvals. Rejections now point at the **"sample message"** — text that Twilio's own team supplied. So the Notion templates are not yet a known-good target; codifying them now would bake in still-rejected text.

  ### Classification (cluster catalog)
  - Primary: **#6 Twilio / WhatsApp / A2P / Meta** (confidence: high). Secondary: #3-ish only insofar as the fix touches automated onboarding/scripts.
  - Misroute: **No** (cluster default team = Enterprise + external Twilio support; ticket is on Enterprise; no "Routed by AI" label). Note: I suggested in the original Slack thread it might belong to another subteam — worth settling when ownership is decided.
  - Owner per catalog: **Eng + external Twilio support ticket**. No CS self-serve path.
  - KB: **no cluster-6 article exists**. Recommend /enterprise:add-to-kb once resolved (this is clearly Recurring-shaped).

  ### Code-side finding (the "careful code change" I flagged in Slack)
  `TwilioService.create_a2p` — backend/canary/messaging_integrations/services/twilio.py:1038 — hardcodes the OLD campaign text and takes no hotel context:
  - `description` is the old "Send pre-arrival hotel digital checkin links..." text, not the new Notion template ("This hotel uses Canary Technologies's platform to collect opt-in..."), and has no legal-name-vs-brand-name clarification.
  - `message_samples` omit the hotel name as message sender — the new templates (and Twilio's approval requirements) want "from <HOTEL_NAME> via Canary Technologies" in each sample.
  - `message_flow` references an old Drive mock-up link; the Notion page has a newer one.
  - Call sites to update (all pass only brand/messaging SIDs, no hotel): twilio_interim_messaging.py:533, twilio_onboarding.py:431, onboarding/services/vendor/wyndham_connect_plus_service.py:937.
  - `legal_business_name` is already collected when the customer profile is created (twilio.py:983, :1145), so the legal-name clarification can be auto-injected when it differs from the hotel's public name — no manual input needed, matching what I proposed in Slack.

  ### Recommended action mode: PR, but gated
  1. First (No-write / external): resolve the sample-message rejection with Twilio via Rachel's contact on CUSTOPS-4398 (https://linear.app/canary-technologies/issue/CUSTOPS-4398/enterprise-best-western-twilio-configuration) — get ONE campaign approved end-to-end so we have known-good text. Connor's "blocked until CUSTOPS-4398 is figured out" comment is correct.
  2. Then (PR): parameterize create_a2p with the hotel + legal name, template the description/samples from the approved text, auto-prefix the legal-name clarification when legal name != public brand. Suggested branch: glloyd/ent-6766-per-hotel-a2p-campaign-text.
  3. Housekeeping the user may want to do in Linear (I made no writes): set a priority, assign an owner, and mark ENT-6766 blocked-by CUSTOPS-4398.

  ### References
  - ENT-6766: https://linear.app/canary-technologies/issue/ENT-6766/twilio-campaigns-consistently-failing-for-best-western
  - CUSTOPS-4398 (live failure thread, In Progress, Cristhian Grijalva): https://linear.app/canary-technologies/issue/CUSTOPS-4398/enterprise-best-western-twilio-configuration
  - Slack thread (origin, incl. my comments): https://canarytechnologies.slack.com/archives/C08P0M47GPQ/p1782934789290359
  - Notion "Twilio Campaign Registration Answers" (new templates): https://app.notion.com/p/canarytechnologies/Twilio-Campaign-Registration-Answers-3810ec4396f540b48ff5959dc58ef4ca
  - Affected BW hotels named so far: hotel 129286227 (q=14241), 129288932 (bw-70304), 129290186 (48092) — admin links in CUSTOPS-4398 comments.
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-6766/twilio-campaigns-consistently-failing-for-best-western
tags:
- morning-gtd
- linear
- from-awareness
time_minutes: 20
title: 'Look at ENT-6766: Twilio campaigns consistently failing for Best Western'
updated: 2026-08-05 13:59:53.740075
waiting_on: null
waiting_since: null
working_on: false
---

Urgent-priority triage ticket: BW Twilio campaigns consistently failing — key account.
https://linear.app/canary-technologies/issue/ENT-6766/twilio-campaigns-consistently-failing-for-best-western