# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-24 23:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iVR', '0003_auto_20160724_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
