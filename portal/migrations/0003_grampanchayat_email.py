# Generated by Django 3.1.4 on 2020-12-20 03:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_auto_20201219_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='grampanchayat',
            name='email',
            field=models.EmailField(default='rayeole@gmail.com', max_length=254, unique=True, validators=[django.core.validators.EmailValidator]),
        ),
    ]
