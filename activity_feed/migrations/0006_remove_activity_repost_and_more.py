# Generated by Django 4.2.2 on 2023-06-14 15:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("activity_feed", "0005_activity_repost_activity_repost_comment"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="activity",
            name="repost",
        ),
        migrations.RemoveField(
            model_name="activity",
            name="repost_comment",
        ),
    ]
