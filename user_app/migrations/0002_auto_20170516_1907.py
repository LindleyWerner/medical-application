# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-16 22:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simple_user',
            name='birth_date',
            field=models.CharField(max_length=10),
        ),
    ]