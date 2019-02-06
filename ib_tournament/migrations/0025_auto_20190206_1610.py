# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-02-06 10:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ib_tournament', '0024_auto_20190206_1300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournament',
            name='winner_id',
        ),
        migrations.AddField(
            model_name='tournament',
            name='winner',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='ib_tournament.Player'),
        ),
    ]
