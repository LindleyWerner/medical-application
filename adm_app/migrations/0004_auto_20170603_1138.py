# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-03 14:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adm_app', '0003_auto_20170603_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pending_doctor',
            name='crm',
            field=models.CharField(max_length=15),
        ),
    ]
