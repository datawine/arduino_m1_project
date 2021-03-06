# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-07-30 08:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Basic_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idnumber', models.IntegerField(db_index=True, default=2015000000, unique=True)),
                ('name', models.CharField(default='', max_length=10)),
                ('department', models.CharField(default='', max_length=10)),
                ('identifies', models.CharField(choices=[('A', '本科生'), ('B', '硕士生'), ('C', '博士生')], default='A', max_length=1)),
                ('sex', models.CharField(choices=[('A', '男'), ('B', '女'), ('C', '不详')], default='C', max_length=1)),
            ],
        ),
    ]
