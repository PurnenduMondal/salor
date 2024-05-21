# Generated by Django 3.1 on 2021-01-07 12:07

from django.db import migrations
from django.db.models import F

import saleor.core.db.fields
import saleor.core.utils.editorjs


def clean_content_field(apps, schema_editor):
    Page = apps.get_model("page", "Page")
    PageTranslation = apps.get_model("page", "PageTranslation")

    Page.objects.all().update(content="{}")
    PageTranslation.objects.all().update(content="{}")


def migrate_content_json_into_content_field(apps, schema_editor):
    Page = apps.get_model("page", "Page")
    PageTranslation = apps.get_model("page", "PageTranslation")

    Page.objects.all().update(content=F("content_json"))
    PageTranslation.objects.all().update(content=F("content_json"))


class Migration(migrations.Migration):
    dependencies = [
        ("page", "0017_pagetype"),
    ]

    operations = [
        migrations.RunPython(
            clean_content_field,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="page",
            name="content",
            field=saleor.core.db.fields.SanitizedJSONField(
                blank=True,
                default=dict,
                sanitizer=saleor.core.utils.editorjs.clean_editor_js,
            ),
        ),
        migrations.AlterField(
            model_name="pagetranslation",
            name="content",
            field=saleor.core.db.fields.SanitizedJSONField(
                blank=True,
                default=dict,
                sanitizer=saleor.core.utils.editorjs.clean_editor_js,
            ),
        ),
        migrations.RunPython(
            migrate_content_json_into_content_field,
            migrations.RunPython.noop,
        ),
    ]
