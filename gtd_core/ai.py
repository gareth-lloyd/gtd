"""AI-powered capture and merge — Claude CLI turns prose into structured Items."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from gtd_core.models import EnvConfig, Item, Project

_JSON_SCHEMA = """{
  "title": "string (required — verb-first concrete next action, fix typos)",
  "body": "string or null (optional markdown notes)",
  "energy": "\"low\" | \"medium\" | \"high\" or null",
  "time_minutes": "integer or null",
  "contexts": "[list of strings] or null — only from the valid contexts listed above",
  "area": "string or null — only from the valid areas listed above",
  "project_query": "string or null — name/keyword of one of the listed projects",
  "due": "string or null — ISO date or natural language like 'tomorrow', '2w', 'eom'",
  "defer_until": "string or null — ISO date or natural language",
  "summary": "string (required — one-line toast, e.g. 'Filed to People — due tomorrow')"
}"""


class AiCaptureError(Exception):
    """Raised when the AI capture pipeline cannot produce a structured result."""


class AiCaptureNotConfiguredError(AiCaptureError):
    """Raised when the claude CLI is not available."""


class AiCaptureUpstreamError(AiCaptureError):
    """Raised for Claude CLI failures."""


class AiCaptureNoExtractionError(AiCaptureError):
    """Raised when the model didn't return parseable JSON."""


@dataclass(slots=True)
class AiCaptureResult:
    title: str
    summary: str
    body: str | None = None
    energy: str | None = None
    time_minutes: int | None = None
    contexts: list[str] | None = None
    area: str | None = None
    project_query: str | None = None
    due: str | None = None
    defer_until: str | None = None


_MERGE_JSON_SCHEMA = """{
  "title": "string (required — one merged verb-first title)",
  "body": "string (required — merged markdown notes; empty string if neither item has notes)"
}"""


@dataclass(slots=True)
class AiMergeResult:
    title: str
    body: str


def ai_capture(
    *,
    text: str,
    cfg: EnvConfig,
    projects: list[Project],
    sample_actions: dict[str, list[str]],
    today: date,
    api_key: str | None = None,
    model: str = "",
) -> AiCaptureResult:
    """Extract a structured Item from unstructured text via the Claude CLI.

    Shells out to `claude -p "..." --model <model>`. Uses the user's Max plan
    so no separate API credits are needed.

    Test seam: if ``GTD_AI_STUB_RESPONSE`` is set in the environment its value
    is parsed as the raw Claude CLI output. The subprocess is not invoked.
    Used by the Playwright e2e suite to drive AI capture without the real CLI.
    """
    stub = os.environ.get("GTD_AI_STUB_RESPONSE")
    if stub:
        return _parse_response(stub)

    claude_path = shutil.which("claude")
    if not claude_path:
        raise AiCaptureNotConfiguredError(
            "claude CLI not found on PATH — install Claude Code to use AI capture"
        )

    prompt = _build_prompt(
        text=text,
        cfg=cfg,
        projects=projects,
        sample_actions=sample_actions,
        today=today,
    )
    raw = _run_claude(claude_path, prompt, model=model, config_dir=cfg.claude_config_dir)
    return _parse_response(raw)


def ai_merge(
    *,
    target: Item,
    source: Item,
    today: date,
    config_dir: str | None = None,
    model: str = "",
) -> AiMergeResult:
    """Fold `source`'s prose into `target`'s via the Claude CLI.

    Returns only the merged title + body; the caller decides what happens to
    the non-prose fields and to the source item. Same stub seam and error
    hierarchy as `ai_capture`.
    """
    stub = os.environ.get("GTD_AI_STUB_RESPONSE")
    if stub:
        return _parse_merge_response(stub)

    claude_path = shutil.which("claude")
    if not claude_path:
        raise AiCaptureNotConfiguredError(
            "claude CLI not found on PATH — install Claude Code to use AI merge"
        )

    prompt = _build_merge_prompt(target=target, source=source, today=today)
    raw = _run_claude(claude_path, prompt, model=model, config_dir=config_dir)
    return _parse_merge_response(raw)


def _run_claude(
    claude_path: str, prompt: str, *, model: str = "", config_dir: str | None = None
) -> str:
    """Run `claude -p <prompt>` and return its trimmed stdout."""
    cmd = [claude_path, "-p", prompt]
    if model:
        cmd.extend(["--model", model])

    # Run under the env's Claude account (see EnvConfig.claude_config_dir) so
    # e.g. home captures never go through the work account.
    env = None
    if config_dir:
        env = {
            **os.environ,
            "CLAUDE_CONFIG_DIR": str(Path(config_dir).expanduser()),
        }

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            env=env,
        )
    except subprocess.TimeoutExpired as err:
        raise AiCaptureUpstreamError("Claude CLI timed out after 30s") from err

    if result.returncode != 0:
        stderr = result.stderr.strip()
        raise AiCaptureUpstreamError(
            f"Claude CLI failed (exit {result.returncode}): {stderr or result.stdout.strip()}"
        )

    return result.stdout.strip()


def _build_prompt(
    *,
    text: str,
    cfg: EnvConfig,
    projects: list[Project],
    sample_actions: dict[str, list[str]],
    today: date,
) -> str:
    lines: list[str] = [
        "You extract structured GTD next actions from raw user input.",
        "Reply ONLY with a single JSON object matching the schema below "
        "— no markdown fences, no commentary.",
        "",
        f"Today: {today.isoformat()}",
        "",
        f"Valid contexts: {', '.join(cfg.contexts) if cfg.contexts else '(none configured)'}",
        f"Valid areas: {', '.join(cfg.areas) if cfg.areas else '(none configured)'}",
        "",
        "Existing projects:",
    ]
    if projects:
        for p in projects:
            parts = [f"- {p.title}"]
            if p.area:
                parts.append(f"(area: {p.area})")
            if p.outcome:
                parts.append(f"— {p.outcome}")
            lines.append(" ".join(parts))
            samples = sample_actions.get(p.id, [])
            if samples:
                joined = "; ".join(f'"{s}"' for s in samples)
                lines.append(f"  Recent actions: {joined}")
    else:
        lines.append("(no active projects)")

    lines.extend(
        [
            "",
            "Rules:",
            "- Fix typos and expand shorthand.",
            "- Write titles as verb-first concrete next actions.",
            "- Only set a field when clearly implied by the input.",
            "- If the input references a project by name or keyword, set project_query "
            "to that project's title.",
            "- When a project matches, phrase the title to fit that project's recent-action style.",
            "- Dates accept natural language ('tomorrow', 'next friday', 'eom', '2w') "
            "or ISO YYYY-MM-DD.",
            "- Always include a one-line summary of what you extracted for the user toast.",
            "",
            f"JSON schema:\n{_JSON_SCHEMA}",
            "",
            f"User input: {text.strip()}",
        ]
    )
    return "\n".join(lines)


def _build_merge_prompt(*, target: Item, source: Item, today: date) -> str:
    def _block(label: str, item: Item) -> list[str]:
        return [
            f"### {label}",
            f"Title: {item.title}",
            "Body:",
            item.body.strip() or "(no notes)",
            "",
        ]

    lines: list[str] = [
        "You merge two GTD next actions that describe the same piece of work into one.",
        "Reply ONLY with a single JSON object matching the schema below "
        "— no markdown fences, no commentary.",
        "",
        f"Today: {today.isoformat()}",
        "",
        "The CURRENT item is the one being kept. The OTHER item is being folded into it "
        "and will be trashed afterwards, so anything you leave out is lost.",
        "",
        *_block("CURRENT item", target),
        *_block("OTHER item", source),
        "Rules:",
        "- Produce exactly one merged title and one merged body.",
        "- De-duplicate repeated information, but err STRONGLY toward including ALL "
        "information from both items. When in doubt, keep it.",
        "- Prefer the CURRENT item's title unless the OTHER item's is clearly better. "
        "Keep the title a verb-first concrete next action.",
        "- Merge the bodies into clean markdown, preserving every distinct note, link, "
        "checklist item, date, and name from either body.",
        "- Do not invent facts, tasks, or details that appear in neither item.",
        "- If neither item has notes, return an empty string for body.",
        "",
        f"JSON schema:\n{_MERGE_JSON_SCHEMA}",
    ]
    return "\n".join(lines)


def _parse_json_object(raw: str, *, hint: str) -> dict:
    """Strip optional ```json fences and parse a JSON object with a `title`."""
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1]
    if cleaned.endswith("```"):
        cleaned = cleaned.rsplit("```", 1)[0]
    cleaned = cleaned.strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as err:
        raise AiCaptureNoExtractionError(
            f"AI did not return valid JSON; {hint}. Raw: {raw[:200]}"
        ) from err

    if not isinstance(data, dict) or "title" not in data:
        raise AiCaptureNoExtractionError(f"AI response missing required 'title' field; {hint}")

    return data


def _parse_response(raw: str) -> AiCaptureResult:
    data = _parse_json_object(raw, hint="try again or use Regular capture")
    return _result_from_dict(data)


def _parse_merge_response(raw: str) -> AiMergeResult:
    data = _parse_json_object(raw, hint="try the merge again")
    body = data.get("body")
    return AiMergeResult(
        title=str(data["title"]).strip(),
        body="" if body is None else str(body).strip(),
    )


def _result_from_dict(data: dict) -> AiCaptureResult:
    def _opt_str(key: str) -> str | None:
        value = data.get(key)
        if value is None:
            return None
        value = str(value).strip()
        return value or None

    return AiCaptureResult(
        title=str(data["title"]).strip(),
        summary=str(data.get("summary", f'Added "{data["title"]}" to inbox')).strip(),
        body=_opt_str("body"),
        energy=_opt_str("energy"),
        time_minutes=(
            data.get("time_minutes") if isinstance(data.get("time_minutes"), int) else None
        ),
        contexts=list(data["contexts"]) if isinstance(data.get("contexts"), list) else None,
        area=_opt_str("area"),
        project_query=_opt_str("project_query"),
        due=_opt_str("due"),
        defer_until=_opt_str("defer_until"),
    )


def recent_action_titles_by_project(
    items: list[Item], projects: list[Project], per_project: int = 3
) -> dict[str, list[str]]:
    """Group recent item titles by project id, capped at `per_project` per project."""
    project_ids = {p.id for p in projects}
    grouped: dict[str, list[str]] = {pid: [] for pid in project_ids}
    for item in items:
        if item.project in project_ids and len(grouped[item.project]) < per_project:
            grouped[item.project].append(item.title)
    return grouped
