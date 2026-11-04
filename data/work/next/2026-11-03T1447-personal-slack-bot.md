---
area: null
completed_at: null
contexts: []
created: 2026-11-03 14:47:55.320372
defer_until: null
due: null
energy: low
id: 2026-11-03T1447-personal-slack-bot
order: null
output: ''
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: 5
title: Personal slack bot
updated: 2026-11-04 16:12:37.025305
waiting_on: null
waiting_since: null
working_on: false
---

# Triggering a personal Claude agent from Slack mentions / DMs

_2026-11-03. Preferences: run locally, stay within the Claude subscription, hook into the local GTD system._

## Options considered

| # | Option | Runs | Cost | GTD fit | Verdict |
|---|--------|------|------|---------|---------|
| 1 | Slack Socket Mode listener → headless `claude -p` | Local (Mac) | Subscription | Direct: runs in your repo with your gtd skills + Bear | **Recommended first build** |
| 2 | Custom Claude Code **channel** (MCP server) feeding a persistent interactive session | Local | Subscription | Direct, plus conversational context | Upgrade path; research preview, dev flag, needs tmux session |
| 3 | iMessage channel plugin (official) | Local | Subscription | Direct | Excluded (not Slack) |
| 4a | Claude Code in Slack (@mention in a channel → cloud session on a GitHub repo) | Anthropic cloud | Pro/Max | Only if GTD state lives in a repo | Channels only, no DMs; being retired for Claude Tag workspaces |
| 4b | Scheduled task with API trigger (Slack Events handler POSTs to the task's fire endpoint) | Anthropic cloud | Pro/Max | Only via a git repo | Cannot wake the Mac |
| 4c | Claude Tag | Anthropic cloud | Team/Enterprise only | Weak | Not on our plan |
| 4d | Remote Control | Local, driven from claude.ai/mobile | Subscription | Direct | No documented Slack → session path (inbox tooling hints at Slack thread linking; unconfirmed) |
| 5a | OpenClaw-style self-hosted gateway | Local | **API key** (subscription OAuth blocked for third parties) | Indirect | Outside subscription |
| 5b | Self-hosted n8n: Slack trigger → Execute Command → `claude -p` | Local | Subscription | Direct | No-code version of option 1 |
| 5c | Zapier / Make → local webhook via Tailscale Funnel | Hosted hop + local | Subscription + Zapier | Direct | No gain over Socket Mode |

Key facts verified against the Claude Code docs (2026-11-03):

- Headless `claude -p` uses the normal subscription login unless `ANTHROPIC_API_KEY` is set.
- Anthropic forbids **third-party products** offering claude.ai login via the Agent SDK. A personal CLI script on your own machine is not addressed by that text — not explicitly blessed either.
- Channels: official plugins exist for Telegram, Discord, iMessage. No Slack plugin. Custom channels need `--dangerously-load-development-channels`, interactive sessions only (ignored under `-p`).
- Scheduled-task API triggers and Claude Code in Slack both run in Anthropic's cloud.

## Proposal: smallest viable build (option 1)

One Python file, no server, no public URL. ~1 hour.

### 1. Slack app (browser, ~5 min)

- Create app at api.slack.com/apps; enable **Socket Mode**; generate an app-level token with `connections:write`.
- Bot token scopes: `app_mentions:read`, `im:history`, `chat:write`.
- Event subscriptions: `app_mention`, `message.im`.
- Install to workspace; note your own Slack member ID.

### 2. Script

```python
# slack_agent.py  — run with: uv run --with slack-bolt python slack_agent.py
import os, subprocess
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

ME = os.environ["MY_SLACK_ID"]
GTD_DIR = os.path.expanduser("~/projects/gtd")   # wherever your gtd files live
app = App(token=os.environ["SLACK_BOT_TOKEN"])

def handle(event, say):
    if event.get("user") != ME or event.get("bot_id"):
        return
    text = event["text"]
    link = f"https://slack.com/archives/{event['channel']}/p{event['ts'].replace('.', '')}"
    prompt = f"Capture this Slack message into my GTD inbox, then reply in one line:\n{text}\nSource: {link}"
    out = subprocess.run(
        ["claude", "-p", prompt, "--permission-mode", "acceptEdits", "--output-format", "text"],
        cwd=GTD_DIR, capture_output=True, text=True, timeout=300,
    )
    say(text=(out.stdout or out.stderr)[-2900:], thread_ts=event.get("thread_ts", event["ts"]))

app.event("app_mention")(lambda event, say: handle(event, say))
app.event("message")(lambda event, say: handle(event, say))   # DMs arrive as message.im

SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
```

### 3. Run

Export `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`, `MY_SLACK_ID`; start the script; @mention or DM the bot. Once it works, wrap it in a launchd plist.

### Things to know

- **Headless permissions.** A `-p` run cannot prompt; anything not pre-allowed is denied. Start with `acceptEdits`, widen with `--allowedTools` only if the gtd skill needs Bash/MCP.
- **Slash commands.** Once the plain prompt works, try `/gtd-inbox …` as the prompt so the existing skill does the capture. If skills don't fire under `-p`, keep the plain-prose prompt.
- **Sender gate.** The member-ID equality check is the entire security model. Keep it; no permission relay or open access until you've considered who else can DM the bot.

### Upgrade path

Re-wrap the same Socket Mode listener as an MCP channel server feeding a persistent `claude --channels` session (option 2) when back-and-forth conversation from Slack is wanted rather than fire-and-forget capture.

## Sources

- https://code.claude.com/docs/en/channels
- https://code.claude.com/docs/en/channels-reference
- https://code.claude.com/docs/en/slack
- https://code.claude.com/docs/en/scheduled-tasks
- https://code.claude.com/docs/en/headless
- https://code.claude.com/docs/en/agent-sdk/overview
- https://code.claude.com/docs/en/remote-control
- https://claude.com/docs/claude-tag/overview