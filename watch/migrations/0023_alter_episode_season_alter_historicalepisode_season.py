# Generated by Django 5.1 on 2024-08-25 11:30

import auto_prefetch
import django.db.models.deletion
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("watch", "0022_migrate_series_data_to_season"),
    ]

    operations = [
        migrations.AlterField(
            model_name="episode",
            name="season",
            field=auto_prefetch.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="episodes",
                to="watch.season",
            ),
        ),
        migrations.AlterField(
            model_name="historicalepisode",
            name="season",
            field=auto_prefetch.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="watch.season",
            ),
        ),
    ]
