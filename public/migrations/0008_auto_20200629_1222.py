# Generated by Django 3.0.6 on 2020-06-29 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0007_classe_lockdownpackage_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lockdownpackage',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='public.Subject'),
        ),
    ]
