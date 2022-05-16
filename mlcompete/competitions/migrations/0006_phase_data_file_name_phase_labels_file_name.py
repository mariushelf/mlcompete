# Generated by Django 4.0.4 on 2022-05-16 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("competitions", "0005_phase_data_file_phase_labels_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="phase",
            name="data_file_name",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name="phase",
            name="labels_file_name",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
