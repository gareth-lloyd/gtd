"""Launch an interactive Claude Code session in an iTerm window.

Spawns iTerm via osascript so the user can supervise the agent. The prompt
is written to a temp file then loaded with `cat` to sidestep shell-quoting
issues for prompts containing quotes, backticks, $vars, or newlines.
"""

from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import tempfile
from pathlib import Path

from gtd_core.models import Bucket, Item, Project

_BUCKET_NAMES = ", ".join(b.value for b in Bucket)


class AgentLaunchError(Exception):
    """Raised when the iTerm launch fails."""


class AgentLaunchNotConfiguredError(AgentLaunchError):
    """Raised when the claude CLI or osascript is not available."""


class AgentLaunchUpstreamError(AgentLaunchError):
    """Raised when osascript runs but errors out (timeout, non-zero exit)."""


def build_prompt(
    item: Item,
    *,
    item_path: Path,
    env_dir: Path,
    project: Project | None = None,
) -> str:
    """Compose the prompt sent to `claude` from a GTD item.

    `item_path` is the absolute path to the markdown file backing the item.
    `env_dir` is the env data directory (parent of the bucket directories).
    Including both lets the agent edit YAML directly and `mv` between buckets
    without going through the HTTP API.
    """
    sections = [
        "You were launched from a GTD next-action item. Do the work described at "
        "the bottom of this prompt, write your findings into the item's `output:` "
        "field, then STOP and hand control back to the user. You are running in "
        "auto mode (permissions bypassed) — be deliberate.",
        "## STRICT: you do not decide when the task is finished",
        (
            "GTD task lifecycle is the user's call, not yours. Your job ends when "
            "you have done the work and recorded what you did. Then you stop and "
            "wait. The user reads your output and decides what happens next: "
            "archive, defer, split into more actions, or follow up.\n\n"
            "Specifically — do NOT do any of the following without explicit "
            "user approval in this session:\n"
            "- `mv` the item file to archive/, trash/, waiting/, someday/, or any "
            "other bucket\n"
            "- Mark the task complete in any way\n"
            "- Delete the item file\n"
            "- Edit `body`, `title`, `due`, `defer_until`, `project`, or other "
            "user-authored fields\n\n"
            "What you SHOULD do when finished: append your work to `output:`, set "
            "`working_on: false`, bump `updated:`, then stop. That's the entire "
            "exit protocol. Don't ask 'should I archive this?' — just stop."
        ),
        "## STRICT: do not touch external services without explicit approval",
        (
            "You are forbidden from making ANY outbound write or state change to a "
            "third-party service unless the user has explicitly approved that "
            "specific action in this session. This is a hard rule, not a default "
            "you can override based on what the task seems to want.\n\n"
            "Forbidden by default (non-exhaustive):\n"
            "- Posting Linear comments, changing issue status, assigning, editing descriptions\n"
            "- Posting Notion comments, editing pages, creating pages\n"
            "- Posting GitHub PR/issue comments, approving/requesting changes, merging, closing\n"
            "- Sending Slack messages, DMs, reactions\n"
            "- Sending emails, calendar invites\n"
            "- Creating/modifying tickets in any tracker\n"
            "- Any POST/PATCH/PUT/DELETE to a non-localhost endpoint\n\n"
            "Read-only operations on these services (fetching issues, reading PRs, "
            "viewing channels) are fine and encouraged for research.\n\n"
            "If a write would be useful, draft it locally and ASK FIRST. Show the "
            "exact text/payload, the destination, and wait for an explicit 'yes, "
            "send it' before doing anything. 'Looks reasonable, proceed' is not "
            "approval — the user must confirm the specific action."
        ),
        "## How to record your work",
        f"The item lives at:\n  {item_path}",
        (
            "Edit the YAML frontmatter directly (no HTTP API needed):\n"
            "- Append your summary to the `output:` field as a multi-line string. "
            "If `output:` already has content, append a new `## Agent run "
            "<ISO timestamp>` section so prior runs aren't overwritten.\n"
            "- Bump `updated:` to the current ISO timestamp on every edit.\n"
            "- Never change `id` or `created`."
        ),
        "## Status changes (reference only — do not initiate)",
        (
            f"Bucket directories live as siblings under {env_dir}/.\n"
            f"Valid buckets: {_BUCKET_NAMES}.\n"
            "Status changes are the user's call. Reference these only if the user "
            "explicitly asks you to move the file in this session."
        ),
        "## Working on",
        (
            "The user pinned this item with `working_on: true` when launching you. "
            "Set it back to `false` as part of your exit protocol — that's the "
            "signal that you've finished and handed back to the user."
        ),
    ]
    if project is not None:
        sections.extend(["## Project context", _project_section(project)])
    if item.output:
        sections.extend(
            [
                "## Prior agent runs on this item",
                (
                    "The item already has `output:` content from one or more "
                    "previous runs (verbatim below). Read it before doing "
                    "anything. Your work should build on it, not duplicate it — "
                    "the user may have re-launched you to verify, refine, "
                    "address a follow-up, or take a next step that depends on "
                    "what was done before. When you record your own work, "
                    "APPEND a new `## Agent run <ISO timestamp>` section to "
                    "`output:` — never overwrite the prior content."
                ),
                "```\n" + item.output + "\n```",
            ]
        )
    sections.extend(["## Task", item.title])
    if item.body:
        sections.append(item.body)
    return "\n\n".join(sections)


def _project_section(project: Project) -> str:
    lines = [f'This item belongs to project "{project.title}".']
    if project.outcome:
        lines.append(f"Outcome: {project.outcome}")
    if project.area:
        lines.append(f"Area: {project.area}")
    return "\n".join(lines)


def launch_claude_session(*, prompt: str, cwd: Path | None = None, auto: bool = True) -> None:
    """Open iTerm and run `claude` with the given prompt as initial input.

    The iTerm session is interactive — the agent stays running so the user
    can supervise, course-correct, and read the result.

    `auto=True` passes `--dangerously-skip-permissions` so the agent runs
    without per-tool prompts. Suitable for the GTD use case where the user
    is launching trusted tasks they intend to be hands-off.
    """
    if not shutil.which("claude"):
        raise AgentLaunchNotConfiguredError(
            "claude CLI not found on PATH — install Claude Code to launch agent sessions"
        )
    osascript = shutil.which("osascript")
    if not osascript:
        raise AgentLaunchNotConfiguredError("osascript not found — agent launch requires macOS")

    cwd = cwd or Path.home()

    fd, raw_path = tempfile.mkstemp(prefix="gtd-agent-", suffix=".txt", text=True)
    prompt_file = Path(raw_path)
    with os.fdopen(fd, "w") as f:
        f.write(prompt)

    auto_flag = " --dangerously-skip-permissions" if auto else ""
    file_q = shlex.quote(str(prompt_file))
    # `trap` ensures the prompt file is removed even if the user closes the
    # iTerm window mid-session (SIGHUP) — bare `; rm` would leak in that case.
    bash_cmd = (
        f"trap 'rm -f {file_q}' EXIT && "
        f"cd {shlex.quote(str(cwd))} && "
        f'claude{auto_flag} "$(cat {file_q})"'
    )
    # Open in a new tab of the current window when iTerm is already running;
    # fall back to a new window when no iTerm window exists yet.
    as_script = (
        f'tell application "iTerm"\n'
        f"    activate\n"
        f"    if (count of windows) = 0 then\n"
        f"        create window with default profile\n"
        f"    else\n"
        f"        tell current window to create tab with default profile\n"
        f"    end if\n"
        f"    tell current session of current window\n"
        f'        write text "{_applescript_escape(bash_cmd)}"\n'
        f"    end tell\n"
        f"end tell"
    )

    try:
        result = subprocess.run(
            [osascript, "-e", as_script],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except subprocess.TimeoutExpired as err:
        prompt_file.unlink(missing_ok=True)
        raise AgentLaunchUpstreamError("osascript timed out after 10s") from err
    except Exception:
        prompt_file.unlink(missing_ok=True)
        raise

    if result.returncode != 0:
        prompt_file.unlink(missing_ok=True)
        raise AgentLaunchUpstreamError(
            f"osascript failed: {result.stderr.strip() or result.stdout.strip()}"
        )


def _applescript_escape(s: str) -> str:
    """Escape a string for inclusion inside an AppleScript double-quoted literal."""
    return s.replace("\\", "\\\\").replace('"', '\\"')
