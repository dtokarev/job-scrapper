# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-23 11:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0018_auto_20180420_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='segment',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
