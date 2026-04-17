"""AI-powered capture — unstructured text → structured Item via Claude CLI."""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from datetime import date

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
    """
    claude_path = shutil.which("claude")
    if not claude_path:
        raise AiCaptureNotConfiguredError(
            "claude CLI not found on PATH — install Claude Code to use AI capture"
        )

    prompt = _build_prompt(
        text=text, cfg=cfg, projects=projects,
        sample_actions=sample_actions, today=today,
    )

    cmd = [claude_path, "-p", prompt]
    if model:
        cmd.extend(["--model", model])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired as err:
        raise AiCaptureUpstreamError("Claude CLI timed out after 30s") from err

    if result.returncode != 0:
        stderr = result.stderr.strip()
        raise AiCaptureUpstreamError(
            f"Claude CLI failed (exit {result.returncode}): {stderr or result.stdout.strip()}"
        )

    raw = result.stdout.strip()
    return _parse_response(raw)


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
            "- When a project matches, phrase the title to fit that project's recent-action "
            "style.",
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


def _parse_response(raw: str) -> AiCaptureResult:
    # Strip markdown code fences if the model wraps in ```json ... ```
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
            f"AI did not return valid JSON; try again or use Regular capture. Raw: {raw[:200]}"
        ) from err

    if not isinstance(data, dict) or "title" not in data:
        raise AiCaptureNoExtractionError(
            "AI response missing required 'title' field; try again or use Regular capture"
        )

    return _result_from_dict(data)


def _result_from_dict(data: dict) -> AiCaptureResult:
    def _opt_str(key: str) -> str | None:
        value = data.get(key)
        if value is None:
            return None
        value = str(value).strip()
        return value or None

    return AiCaptureResult(
        title=str(data["title"]).strip(),
        summary=str(data.get("summary", f"Added \"{data['title']}\" to inbox")).strip(),
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
