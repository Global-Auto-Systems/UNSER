# Generated by Django 3.0.6 on 2020-08-18 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ministry', '0016_auto_20200818_1534'),
        ('school', '0007_auto_20200817_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestteacher',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ministry.Subject'),
        ),
        migrations.DeleteModel(
            name='Subject',
        ),
    ]
