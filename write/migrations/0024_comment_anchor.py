# Generated by Django 4.2.2 on 2023-11-10 13:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("write", "0023_project_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="anchor",
            field=models.CharField(blank=True, editable=False, max_length=4),
        ),
    ]
