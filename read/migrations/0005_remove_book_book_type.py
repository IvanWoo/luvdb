# Generated by Django 4.2.2 on 2023-06-25 15:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("read", "0004_editionrole_alt_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book",
            name="book_type",
        ),
    ]
