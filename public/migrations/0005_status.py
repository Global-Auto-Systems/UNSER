# Generated by Django 3.0.6 on 2020-06-29 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0004_auto_20200629_1017'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, unique=True, verbose_name='Application Status')),
            ],
        ),
    ]
