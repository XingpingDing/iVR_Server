# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-12 17:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iVR', '0013_auto_20160812_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='picture',
            field=models.ImageField(blank=True, default='', upload_to='static/feeds_images'),
        ),
    ]
