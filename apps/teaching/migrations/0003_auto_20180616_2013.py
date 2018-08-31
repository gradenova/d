# Generated by Django 2.0.5 on 2018-06-16 20:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teaching', '0002_teachinginfonotification_publishtime'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubmitFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_file', models.FileField(default='', upload_to='project_file/%Y/%m')),
                ('is_medium', models.BooleanField(default=False)),
                ('is_final', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TeachingProjectApply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=100, verbose_name='题目')),
                ('category', models.CharField(choices=[('reform', '教改'), ('research', '教研'), ('textbook', '教材'), ('other', '其他')], default='reform', max_length=10, verbose_name='项目类型')),
                ('applicant', models.CharField(default='', max_length=10, verbose_name='申请人')),
                ('funds', models.IntegerField(default=0, verbose_name='经费')),
                ('intro', models.CharField(default='', max_length=500, verbose_name='简介')),
                ('fileUpload', models.FileField(default='', upload_to='fileUpload/%Y/%m')),
                ('process', models.CharField(default='', max_length=10, verbose_name='项目进度')),
                ('check_status', models.CharField(default='', max_length=10, verbose_name='审核结果')),
                ('belongTea', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='所属教师')),
            ],
        ),
        migrations.AddField(
            model_name='submitfile',
            name='TPA_belong',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teaching.TeachingProjectApply', verbose_name='所属项目'),
        ),
    ]
