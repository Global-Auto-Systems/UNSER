# Generated by Django 3.0.6 on 2020-06-29 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0005_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceprovider',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='public.Status'),
        ),
        migrations.DeleteModel(
            name='Apply',
        ),
    ]
