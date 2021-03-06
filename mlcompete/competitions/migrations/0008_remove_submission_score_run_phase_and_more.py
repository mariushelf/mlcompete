# Generated by Django 4.0.4 on 2022-05-17 14:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("competitions", "0007_submission_label_submission_script_file_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="submission",
            name="score",
        ),
        migrations.AddField(
            model_name="run",
            name="phase",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                to="competitions.phase",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="run",
            name="timestamp",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
