# Generated by Django 2.0.5 on 2018-06-16 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teaching', '0007_auto_20180616_2335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teachingprojectapply',
            name='fileUpload',
        ),
        migrations.AddField(
            model_name='submitfile',
            name='is_apply',
            field=models.BooleanField(default=False),
        ),
    ]
