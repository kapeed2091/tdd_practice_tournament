# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-02-02 09:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ib_tournament', '0009_tournamentmatch_tournament'),
    ]

    operations = [
        migrations.CreateModel(
            name='TMPlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_id', models.IntegerField()),
                ('tournament_match_id', models.IntegerField()),
            ],
        ),
    ]