# Generated by Django 4.0.6 on 2022-07-23 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_alter_job_apps_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='city',
            field=models.CharField(default='', max_length=44),
        ),
    ]
