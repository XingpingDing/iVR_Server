# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-12 17:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iVR', '0012_auto_20160810_0041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='picture',
            field=models.ImageField(blank=True, upload_to='static/feeds_images'),
        ),
    ]
