# Generated by Django 3.1.4 on 2020-12-29 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0014_auto_20201228_2142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountantapprovel',
            name='id',
        ),
        migrations.RemoveField(
            model_name='auditdocument',
            name='id',
        ),
        migrations.RemoveField(
            model_name='certificate',
            name='id',
        ),
        migrations.RemoveField(
            model_name='directorapprovel',
            name='id',
        ),
        migrations.RemoveField(
            model_name='phase',
            name='id',
        ),
        migrations.RemoveField(
            model_name='trainning',
            name='id',
        ),
        migrations.AlterField(
            model_name='accountantapprovel',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='portal.accountant', verbose_name='accontant_app'),
        ),
        migrations.AlterField(
            model_name='auditdocument',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='portal.grampanchayat', verbose_name='gp_audit_doc'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='portal.grampanchayat', verbose_name='gp_cert'),
        ),
        migrations.AlterField(
            model_name='directorapprovel',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='portal.director', verbose_name='director_app'),
        ),
        migrations.AlterField(
            model_name='phase',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='portal.grampanchayat', verbose_name='gp_phase'),
        ),
        migrations.AlterField(
            model_name='trainning',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='portal.grampanchayat', verbose_name='gp_trainning'),
        ),
    ]