# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-25 15:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iVR', '0005_auto_20160725_1527'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='url',
            new_name='website',
        ),
        migrations.AddField(
            model_name='game',
            name='website',
            field=models.URLField(blank=True),
        ),
    ]
