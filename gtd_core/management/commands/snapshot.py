from django.conf import settings
from django.core.management.base import BaseCommand

from gtd_core.recurring import spawn_recurring
from gtd_core.repository import EnvRepository
from gtd_core.service import GtdService
from gtd_core.snapshot import snapshot


class Command(BaseCommand):
    help = "Spawn recurring items, then commit data/ changes as a single snapshot."

    def add_arguments(self, parser):
        parser.add_argument("-m", "--message", type=str, default=None)
        parser.add_argument("--push", action="store_true", default=False)

    def handle(self, *args, message=None, push=False, **options):
        svc = GtdService(settings.GTD_DATA_ROOT)
        for env_name in svc.list_envs():
            repo = svc.repo(env_name)
            spawned = spawn_recurring(repo)
            if spawned:
                titles = ", ".join(i.title for i in spawned)
                self.stdout.write(f"[{env_name}] spawned {len(spawned)} recurring: {titles}")

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
