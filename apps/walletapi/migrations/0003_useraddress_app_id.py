# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-03-07 15:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('walletapi', '0002_transactionsid_used'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='app_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='walletapi.ApiCallback', verbose_name='\u5e94\u7528'),
        ),
    ]
