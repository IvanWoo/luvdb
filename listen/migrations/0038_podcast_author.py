# Generated by Django 4.2.2 on 2023-08-17 18:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("listen", "0037_alter_podcast_explicit"),
    ]

    operations = [
        migrations.AddField(
            model_name="podcast",
            name="author",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
