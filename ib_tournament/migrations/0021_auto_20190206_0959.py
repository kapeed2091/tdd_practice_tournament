# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-02-06 04:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ib_tournament', '0020_auto_20190206_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tmplayer',
            name='tournament_match',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ib_tournament.TournamentMatch'),
            preserve_default=False,
        ),
    ]