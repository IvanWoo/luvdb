# Generated by Django 4.2.2 on 2023-07-31 17:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("play", "0015_alter_gamecheckin_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="Genre",
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
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name="work",
            name="genres",
            field=models.ManyToManyField(
                blank=True, related_name="play_works", to="play.genre"
            ),
        ),
    ]
