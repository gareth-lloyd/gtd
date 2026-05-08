---
area: null
contexts: []
created: 2026-05-06 13:34:09.537949
defer_until: null
due: null
energy: low
id: 2026-05-06T1334-seed-account-groups-for-ihg
order: 5
output: ''
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: 5
title: Seed account groups for IHG
updated: 2026-05-08 14:16:26.126164
waiting_on: null
waiting_since: null
working_on: true
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