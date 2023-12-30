# Generated by Django 5.0 on 2023-12-30 20:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("visit", "0002_historicallocation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicallocation",
            name="level",
            field=models.CharField(
                choices=[
                    ("continent", "Continent"),
                    ("polity", "Polity"),
                    ("region", "Region"),
                    ("city", "City"),
                    ("town", "Town"),
                    ("village", "Village"),
                    ("district", "District"),
                    ("poi", "Point of Interest"),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="level",
            field=models.CharField(
                choices=[
                    ("continent", "Continent"),
                    ("polity", "Polity"),
                    ("region", "Region"),
                    ("city", "City"),
                    ("town", "Town"),
                    ("village", "Village"),
                    ("district", "District"),
                    ("poi", "Point of Interest"),
                ],
                max_length=20,
            ),
        ),
    ]
