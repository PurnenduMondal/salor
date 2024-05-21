# Generated by Django 2.0.8 on 2018-09-26 09:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("order", "0062_auto_20180921_0949")]

    operations = [
        migrations.AlterField(
            model_name="orderevent",
            name="type",
            field=models.CharField(
                choices=[
                    ("PLACED", "placed"),
                    ("PLACED_FROM_DRAFT", "draft_placed"),
                    ("OVERSOLD_ITEMS", "oversold_items"),
                    ("ORDER_MARKED_AS_PAID", "marked_as_paid"),
                    ("CANCELED", "canceled"),
                    ("ORDER_FULLY_PAID", "order_paid"),
                    ("UPDATED", "updated"),
                    ("EMAIL_SENT", "email_sent"),
                    ("PAYMENT_CAPTURED", "captured"),
                    ("PAYMENT_REFUNDED", "refunded"),
                    ("PAYMENT_RELEASED", "released"),
                    ("FULFILLMENT_CANCELED", "fulfillment_canceled"),
                    ("FULFILLMENT_RESTOCKED_ITEMS", "restocked_items"),
                    ("FULFILLMENT_FULFILLED_ITEMS", "fulfilled_items"),
                    ("TRACKING_UPDATED", "tracking_updated"),
                    ("NOTE_ADDED", "note_added"),
                    ("OTHER", "other"),
                ],
                max_length=255,
            ),
        )
    ]
