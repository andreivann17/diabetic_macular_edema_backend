# Generated by Django 4.2.3 on 2023-07-24 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detection', '0002_alter_detections_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='detections',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]