# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-05-15 04:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('display_reports', '0003_salereport'),
    ]

    operations = [
        migrations.AddField(
            model_name='displayreport',
            name='franchise_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
