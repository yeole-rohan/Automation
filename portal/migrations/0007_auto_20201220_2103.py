# Generated by Django 3.1.4 on 2020-12-20 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_auto_20201220_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountant',
            name='username',
            field=models.TextField(default='ac'),
        ),
        migrations.AddField(
            model_name='director',
            name='username',
            field=models.TextField(default='ac'),
        ),
        migrations.AddField(
            model_name='observar',
            name='username',
            field=models.TextField(default='ac'),
        ),
    ]
