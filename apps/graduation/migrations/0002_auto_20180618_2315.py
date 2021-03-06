# Generated by Django 2.0.5 on 2018-06-18 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GraduationReportTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DeclareBeginTime', models.DateField(null=True)),
                ('DeclareEndTime', models.DateField(null=True)),
                ('TaskBeginTime', models.DateField(null=True)),
                ('TaskEndTime', models.DateField(null=True)),
                ('MidtermBeginTime', models.DateField(null=True)),
                ('MidtermEndTime', models.DateField(null=True)),
                ('GraduatinoBeginTime', models.DateField(null=True)),
                ('GraduationEndTime', models.DateField(null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='graduationpaper',
            name='DeclareBeginTime',
        ),
        migrations.RemoveField(
            model_name='graduationpaper',
            name='DeclareEndTime',
        ),
        migrations.RemoveField(
            model_name='graduationpaper',
            name='GraduatinoBeginTime',
        ),
        migrations.RemoveField(
            model_name='graduationpaper',
            name='GraduationEndTime',
        ),
        migrations.RemoveField(
            model_name='graduationpaper',
            name='MidtermBeginTime',
        ),
        migrations.RemoveField(
            model_name='graduationpaper',
            name='MidtermEndTime',
        ),
        migrations.RemoveField(
            model_name='graduationpaper',
            name='TaskBeginTime',
        ),
        migrations.RemoveField(
            model_name='graduationpaper',
            name='TaskEndTime',
        ),
    ]
