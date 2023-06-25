# Generated by Django 4.2.2 on 2023-06-24 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import read.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("entity", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Book",
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
                ("title", models.CharField(max_length=255)),
                ("subtitle", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "cover",
                    models.ImageField(
                        blank=True, null=True, upload_to=read.models.rename_book_cover
                    ),
                ),
                ("cover_sens", models.BooleanField(default=False)),
                ("language", models.CharField(blank=True, max_length=255, null=True)),
                ("details", models.TextField(blank=True, null=True)),
                (
                    "publication_date",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                (
                    "book_format",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("pages", models.IntegerField(blank=True, null=True)),
                ("price", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "isbn_10",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        null=True,
                        validators=[read.models.validate_isbn_10],
                    ),
                ),
                (
                    "isbn_13",
                    models.CharField(
                        blank=True,
                        max_length=13,
                        null=True,
                        validators=[read.models.validate_isbn_13],
                    ),
                ),
                (
                    "asin",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        null=True,
                        validators=[read.models.validate_asin],
                    ),
                ),
                (
                    "book_type",
                    models.CharField(
                        choices=[
                            ("SB", "Standalone"),
                            ("SS", "Short Stories Collection"),
                            ("ES", "Essays Collection"),
                        ],
                        default="SB",
                        max_length=2,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Work",
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
                ("title", models.CharField(max_length=255)),
                ("subtitle", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "publication_date",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                ("language", models.CharField(blank=True, max_length=255, null=True)),
                ("work_type", models.CharField(blank=True, max_length=255, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="works_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WorkRole",
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
                (
                    "person",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="entity.person",
                    ),
                ),
                (
                    "role",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="entity.role",
                    ),
                ),
                (
                    "work",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="read.work"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="work",
            name="persons",
            field=models.ManyToManyField(
                related_name="works", through="read.WorkRole", to="entity.person"
            ),
        ),
        migrations.AddField(
            model_name="work",
            name="updated_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="works_updated",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="Publisher",
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
                ("name", models.CharField(max_length=255)),
                (
                    "romanized_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("history", models.TextField(blank=True, null=True)),
                ("location", models.CharField(blank=True, max_length=255, null=True)),
                ("website", models.URLField(blank=True, null=True)),
                (
                    "founded_date",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                ("closed_date", models.CharField(blank=True, max_length=10, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_updated",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="BookWorkRole",
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
                (
                    "publication_date",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                ("alt_name", models.CharField(blank=True, max_length=255, null=True)),
                ("alt_title", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "order",
                    models.PositiveIntegerField(blank=True, default=1, null=True),
                ),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="read.book"
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_query_name="book_work_roles",
                        to="entity.person",
                    ),
                ),
                (
                    "role",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="entity.role",
                    ),
                ),
                (
                    "work",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="read.work",
                    ),
                ),
            ],
            options={
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="BookWork",
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
                (
                    "order",
                    models.PositiveIntegerField(blank=True, default=1, null=True),
                ),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="read.book"
                    ),
                ),
                (
                    "work",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="read.work",
                    ),
                ),
            ],
            options={
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="BookRole",
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
                ("alt_name", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="read.book"
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_query_name="book_roles",
                        to="entity.person",
                    ),
                ),
                (
                    "role",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="entity.role",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BookCheckIn",
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
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("to_read", "To Read"),
                            ("currently_reading", "Reading"),
                            ("finished_reading", "Read"),
                            ("paused", "Paused"),
                            ("abandoned", "Abandoned"),
                            ("rereading", "Rereading"),
                            ("finished_rereading", "Reread"),
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
                        choices=[("PG", "Page"), ("PC", "Percentage")],
                        default="PG",
                        max_length=2,
                    ),
                ),
                ("comments_enabled", models.BooleanField(default=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="read.book"
                    ),
                ),
            ],
        ),
    ]
