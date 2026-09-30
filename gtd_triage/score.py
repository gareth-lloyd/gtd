"""Turn Jev's answers into attention, uncertainty, dive priority and a band.

Answers are plain dicts as `jev_client` returns them:

  {"awaiting_me": {"noul": 0.8},
   "deadline": {"choice": "today", "confidence": 0.7, "probabilities": {...}},
   "stakes": {"score": 1.9, "confidence": 0.6, "probabilities": {"0": ...}}}

Jev answers each question independently, so two answers can contradict each
other. That is treated as a signal (it raises `uncertainty`), not an error.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml

from gtd_triage import rules

WEIGHTS_PATH = Path(__file__).with_name("weights.yml")
STAKES_MAX = 3.0

Answers = dict[str, dict[str, Any]]


@dataclass
class Scored:
    attention: float
    uncertainty: float
    dive_priority: float
    band: str
    features: dict[str, float]

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        for key in ("attention", "uncertainty", "dive_priority"):
            out[key] = round(out[key], 3)
        out["features"] = {k: round(v, 3) for k, v in self.features.items()}
        return out


def load_weights(path: Path = WEIGHTS_PATH) -> dict[str, Any]:
    return yaml.safe_load(path.read_text())


def _noul(answers: Answers, key: str, default: float = 0.0) -> float:
    return float(answers.get(key, {}).get("noul", default))


def _probabilities(answers: Answers, key: str) -> dict[str, float]:
    return {str(k): float(v) for k, v in (answers.get(key, {}).get("probabilities") or {}).items()}


def kind_key(item: dict[str, Any]) -> str:
    return f"{item.get('source')}:{item.get('kind')}"


def kind_prior(item: dict[str, Any], weights: dict[str, Any]) -> float:
    """Log-odds that I act on an item of this kind, from history. It costs no
    model call, and Jev's answers are fitted on top of it, so the weights on
    Jev's features measure what Jev adds beyond the kind."""
    table = weights.get("kind_prior") or {}
    return float(table.get(kind_key(item), table.get("default", 0.0)))


def features(item: dict[str, Any], answers: Answers, weights: dict[str, Any]) -> dict[str, float]:
    deadline = _probabilities(answers, "deadline")
    disposition = _probabilities(answers, "disposition")
    proximity = weights["deadline_proximity"]
    account = _probabilities(answers, "key_account")
    key_account = 1.0 - account["none"] if "none" in account else 0.0
    if rules.key_account_by_rule(item):
        key_account = 1.0
    return {
        "awaiting_me": _noul(answers, "awaiting_me"),
        "addressed_to_me": _noul(answers, "addressed_to_me"),
        "already_handled": _noul(answers, "already_handled"),
        "automated": _noul(answers, "automated"),
        "stakes": float(answers.get("stakes", {}).get("score", 0.0)) / STAKES_MAX,
        "deadline": sum(p * proximity.get(option, 0.0) for option, p in deadline.items()),
        "key_account": key_account,
        "ent_serious": _noul(answers, "ent_serious"),
        # Jev's direct answer is overconfident alone but adds to the atoms.
        "disp_actionable": disposition.get("actionable", 0.0),
        "disp_aware": disposition.get("aware", 0.0),
        "disp_noise": disposition.get("noise", 0.0),
        "kind_prior": kind_prior(item, weights),
    }


def attention(feats: dict[str, float], weights: dict[str, Any]) -> float:
    w = weights["attention"]
    z = w["bias"] + sum(w.get(name, 0.0) * value for name, value in feats.items())
    return 1.0 / (1.0 + math.exp(-z))


def uncertainty(answers: Answers) -> float:
    """0..1. Half how spread the direct disposition is, half how far it
    disagrees with the `awaiting_me` atom."""
    disposition = _probabilities(answers, "disposition")
    if not disposition:
        return 1.0
    entropy = -sum(p * math.log(p) for p in disposition.values() if p > 0)
    spread = entropy / math.log(len(disposition))
    # `cannot_tell` is Jev saying so directly; count it in full.
    spread = max(spread, disposition.get("cannot_tell", 0.0))
    disagreement = abs(disposition.get("actionable", 0.0) - _noul(answers, "awaiting_me"))
    return min(1.0, 0.5 * spread + 0.5 * disagreement)


def band(
    item: dict[str, Any],
    feats: dict[str, float],
    attention_value: float,
    uncertainty_value: float,
    weights: dict[str, Any],
) -> str:
    """`act`, `know` or `check`. A band sets how much of the item the LLM reads;
    it never removes the item from the report."""
    b = weights["bands"]
    rule = rules.rule_disposition(item)
    if rule == "actionable":
        return "act"
    if rules.is_interview_pr(item):
        return "know"
    certain = uncertainty_value <= b["max_uncertainty"]
    key_account = feats["key_account"] >= b["key_account_threshold"]
    quiet = (
        attention_value <= b["know_attention"]
        and feats["awaiting_me"] <= b["know_max_awaiting"]
        and not key_account
        and item.get("kind") not in rules.NEVER_KNOW_KINDS
    )
    if rule == "aware":
        # Never an inbox item, but a loud one is still read in full.
        return "know" if quiet else "check"
    if certain and attention_value >= b["act_attention"]:
        return "act"
    if certain and quiet:
        return "know"
    return "check"


def dive_priority(
    item: dict[str, Any],
    answers: Answers,
    feats: dict[str, float],
    uncertainty_value: float,
    weights: dict[str, Any],
) -> float:
    """How much a thread read could change what happens to the item.

    A dive is worth most where a capture hangs on it: a pending reply whose
    item carries no thread, so nobody can tell whether I already answered. It
    is worth least on kinds that never reach the inbox, where only an ENT
    triage ticket of unclear seriousness earns one.
    """
    if not rules.can_dive(item):
        return 0.0
    d = weights["dives"]
    rule = rules.rule_disposition(item)
    if rule == "aware":
        serious = _noul(answers, "ent_serious", 0.0)
        return 1.0 - abs(2.0 * serious - 1.0) if "ent_serious" in answers else 0.0
    priority = (1.0 - _noul(answers, "context_sufficient", 0.5)) + uncertainty_value
    priority += d["key_account_bonus"] * feats["key_account"]
    unverified = str(item.get("kind") or "").endswith("_pending_reply") and not item.get("context")
    if unverified:
        priority += d["unverified_ask_bonus"]
    return priority


def score_item(item: dict[str, Any], answers: Answers, weights: dict[str, Any]) -> Scored:
    feats = features(item, answers, weights)
    attention_value = attention(feats, weights)
    uncertainty_value = uncertainty(answers)
    dive = dive_priority(item, answers, feats, uncertainty_value, weights)
    return Scored(
        attention=attention_value,
        uncertainty=uncertainty_value,
        dive_priority=dive,
        band=band(item, feats, attention_value, uncertainty_value, weights),
        features=feats,
    )
