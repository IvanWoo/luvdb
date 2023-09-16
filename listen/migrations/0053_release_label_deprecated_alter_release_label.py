# Generated by Django 4.2.2 on 2023-09-16 11:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("entity", "0011_company"),
        ("listen", "0052_audiobook_audiobookrole_audiobookinstance_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="release",
            name="label_deprecated",
            field=models.ManyToManyField(
                db_column="label", related_name="releases_deprecated", to="listen.label"
            ),
        ),
        migrations.AlterField(
            model_name="release",
            name="label",
            field=models.ManyToManyField(related_name="releases", to="entity.company"),
        ),
    ]
