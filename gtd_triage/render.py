"""Text the pipeline produces: the LLM's working view and the awareness report."""

from __future__ import annotations

import json
from typing import Any

from gtd_triage import rules

SNIPPET_CHARS = 160
FALLBACK_TEMPLATE = {
    "title_verb": "Read",
    "contexts": ["consume"],
    "energy": "low",
    "time_minutes": 5,
}
ABSTAIN = frozenset({"Other", "other", "unknown"})


def one_line(text: str | None, limit: int = SNIPPET_CHARS) -> str:
    flat = " ".join((text or "").split())
    return flat if len(flat) <= limit else flat[: limit - 1].rstrip() + "…"


def default_template(answers: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Promotion defaults from Jev's answers, falling back where it abstained."""

    def pick(key: str) -> str | None:
        choice = answers.get(key, {}).get("choice")
        return None if choice is None or choice in ABSTAIN else choice

    context = pick("contexts")
    minutes = pick("time")
    return {
        "title_verb": pick("title_verb") or FALLBACK_TEMPLATE["title_verb"],
        "contexts": [context] if context else FALLBACK_TEMPLATE["contexts"],
        "energy": pick("energy") or FALLBACK_TEMPLATE["energy"],
        "time_minutes": int(minutes) if minutes else FALLBACK_TEMPLATE["time_minutes"],
    }


def _full(entry: dict[str, Any]) -> str:
    item = entry["item"]
    view = {
        "source_id": entry["source_id"],
        "kind": entry["kind"],
        "title": item.get("title"),
        "snippet": item.get("snippet"),
        "context": item.get("context"),
        "facts": item.get("facts"),
        "ts": item.get("ts"),
    }
    for key in ("attention", "uncertainty", "rule", "also", "dive"):
        if entry.get(key) not in (None, [], ""):
            view[key] = entry[key]
    if entry.get("answers"):
        view["defaults"] = default_template(entry["answers"])
    return json.dumps(view, ensure_ascii=False, separators=(",", ":"))


def _brief(entry: dict[str, Any]) -> str:
    attention = entry.get("attention")
    score = f" att={attention:.2f}" if attention is not None else ""
    return (
        f"- [{entry['kind']}]{score} {one_line(entry['item'].get('title'), 90)}"
        f" — {one_line(entry['item'].get('snippet'), 110)} <{entry['source_id']}>"
    )


def coverage_line(triage: dict[str, Any]) -> str:
    jev = triage["jev"]
    if jev["status"] == "ok":
        jev_text = (
            f"jev {triage['model']} ok ({jev['requests']} requests, {jev['cached']} cached, "
            f"{jev['input_tokens']} tokens, {len(jev['failed'])} failed)"
        )
    else:
        jev_text = f"JEV FALLBACK ({jev['reason']}): every item was read in full by the LLM"
    coverage = triage.get("coverage") or {}
    sources = " · ".join(
        f"{name} {info.get('items', 0)}"
        + (f" ({info['errors']} errors)" if info.get("errors") else "")
        for name, info in coverage.items()
    )
    errors = " · ".join(f'"{e}"' for e in triage.get("errors") or [])
    return " · ".join(part for part in (sources, jev_text, errors) if part)


def llm_view(triage: dict[str, Any]) -> str:
    """What the skill prompt reads: `act` and `check` in full, `know` one line each."""
    entries = [e for e in triage["entries"] if not e.get("folded_into")]
    by_band = {name: [e for e in entries if e["band"] == name] for name in ("act", "check", "know")}
    lines = [
        f"# gtd2 triage {triage['date']}",
        f"Coverage: {coverage_line(triage)}",
        f"Items: {len(triage['entries'])} fetched, {len(entries)} after clustering.",
        "",
        f"## ACT ({len(by_band['act'])}): write an inbox item for each unless a dive or "
        "the thread shows it is already handled",
        *[_full(e) for e in by_band["act"]],
        "",
        f"## CHECK ({len(by_band['check'])}): judge each one: inbox item, or leave for awareness",
        *[_full(e) for e in by_band["check"]],
        "",
        f"## KNOW ({len(by_band['know'])}): awareness only. Skim; promote only with a reason",
        *[_brief(e) for e in by_band["know"]],
        "",
        f"## DIVE CANDIDATES (budget {triage['dive_budget']}, highest priority first)",
        *[
            f"- dive={e['dive_priority']:.2f} [{e['kind']}] {one_line(e['item'].get('title'), 90)}"
            f" <{e['source_id']}>"
            for e in sorted(entries, key=lambda e: -e["dive_priority"])
            if e["source_id"] in triage["dive_candidates"]
        ],
    ]
    return "\n".join(lines) + "\n"


def awareness_index(
    triage: dict[str, Any], captured: set[str], notes: dict[str, str]
) -> list[dict[str, Any]]:
    """Every clustered entry that is not being captured, numbered in report order."""
    remaining = [
        e for e in triage["entries"] if not e.get("folded_into") and e["source_id"] not in captured
    ]
    order = {name: i for i, name in enumerate(rules.SECTION_ORDER)}
    remaining.sort(
        key=lambda e: (order.get(e["section"], len(order)), -(e.get("attention") or 0.0))
    )
    index = []
    for n, entry in enumerate(remaining, start=1):
        item = entry["item"]
        index.append(
            {
                "n": n,
                "section": entry["section"],
                "title": one_line(item.get("title"), 120),
                "line": notes.get(entry["source_id"]) or one_line(item.get("snippet")),
                "url": entry["source_id"],
                "source": entry["source"],
                "source_id": entry["source_id"],
                "also_source_ids": entry.get("also") or [],
                "band": entry["band"],
                "attention": entry.get("attention"),
                "force": False,
                "default_template": default_template(entry.get("answers") or {}),
            }
        )
    return index


def awareness_markdown(triage: dict[str, Any], index: list[dict[str, Any]], tldr: str) -> str:
    lines = [
        f"# Morning awareness (gtd2) — {triage['date']}",
        "",
        f"> **TL;DR:** {tldr}",
        "",
        f"> **Coverage:** {coverage_line(triage)}",
        "",
        "> Compare mode: nothing was captured and no Linear notification was marked read.",
    ]
    section = None
    for entry in index:
        if entry["section"] != section:
            section = entry["section"]
            lines += ["", f"## {section}"]
        attention = entry["attention"]
        score = f" `{attention:.2f}`" if attention is not None else ""
        extra = f" (+{len(entry['also_source_ids'])} related)" if entry["also_source_ids"] else ""
        lines.append(
            f"{entry['n']}. [{entry['title']}]({entry['url']}){score} — {entry['line']}{extra}"
        )
    return "\n".join(lines) + "\n"
