"""Ask Jev the questions in `questions.py`, one request per item.

The API key is read from the `TYPESAFE_API_KEY` environment variable only.
Any failure raises `JevUnavailableError`; the caller falls back to handing every
item to the LLM, so a Jev outage costs context, never coverage.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from gtd_triage import rules
from gtd_triage.questions import QUESTIONS_VERSION, QuestionSpec, build_state, questions_for

API_KEY_ENV = "TYPESAFE_API_KEY"
# Rate limit is 1,200 requests/min. At ~200 ms a call, 4 in flight stays under it.
MAX_IN_FLIGHT = 4
# Give up on the whole run once this share of items has failed.
MAX_FAILURE_SHARE = 0.1


class JevUnavailableError(RuntimeError):
    """Jev could not be used for this run."""


@dataclass
class JevRun:
    answers: dict[str, dict[str, dict[str, Any]]] = field(default_factory=dict)
    failed: list[str] = field(default_factory=list)
    requests: int = 0
    cached: int = 0
    input_tokens: int = 0


def _to_sdk_questions(specs: dict[str, QuestionSpec]) -> dict[str, Any]:
    from typesafe_sdk import Choice, Noul, Score

    built: dict[str, Any] = {}
    for key, spec in specs.items():
        if spec["type"] == "noul":
            built[key] = Noul(instructions=spec["instructions"], criteria=spec["criteria"])
        elif spec["type"] == "choice":
            built[key] = Choice(instructions=spec["instructions"], criteria=spec["criteria"])
        else:
            built[key] = Score(instructions=spec["instructions"], criteria=spec["criteria"])
    return built


def _plain(answer: Any) -> dict[str, Any]:
    """An SDK answer object as a JSON-safe dict with string keys."""
    out: dict[str, Any] = {}
    for name in ("noul", "choice", "score", "confidence", "probabilities"):
        value = getattr(answer, name, None)
        if value is None:
            continue
        out[name] = {str(k): v for k, v in value.items()} if isinstance(value, dict) else value
    return out


def cache_key(state: dict[str, Any], specs: dict[str, QuestionSpec], model: str) -> str:
    payload = json.dumps([model, QUESTIONS_VERSION, state, specs], sort_keys=True, default=str)
    return hashlib.sha256(payload.encode()).hexdigest()


class AnswerCache:
    """Append-only JSONL of answers, so a replay never pays for an item twice."""

    def __init__(self, path: Path | None) -> None:
        self.path = path
        self._entries: dict[str, dict[str, Any]] = {}
        if path and path.exists():
            for line in path.read_text().splitlines():
                if line:
                    entry = json.loads(line)
                    self._entries[entry["key"]] = entry["answers"]

    def get(self, key: str) -> dict[str, Any] | None:
        return self._entries.get(key)

    def put(self, key: str, answers: dict[str, Any]) -> None:
        self._entries[key] = answers
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a") as fh:
                fh.write(json.dumps({"key": key, "answers": answers}) + "\n")


async def _ask_all(items: list[dict[str, Any]], model: str, cache: AnswerCache) -> JevRun:
    from typesafe_sdk import AsyncTypeSafeClient, TypeSafeAuthenticationError, TypeSafeError

    run = JevRun()
    gate = asyncio.Semaphore(MAX_IN_FLIGHT)
    client = AsyncTypeSafeClient(model=model)
    auth_failed = False

    async def ask(item: dict[str, Any]) -> None:
        nonlocal auth_failed
        source_id = item["source_id"]
        specs = questions_for(item)
        state = build_state(rules.scrub(item))
        key = cache_key(state, specs, model)
        hit = cache.get(key)
        if hit is not None:
            run.answers[source_id] = hit
            run.cached += 1
            return
        async with gate:
            if auth_failed:
                run.failed.append(source_id)
                return
            try:
                response = await client.system_one(state=state, questions=_to_sdk_questions(specs))
            except TypeSafeAuthenticationError:
                auth_failed = True
                run.failed.append(source_id)
                return
            except TypeSafeError:
                run.failed.append(source_id)
                return
        answers = {name: _plain(answer) for name, answer in response.answers.items()}
        cache.put(key, answers)
        run.answers[source_id] = answers
        run.requests += 1
        run.input_tokens += response.usage.input_tokens or 0

    await asyncio.gather(*(ask(item) for item in items))
    if auth_failed:
        raise JevUnavailableError(f"{API_KEY_ENV} was rejected (401)")
    return run


def ask_jev(items: list[dict[str, Any]], model: str, cache_path: Path | None = None) -> JevRun:
    if not os.environ.get(API_KEY_ENV):
        raise JevUnavailableError(f"{API_KEY_ENV} is not set")
    try:
        import typesafe_sdk  # noqa: F401
    except ImportError as exc:
        raise JevUnavailableError("typesafe-sdk is not installed (uv sync)") from exc
    if not items:
        return JevRun()
    run = asyncio.run(_ask_all(items, model, AnswerCache(cache_path)))
    if len(run.failed) > MAX_FAILURE_SHARE * len(items):
        raise JevUnavailableError(f"{len(run.failed)} of {len(items)} Jev requests failed")
    return run
