# Generated by Django 4.0.6 on 2022-07-10 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0004_resume_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='email',
            field=models.TextField(default='', max_length=44),
        ),
    ]