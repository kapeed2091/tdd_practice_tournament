# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-31 11:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0008_match_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='tournament',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='tournament.KoTournament'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='tournament.User'),
            preserve_default=False,
        ),
    ]
