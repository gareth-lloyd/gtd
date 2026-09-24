"""Apply a merge: fold one item into another with an already-merged title/body.

Used by the agent session that `launch_merge_session` opens — the agent
composes the prose, this command does everything deterministic (union
contexts/tags, fill empty scalars, keep project/bucket, trash the source).
"""

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from gtd_core.service import GtdService


class Command(BaseCommand):
    help = "Merge SOURCE into TARGET using the given title/body, then trash SOURCE."

    def add_arguments(self, parser):
        parser.add_argument("env")
        parser.add_argument("target_id")
        parser.add_argument("source_id")
        parser.add_argument("--title", required=True, help="Merged title")
        group = parser.add_mutually_exclusive_group()
        group.add_argument("--body", default=None, help="Merged body (markdown)")
        group.add_argument("--body-file", default=None, help="Path to a file holding the body")

    def handle(self, *args, env, target_id, source_id, title, body, body_file, **options):
        if body_file is not None:
            try:
                body = Path(body_file).read_text()
            except OSError as e:
                raise CommandError(f"cannot read --body-file: {e}") from e
        svc = GtdService(settings.GTD_DATA_ROOT)
        try:
            merged = svc.merge_items(env, target_id, source_id, title=title, body=body or "")
        except KeyError as e:
            raise CommandError(f"no such item: {e.args[0]}") from e
        except ValueError as e:
            raise CommandError(str(e)) from e
        self.stdout.write(f"merged {source_id} into {merged.id} ({merged.status.value})")
        self.stdout.write(f"  title: {merged.title}")
        self.stdout.write(f"  contexts: {merged.contexts}  tags: {merged.tags}")
        self.stdout.write(f"  {source_id} moved to trash")
