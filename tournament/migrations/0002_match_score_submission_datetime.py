# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-02-06 06:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='score_submission_datetime',
            field=models.DateTimeField(null=True),
        ),
    ]
