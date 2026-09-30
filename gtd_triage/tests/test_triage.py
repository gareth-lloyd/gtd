"""Rules, scoring and the fallback path. No network: answers are hand-built."""

from __future__ import annotations

from typing import Any

import pytest

from gtd_triage import jev_client, pipeline, render, rules
from gtd_triage.labels import join_key
from gtd_triage.questions import CORE, questions_for
from gtd_triage.score import load_weights, score_item, uncertainty

WEIGHTS = load_weights()


def make_item(**overrides: Any) -> dict[str, Any]:
    item = {
        "source": "slack",
        "kind": "channel_unread",
        "source_id": "https://canarytechnologies.slack.com/archives/C1/p100",
        "title": "Someone in #eng-general",
        "snippet": "lunch is here",
        "context": [],
        "facts": {"channel": "#eng-general"},
        "ts": "2026-09-18T06:00:00Z",
    }
    return {**item, **overrides}


def make_answers(
    *,
    awaiting_me: float = 0.05,
    addressed_to_me: float = 0.05,
    disposition: dict[str, float] | None = None,
    key_account_none: float = 0.97,
    context_sufficient: float = 0.9,
    automated: float = 0.1,
) -> dict[str, dict[str, Any]]:
    disposition = disposition or {
        "actionable": 0.02,
        "aware": 0.08,
        "noise": 0.88,
        "cannot_tell": 0.02,
    }
    return {
        "awaiting_me": {"noul": awaiting_me},
        "addressed_to_me": {"noul": addressed_to_me},
        "already_handled": {"noul": 0.05},
        "automated": {"noul": automated},
        "context_sufficient": {"noul": context_sufficient},
        "stakes": {"score": 0.3},
        "deadline": {"choice": "none_stated", "probabilities": {"none_stated": 1.0}},
        "key_account": {
            "choice": "none",
            "probabilities": {"none": key_account_none, "wyndham": 1 - key_account_none},
        },
        "disposition": {
            "choice": max(disposition, key=lambda k: disposition[k]),
            "probabilities": disposition,
        },
    }


class TestRules:
    def test_pending_reply_is_always_actionable(self) -> None:
        assert rules.rule_disposition(make_item(kind="dm_pending_reply")) == "actionable"

    def test_team_review_is_never_inbox(self) -> None:
        assert rules.rule_disposition(make_item(kind="review_team_only")) == "aware"

    def test_interview_pr_is_awareness_even_when_action_needed(self) -> None:
        item = make_item(
            source="github",
            kind="mine_action_needed",
            source_id="https://github.com/canary-technologies-corp-interviews/someone/pull/1",
        )
        assert rules.rule_disposition(item) == "aware"
        assert not rules.needs_jev(item)

    def test_judgment_kinds_are_left_to_jev(self) -> None:
        assert rules.rule_disposition(make_item()) is None

    def test_cluster_key_groups_linear_notifications_for_one_issue(self) -> None:
        url = "https://linear.app/canary-technologies/issue/ENT-7545/some-slug"
        a = make_item(source="linear", kind="subscribed", source_id=url)
        b = make_item(source="linear", kind="new_comment", source_id=url + "#comment-abc")
        assert rules.cluster_key(a) == rules.cluster_key(b) == "linear:ENT-7545"

    def test_scrub_removes_credentials_at_any_depth(self) -> None:
        token = "xoxb-" + "1234567890-abcdefghij"
        scrubbed = rules.scrub({"snippet": f"token {token}", "context": [{"text": token}]})
        assert token not in str(scrubbed)
        assert rules.REDACTED in scrubbed["snippet"]

    def test_saved_facts_computed_from_channel_id(self) -> None:
        item = make_item(kind="saved", facts={"channel_id": "D123", "from_id": "U1"})
        facts = rules.saved_facts(item, my_slack_id="U1")
        assert facts == {"is_dm": True, "is_self_save": True, "mentions_me": False}


class TestQuestions:
    def test_every_choice_can_abstain(self) -> None:
        abstain = {"none", "none_stated", "cannot_tell", "other", "Other", "unknown"}
        for key, spec in CORE.items():
            if spec["type"] == "choice":
                assert abstain & set(spec["criteria"]), key

    def test_source_specific_questions_are_gated(self) -> None:
        assert "ent_serious" not in questions_for(make_item())
        assert "ent_serious" in questions_for(make_item(source="linear", kind="ent_triage"))
        assert "gmail_category" in questions_for(make_item(source="gmail", kind="other"))


class TestScore:
    def test_confident_bot_noise_is_banded_know(self) -> None:
        item = make_item(source="linear", kind="status_change")
        assert score_item(item, make_answers(automated=0.97), WEIGHTS).band == "know"

    def test_kind_prior_separates_identical_answers(self) -> None:
        saved = score_item(make_item(kind="saved"), make_answers(), WEIGHTS)
        unread = score_item(make_item(), make_answers(), WEIGHTS)
        assert saved.attention > unread.attention

    def test_unseen_kind_gets_the_default_prior(self) -> None:
        scored = score_item(make_item(kind="brand_new_kind"), make_answers(), WEIGHTS)
        assert scored.features["kind_prior"] == WEIGHTS["kind_prior"]["default"]

    def test_contradiction_between_atoms_raises_uncertainty(self) -> None:
        agree = uncertainty(make_answers())
        contradict = uncertainty(make_answers(awaiting_me=0.9))
        assert contradict > agree
        assert score_item(make_item(), make_answers(awaiting_me=0.9), WEIGHTS).band != "know"

    def test_key_account_item_is_never_banded_know(self) -> None:
        by_jev = score_item(make_item(), make_answers(key_account_none=0.1), WEIGHTS)
        by_rule = score_item(make_item(facts={"channel": "#wyndham"}), make_answers(), WEIGHTS)
        assert by_jev.band != "know"
        assert by_rule.band != "know"

    def test_saved_item_is_never_banded_know(self) -> None:
        answers = make_answers(automated=0.97)
        assert score_item(make_item(kind="saved"), answers, WEIGHTS).band == "check"

    def test_rule_actionable_is_act_whatever_jev_says(self) -> None:
        item = make_item(kind="mention_pending_reply")
        assert score_item(item, make_answers(), WEIGHTS).band == "act"

    def test_never_inbox_kind_is_never_act(self) -> None:
        loud = make_answers(
            awaiting_me=0.95,
            addressed_to_me=0.95,
            disposition={"actionable": 0.94, "aware": 0.03, "noise": 0.02, "cannot_tell": 0.01},
        )
        scored = score_item(make_item(source="linear", kind="ent_triage"), loud, WEIGHTS)
        assert scored.band == "check"

    def test_thin_context_raises_dive_priority(self) -> None:
        thin = score_item(make_item(), make_answers(context_sufficient=0.1), WEIGHTS)
        full = score_item(make_item(), make_answers(context_sufficient=0.9), WEIGHTS)
        assert thin.dive_priority > full.dive_priority

    def test_pending_reply_without_thread_outranks_a_key_account_ticket(self) -> None:
        reply = score_item(make_item(kind="dm_pending_reply"), make_answers(), WEIGHTS)
        ticket = score_item(
            make_item(source="linear", kind="subscribed", title="ENT-1: Wyndham thing"),
            make_answers(context_sufficient=0.2),
            WEIGHTS,
        )
        assert reply.dive_priority > ticket.dive_priority

    def test_never_inbox_kind_dives_only_on_unclear_seriousness(self) -> None:
        item = make_item(source="linear", kind="ent_triage")
        unclear = {**make_answers(), "ent_serious": {"noul": 0.5}}
        clear = {**make_answers(), "ent_serious": {"noul": 0.02}}
        assert score_item(item, unclear, WEIGHTS).dive_priority > 0.9
        assert score_item(item, clear, WEIGHTS).dive_priority < 0.1

    def test_no_dive_kind_has_zero_dive_priority(self) -> None:
        item = make_item(source="github", kind="review_team_only")
        assert score_item(item, make_answers(context_sufficient=0.0), WEIGHTS).dive_priority == 0


class TestPipeline:
    def test_missing_key_falls_back_and_keeps_every_item(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv(jev_client.API_KEY_ENV, raising=False)
        blob = {
            "items": [
                make_item(),
                make_item(kind="dm_pending_reply", source_id="https://x.slack.com/archives/D1/p2"),
            ]
        }
        triage = pipeline.run_triage(blob, WEIGHTS)
        assert triage["jev"]["status"] == "fallback"
        assert {e["band"] for e in triage["entries"]} == {"act", "check"}
        assert "JEV FALLBACK" in render.llm_view(triage)

    def test_every_source_id_lands_in_exactly_one_place(self) -> None:
        url = "https://linear.app/canary-technologies/issue/ENT-1234/slug"
        blob = {
            "items": [
                make_item(),
                make_item(source="linear", kind="subscribed", source_id=url),
                make_item(source="linear", kind="new_comment", source_id=url + "#comment-1"),
            ]
        }
        triage = pipeline.run_triage(blob, WEIGHTS, use_jev=False)
        captured = {url}
        index = render.awareness_index(triage, captured, notes={})
        assert pipeline.check_coverage(triage, captured, index) == []
        assert [e["source_id"] for e in index] == [blob["items"][0]["source_id"]]

    def test_duplicate_source_ids_merge_to_the_actionable_one(self) -> None:
        a = make_item(kind="channel_unread")
        b = make_item(kind="mention_pending_reply")
        assert [i["kind"] for i in pipeline.merge_duplicates([a, b])] == ["mention_pending_reply"]


def test_join_key_ignores_thread_query_and_linear_slug() -> None:
    assert join_key("https://x.slack.com/archives/C1/p100?thread_ts=1.2&cid=C1") == "C1/p100"
    assert join_key("https://linear.app/acme/issue/ENT-12/some-slug") == "ENT-12"
