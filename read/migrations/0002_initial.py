# Generated by Django 4.2.2 on 2023-06-24 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("read", "0001_initial"),
        ("write", "0001_initial"),
        ("entity", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookcheckin",
            name="tags",
            field=models.ManyToManyField(blank=True, to="write.tag"),
        ),
        migrations.AddField(
            model_name="book",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="books_created",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="persons",
            field=models.ManyToManyField(
                related_name="books", through="read.BookRole", to="entity.person"
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="publisher",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="books",
                to="read.publisher",
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="updated_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="books_updated",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="work_roles",
            field=models.ManyToManyField(
                related_name="books", through="read.BookWorkRole", to="read.work"
            ),
        ),
    ]
