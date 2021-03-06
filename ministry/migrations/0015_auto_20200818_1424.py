# Generated by Django 3.0.6 on 2020-08-18 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ministry', '0014_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherEducation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('education_level', models.CharField(max_length=45, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeacherProfession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profession', models.CharField(max_length=45, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeacherResponsibility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('responsibility', models.CharField(max_length=45, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeacherSalaryScale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profession', models.CharField(max_length=45, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeacherTraining',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training', models.CharField(max_length=45, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='transferteacher',
            name='designation',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='ministry.TeacherResponsibility'),
        ),
        migrations.DeleteModel(
            name='Designation',
        ),
    ]
