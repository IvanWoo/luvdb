# Generated by Django 4.2.2 on 2023-06-21 11:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("entity", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="awardrecipient",
            name="award",
        ),
        migrations.RemoveField(
            model_name="awardrecipient",
            name="book",
        ),
        migrations.RemoveField(
            model_name="awardrecipient",
            name="person",
        ),
        migrations.RemoveField(
            model_name="awardrecipient",
            name="release",
        ),
        migrations.RemoveField(
            model_name="awardrecipient",
            name="track",
        ),
        migrations.RemoveField(
            model_name="awardrecipient",
            name="work",
        ),
        migrations.DeleteModel(
            name="Award",
        ),
        migrations.DeleteModel(
            name="AwardRecipient",
        ),
    ]
