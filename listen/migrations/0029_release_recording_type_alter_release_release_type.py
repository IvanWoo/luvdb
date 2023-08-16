# Generated by Django 4.2.2 on 2023-08-16 20:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("listen", "0028_workrole_alt_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="release",
            name="recording_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Studio", "Studio"),
                    ("Live", "Live"),
                    ("Studio and Live", "Studio and Live"),
                    ("Compilation", "Compilation"),
                    ("Box Set", "Box Set"),
                ],
                max_length=255,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="release",
            name="release_type",
            field=models.CharField(
                blank=True,
                choices=[("LP", "LP"), ("EP", "EP"), ("Single", "Single")],
                max_length=255,
                null=True,
            ),
        ),
    ]
