# Generated by Django 2.0.5 on 2018-06-17 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teaching', '0009_auto_20180617_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachingprojectapply',
            name='apply_time',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='申请时间'),
        ),
    ]
