# Generated by Django 4.0.6 on 2022-07-10 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='heading',
            field=models.CharField(default='', max_length=44),
        ),
    ]
