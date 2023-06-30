# Generated by Django 4.2.2 on 2023-06-30 10:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("listen", "0007_track_subtitle"),
    ]

    operations = [
        migrations.AddField(
            model_name="release",
            name="romanized_title",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="work",
            name="romanized_title",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="work",
            name="subtitle",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
