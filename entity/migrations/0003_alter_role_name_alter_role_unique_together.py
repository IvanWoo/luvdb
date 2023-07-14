# Generated by Django 4.2.2 on 2023-07-14 13:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("entity", "0002_person_note"),
    ]

    operations = [
        migrations.AlterField(
            model_name="role",
            name="name",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name="role",
            unique_together={("name", "domain")},
        ),
    ]
