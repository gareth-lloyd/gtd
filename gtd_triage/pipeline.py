"""The `/gtd2` pipeline. Three commands, called in order by the skill:

  triage    blob -> rules -> Jev -> score -> cluster -> bands. Prints the LLM view.
  rescore   fold the LLM's dive summaries into their items and ask Jev again.
  finish    take the LLM's inbox items, dry-run them through `capture_items.py`,
            and write the awareness report from everything else.

Compare mode only: nothing here writes to the GTD inbox or to any source.
Jev never removes an item. Whatever it says, every fetched `source_id` ends
up in exactly one of would-capture or the awareness index.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any

from gtd_triage import render, rules
from gtd_triage.jev_client import JevRun, JevUnavailableError, ask_jev
from gtd_triage.paths import CAPTURE_SCRIPT, GTD2_OUTPUT, GTD_ROOT, GTD_SKILL_OUTPUT
from gtd_triage.score import load_weights, score_item

BAND_RANK = {"act": 2, "check": 1, "know": 0}


def _fallback_band(item: dict[str, Any]) -> str:
    """Without Jev the LLM reads everything the rules do not settle."""
    if rules.rule_disposition(item) == "actionable":
        return "act"
    return "know" if rules.is_interview_pr(item) else "check"


def build_entry(
    item: dict[str, Any], answers: dict[str, Any] | None, weights: dict[str, Any]
) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "source_id": item["source_id"],
        "source": item.get("source"),
        "kind": item.get("kind"),
        "section": rules.section_for(item),
        "cluster": rules.cluster_key(item),
        "rule": rules.rule_disposition(item),
        "item": item,
    }
    if answers is None:
        entry.update(band=_fallback_band(item), attention=None, uncertainty=None, dive_priority=0.0)
        return entry
    scored = score_item(item, answers, weights).to_dict()
    entry.update(scored, answers=answers)
    return entry


def merge_duplicates(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """One item per source_id. A blob can carry two notifications for the same
    URL (a Linear issue both `subscribed` and `status_change`); keep the one the
    rules care about most, then the one with the most thread context."""
    best: dict[str, dict[str, Any]] = {}
    for item in items:
        current = best.get(item["source_id"])
        if current is None:
            best[item["source_id"]] = item
            continue
        rank = (rules.rule_disposition(item) == "actionable", len(item.get("context") or []))
        held = (rules.rule_disposition(current) == "actionable", len(current.get("context") or []))
        if rank > held:
            best[item["source_id"]] = item
    return list(best.values())


def fold_clusters(entries: list[dict[str, Any]]) -> None:
    """One line per object: the strongest member speaks for its cluster."""
    clusters: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        clusters.setdefault(entry["cluster"], []).append(entry)
    for members in clusters.values():
        if len(members) == 1:
            continue
        members.sort(
            key=lambda e: (e["rule"] == "actionable", BAND_RANK[e["band"]], e["attention"] or 0.0),
            reverse=True,
        )
        head, rest = members[0], members[1:]
        head["also"] = [e["source_id"] for e in rest]
        for entry in rest:
            entry["folded_into"] = head["source_id"]


def pick_dives(entries: list[dict[str, Any]], budget: int) -> list[str]:
    candidates = [e for e in entries if not e.get("folded_into") and e["dive_priority"] > 0]
    candidates.sort(key=lambda e: e["dive_priority"], reverse=True)
    return [e["source_id"] for e in candidates[:budget]]


def order_entries(entries: list[dict[str, Any]]) -> None:
    entries.sort(key=lambda e: (-BAND_RANK[e["band"]], -(e["attention"] or 0.0)))


def jev_status(run: JevRun | None, reason: str | None) -> dict[str, Any]:
    if run is None:
        return {"status": "fallback", "reason": reason}
    return {
        "status": "ok",
        "requests": run.requests,
        "cached": run.cached,
        "input_tokens": run.input_tokens,
        "failed": run.failed,
    }


def run_triage(
    blob: dict[str, Any], weights: dict[str, Any], use_jev: bool = True
) -> dict[str, Any]:
    items = merge_duplicates([i for i in blob.get("items") or [] if i.get("source_id")])
    run: JevRun | None = None
    reason: str | None = "disabled with --no-jev"
    if use_jev:
        try:
            run = ask_jev([i for i in items if rules.needs_jev(i)], weights["model"])
        except JevUnavailableError as exc:
            reason = str(exc)
    answers = run.answers if run else {}
    entries = [build_entry(item, answers.get(item["source_id"]), weights) for item in items]
    fold_clusters(entries)
    order_entries(entries)
    budget = weights["dives"]["budget"]
    return {
        "date": date.today().isoformat(),
        "model": weights["model"],
        "jev": jev_status(run, reason),
        "coverage": blob.get("coverage"),
        "errors": blob.get("errors") or [],
        "dive_budget": budget,
        "dive_candidates": pick_dives(entries, budget),
        "entries": entries,
    }


def apply_dives(
    triage: dict[str, Any], dives: list[dict[str, Any]], weights: dict[str, Any]
) -> list[dict[str, Any]]:
    """Re-score dived items with the dive summary inside the item Jev sees."""
    by_id = {e["source_id"]: e for e in triage["entries"]}
    dived = []
    for dive in dives:
        entry = by_id.get(dive.get("source_id"))
        if entry is None:
            print(f"dive for unknown source_id skipped: {dive.get('source_id')}", file=sys.stderr)
            continue
        entry["dive"] = dive.get("summary") or ""
        entry["item"] = {**entry["item"], "thread_summary_from_dive": entry["dive"]}
        dived.append(entry)
    if triage["jev"]["status"] != "ok" or not dived:
        return dived
    try:
        run = ask_jev([e["item"] for e in dived if rules.needs_jev(e["item"])], weights["model"])
    except JevUnavailableError as exc:
        print(f"rescore skipped, Jev unavailable: {exc}", file=sys.stderr)
        return dived
    for entry in dived:
        answers = run.answers.get(entry["source_id"])
        if answers is None:
            continue
        kept = {k: entry[k] for k in ("also", "folded_into", "dive") if k in entry}
        entry.update(build_entry(entry["item"], answers, weights), **kept)
    triage["jev"]["requests"] += run.requests
    triage["jev"]["input_tokens"] += run.input_tokens
    order_entries(triage["entries"])
    return dived


def dry_run_capture(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Receipts from `/gtd`'s own capture script in --dry-run. Writes nothing."""
    if not items:
        return []
    result = subprocess.run(
        [sys.executable, str(CAPTURE_SCRIPT), "--env", "work", "--dry-run"],
        input=json.dumps(items),
        capture_output=True,
        text=True,
        cwd=GTD_ROOT,
        check=False,
    )
    if result.returncode not in (0, 1):
        raise RuntimeError(f"capture_items.py --dry-run failed: {result.stderr.strip()}")
    return [json.loads(line) for line in result.stdout.splitlines() if line.strip()]


def check_coverage(
    triage: dict[str, Any], captured: set[str], index: list[dict[str, Any]]
) -> list[str]:
    """source_ids that are not in exactly one of would-capture or the index."""
    in_index: set[str] = set()
    for entry in index:
        in_index.add(entry["source_id"])
        in_index.update(entry["also_source_ids"])
    folded_under_capture = {
        e["source_id"] for e in triage["entries"] if e.get("folded_into") in captured
    }
    problems = []
    for entry in triage["entries"]:
        source_id = entry["source_id"]
        places = (
            (source_id in captured) + (source_id in in_index) + (source_id in folded_under_capture)
        )
        if places != 1:
            problems.append(f"{source_id} appears {places} times")
    return problems


def _triage_path(out_dir: Path, day: str) -> Path:
    return out_dir / f"{day}-triage.json"


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2))


def cmd_triage(args: argparse.Namespace) -> int:
    weights = load_weights()
    blob = json.loads(Path(args.blob).read_text())
    fetched = str(blob.get("fetched_at") or "")[:10]
    if fetched != date.today().isoformat() and not args.allow_stale:
        print(f"breadth blob is from {fetched or 'an unknown date'}, not today. Run /gtd first.")
        return 2
    triage = run_triage(blob, weights, use_jev=not args.no_jev)
    args.out.mkdir(parents=True, exist_ok=True)
    _write_json(_triage_path(args.out, triage["date"]), triage)
    sys.stdout.write(render.llm_view(triage))
    return 0


def cmd_rescore(args: argparse.Namespace) -> int:
    weights = load_weights()
    path = _triage_path(args.out, date.today().isoformat())
    triage = json.loads(path.read_text())
    dives = json.loads(Path(args.dives).read_text())
    dived = apply_dives(triage, dives, weights)
    triage["dives"] = dives
    _write_json(path, triage)
    for entry in dived:
        attention = entry.get("attention")
        score = f"{attention:.2f}" if attention is not None else "n/a"
        print(f"- {entry['band']} att={score} <{entry['source_id']}>")
    return 0


def cmd_finish(args: argparse.Namespace) -> int:
    day = date.today().isoformat()
    triage = json.loads(_triage_path(args.out, day).read_text())
    decided = json.loads(Path(args.items).read_text())
    items, notes, tldr = decided.get("items") or [], decided.get("notes") or {}, decided["tldr"]

    known = {e["source_id"] for e in triage["entries"]}
    unknown = [i.get("source_id") for i in items if i.get("source_id") not in known]
    if unknown:
        print(f"items with a source_id not in today's triage: {unknown}", file=sys.stderr)
        return 2

    receipts = dry_run_capture(items)
    captured = {i["source_id"] for i in items}
    index = render.awareness_index(triage, captured, notes)
    problems = check_coverage(triage, captured, index)

    _write_json(args.out / f"{day}-would-capture.json", {"items": items, "receipts": receipts})
    _write_json(args.out / f"{day}-awareness-index.json", index)
    report = args.out / f"{day}-awareness.md"
    report.write_text(render.awareness_markdown(triage, index, tldr))

    summary = next((r["summary"] for r in receipts if "summary" in r), {})
    print(f"would-capture: {len(items)} items, dry-run receipts {summary}")
    print(f"awareness: {len(index)} entries -> {report}")
    if problems:
        print(f"COVERAGE CHECK FAILED ({len(problems)}):", *problems[:10], sep="\n  ")
        return 1
    print(f"coverage check ok: all {len(known)} source_ids accounted for exactly once")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--out", type=Path, default=GTD2_OUTPUT)
    commands = parser.add_subparsers(dest="command", required=True)

    triage = commands.add_parser("triage")
    triage.add_argument("--blob", default=str(GTD_SKILL_OUTPUT / "latest-breadth.json"))
    triage.add_argument("--no-jev", action="store_true", help="Force the LLM-only fallback.")
    triage.add_argument("--allow-stale", action="store_true", help="Accept an older blob.")
    triage.set_defaults(func=cmd_triage)

    rescore = commands.add_parser("rescore")
    rescore.add_argument("--dives", required=True, help="JSON list of {source_id, summary}.")
    rescore.set_defaults(func=cmd_rescore)

    finish = commands.add_parser("finish")
    finish.add_argument("--items", required=True, help="JSON {items, notes, tldr}.")
    finish.set_defaults(func=cmd_finish)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
