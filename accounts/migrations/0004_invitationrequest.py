# Generated by Django 4.2.2 on 2023-08-27 11:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_customuser_timezone"),
    ]

    operations = [
        migrations.CreateModel(
            name="InvitationRequest",
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
                ("email", models.EmailField(max_length=254, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_invited", models.BooleanField(default=False)),
            ],
        ),
    ]
