# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-08-01 11:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0003_auto_20180731_0650'),
    ]

    operations = [
        migrations.AddField(
            model_name='basic_info',
            name='money',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='basic_info',
            name='identifies',
            field=models.CharField(choices=[('1', '本科生'), ('2', '硕士生'), ('3', '博士生')], default='1', max_length=1),
        ),
        migrations.AlterField(
            model_name='basic_info',
            name='sex',
            field=models.CharField(choices=[('1', '男'), ('2', '女'), ('3', '不详')], default='3', max_length=1),
        ),
    ]
