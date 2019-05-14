# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-05-14 15:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('display_reports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisplayReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_update_datetime', models.DateTimeField(auto_now=True)),
                ('sale_report_reference_no', models.CharField(max_length=125)),
                ('payment_report_reference_no', models.CharField(max_length=125)),
                ('sale_report_amount', models.FloatField()),
                ('payment_report_amount', models.FloatField()),
                ('status', models.CharField(max_length=125)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]