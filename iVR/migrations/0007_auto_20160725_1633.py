# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-25 16:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iVR', '0006_auto_20160725_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamereview',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iVR.Game'),
        ),
        migrations.AlterField(
            model_name='videoreview',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iVR.Video'),
        ),
    ]
