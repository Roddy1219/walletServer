# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-03-07 10:42
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiCallback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_url', models.URLField(verbose_name='\u56de\u8c03\u5730\u5740')),
                ('app_name', models.CharField(max_length=50, verbose_name='\u5e94\u7528\u540d')),
            ],
            options={
                'db_table': 'app_callback',
                'verbose_name': '\u5e94\u7528\u56de\u8c03',
                'verbose_name_plural': '\u5e94\u7528\u56de\u8c03',
            },
        ),
        migrations.CreateModel(
            name='AppUserRecharge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('order', models.CharField(max_length=255, verbose_name='\u8ba2\u5355\u53f7')),
                ('user_id', models.IntegerField(blank=True, null=True, verbose_name='\u7528\u6237ID')),
                ('amount', models.DecimalField(decimal_places=8, max_digits=16, verbose_name='\u5145\u503c\u91d1\u989d')),
                ('platform', models.IntegerField(blank=True, null=True, verbose_name='\u5e94\u7528\u5e73\u53f0')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u5145\u503c\u5730\u5740')),
                ('transaction_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u4ea4\u6613ID')),
                ('confirmations', models.IntegerField(blank=True, default=0, null=True, verbose_name='\u786e\u8ba4\u6570')),
                ('request_status', models.CharField(choices=[('Pending', '\u672a\u786e\u8ba4'), ('Confirmed', '\u5df2\u786e\u8ba4')], default='Pending', max_length=255, verbose_name='\u5145\u503c\u72b6\u6001')),
                ('is_callback', models.BooleanField(default=False, verbose_name='\u901a\u77e5\u72b6\u6001')),
                ('coin_type', models.CharField(choices=[('BTC', '\u6bd4\u7279\u5e01'), ('BCH', '\u6bd4\u7279\u5e01\u73b0\u91d1')], default='BCH', max_length=255)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'user_recharge',
                'verbose_name': '\u5145\u503c\u6570\u636e',
                'verbose_name_plural': '\u5145\u503c\u6570\u636e',
            },
        ),
        migrations.CreateModel(
            name='CoinType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin_type', models.CharField(max_length=50, verbose_name='\u5e01\u79cd')),
                ('rpc_host', models.GenericIPAddressField(verbose_name='\u4e3b\u673a')),
                ('rpc_user', models.CharField(max_length=50, verbose_name='\u7528\u6237\u540d')),
                ('rpc_password', models.CharField(max_length=50, verbose_name='\u5bc6\u7801')),
                ('rpc_port', models.IntegerField(verbose_name='\u7aef\u53e3')),
            ],
            options={
                'db_table': 'coin_host',
                'verbose_name': '\u652f\u6301\u5e01\u79cd',
                'verbose_name_plural': '\u652f\u6301\u5e01\u79cd',
            },
        ),
        migrations.CreateModel(
            name='TransactionsID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin_type', models.CharField(max_length=50, verbose_name='\u5e01\u79cd')),
                ('transaction_id', models.CharField(max_length=255, verbose_name='\u4ea4\u6613ID')),
            ],
            options={
                'db_table': 'transaction_id',
                'verbose_name': '\u4ea4\u6613ID',
                'verbose_name_plural': '\u4ea4\u6613ID',
            },
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin_address', models.CharField(max_length=255, verbose_name='\u94b1\u5305\u5730\u5740')),
                ('user_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u7528\u6237ID')),
                ('coin_type', models.CharField(default='BTC', max_length=255)),
                ('used', models.BooleanField(default=True, verbose_name='\u5f53\u524d\u4f7f\u7528')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
            ],
            options={
                'db_table': 'user_address',
                'verbose_name': '\u7528\u6237\u5730\u5740',
                'verbose_name_plural': '\u7528\u6237\u5730\u5740',
            },
        ),
        migrations.CreateModel(
            name='UserBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='\u7528\u6237ID')),
                ('user_balance', models.DecimalField(decimal_places=8, max_digits=16)),
                ('coin_type', models.CharField(default='BTC', max_length=255)),
            ],
            options={
                'db_table': 'user_balance',
                'verbose_name': '\u7528\u6237\u4f59\u989d',
                'verbose_name_plural': '\u7528\u6237\u4f59\u989d',
            },
        ),
    ]
