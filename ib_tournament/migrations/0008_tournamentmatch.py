# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-02-02 06:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ib_tournament', '0007_auto_20190130_1510'),
    ]

    operations = [
        migrations.CreateModel(
            name='TournamentMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
