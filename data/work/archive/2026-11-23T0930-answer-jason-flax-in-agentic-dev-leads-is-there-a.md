---
area: null
completed_at: 2026-11-23 17:41:27.957637
contexts:
- react
created: 2026-11-23 09:30:58.642258
defer_until: null
due: null
energy: medium
id: 2026-11-23T0930-answer-jason-flax-in-agentic-dev-leads-is-there-a
order: null
output: |
  ## Agent run 2026-11-23T12:36:21Z

  Nothing was sent. Two draft replies are below for you to post in the thread
  (https://canarytechnologies.slack.com/archives/C0AJW6KHE1E/p1795215259996279?thread_ts=1795179848.113409&cid=C0AJW6KHE1E).

  ### What the thread asks of you

  - Blake (Fri 20 Nov, 22:29 EET): "All in all: just turn it on". Jason: "i agree with Blake". Sudarshan: "also on board".
  - Jason: "is there a channel for this?"
  - Sudarshan: "not sure how settings assist might use engram ... i guess the yaml would just be checked in, and theres no engram in that path?"
  - Still owed from earlier in the thread: you told Jason "If we go forward, i'll run it by you" on the Engram project/topic layout.

  ### Channel: there is none

  Channel search found no channel for the settings guide or Settings Assist. The nearest existing ones:

  - #project-workup (https://canarytechnologies.slack.com/archives/C0AL1T2H43V), topic "Project to improve triage skills across the engineering org".
  - #eng-engram (https://canarytechnologies.slack.com/archives/C0AG3FGM8SX), Jason's channel for Engram users.
  - #agent-workup-actions (https://canarytechnologies.slack.com/archives/C0CD9Q7SNJK) is automated output, not a fit.

  My recommendation: use #project-workup for the rollout and test results rather than open a new channel, and take the Engram layout review to #eng-engram. Draft A assumes that. If you would rather open a dedicated channel, swap the first sentence.

  ### Draft A, to Jason

  > No channel yet. I'll post the rollout and the test results in #project-workup, since Workup is the first consumer. Going live it is, thanks all. Before I load anything I'll bring the Engram project and topic layout to you in #eng-engram, as promised.

  ### Draft B, to Sudarshan

  > Good question, and the doc doesn't answer it. The guide is checked-in YAML either way, and Engram is a load of that YAML. If Settings Assist reads the YAML directly, there is no Engram in its path and the live trial starts as Workup only. Is that how you'd want Settings Assist to consume it, or would you rather it query Engram too?

  ### Check before posting

  - Draft B rests on an assumption I could not verify: Settings Assist is not in the canary repo, and the proposal doc (https://claude.ai/artifact/5fhfxvD3kBRRzVReNgQu7B) names it as a consumer without saying how it retrieves. The doc's aim and thesis both name "Workup and Settings Assist", so if Sudarshan is right the test scope in the doc narrows to Workup and the doc needs an edit.
  - "Just turn it on" changes the doc's sequence: the doc says the pass mark is fixed "before launch", and the ticket pool for that test does not exist yet (memories/README.md, 2026-11-20). Worth deciding whether you still fix the pass mark before loading, or load first.
  - The 10 restricted curated notes (security gaps) are still an open question for a shared store; nobody in the thread addressed it.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0AJW6KHE1E/p1795215259996279?thread_ts=1795179848.113409&cid=C0AJW6KHE1E
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Answer Jason Flax in #agentic-dev-leads: is there a channel for the settings-guide
  proposal'
updated: 2026-11-23 17:41:27.957629
waiting_on: null
waiting_since: null
working_on: false
---

Thread on my Workup / Settings Assist settings-guide-in-Engram proposal. Blake decided "just turn it on" (no shadow mode); Jason and Sudarshan agree. Jason asks if there is a channel for this; Sudarshan asks whether Settings Assist would use Engram at all or just the checked-in YAML. Open 2 days, no reply from me.
https://canarytechnologies.slack.com/archives/C0AJW6KHE1E/p1795215259996279?thread_ts=1795179848.113409&cid=C0AJW6KHE1E