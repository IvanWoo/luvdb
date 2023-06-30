# Generated by Django 4.2.2 on 2023-06-30 11:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("listen", "0009_track_work"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="trackinrelease",
            options={"ordering": ["order"]},
        ),
        migrations.RenameField(
            model_name="trackinrelease",
            old_name="track_order",
            new_name="order",
        ),
        migrations.AddField(
            model_name="releaserole",
            name="alt_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
