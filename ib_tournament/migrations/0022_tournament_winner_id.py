# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-02-06 04:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ib_tournament', '0021_auto_20190206_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='winner_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]