# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-09 03:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20170708_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='spectator',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
