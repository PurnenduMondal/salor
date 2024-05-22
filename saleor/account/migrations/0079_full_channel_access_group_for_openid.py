# Generated by Django 3.2.18 on 2023-03-24 14:14

from django.apps import apps as registry
from django.db import migrations
from django.db.models import Exists, OuterRef, Q
from django.db.models.signals import post_migrate

OPENID_ID = "mirumee.authentication.openidconnect"

# The batch of size 5000 took about 0.5 s to assign users to groups
BATCH_SIZE = 5000


def create_full_channel_access_group_for_openid(apps, schema_editor):
    group_name = "OpenID default group"
    User = apps.get_model("account", "User")
    Group = apps.get_model("account", "Group")

    def on_migrations_complete(sender=None, **kwargs):
        create_full_channel_access_group_task(User, Group, group_name)

    PluginConfiguration = apps.get_model("plugins", "PluginConfiguration")
    plugin_conf = PluginConfiguration.objects.filter(
        active=True, identifier=OPENID_ID
    ).first()
    if plugin_conf:
        Group = apps.get_model("account", "Group")
        Group.objects.get_or_create(
            name=group_name, restricted_access_to_channels=False
        )
        update_plugin_default_group_name(plugin_conf, group_name)

        sender = registry.get_app_config("account")
        post_migrate.connect(on_migrations_complete, weak=False, sender=sender)


def update_plugin_default_group_name(plugin_conf, group_name):
    default_group_name_field = "default_group_name_for_new_staff_users"
    for conf in plugin_conf.configuration:
        if conf["name"] == default_group_name_field:
            conf.update([("value", group_name)])
            plugin_conf.save(update_fields=["configuration"])
            return

    group_conf = {"name": default_group_name_field, "value": group_name}
    plugin_conf.configuration.append(group_conf)
    plugin_conf.save(update_fields=["configuration"])


def create_full_channel_access_group_task(User, Group, group_name):
    full_channel_access_group, _ = Group.objects.get_or_create(
        name=group_name, defaults={"restricted_access_to_channels": False}
    )
    GroupUser = User.groups.through
    group_users = GroupUser.objects.filter(group_id=full_channel_access_group.id)
    users = User.objects.filter(
        Q(is_staff=True) & ~Exists(group_users.filter(user_id=OuterRef("id")))
    )
    for user_ids in queryset_in_batches(users):
        if user_ids:
            full_channel_access_group.user_set.add(*user_ids)


def queryset_in_batches(queryset):
    """Slice a queryset into batches.

    Input queryset should be sorted be pk.
    """
    start_pk = 0

    while True:
        qs = queryset.order_by("pk").filter(pk__gt=start_pk)[:BATCH_SIZE]
        pks = list(qs.values_list("pk", flat=True))

        if not pks:
            break

        yield pks

        start_pk = pks[-1]


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0078_add_group_channels_conf"),
    ]

    operations = [
        migrations.RunPython(
            create_full_channel_access_group_for_openid,
            reverse_code=migrations.RunPython.noop,
        ),
    ]