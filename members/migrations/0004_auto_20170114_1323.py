# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-14 13:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_auto_20170114_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='pet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='members', to='cefet.Pet'),
        ),
    ]