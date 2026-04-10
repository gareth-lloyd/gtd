from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from gtd_core.importer_nirvana import import_csv
from gtd_core.repository import EnvRepository


class Command(BaseCommand):
    help = "Import a Nirvana CSV export into a given environment."

    def add_arguments(self, parser):
        parser.add_argument("env", type=str, help="Target environment (e.g. work, home)")
        parser.add_argument("csv_path", type=Path, help="Path to Nirvana CSV export")
        parser.add_argument("--dry-run", action="store_true", help="Parse only, no writes")
        parser.add_argument(
            "--skip-archive",
            action="store_true",
            help="Skip Logbook (archive) items to keep the imported set small",
        )

    def handle(self, *args, env, csv_path, dry_run, skip_archive, **options):
        if not csv_path.exists():
            raise CommandError(f"CSV not found: {csv_path}")

        repo = EnvRepository(settings.GTD_DATA_ROOT, env)
        try:
            cfg = repo.load_config()
        except FileNotFoundError:
            raise CommandError(f"No config.yml found for env '{env}'")

        stats = import_csv(
            csv_path=csv_path,
            repo=repo,
            env_name=env,
            cfg=cfg,
            dry_run=dry_run,
            skip_archive=skip_archive,
        )

        prefix = "[dry-run] " if dry_run else ""
        self.stdout.write(
            f"{prefix}Imported {stats.projects} projects, {stats.tasks} tasks, "
            f"skipped {stats.skipped}"
        )
        if stats.unknown_states:
            self.stdout.write(
                f"Unknown STATE values: "
                + ", ".join(f"{k}={v}" for k, v in stats.unknown_states.items())
            )
