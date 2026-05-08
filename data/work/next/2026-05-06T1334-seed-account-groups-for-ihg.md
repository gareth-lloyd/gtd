---
area: null
contexts: []
created: 2026-05-06 13:34:09.537949
defer_until: null
due: null
energy: low
id: 2026-05-06T1334-seed-account-groups-for-ihg
order: 5
output: |
  ## Agent run 2026-05-08T11:26:00Z

  Created data migration for IHG AccountGroups in pms-gateway.

  **Branch:** `glloyd/seed-ihg-account-groups` (off latest origin/master, fast-forwarded from 592e699b934 → f45865cf9d1)

  **File:** `backend/pms-gateway/accounts/migrations/0033_seed_ihg_account_groups.py`
  - Dependency: `accounts.0032_alter_accountvalidation_vendor` (current head — verified)
  - Forward: `update_or_create` for `IHG` (kind=brand) and `IHG Onboarding Project` (kind=onboarding_group) — idempotent
  - Reverse: deletes those two AccountGroups by name

  **Verification:**
  - Confirmed `AccountGroup` model lives at `pms-gateway/accounts/models/account_group.py` with `name` (unique, max_length=220) and `kind` (choices: brand, onboarding_group)
  - `python manage.py makemigrations --check accounts` → "No changes detected" (no schema drift introduced)
  - `python -m py_compile` clean
  - Pyright "import django.db could not be resolved" warning is a false positive from a different conductor venv path; unused `schema_editor` params are required by Django's RunPython contract

  **Not done — needs your call:**
  - No commit, no push, no PR. File is untracked on the branch.
  - Did not run the migration against local DB (Postgres wasn't up; this is a low-risk seed and the model invariants check out)

  Next step is yours: review the file, then `git add && commit && push && gh pr create` (or ask me to draft those).
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: 5
title: Seed account groups for IHG
updated: 2026-05-08 11:26:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

```def seed_ihg_account_groups(apps, schema_editor):
    AccountGroup = apps.get_model("accounts", "AccountGroup")
    AccountGroup.objects.update_or_create(name="IHG", defaults={"kind": "brand"})
    AccountGroup.objects.update_or_create(name="IHG Onboarding Project", defaults={"kind": "onboarding_group"})


def remove_ihg_account_groups(apps, schema_editor):
    AccountGroup = apps.get_model("accounts", "AccountGroup")
    AccountGroup.objects.filter(name__in=["IHG", "IHG Onboarding Project"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0032_alter_accountvalidation_vendor"),
    ]

    operations = [
        migrations.RunPython(seed_ihg_account_groups, remove_ihg_account_groups),```