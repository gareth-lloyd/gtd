"""Filesystem locations shared by the triage modules."""

from __future__ import annotations

from pathlib import Path

GTD_ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = GTD_ROOT / "data"

SKILLS_DIR = Path.home() / ".claude" / "skills"
GTD_SKILL_OUTPUT = SKILLS_DIR / "gtd" / "output"
GTD2_OUTPUT = SKILLS_DIR / "gtd2" / "output"
CAPTURE_SCRIPT = SKILLS_DIR / "gtd" / "capture_items.py"

LABELS_PATH = GTD2_OUTPUT / "eval" / "labels.jsonl"
ANSWERS_CACHE = GTD2_OUTPUT / "eval" / "answers.jsonl"
