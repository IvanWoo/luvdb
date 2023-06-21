# Generated by Django 4.2.2 on 2023-06-21 09:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("read", "0005_rename_name_bookworkrole_alt_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="book_subtitle",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="work",
            name="subtitle",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
