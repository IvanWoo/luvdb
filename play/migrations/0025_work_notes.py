# Generated by Django 4.2.2 on 2023-09-07 13:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("play", "0024_game_wikipedia"),
    ]

    operations = [
        migrations.AddField(
            model_name="work",
            name="notes",
            field=models.TextField(blank=True, null=True),
        ),
    ]
