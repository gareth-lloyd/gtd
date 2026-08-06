---
area: null
completed_at: 2026-08-06 13:42:01.289570
contexts: []
created: 2026-08-05 23:47:18.538527
defer_until: null
due: null
energy: low
id: 2026-08-05T2347-analyze-where-i-post-and-add-to-notes-channels-gtd
order: null
output: |
  ## Agent run 2026-08-06T10:20

  Analysed Slack via the xoxp token in `~/.claude/skills/triage-slack/fetch_unread.py`
  (read-only `search.messages` / `reminders.list`). Scripts in
  `/private/tmp/claude-501/-Users-garethlloyd-projects-canary/a338c489-b0ab-4a27-aad4-7b0b781f26ac/scratchpad/`.

  Corpus: **5,986 sent messages** (2026-02-11 → 08-06; hit the 60-page cap, so the
  Feb end is truncated) and **905 saved-for-later items** (2024-08-16 → 2026-08-05,
  exact API total).

  ### 1. Where I post (sent volume)

  | window | 1:1 DM | group DM | public ch | private ch |
  |---|---|---|---|---|
  | last 30d (827 msgs, 27.6/day) | 50% | 8% | 17% | 22% |
  | last 90d | 47% | 12% | 20% | 21% |
  | full 6mo | 48% | 12% | 25% | 14% |

  **~60% of everything I send is a DM or group DM.** Channels are the minority
  surface. 41% of sent messages are thread replies.

  Top surfaces, last 90 days:

  ```
   153  GROUPDM cswords+abradshaw+glloyd   <- bigger than ANY single channel
   171  #epd-enterprise
   142  #epd-enterprise-engineers          <- NOT in PRIORITY_CHANNELS
   136  DM:Martijn Dekker
   129  DM:Connor Swords
   121  DM:Andrea Bradshaw
   101  #wyndham
    74  #tmp-check-in-configuration-location  <- didn't exist 6 months ago, #1 channel in last 30d
    70  #eng-directors                     <- NOT in PRIORITY_CHANNELS
    69  DM:Ian Clark
    68  DM:Laura DeWald
  ```

  Only **51% of my channel messages (20% of all sent messages) land in a
  `PRIORITY_CHANNELS` channel.** The list has drifted badly:

  | in PRIORITY_CHANNELS | sent 90d | sent 6mo | saved 90d | saved 1y |
  |---|---|---|---|---|
  | epd-enterprise | 171 | 328 | 17 | 65 |
  | wyndham | 101 | 350 | 18 | 62 |
  | eng-acceleration-guild | 52 | 75 | 3 | 18 |
  | eng-leads | 42 | 72 | 2 | 18 |
  | eng-general | 32 | 39 | 6 | 8 |
  | upleveling-enterprise-deployment | 31 | 195 | 2 | 30 |
  | best-western | 29 | 38 | 7 | 15 |
  | epd-core-engineers | 22 | 219 | 3 | 33 |
  | epd-emea-engineers | 16 | 27 | 8 | 8 |
  | **ihg** | **12** | 52 | **1** | 13 |
  | epd-emea | 7 | 7 | 1 | 3 |
  | blake-directs | 3 | 4 | 1 | 1 |
  | **eng-hiring-managers** | **0** | **0** | 0 | 5 |
  | **epd-customer-activation** | **0** | **0** | **0** | **0** |
  | **epd-customer-activation-engineers** | **0** | **0** | **0** | **0** |

  Missing from the list but genuinely active:

  ```
  #epd-enterprise-engineers   sent90 142  saved1y 11
  #eng-directors              sent90  70  saved1y  8
  #tmp-check-in-config...     sent90  74  saved1y  7
  #project-ihg-pilot          sent90   3  saved1y 21  (sent6mo 122 — where IHG work actually is)
  #project-triage-agent       sent90  23  saved1y 11
  #epd-internal-tools(-engineers)  sent90 15  saved1y 24
  #eng-security               sent90  16  saved1y  0
  #agentic-dev-leads          sent90  13  saved1y  2
  #ihg_sso                    sent90   0  saved1y 13
  ```

  ### 2. Where saved-for-later items come from

  905 saves, ~2.3/day currently (65 in Jul, 92 in May). Distribution:

  | | last 90d (n=208) | all time (n=905) |
  |---|---|---|
  | public channel | 42% | 48% |
  | private channel | 25% | 16% |
  | 1:1 DM | 20% | 25% |
  | group DM | 11% | 9% |
  | **is_self_save** | **4%** | **6%** |
  | **mentions_me** | **13%** | **17%** |
  | **is thread reply** | **60%** | **62%** |
  | falls through to AWARE bucket | **51%** | **45%** |

  Top save sources (90d): #wyndham 18, #epd-enterprise 17,
  #epd-enterprise-engineers 11, #epd-emea-engineers 8, #eng-directors 7,
  #best-western 7, #tmp-check-in-configuration-location 7.
  Top authors saved: Andrea Bradshaw 16, Connor Swords 14, Blake VanLandingham 13.

  **The inverse of posting.** 64% of saves are channel messages but only 31% of
  what I send is. I *transact* in DMs and *park* in channels.

  Two asymmetries worth encoding:
  - **read-and-park surfaces** (save a lot, post almost nothing): #project-ihg-pilot
    (21 saved / 3 sent), #ihg_sso (13/0), #epd-internal-tools+engineers (24/15),
    #eng-announce (8/5), #epd-communications-core (6/1).
  - **working surfaces** (post a lot, never save): the cswords+abradshaw triad
    (153 sent / 5 saved), DM:Andrea Bradshaw (121/8), DM:Ian Clark (69/1),
    #eng-security (16/0), #eng-alerts-oncall (52/0).

  ### 3. Two hard findings about the data sources

  **`is:saved` is a lifetime archive, not the Later list.** It returns all 905 items
  back to Aug 2024, including ones long since completed. Slack search offers no
  in-progress / archived / completed filter. I checked the alternatives:
  `stars.list` → `missing_scope`, `saved.list` → `not_allowed_token_type`.
  So the skill **cannot tell "still parked" from "already dealt with"** and must
  lean entirely on GTD-side `source_id` dedup (which `capture_items.py` does do
  across every bucket including archive/trash, so this is mitigated but not solved).

  **Slack reminders are dead.** `reminders.list` → `ok:true`, **0 reminders**,
  none complete, none incomplete. The `reminder` item kind and the
  `slack reminder` classification row have never fired.

  ---

  ## Suggested edits to the /gtd skill

  **A. `PRIORITY_CHANNELS` (`~/.claude/skills/triage-slack/fetch_unread.py:17`) — highest impact**

  Drop: `epd-customer-activation`, `epd-customer-activation-engineers` (0 sent /
  0 saved, ever), `eng-hiring-managers` (0 sent).
  Add: `epd-enterprise-engineers`, `eng-directors`, `project-ihg-pilot`,
  `project-triage-agent`, `epd-internal-tools`, `epd-internal-tools-engineers`,
  `epd-voice`.
  Keep-but-note: `#ihg` is nearly dormant (12 sent / 1 save in 90d) — the IHG
  conversation moved to `#project-ihg-pilot` and `#ihg_sso`. `blake-directs` stays
  on stakes, not volume.

  **B. Make the channel list partly dynamic.**
  `#tmp-check-in-configuration-location` was the highest-volume channel of the last
  30 days and did not exist 6 months ago. A hand-maintained set will always lag.
  Add to the fetcher: any channel where I sent ≥10 messages in the last 14 days is
  treated as priority for that run. One extra `search.messages` call
  (`from:me after:<14d>`), bucketed by channel.

  **C. Phase 1.6 — recalibrate the saved-items heuristics (SKILL.md:132-135).**
  The three ACTIONABLE triggers cover a minority of saves: self_save 4%,
  mentions_me 13%, DM/group-DM 31%. **51% of every pull falls through to AWARE.**
  The skill spends three bullets on the actionable path and one line on the
  dominant outcome. Invert the emphasis: default a saved item to "context I
  parked", and give the AWARE path real treatment in the awareness report
  (group by theme, age out anything >30d rather than re-listing it).

  **D. Phase 1.6 — fetch thread parents (SKILL.md:105).**
  62% of saved items are mid-thread replies, but the phase specifies
  `include_context=false`. A reply with no parent is frequently unclassifiable
  ("Will share", "We did - context is in that ticket" are both real saves).
  Add: where the permalink carries `thread_ts` ≠ `ts`, do one `slack_read_thread`
  on the parent before classifying. Cap at 8 calls.

  **E. Phase 1.6 — bound by date, and state the archive caveat (SKILL.md:105).**
  At 2.3 saves/day, `limit=30` ≈ 13 days — roughly right by accident. Make it
  explicit: add `after:<today-10d>`. And document that `is:saved` returns the
  lifetime archive with no completed/in-progress distinction, so the classifier
  knows staleness is expected and dedup is load-bearing.

  **F. Phase 1.7 — the missed-yesterday sweep watches the wrong four (SKILL.md:145).**
  Currently `#wyndham`, `#best-western`, `#ihg`, `#epd-enterprise`. Keep #wyndham
  and #epd-enterprise (both top-2 on sent and saved). Keep #best-western
  (moderate: 29 sent / 7 saved). **Swap `#ihg` for `#epd-enterprise-engineers`** —
  142 sent and 11 saves in 90d vs #ihg's 12 and 1.

  **G. Priority lens (SKILL.md:18-22) — name people and the ENT triad, not just accounts.**
  The lens names Wyndham/BW/IHG and four channels. It names no people, yet 60% of
  my output is DMs. Add: the group DM `cswords+abradshaw+glloyd` is my single
  highest-volume surface (153 msgs/90d, more than any channel) and should rank
  with the key-account channels. Top DM partners by volume — Martijn Dekker,
  Connor Swords, Andrea Bradshaw, Ian Clark, Laura DeWald, Andrés Figueira — a DM
  from one of these should outrank a DM from someone I rarely talk to.

  **H. Encode the transact/park asymmetry in Phase 3 classification (SKILL.md:186-213).**
  A save from a DM/group DM = someone is waiting on me (ACTIONABLE).
  A save from a read-and-park channel (#project-ihg-pilot, #ihg_sso,
  #epd-internal-tools*, #eng-announce) = reading material (AWARE, and say so).
  This is already roughly the intent; the channel lists make it decidable.

  **I. Delete the reminder path.** `reminder` kind in `fetchers/slack.py`,
  SKILL.md:190 and the `slack reminder` row at SKILL.md:242. Zero reminders exist;
  Save-for-later is the sole parking mechanism. Removing it shrinks the skill and
  the fetcher for no loss.

  ### Caveats
  - Sent corpus is capped at 60 pages, so it floors at 2026-02-11 (~400 older
    messages dropped). All 90d/30d figures are unaffected.
  - `search.messages` indexes only conversations this token can see; a private
    channel I'm not in wouldn't appear (not a real gap here).
  - Nothing was written to Slack. No completed/in-progress split is obtainable for
    saved items with the current token scopes.

  ### Not done
  The title also says "add Current projects in gtd" — that's a separate action
  and I left it alone.
project: null
source_id: null
tags: []
time_minutes: 5
title: Analyze where I post and add to notes channels gtd add Current projects in
  gtd
updated: 2026-08-06 13:42:01.289561
waiting_on: null
waiting_since: null
working_on: false
---

Do an analysis of my sent messages on slack. 
Where do I post most?
Analyze current and completed messages that are/were "saved for later / reminded". Where are most of these?

Output: suggestions for edits to /gtd skill slack attention guidance.