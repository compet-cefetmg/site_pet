# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-12 01:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20170612_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(max_length=800),
        ),
    ]
