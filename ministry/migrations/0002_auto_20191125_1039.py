# Generated by Django 2.2.6 on 2019-11-25 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ministry', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deo',
            name='region',
        ),
        migrations.RemoveField(
            model_name='school',
            name='region',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='region',
        ),
        migrations.AddField(
            model_name='district',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ministry.Region', verbose_name='Region'),
        ),
    ]
