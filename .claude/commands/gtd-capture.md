# GTD Quick Capture

Capture a new item into the inbox. Arguments are the item title.

## Usage

`/gtd-capture Buy birthday present for Sarah`

## Behavior

1. Determine the environment. If the user doesn't specify, use the last-used env from `localStorage` or default to "work". Ask if ambiguous.
2. Generate an ID: `YYYY-MM-DDTHHMM-<slugified-title>.md` using the current time.
3. Create the file at `data/<env>/inbox/<id>.md` with this frontmatter:

```yaml
---
id: <generated-id>
title: <title from arguments>
created: <now>
updated: <now>
contexts: []
energy: low
time_minutes: 5
project: null
area: null
tags: []
due: null
defer_until: null
waiting_on: null
waiting_since: null
---
```

4. If the user included additional context in the conversation (not just the title), add it as the markdown body below the frontmatter.
5. Confirm: "Captured: <title> → data/<env>/inbox/<id>.md"

## Notes

- Defaults to energy=low, time=5min (same as the web UI capture bar)
- The user can chain multiple captures: just keep providing titles
- No validation needed for inbox items — they get processed later
