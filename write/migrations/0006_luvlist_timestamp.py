# Generated by Django 4.2.2 on 2023-07-13 18:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("write", "0005_contentinlist_comment_alter_contentinlist_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="luvlist",
            name="timestamp",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
