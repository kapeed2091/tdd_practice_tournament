# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-02-02 11:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0012_tournamentmatch'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournamentmatch',
            name='match_id',
            field=models.CharField(default='Dummy', max_length=20),
            preserve_default=False,
        ),
    ]