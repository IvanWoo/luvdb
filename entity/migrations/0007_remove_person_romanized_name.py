# Generated by Django 4.2.2 on 2023-08-19 06:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("entity", "0006_alter_person_other_names"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="person",
            name="romanized_name",
        ),
    ]
