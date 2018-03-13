#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Luodi'

import os
import sys
import json
import urllib
import urllib2
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ["DJANGO_SETTINGS_MODULE"] = 'walletServer.settings'
import django


django.setup()
from walletapi import models as wallet_models



class callbackPost(object):
    def __init__(self,url):
        self.__url = url.strip('/')

    def request_post(self,url,arg):
        pass

    def search_tx_id(self):
        not_callback = wallet_models.AppUserRecharge.objects.filter(is_callback=False)

        for id in not_callback:
            try:
                app_id = wallet_models.ApiCallback.objects.get(id=id.platform)
            except wallet_models.ApiCallback.DoesNotExist:
                continue

            user_balace_obj = wallet_models.UserBalance.objects.get(user_id=id.user_id)
            url = app_id.app_url
            app_user_id = id.user_id
            amount = id.amount
            address = id.address
            balance = user_balace_obj.user_balance

            params = {'user_id':app_user_id,'amount':amount,'address':address,'total_balance':balance}
            req = requests.post(url, data=params, allow_redirects=False)
            content = req.json()
            return content