---
area: null
contexts:
- consume
created: 2026-05-25 04:18:16.553890
defer_until: null
due: null
energy: medium
id: 2026-05-25T0418-read-linear-sla-patterns-thread-mat-as-eng-leads
order: null
output: |
  ## Agent run 2026-05-25T11:45:00

  Read the 10-reply thread (started by Matías Marco del Pont, 2026-05-22 in #eng-leads).

  ### Matías's opening concerns
  1. Ticket creators don't realize that setting a priority sets an SLA.
  2. All customers get the same SLA policy even though some are more important.
  3. Issues that don't block day-to-day ops arguably shouldn't have SLAs — usually no value in <1d vs 2-3d vs 1wk.
  4. Too many SLAs makes them feel less important.

  ### Responses

  - **Andrea Bradshaw**: Existing Notion rules (multiple hotels / key accounts) but may be stale. Triage engineer CAN adjust/remove SLA to match priority (with comment, confirm with PM/EL if unsure). For non-blocking/feature-request items she creates a related team ticket and closes the SLA ticket (since it's tied to Zendesk and impacts support attainment).
  - **Laura DeWald (PM, owner of SLA guide)**:
    - Internal bug form auto-sets priority based on #hotels affected + time-sensitivity/blocking — creators aren't really picking SLA.
    - Key-account policy exists in guide, but properties aren't tagged as key accounts anywhere → that's the real gap, not the policy.
    - Support is trained on SLA guide; if they inflate urgency, raise directly.
    - Pushes back on "drop SLAs for non-blocking": customers DO escalate when things sit, even low-impact. Low = 1wk/backlog already, which is generous. Real question: are tickets over-prioritized rather than SLAs being wrong?
    - Only 4 tiers — not a lot. Asks if the problem is too many tickets landing urgent/high.
    - Asks for example tickets.
  - **Matías** confirms: yes, too many tickets are landing urgent/high. Also asks: thought only PMs could change/remove SLA — has that changed? Deeper point: priority and SLA shouldn't be coupled. Feature requests can be important without being time-sensitive. Guide should be more explicit.
  - **Laura** clarifies: triage engineer CAN adjust priority if mismatched, but removing/extending SLA manually should be PM only. Feature requests should have no SLA — adding the "Feature request" label removes it. Will update guidelines for clarity.
  - **Justin Ligman**: Do we have data on % of tickets that get an SLA today? Feels like the large majority — is that intended?
  - **Yasmin Lucero**: Wants a lowest-tier SLA at 2 weeks or even a month. Under normal load everything gets handled GTD-style; the SLA tiers only matter under strain, and current spread doesn't give enough flexibility to actually prioritize when overloaded.
  - **Dana Levine**: Goes back and forth. Was on triage this week — bunch of issues without SLAs never got handled until she cleared them. Most team members will ignore/de-prioritize anything without an SLA.

  ### Net takeaways for me
  - Open tensions: (a) SLAs as forcing function (Dana) vs SLAs as dilution risk (Matías/Yasmin); (b) coupling priority↔SLA vs decoupling (Matías); (c) actual fixes likely: key-account tagging, "Feature request" label discipline, possibly a longer low-tier SLA, data on SLA-attached ticket %.
  - Laura is going to update the SLA guide; Justin's data ask is the obvious lever to bring back to the conversation.
  - Action for me: none required from the thread directly. Worth keeping the SLA guide link handy (Notion: "Service Level Agreements (SLAs) Guide" — 1ab8146861518097811de20fc98be9d1). If I see SLA mismatches in triage I can adjust priority (with comment); only PMs remove/extend SLA. Feature requests → add "Feature request" label.
project: null
source_id: https://canarytechnologies.slack.com/archives/C02MVAEJD0Q/p1779460077988889?thread_ts=1779460077.988889&cid=C02MVAEJD0Q
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 15
title: 'Read: Linear SLA patterns thread (Matías, #eng-leads)'
updated: 2026-05-25 11:50:16.383901
waiting_on: null
waiting_since: null
working_on: false
---

10-reply thread on triage SLA issues. https://canarytechnologies.slack.com/archives/C02MVAEJD0Q/p1779460077988889?thread_ts=1779460077.988889&cid=C02MVAEJD0Q