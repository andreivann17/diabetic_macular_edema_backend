# Generated by Django 4.2.3 on 2023-08-23 21:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detection', '0006_remove_detections_prediction_result_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detectionspredictions',
            old_name='CNV',
            new_name='cnv',
        ),
    ]
