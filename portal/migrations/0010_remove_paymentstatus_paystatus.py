# Generated by Django 3.1.4 on 2020-12-21 01:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0009_auto_20201221_0603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentstatus',
            name='payStatus',
        ),
    ]