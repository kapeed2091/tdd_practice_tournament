# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-02-03 15:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ib_tournament', '0018_tmplayer_completed_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournamentmatch',
            name='round_no',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
    ]
