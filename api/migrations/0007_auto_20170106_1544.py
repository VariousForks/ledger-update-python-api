# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-06 15:44
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20170106_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='version',
            name='app_hash',
            field=models.CharField(default='0000000000000000000000000000000000000000000000000000000000000000', max_length=64, validators=[django.core.validators.MinLengthValidator(64), django.core.validators.RegexValidator(code='invalid_username', message='Username must be Alphanumeric', regex='^[a-fA-F0-9]*$')]),
        ),
        migrations.AlterField(
            model_name='app',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]