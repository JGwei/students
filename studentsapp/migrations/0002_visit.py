# Generated by Django 4.1.2 on 2022-12-27 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("studentsapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Visit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user", models.CharField(max_length=20)),
                ("times", models.IntegerField()),
            ],
        ),
    ]
