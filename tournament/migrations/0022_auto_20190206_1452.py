# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-02-06 09:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0021_tournamentuser_current_round_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournamentuser',
            name='current_round_number',
            field=models.IntegerField(default=1),
        ),
    ]