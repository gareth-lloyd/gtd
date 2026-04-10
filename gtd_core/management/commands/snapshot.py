from django.conf import settings
from django.core.management.base import BaseCommand

from gtd_core.snapshot import snapshot


class Command(BaseCommand):
    help = "Commit (and optionally push) data/ changes as a single snapshot."

    def add_arguments(self, parser):
        parser.add_argument("-m", "--message", type=str, default=None)
        parser.add_argument("--push", action="store_true", default=False)

    def handle(self, *args, message=None, push=False, **options):
        result = snapshot(settings.BASE_DIR, message=message, push=push)
        if not result.committed:
            self.stdout.write("nothing to snapshot")
            return
        self.stdout.write(f"{result.sha[:12]} {result.message}")
        if push:
            if result.pushed:
                self.stdout.write("pushed to origin")
            else:
                self.stdout.write("push skipped (no remote or push failed)")
