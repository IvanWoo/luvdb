# Generated by Django 4.2.2 on 2023-06-14 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("activity_feed", "0002_repost"),
    ]

    operations = [
        migrations.AddField(
            model_name="activity",
            name="reposted_by",
            field=models.ManyToManyField(
                blank=True, related_name="reposts", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="activity",
            name="reposted_from",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="activity_feed.activity",
            ),
        ),
        migrations.DeleteModel(
            name="Repost",
        ),
    ]
