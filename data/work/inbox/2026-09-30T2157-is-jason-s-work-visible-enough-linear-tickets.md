---
area: null
completed_at: null
contexts: []
created: 2026-09-30 21:57:02.989677
defer_until: 2026-10-05 09:00:00
due: null
energy: low
id: 2026-09-30T2157-is-jason-s-work-visible-enough-linear-tickets
order: null
output: |-
  ## Agent run 2026-10-01T10:36

  **Answer: no. Jason Flax's Orbital work is not visible in Linear, and it is not consistently documented.** There is a lot of text, but it is neither current nor readable, and almost none of the shipped code traces back to a ticket.

  ### The numbers

  - **Code:** 117 PRs opened and 93 merged in canary-technologies-corp/Orbital between Sep 25 and Oct 1 (https://github.com/canary-technologies-corp/Orbital/pulls). All were authored and merged by `jsflax`, and none of the 93 merged PRs has a review.
  - **Ticket linkage:** 6 of the 117 PRs mention an ORB ticket in the title, body or branch name (#19, #25, #31, #65 mention ORB-40; #39, #42 mention ORB-41). The other 111 have no ticket.
  - **Tickets:** the Orbital team has 46 tickets (ORB-1 to ORB-46). 25 are In Progress, and 23 of those have not been updated since Sep 18-19, the day they were bulk-imported.
  - **Completions:** one ticket has been opened and closed for new work since the import, ORB-41. The other Done tickets are historical imports or were closed on import day.
  - **Status updates:** zero on Orbital alpha, Release Desk & delivery and Orbital Orchestration v1. Jason has posted no project status update on any Orbital project. His only one anywhere is on the Nest project, dated Aug 19.
  - **Comments:** zero on the five tickets I sampled (ORB-8, ORB-37, ORB-39, ORB-41, ORB-42) and zero on the Orbital alpha project.

  ### Projects

  | Project | Status | Last updated | State of the documentation |
  | --- | --- | --- | --- |
  | Orbital alpha (https://linear.app/canary-technologies/project/orbital-alpha-cd269a2d7960) | Implementation | Sep 25 | Description is about 120,000 characters (13,400 words) of agent-written release log. Describes Build 71; nothing on Build 72. |
  | Release Desk & delivery (https://linear.app/canary-technologies/project/release-desk-and-delivery-c9002950716b) | Implementation | Sep 22 | Describes the alpha70 hold. Four tickets In Progress, untouched since Sep 18-25. |
  | Lattice foundation (https://linear.app/canary-technologies/project/lattice-foundation-53950e338c06) | Backlog | Sep 18 | Marked Backlog although it holds two In Progress tickets and one Done. |
  | Engram runtime & integrations (https://linear.app/canary-technologies/project/engram-runtime-and-integrations-ab760de93ead) | Backlog | Sep 18 | Two historical-import tickets, both Done. No open work recorded. |
  | Orbital Orchestration v1, in the EE team (https://linear.app/canary-technologies/project/orbital-orchestration-v1-68cf45a49fb1) | Backlog | Sep 23 | The clearest description of the five (version ladder, design decisions, risks). 21 tickets, 20 in Backlog. EE-2131 has been In Progress since Aug 8 and its last progress note is dated Aug 8. |

  No project has a target date. None has a lead other than Jason, and he is the only member on each.

  ### What is wrong

  1. **Linear lags the code by about six days.** The Orbital alpha description still opens with "Build71 convergence". The PRs since Sep 26 are titled Build 72 and none of that work appears in Linear apart from ORB-40 and ORB-41.
  2. **The documentation is unreadable for a human.** The Orbital alpha description and ORB-37 (https://linear.app/canary-technologies/issue/ORB-37/implement-orbital-repository-cicd-and-validated-release-candidates) are near-identical 120,000-character logs with about 30 timestamped sections of hashes, byte counts and build numbers. A typical sentence: "Native v5 remains incomplete at replica5/6 and remote App33 reconnect returned companion offline". There is no summary of what works, what is broken and what is next.
  3. **Ticket status does not mean what it says.** The 20 QA tickets ORB-8 to ORB-27 (T001-T020) were imported on Sep 18 with 18 of them In Progress. Each carries the text "In Progress means partially implemented/open, not a currently running executor". None has moved in 12 days. Example: ORB-8 (https://linear.app/canary-technologies/issue/ORB-8/t001-chats-stays-at-loading-rooms-navigation-stalls).
  4. **Tickets cite sources nobody else can open.** The imported tickets reference files under `/Users/jason/localdev/...` on Jason's laptop, and name an agent ("orbital-shock-trooper") as the execution owner.
  5. **Work that is done is not closed.** ORB-40 (https://linear.app/canary-technologies/issue/ORB-40/bug-sweep-room-chat-virtualization-blackout-agent-switch-failures-and) is High priority, in Backlog and unassigned, with no linked PRs, although four merged PRs reference it.
  6. **Other people's reports get no response.** Laura DeWald filed ORB-39 (https://linear.app/canary-technologies/issue/ORB-39) on Sep 25 and ORB-42 (https://linear.app/canary-technologies/issue/ORB-42/swarm-view-doesnt-show-all-agents) on Sep 29. Arihant Daga filed ORB-43 to ORB-45 on Sep 29. All five have no assignee, no priority and no comment, and Laura's two are not in a project. ORB-43 repeats ORB-39 (Shift+Enter), which suggests nobody is triaging.

  ### What is good

  - ORB-41 (https://linear.app/canary-technologies/issue/ORB-41/agents-save-changes-in-edit-agent-modal-is-unresponsive-unable-to) is the model: Blake reported a bug by Loom, the ticket has repro steps and acceptance criteria, PR #39 is linked, and it went from filed to Done in about two hours on Sep 27.
  - ORB-40 is also a well-written ticket. Only its status is wrong.
  - The Orbital Orchestration v1 project description is clear and decision-oriented.

  So Jason, or his agents, can write good tickets. The problem is that this happens for two tickets out of a week of 93 merged PRs.

  ### Other things you may want to know

  - Release artifacts sit on personal infrastructure: GitHub releases on `jsflax/Orbital` and downloads on `orbital-private-docs-20260917-jf.fly.dev`. The project text also says "Hosted Actions remains billing-blocked".
  - A second public team, "Orbital R02 Qualification 20260919", is a disposable test team with two leftover tickets (ORQ-1, ORQ-2).
  - The Orbital team in Linear has two members: Jason and Laura DeWald.

  ### If you raise it with Jason

  These follow from the findings; they are suggestions, not things I have done.

  - One short human-written status update per week on Orbital alpha: what shipped, what is broken, what is next.
  - Every PR names an ORB ticket, and tickets close when the PR merges.
  - Move the build log out of the project description and ORB-37 into a document, and replace it with a one-screen summary.
  - Reset the 18 stale In Progress QA tickets to what is true today.
  - Triage tickets from other people within a day or two.

  ### Not checked

  - Slack. His work may be more visible there than in Linear.
  - I read the headings plus the opening and closing sections of the two 120,000-character texts, not every word.
  - Comments on the other 41 tickets, and status updates by anyone other than Jason on Lattice foundation and Engram runtime.
  - Cycles and estimates.

  Nothing was written to Linear, GitHub or any other service.
project: null
source_id: null
tags: []
time_minutes: 5
title: Is jason's work visible enough? Linear tickets?
updated: 2026-10-02 12:23:43.621244
waiting_on: null
waiting_since: null
working_on: false
---

Check the projects and tickets in the Orbital projects on Linear. 

Is the work consistently documented?