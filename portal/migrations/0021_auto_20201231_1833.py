# Generated by Django 3.1.4 on 2020-12-31 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0020_auto_20201231_1823'),
    ]

    operations = [
        migrations.RenameField(
            model_name='directorapprovel',
            old_name='gp',
            new_name='gp_user',
        ),
    ]
