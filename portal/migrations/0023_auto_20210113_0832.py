# Generated by Django 3.1.4 on 2021-01-13 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0022_auto_20210112_2053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainning',
            name='place',
        ),
        migrations.RemoveField(
            model_name='trainning',
            name='tranning',
        ),
        migrations.AddField(
            model_name='trainning',
            name='trainning_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='trainning',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
