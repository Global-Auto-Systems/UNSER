# Generated by Django 3.0.6 on 2020-08-13 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0009_auto_20200728_1101'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lockdownpackage',
            name='subject',
        ),
        migrations.AddField(
            model_name='lockdownpackage',
            name='subject',
            field=models.ManyToManyField(to='public.Subject'),
        ),
    ]
