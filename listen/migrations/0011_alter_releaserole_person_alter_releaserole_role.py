# Generated by Django 4.2.2 on 2023-06-30 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("entity", "0001_initial"),
        ("listen", "0010_alter_trackinrelease_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="releaserole",
            name="person",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_query_name="release_roles",
                to="entity.person",
            ),
        ),
        migrations.AlterField(
            model_name="releaserole",
            name="role",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="entity.role",
            ),
        ),
    ]
