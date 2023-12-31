# Generated by Django 4.2.3 on 2023-11-19 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detection', '0021_remove_detections_prediction_details_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detections',
            name='prediction',
        ),
        migrations.RemoveField(
            model_name='detectionspredictions',
            name='img',
        ),
        migrations.RemoveField(
            model_name='detectionspredictions',
            name='prediction_probability',
        ),
        migrations.AddField(
            model_name='detectionspredictions',
            name='diagnosis_confirmed',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
