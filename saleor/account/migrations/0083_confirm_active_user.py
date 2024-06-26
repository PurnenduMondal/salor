# Generated by Django 3.2.24 on 2024-02-29 13:21

from django.apps import apps as registry
from django.db import migrations
from django.db.models.signals import post_migrate

from .tasks.saleor3_19 import confirm_active_users_task


def confirm_active_users(apps, _schema_editor):
    def on_migrations_complete(sender=None, **kwargs):
        confirm_active_users_task.delay()

    sender = registry.get_app_config("account")

    post_migrate.connect(on_migrations_complete, weak=False, sender=sender)


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0082_auto_20231204_1419"),
    ]

    operations = [migrations.RunPython(confirm_active_users, migrations.RunPython.noop)]
