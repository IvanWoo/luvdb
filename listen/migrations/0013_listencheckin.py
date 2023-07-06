# Generated by Django 4.2.2 on 2023-06-30 12:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("write", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("listen", "0012_rename_trackinrelease_releasetrack"),
    ]

    operations = [
        migrations.CreateModel(
            name="ListenCheckIn",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("object_id", models.PositiveIntegerField(null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("to_listen", "To Listen"),
                            ("looping", "Looping"),
                            ("listened", "Listened"),
                            ("paused", "Paused"),
                            ("abandoned", "Abandoned"),
                        ],
                        max_length=255,
                    ),
                ),
                ("share_to_feed", models.BooleanField(default=False)),
                ("content", models.TextField(blank=True, null=True)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("progress", models.IntegerField(blank=True, null=True)),
                (
                    "progress_type",
                    models.CharField(
                        choices=[
                            ("TT", "Accumulated Listen Time"),
                            ("LT", "Loop Time"),
                        ],
                        default="LT",
                        max_length=2,
                    ),
                ),
                ("comments_enabled", models.BooleanField(default=True)),
                (
                    "content_type",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                ("tags", models.ManyToManyField(blank=True, to="write.tag")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
