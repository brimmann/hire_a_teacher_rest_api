# Generated by Django 4.0.6 on 2022-07-23 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=55)),
                ('status', models.CharField(default='active', max_length=10)),
                ('exp_level', models.CharField(default='', max_length=55)),
                ('type', models.CharField(default='', max_length=44)),
                ('date_posted', models.CharField(default='', max_length=16)),
                ('expire_date', models.CharField(default='', max_length=12)),
                ('description', models.TextField(default='')),
                ('tags', models.CharField(default='', max_length=128)),
                ('apps_no', models.IntegerField()),
            ],
        ),
    ]
