# Generated by Django 4.0.4 on 2022-05-17 15:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("competitions", "0008_remove_submission_score_run_phase_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="run",
            name="phase",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="runs",
                to="competitions.phase",
            ),
        ),
        migrations.AlterField(
            model_name="run",
            name="submission",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="runs",
                to="competitions.submission",
            ),
        ),
    ]
