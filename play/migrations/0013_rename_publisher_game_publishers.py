# Generated by Django 4.2.2 on 2023-07-14 12:25

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("play", "0012_gamepublisher_game_publisher"),
    ]

    operations = [
        migrations.RenameField(
            model_name="game",
            old_name="publisher",
            new_name="publishers",
        ),
    ]
