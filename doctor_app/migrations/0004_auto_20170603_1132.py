# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-03 14:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_app', '0003_auto_20170531_1429'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor_user',
            name='validation_code',
        ),
        migrations.AddField(
            model_name='doctor_user',
            name='adm_father',
            field=models.IntegerField(default=1),
        ),
    ]