# GTD Weekly Review

You are running a GTD weekly review for the user. Read the text files directly under `data/` — no server needed.

## Environment

Ask the user which environment to review (work or home), or do both sequentially.

## Steps

### 1. Inbox → Zero

Read all files in `data/<env>/inbox/`. For each item:
- Show the title and body
- Ask: "Actionable? (next / waiting / someday / reference / trash / 2-min rule)"
- If actionable: ask for context, energy, time estimate. Move the file to the appropriate bucket directory and update frontmatter fields.
- If not: move to reference, someday, or trash.
- Goal: empty the inbox.

### 2. Review active projects

Read `data/<env>/projects/*.md`. For each project where `status: active`:
- Show title and outcome
- List linked actions: `grep -l "project: <id>" data/<env>/next/*.md data/<env>/waiting/*.md`
- Ask: "Is there a clear next action? Should any be added? Should this project be completed or put on hold?"

### 3. Check waiting-for items

Read `data/<env>/waiting/*.md`. For each item:
- Show title, waiting_on, waiting_since, and updated date
- Flag items where updated is >7 days ago as stale
- Ask: "Follow up? Still waiting? Move to next/trash?"

### 4. Review deferred items

Read `data/<env>/next/*.md` and check `defer_until` fields. Show items where `defer_until` is within the next 7 days. Ask if they should be activated (clear defer_until) or re-deferred.

### 5. Someday/Maybe sweep

Read `data/<env>/someday/*.md`. Show each item briefly. Ask: "Still interested? Move to next? Trash?"

### 6. Summary

Print a table:
- Inbox: count (should be 0 after step 1)
- Next: count
- Waiting: count (flag stale)
- Someday: count
- Projects (active): count
- Items processed this review

After completing the review, offer to run `uv run manage.py snapshot -m "weekly review"` to commit all changes.

## Important

- Move files between directories using `mv` (or Python `Path.rename`). Also update frontmatter fields as needed (contexts, energy, etc.) using the Edit tool.
- Status is the directory name, not a frontmatter field. Moving the file IS the status change.
- Always confirm destructive actions (trash, project completion) before executing.
