"""The typed questions Jev is asked about one breadth item.

Questions are atomic, observable facts. The decision is computed from them in
`score.py`, so priorities change by editing `weights.yml`, not these prompts.
Jev answers every question it is sent whether or not it applies, so questions
that only make sense for one source are gated here in code.

Specs are plain dicts (`type`, `instructions`, `criteria`) so this module and
its tests need no SDK. `jev_client` turns them into SDK question objects.
"""

from __future__ import annotations

from typing import Any

# Bump when any instruction or criteria text changes: cached answers are keyed
# on it, and thresholds in weights.yml were tuned against it.
QUESTIONS_VERSION = "1"

ME = {
    "name": "Gareth Lloyd",
    "role": "Engineering lead for the Enterprise (ENT) team at Canary Technologies",
    "slack_user_id": "U04MQUC8WUW",
    "slack_handle": "glloyd",
    "github_login": "gareth-lloyd",
}

QuestionSpec = dict[str, Any]

TIME_OPTIONS = (5, 10, 15, 20, 60, 90)
GTD_CONTEXTS = ("deep", "craft", "react", "consume", "autopilot", "listen", "fun")

_PREAMBLE = (
    "`state.item` is one notification from the work inbox of the person in `state.me`. "
    "'Me' means that person. "
)


def _noul(instructions: str, true: str, false: str) -> QuestionSpec:
    return {
        "type": "noul",
        "instructions": _PREAMBLE + instructions,
        "criteria": {"true": true, "false": false},
    }


def _choice(instructions: str, criteria: dict[str, str]) -> QuestionSpec:
    return {"type": "choice", "instructions": _PREAMBLE + instructions, "criteria": criteria}


def _score(instructions: str, levels: list[str]) -> QuestionSpec:
    return {"type": "score", "instructions": _PREAMBLE + instructions, "criteria": levels}


CORE: dict[str, QuestionSpec] = {
    "addressed_to_me": _noul(
        "Is the item aimed at me personally?",
        true="It names me, @-mentions me, is a direct message to me, or is assigned to me.",
        false="It is aimed at a channel, a team, or somebody else.",
    ),
    "awaiting_me": _noul(
        "Is somebody waiting on me to do something?",
        true="A person is waiting for my reply, my review, my decision or my work.",
        false="Nobody is waiting on me; it is information, or the ask is for someone else.",
    ),
    "already_handled": _noul(
        "Does the item show that the matter is already dealt with?",
        true="I already replied, or it is resolved, merged, closed, done or answered by others.",
        false="It is still open, or the item does not say.",
    ),
    "automated": _noul(
        "Was the item produced by a machine with no human asking for anything?",
        true="A bot post, digest, alert, status notification or automated reminder.",
        false="A person wrote it.",
    ),
    "context_sufficient": _noul(
        "Does the item itself contain enough to tell what, if anything, is wanted from me?",
        true="The actual message or ask is present in the item text.",
        false="It only points at a thread, ticket or document that would have to be opened.",
    ),
    "deadline": _choice(
        "When must this be dealt with, going only by dates or urgency stated in the item?",
        {
            "today": "Due today, overdue, or explicitly urgent.",
            "this_week": "Due within about a week.",
            "later": "A date further out is stated.",
            "none_stated": "No deadline or urgency is stated.",
        },
    ),
    "key_account": _choice(
        "Which key hotel-brand account, if any, is the item about?",
        {
            "wyndham": "Wyndham, including its brands, OHIP or SynXis work for Wyndham.",
            "best_western": "Best Western, BW or BWH.",
            "ihg": "IHG, including Holiday Inn, InterContinental, Kimpton.",
            "none": "None of these accounts, or not stated.",
        },
    ),
    "stakes": _score(
        "How much is at stake in the matter the item describes?",
        [
            "Chatter, social or routine noise. Nothing is at stake.",
            "Routine work: an ordinary ticket, pull request or update.",
            "Matters to a customer, a deadline, a colleague who is blocked, or my team's plans.",
            "Production incident, customer escalation, security, payments or legal exposure.",
        ],
    ),
    "disposition": _choice(
        "What should I do with this item this morning?",
        {
            "actionable": "I need to do something: reply, review, decide, fix or follow up.",
            "aware": "Worth knowing about, but nothing is needed from me.",
            "noise": "Not worth my attention at all.",
            "cannot_tell": "The item does not contain enough to say.",
        },
    ),
    "title_verb": _choice(
        "If I did act on this item, which verb would start the task?",
        {
            "Reply": "Answer a person.",
            "Review": "Review a pull request, document or proposal.",
            "Decide": "Make or communicate a decision.",
            "Fix": "Fix code, configuration or data.",
            "Follow up": "Chase someone or check progress.",
            "Read": "Read for context.",
            "Other": "None of these.",
        },
    ),
    "contexts": _choice(
        "Which kind of work would acting on this item be?",
        {
            "deep": "Long focused thinking or design.",
            "craft": "Hands-on building: code, documents.",
            "react": "Quick responses: replies, approvals, small reviews.",
            "consume": "Reading or watching.",
            "autopilot": "Rote administrative steps.",
            "listen": "Audio or meetings.",
            "other": "None of these.",
        },
    ),
    "energy": _choice(
        "How much mental energy would acting on this item take?",
        {"low": "Little.", "medium": "Moderate.", "high": "A lot.", "unknown": "Cannot tell."},
    ),
    "time": _choice(
        "Roughly how many minutes would acting on this item take?",
        {
            **{str(m): f"About {m} minutes." for m in TIME_OPTIONS},
            "unknown": "Cannot tell.",
        },
    ),
}

ENT_SERIOUS = _noul(
    "Is this triage ticket serious enough that an engineering manager should look today?",
    true="Production impact, a key account blocked, data loss, payments or security.",
    false="Routine request, question or low-impact bug.",
)

GMAIL_CATEGORY = _choice(
    "Which category of email is this?",
    {
        "human": "A person wrote to me or to a small group including me.",
        "calendar": "Calendar invitation, update or response.",
        "tool_notification": "Notification from a work tool (GitHub, Linear, Notion, Slack, Jira).",
        "alert": "Monitoring, incident or failure alert.",
        "digest": "Digest, newsletter or summary.",
        "hr_admin": "HR, payroll, reviews, expenses or IT administration.",
        "vendor": "Vendor marketing, sales outreach or product announcements.",
        "recruiting": "Recruiting, interview feedback or candidate updates.",
        "billing": "Receipt, invoice or billing notice.",
        "security": "Sign-in, verification code or security notice.",
        "other": "None of these.",
    },
)


def questions_for(item: dict[str, Any]) -> dict[str, QuestionSpec]:
    questions = dict(CORE)
    if item.get("kind") == "ent_triage":
        questions["ent_serious"] = ENT_SERIOUS
    if item.get("source") == "gmail":
        questions["gmail_category"] = GMAIL_CATEGORY
    return questions


def build_state(item: dict[str, Any]) -> dict[str, Any]:
    return {"me": ME, "item": item}
