# Generated by Django 4.0.3 on 2022-03-07 07:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_orgdetail_id_alter_orgdetail_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orgdetail',
            old_name='user_id',
            new_name='user',
        ),
    ]