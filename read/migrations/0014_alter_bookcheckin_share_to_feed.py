# Generated by Django 4.2.2 on 2023-06-21 21:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("read", "0013_remove_bookcheckin_share_on_feed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookcheckin",
            name="share_to_feed",
            field=models.BooleanField(default=False),
        ),
    ]
