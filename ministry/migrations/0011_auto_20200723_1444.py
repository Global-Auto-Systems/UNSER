# Generated by Django 3.0.6 on 2020-07-23 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ministry', '0010_auto_20200626_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='cen_no',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Center Number'),
        ),
        migrations.AlterField(
            model_name='school',
            name='motto',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='School Motto'),
        ),
        migrations.AlterField(
            model_name='school',
            name='reg_no',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Registration Number'),
        ),
        migrations.AlterField(
            model_name='school',
            name='yr_est',
            field=models.IntegerField(blank=True, null=True, verbose_name='Year Established'),
        ),
    ]
