# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-21 15:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20160821_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='thumbnail',
            field=models.ImageField(upload_to=''),
        ),
    ]
