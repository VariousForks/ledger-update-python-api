# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-06 10:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='firmware',
            name='identifier',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='version',
            name='identifier',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]