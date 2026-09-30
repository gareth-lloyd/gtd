"""Offline replay of the pipeline over labelled history. The go/no-go gate.

Reads `labels.jsonl` (run `gtd_triage.labels` first), asks Jev about each
item once (answers are cached, so re-runs are free), and reports on the
August-September test split:

  - how well Jev's direct `disposition` and the composite `attention` separate
    items that were acted on from items that were not (AUC, reliability table)
  - for each `know` threshold: how much of the morning it would shrink, and
    which acted-on items it would have shrunk by mistake

Human labels (`promoted`, `overcaptured`) are scored separately. The rest are
`/gtd`'s own LLM calls, so matching them shows consistency, not correctness.

Gate: some threshold bands at least 40% of test items `know`, misplaces at
most 1% of acted-on items, and misplaces no promoted item.

Usage:
  uv run python -m gtd_triage.evaluate --rules-only       # no API key needed
  uv run python -m gtd_triage.evaluate --limit 50
  uv run python -m gtd_triage.evaluate [--fit]
"""

from __future__ import annotations

import argparse
import math
import random
import sys
from collections import Counter
from typing import Any

from gtd_triage import rules
from gtd_triage.jev_client import JevUnavailableError, ask_jev
from gtd_triage.labels import ACTED_ON_LABELS, LabelRow, load_rows
from gtd_triage.paths import ANSWERS_CACHE
from gtd_triage.score import band, features, kind_key, kind_prior, load_weights, score_item

TEST_FROM = "2026-08-01"
PRICE_PER_MTOK = 0.042
GATE_MIN_KNOW_SHARE = 0.40
GATE_MAX_ACTED_MISPLACED = 0.01
KNOW_THRESHOLDS = (0.01, 0.015, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1, 0.15, 0.2, 0.3)
FIT_FEATURES = (
    "awaiting_me",
    "addressed_to_me",
    "stakes",
    "deadline",
    "key_account",
    "ent_serious",
    "already_handled",
    "automated",
    "disp_actionable",
    "disp_aware",
    "disp_noise",
    "kind_prior",
)
# Pseudo-count pulling a rare kind's acted-on rate towards the overall rate.
KIND_PRIOR_SMOOTHING = 5


def acted_on(row: LabelRow) -> bool:
    return row.label in ACTED_ON_LABELS


def auc(scores: list[float], positives: list[bool]) -> float:
    """Probability a random acted-on item outranks a random other item."""
    ranked = sorted(zip(scores, positives, strict=True), key=lambda pair: pair[0])
    n_pos = sum(positives)
    n_neg = len(positives) - n_pos
    if not n_pos or not n_neg:
        return float("nan")
    rank_sum, i = 0.0, 0
    while i < len(ranked):
        j = i
        while j < len(ranked) and ranked[j][0] == ranked[i][0]:
            j += 1
        mean_rank = (i + 1 + j) / 2
        rank_sum += mean_rank * sum(1 for k in range(i, j) if ranked[k][1])
        i = j
    return (rank_sum - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg)


def reliability(scores: list[float], positives: list[bool], bins: int = 5) -> list[str]:
    lines = []
    for b in range(bins):
        low, high = b / bins, (b + 1) / bins
        inside = [
            (s, p)
            for s, p in zip(scores, positives, strict=True)
            if low <= s < high or (b == bins - 1 and s == 1.0)
        ]
        if not inside:
            continue
        predicted = sum(s for s, _ in inside) / len(inside)
        observed = sum(p for _, p in inside) / len(inside)
        lines.append(
            f"    {low:.1f}-{high:.1f}  n={len(inside):5}  "
            f"predicted={predicted:.2f}  acted-on={observed:.2f}"
        )
    return lines


def fit_logistic(
    rows: list[dict[str, float]], targets: list[bool], epochs: int = 400, rate: float = 0.5
) -> dict[str, float]:
    """Plain gradient descent with a small L2 penalty. ~3k rows x 8 features."""
    weights = dict.fromkeys(FIT_FEATURES, 0.0)
    bias = 0.0
    n = len(rows)
    for _ in range(epochs):
        grad = dict.fromkeys(FIT_FEATURES, 0.0)
        grad_bias = 0.0
        for feats, target in zip(rows, targets, strict=True):
            z = bias + sum(weights[name] * feats[name] for name in FIT_FEATURES)
            error = 1.0 / (1.0 + math.exp(-z)) - float(target)
            grad_bias += error
            for name in FIT_FEATURES:
                grad[name] += error * feats[name]
        bias -= rate * grad_bias / n
        for name in FIT_FEATURES:
            weights[name] -= rate * (grad[name] / n + 0.001 * weights[name])
    return {"bias": bias, **weights}


def fit_kind_prior(rows: list[LabelRow]) -> dict[str, float]:
    """Smoothed log-odds of acting on each `source:kind`, plus a `default`."""
    seen: Counter[str] = Counter()
    acted: Counter[str] = Counter()
    for row in rows:
        seen[kind_key(row.item)] += 1
        acted[kind_key(row.item)] += acted_on(row)
    base = sum(acted.values()) / sum(seen.values())

    def log_odds(p: float) -> float:
        return math.log(p / (1.0 - p))

    table = {"default": log_odds(base)}
    for kind, n in sorted(seen.items()):
        rate = (acted[kind] + KIND_PRIOR_SMOOTHING * base) / (n + KIND_PRIOR_SMOOTHING)
        table[kind] = log_odds(rate)
    return table


def report_rules(rows: list[LabelRow]) -> None:
    """What the code-only rules get right and wrong against history. No API."""
    print("\nRules against history (all dates)")
    table: dict[str, Counter[str]] = {}
    for row in rows:
        rule = rules.rule_disposition(row.item) or "judgment"
        if rules.is_interview_pr(row.item):
            rule = "interview_pr"
        table.setdefault(rule, Counter())[row.label] += 1
    labels = ("promoted", "acted", "overcaptured", "aware", "dropped")
    print(f"    {'rule':14}" + "".join(f"{name:>14}" for name in labels))
    for rule, counts in sorted(table.items()):
        print(f"    {rule:14}" + "".join(f"{counts[name]:>14}" for name in labels))
    print(
        "    `aware` rows that were promoted are the rule's misses. `actionable` rows that\n"
        "    were dropped or aware were not captured by `/gtd`: dedup, a dive, or its judgment."
    )


def report_judgment(rows: list[LabelRow], scored: dict[str, Any], weights: dict[str, Any]) -> None:
    """The honest numbers: only kinds no rule decides, against a kind-only
    baseline, and on the one human label there is."""
    judged = [r for r in rows if r.source_id in scored and rules.rule_disposition(r.item) is None]
    positives = [acted_on(r) for r in judged]
    composite = [scored[r.source_id]["scored"].attention for r in judged]
    baseline = [kind_prior(r.item, weights) for r in judged]
    left = [r for r in judged if r.label in ("promoted", "aware", "dropped")]
    promoted = [r.label == "promoted" for r in left]
    left_scores = [scored[r.source_id]["scored"].attention for r in left]
    print(f"  Judgment kinds only: {len(judged)} items, {sum(positives)} acted on")
    print(
        f"    AUC  kind alone={auc(baseline, positives):.3f}  "
        f"composite={auc(composite, positives):.3f}"
    )
    print(
        f"    AUC  promoted ({sum(promoted)}) vs left in awareness or dropped="
        f"{auc(left_scores, promoted):.3f}   (human label: what `/gtd` missed)"
    )


def report_split(name: str, rows: list[LabelRow], scored: dict[str, Any]) -> None:
    judged = [r for r in rows if r.source_id in scored]
    positives = [acted_on(r) for r in judged]
    direct = [
        scored[r.source_id]["answers"]
        .get("disposition", {})
        .get("probabilities", {})
        .get("actionable", 0.0)
        for r in judged
    ]
    composite = [scored[r.source_id]["scored"].attention for r in judged]
    print(f"\n{name}: {len(judged)} items, {sum(positives)} acted on")
    print(
        f"  AUC  direct disposition={auc(direct, positives):.3f}  "
        f"composite={auc(composite, positives):.3f}"
    )
    print("  Reliability of direct p(actionable):")
    print("\n".join(reliability(direct, positives)))
    print("  Reliability of composite attention:")
    print("\n".join(reliability(composite, positives)))


def sweep_know(rows: list[LabelRow], scored: dict[str, Any], weights: dict[str, Any]) -> bool:
    """Threshold sweep on the test split. Returns whether any setting passes the gate."""
    judged = [r for r in rows if r.source_id in scored]
    acted_total = sum(1 for r in judged if acted_on(r))
    print(f"\nKnow-band sweep on the test split ({len(judged)} items, {acted_total} acted on)")
    print(
        "    know_attention  know-share  acted-misplaced  promoted-misplaced  overcaptured-in-know"
    )
    passed = False
    for threshold in KNOW_THRESHOLDS:
        trial = {**weights, "bands": {**weights["bands"], "know_attention": threshold}}
        know = []
        for row in judged:
            entry = scored[row.source_id]["scored"]
            if band(row.item, entry.features, entry.attention, entry.uncertainty, trial) == "know":
                know.append(row)
        share = len(know) / len(judged) if judged else 0.0
        misplaced = sum(1 for r in know if acted_on(r))
        promoted = sum(1 for r in know if r.label == "promoted")
        over = sum(1 for r in know if r.label == "overcaptured")
        rate = misplaced / acted_total if acted_total else 0.0
        ok = share >= GATE_MIN_KNOW_SHARE and rate <= GATE_MAX_ACTED_MISPLACED and promoted == 0
        passed = passed or ok
        print(
            f"    {threshold:>14.3f}  {share:>10.1%}  {misplaced:>6} ({rate:>5.1%})"
            f"  {promoted:>18}  {over:>20}  {'PASS' if ok else ''}"
        )
    return passed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--limit", type=int, help="Replay a random sample of this many items.")
    parser.add_argument("--rules-only", action="store_true", help="Skip Jev entirely.")
    parser.add_argument(
        "--fit", action="store_true", help="Fit attention weights on the tune split."
    )
    args = parser.parse_args(argv)

    rows = load_rows()
    print(f"labelled rows: {len(rows)}  {dict(Counter(r.label for r in rows))}")
    report_rules(rows)
    if args.rules_only:
        return 0

    candidates = [r for r in rows if rules.needs_jev(r.item)]
    if args.limit:
        # Keep every human label: they are rare and the only ground truth.
        random.seed(0)
        human = [r for r in candidates if r.label in ("promoted", "overcaptured")]
        rest = [r for r in candidates if r.label not in ("promoted", "overcaptured")]
        candidates = (human + random.sample(rest, len(rest)))[: args.limit]

    weights = load_weights()
    try:
        run = ask_jev([r.item for r in candidates], weights["model"], cache_path=ANSWERS_CACHE)
    except JevUnavailableError as exc:
        print(f"\nJev unavailable: {exc}", file=sys.stderr)
        return 2
    cost = run.input_tokens / 1_000_000 * PRICE_PER_MTOK
    per_item = run.input_tokens / run.requests if run.requests else 0
    print(
        f"\nJev: {run.requests} requests, {run.cached} cached, {len(run.failed)} failed, "
        f"{run.input_tokens} tokens ({per_item:.0f}/item), ${cost:.3f}"
    )

    tune = [r for r in candidates if r.blob_date < TEST_FROM]
    test = [r for r in candidates if r.blob_date >= TEST_FROM]

    if args.fit:
        fit_rows = [r for r in tune if r.source_id in run.answers]
        weights = {**weights, "kind_prior": fit_kind_prior(fit_rows)}
        fitted = fit_logistic(
            [features(r.item, run.answers[r.source_id], weights) for r in fit_rows],
            [acted_on(r) for r in fit_rows],
        )
        print("\nFitted on the tune split. Paste under `attention:` in weights.yml to adopt:")
        for name, value in fitted.items():
            print(f"  {name}: {value:.2f}")
        print("And this as the top-level `kind_prior:` table:")
        for kind, value in weights["kind_prior"].items():
            print(f'  "{kind}": {value:.2f}')
        weights = {**weights, "attention": fitted}

    scored = {
        r.source_id: {
            "answers": run.answers[r.source_id],
            "scored": score_item(r.item, run.answers[r.source_id], weights),
        }
        for r in candidates
        if r.source_id in run.answers
    }
    report_split("Tune split (before 2026-08-01)", tune, scored)
    report_judgment(tune, scored, weights)
    report_split("Test split (2026-08-01 onward)", test, scored)
    report_judgment(test, scored, weights)
    passed = sweep_know(test, scored, weights)
    print(f"\nGATE: {'PASS' if passed else 'FAIL'}")
    if args.limit:
        print("(sample run: the gate verdict is not meaningful below the full replay)")
    return 0 if passed or args.limit else 1


if __name__ == "__main__":
    raise SystemExit(main())
