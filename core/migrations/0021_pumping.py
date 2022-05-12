# Generated by Django 4.0.3 on 2022-04-04 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0020_bmi_tags_diaperchange_tags_feeding_tags_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Pumping",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.FloatField(verbose_name="Amount")),
                ("time", models.DateTimeField(verbose_name="Time")),
                (
                    "notes",
                    models.TextField(blank=True, null=True, verbose_name="Notes"),
                ),
                (
                    "child",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pumping",
                        to="core.child",
                        verbose_name="Child",
                    ),
                ),
            ],
            options={
                "verbose_name": "Pumping",
                "verbose_name_plural": "Pumping",
                "ordering": ["-time"],
                "default_permissions": ("view", "add", "change", "delete"),
            },
        ),
    ]
