"""Triage decisions that need no model.

Everything here is decided by an item's `source`, `kind`, `source_id` or
`facts`. Jev is only asked about what is left.
"""

from __future__ import annotations

import re
from typing import Any

# Kinds whose disposition `/gtd`'s rubric fixes outright.
ALWAYS_ACTIONABLE_KINDS = frozenset(
    {"dm_pending_reply", "mention_pending_reply", "review_personal", "mine_action_needed"}
)
NEVER_INBOX_KINDS = frozenset({"review_team_only", "ent_triage"})
# Kinds I act on too often for a quiet score to be trusted: 58% of Slack saved
# items and every morning-brief priority in the April-July history.
NEVER_KNOW_KINDS = frozenset({"saved", "brief_priority"})
# Never worth a thread read: the breadth facts already settle them.
NO_DIVE_KINDS = frozenset({"review_team_only", "mine_in_flight"})

# Mock code-review PRs opened for interview candidates. Awareness only.
INTERVIEWS_ORG = "canary-technologies-corp-interviews"

KEY_ACCOUNT_CHANNELS = frozenset({"#wyndham", "#best-western", "#ihg", "#epd-enterprise"})
KEY_ACCOUNT_RE = re.compile(
    r"\b(wyndham|best\s*western|bwh|ihg|holiday inn|intercontinental|kimpton)\b", re.IGNORECASE
)

# Same object-identity patterns `capture_items.py` dedups on, so one Linear
# issue or pull request yields one line however many notifications it produced.
LINEAR_ID_RE = re.compile(r"\b([A-Z]{2,5}-\d{3,6})\b")
PR_URL_RE = re.compile(r"https?://github\.com/([^/\s]+/[^/\s]+)/pull/(\d+)")

CREDENTIAL_RES = (
    re.compile(r"xox[abeoprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"lin_(?:api|oauth)_[A-Za-z0-9]{16,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._~+/-]{20,}=*"),
    re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
)
REDACTED = "[redacted-credential]"

SECTION_BY_KIND = {
    "review_team_only": "Team review queue",
    "review_personal": "Team review queue",
    "mine_in_flight": "My PRs in flight",
    "mine_action_needed": "My PRs in flight",
    "ent_triage": "ENT triage watch",
    "saved": "Saved-for-context",
    "missed_yesterday": "Missed yesterday",
}
SECTION_BY_SOURCE = {
    "slack": "Slack highlights",
    "linear": "Linear watching",
    "github": "My PRs in flight",
    "gmail": "Email",
    "notion": "Morning brief",
}
SECTION_ORDER = (
    "Missed yesterday",
    "Slack highlights",
    "Linear watching",
    "ENT triage watch",
    "My PRs in flight",
    "Team review queue",
    "Email",
    "Morning brief",
    "Saved-for-context",
    "Other",
)


def is_interview_pr(item: dict[str, Any]) -> bool:
    return f"github.com/{INTERVIEWS_ORG}/" in (item.get("source_id") or "")


def rule_disposition(item: dict[str, Any]) -> str | None:
    """`actionable`, `aware`, or None when the rubric leaves it to judgment."""
    if is_interview_pr(item):
        return "aware"
    kind = item.get("kind")
    if kind in NEVER_INBOX_KINDS:
        return "aware"
    if kind in ALWAYS_ACTIONABLE_KINDS:
        return "actionable"
    return None


def needs_jev(item: dict[str, Any]) -> bool:
    """Interview PRs are settled and unranked; everything else gets scored."""
    return not is_interview_pr(item)


def can_dive(item: dict[str, Any]) -> bool:
    return item.get("kind") not in NO_DIVE_KINDS and not is_interview_pr(item)


def section_for(item: dict[str, Any]) -> str:
    kind = item.get("kind") or ""
    if kind in SECTION_BY_KIND:
        return SECTION_BY_KIND[kind]
    return SECTION_BY_SOURCE.get(item.get("source") or "", "Other")


def key_account_by_rule(item: dict[str, Any]) -> bool:
    """A key-account signal readable without a model. Jev's answer is OR-ed in."""
    facts = item.get("facts") or {}
    if facts.get("channel") in KEY_ACCOUNT_CHANNELS:
        return True
    text = f"{item.get('title') or ''} {item.get('snippet') or ''}"
    return bool(KEY_ACCOUNT_RE.search(text))


def saved_facts(item: dict[str, Any], my_slack_id: str) -> dict[str, bool]:
    """Facts about a Slack saved item, computed when the blob lacks them."""
    facts = item.get("facts") or {}
    channel_id = str(facts.get("channel_id") or "")
    text = f"{item.get('snippet') or ''} {item.get('context') or ''}"
    return {
        "is_dm": bool(facts.get("is_dm", channel_id.startswith("D"))),
        "is_self_save": bool(facts.get("is_self_save", facts.get("from_id") == my_slack_id)),
        "mentions_me": bool(facts.get("mentions_me", f"<@{my_slack_id}>" in text)),
    }


def cluster_key(item: dict[str, Any]) -> str:
    """Identity of the object an item is about. Falls back to its own source_id."""
    source_id = item.get("source_id") or ""
    pr = PR_URL_RE.search(source_id)
    if pr:
        return f"pr:{pr.group(1)}/{pr.group(2)}"
    if item.get("source") == "linear":
        issue = LINEAR_ID_RE.search(f"{source_id} {item.get('title') or ''}")
        if issue:
            return f"linear:{issue.group(1)}"
    return source_id


def scrub(value: Any) -> Any:
    """Strip credential-shaped strings from every string inside `value`."""
    if isinstance(value, str):
        for pattern in CREDENTIAL_RES:
            value = pattern.sub(REDACTED, value)
        return value
    if isinstance(value, list):
        return [scrub(v) for v in value]
    if isinstance(value, dict):
        return {k: scrub(v) for k, v in value.items()}
    return value
