# Generated by Django 5.1 on 2024-08-23 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("listen", "0011_listencheckin_visibility_listencheckin_visible_to"),
        ("play", "0012_remove_historicalgame_work"),
        ("read", "0013_bookgroup_bookingroup_bookgroup_books_and_more"),
        ("visit", "0017_visitcheckin_visibility_visitcheckin_visible_to"),
        ("watch", "0020_watchcheckin_visibility_watchcheckin_visible_to"),
    ]

    operations = [
        migrations.AddField(
            model_name="instance",
            name="mentioned_books",
            field=models.ManyToManyField(
                blank=True,
                related_name="mentioned_in_publication_instances",
                to="read.book",
            ),
        ),
        migrations.AddField(
            model_name="instance",
            name="mentioned_games",
            field=models.ManyToManyField(
                blank=True,
                related_name="mentioned_in_publication_instances",
                to="play.game",
            ),
        ),
        migrations.AddField(
            model_name="instance",
            name="mentioned_gameworks",
            field=models.ManyToManyField(
                blank=True,
                related_name="mentioned_in_publication_instances",
                to="play.work",
            ),
        ),
        migrations.AddField(
            model_name="instance",
            name="mentioned_issues",
            field=models.ManyToManyField(
                blank=True,
                related_name="mentioned_in_publication_instances",
                to="read.issue",
            ),
        ),
        migrations.AddField(
            model_name="instance",
            name="mentioned_litinstances",
            field=models.ManyToManyField(
                blank=True,
                related_name="mentioned_in_publication_instances",
                to="read.instance",
            ),
        ),
        migrations.AddField(
            model_name="instance",
            name="mentioned_litworks",
            field=models.ManyToManyField(
                blank=True,
                related_name="mentioned_in_publication_instances",
                to="read.work",
            ),
        ),
        migrations.AddField(
            model_name="instance",
            name="mentioned_locations",
            field=models.ManyToManyField(
                blank=True,
                related_name="mentioned_in_publication_instances",
                to="visit.location",
            ),
        ),
        migrations.AddField(
            model_name="instance",
            name="mentioned_movies",
            field=models.ManyToManyField(
                blank=True,
                related_name="mentioned_in_publication_instances",
                to="watch.movie",
            ),
        ),
        migrations.AddField(
            model_name="instance",
            name="mentioned_musicalworks",
            field=models.ManyToManyField(
                blank=True,
                related_name="mentioned_in_publication_instances",
                to="listen.work",
            ),
        ),
        migrations.AddField(
            model_name="instance",
            name="mentioned_periodicals",
            field=models.ManyToManyField(
                blank=True,
                related_name="mentioned_in_publication_instances",
                to="read.periodical",
            ),
        ),
        migrations.AddField(
            model_name="instance",
            name="mentioned_releases",
            field=models.ManyToManyField(
                blank=True,
                related_name="mentioned_in_publication_instances",
                to="listen.release",
            ),
        ),
        migrations.AddField(
            model_name="instance",
            name="mentioned_series",
            field=models.ManyToManyField(
                blank=True,
                related_name="mentioned_in_publication_instances",
                to="watch.series",
            ),
        ),
        migrations.AddField(
            model_name="instance",
            name="mentioned_tracks",
            field=models.ManyToManyField(
                blank=True,
                related_name="mentioned_in_publication_instances",
                to="listen.track",
            ),
        ),
    ]
