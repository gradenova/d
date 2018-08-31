# Generated by Django 2.0.5 on 2018-06-18 23:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0002_auto_20180529_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building', models.CharField(max_length=3, null=True)),
                ('number', models.IntegerField(default=0)),
                ('useage', models.CharField(max_length=4, null=True)),
            ],
            options={
                'db_table': 'ClassRoom',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=15)),
                ('thyHours', models.IntegerField(default=0)),
                ('labHours', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'Course',
            },
        ),
        migrations.CreateModel(
            name='CourseArrange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classes', models.CharField(max_length=15, null=True)),
                ('laborthy', models.BooleanField(default=False)),
                ('watch', models.BooleanField(default=False)),
                ('week', models.IntegerField(default=0)),
                ('day', models.IntegerField(default=0)),
                ('number', models.IntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coursArrange.Course')),
                ('place', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='coursArrange.ClassRoom')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Teacher')),
            ],
            options={
                'db_table': 'CourseArrange',
            },
        ),
        migrations.CreateModel(
            name='CourseOtherDemand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classes', models.CharField(max_length=15, null=True)),
                ('demand', models.CharField(default='', max_length=50)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coursArrange.Course')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Teacher')),
            ],
            options={
                'db_table': 'CourseOtherDemand',
            },
        ),
    ]
