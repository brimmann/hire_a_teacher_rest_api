# Generated by Django 4.1 on 2022-08-11 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0010_resume_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='address',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='resume',
            name='email',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='resume',
            name='heading',
            field=models.CharField(default='', max_length=80),
        ),
    ]