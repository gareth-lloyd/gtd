# GTD Inbox Processing

Interactive inbox processor. Walks through each inbox item and helps the user clarify and organize it.

## Usage

`/gtd-inbox` or `/gtd-inbox work` or `/gtd-inbox home`

## Behavior

1. If no env specified, ask "Which environment? (work / home / both)"
2. Read all files in `data/<env>/inbox/`, sorted by created date (oldest first).
3. Show count: "N items in <env> inbox. Let's process them."

For each item:
- Display: title, body (if any), created date
- Ask the GTD clarifying question: **"Is this actionable?"**

### If actionable:
- Ask: "What's the very next physical action?" (help refine the title if needed)
- Ask: "Context?" — show the env's contexts from config.yml as options
- Ask: "Energy? (low / medium / high)"
- Ask: "Time estimate in minutes?"
- Ask: "Part of a project?" — list active projects as options, or "standalone"
- Apply the two-minute rule: if time ≤ 2 min, suggest "Just do it now and mark done"
- Move the file to `data/<env>/next/` and update frontmatter fields

### If NOT actionable:
- Ask: "Is it reference material, a someday/maybe, or trash?"
  - Reference → move to `data/<env>/reference/`
  - Someday → move to `data/<env>/someday/`
  - Trash → move to `data/<env>/trash/`

### If it's actually a project (requires multiple actions):
- Create a project file in `data/<env>/projects/`
- Identify the first next action
- Create that as an item in `data/<env>/next/` linked to the project

4. After all items processed, show summary: "Processed N items: X→next, Y→someday, Z→trash, W→reference"
5. Offer to snapshot: `uv run manage.py snapshot -m "inbox processing"`

## Important

- Move files using the filesystem directly. Status = directory.
- Update frontmatter fields using the Edit tool when adding contexts/energy/time.
- Confirm each move before executing. Let the user skip items ("skip" / "later").
- Keep the pace brisk — don't over-explain GTD concepts unless asked.
