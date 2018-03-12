#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Luodi'

import os, sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ["DJANGO_SETTINGS_MODULE"] = 'walletServer.settings'
import django
import random

django.setup()

from bitcoinrpc.authproxy import JSONRPCException
from comm.bitcoin_conn import RPCBitcoin
from walletapi import models as wallet_models


class ForTransaction(object):
    """
        1.获取币种信息
        2.遍历币种信息，根据交易ID去连接所对应的RPC服务器
    """

    # def get_transaction_id(self,coin_type):
    #     """
    #     获取交易ID列表
    #     :return: trx_list[]
    #     """
    #     tx_id = wallet_models.TransactionsID.objects.filter(used=False,coin_type=coin_type)
    #     trx_list = [id.transaction_id for id in tx_id ]
    #
    #
    #    return trx_list
    #

    def order_id(self):

        timeid = datetime.now().strftime('%Y%m%d%H%M%S')
        random_value = random.randrange(0, 10000, 4)
        id_value = str(timeid) + str(random_value)
        return id_value



    def get_transcation_info(self):

        """
            通过交易列表获取每个交易的交易详细情况
        """
        coin_obj = wallet_models.CoinType.objects.all()
        for coin in coin_obj:

            # select tx_id  used is False
            tx_obj = wallet_models.TransactionsID.objects.filter(coin_type=coin.coin_type, used=False)

            # get rpc connection info from tx_id object
            conn_obj = RPCBitcoin.rpc_conn(coin.rpc_user, coin.rpc_password, coin.rpc_host, coin.rpc_port)

            for tx in tx_obj:
                try:
                    transaction_info = conn_obj.gettransaction(tx.transaction_id)
                except JSONRPCException:
                    continue

                for tx_detail in transaction_info['details']:
                    print tx_detail['address']
                    if tx_detail['category'] == 'receive':
                        amount_var = tx_detail['amount']       # if not confirmed enough
                        if transaction_info['confirmations'] < 1:
                            request_status = "Pending"
                            confirmations = transaction_info['confirmations']

                        else:
                            request_status = "Confirmed"
                            confirmations = transaction_info['confirmations']
                        try:
                            user_address_obj = wallet_models.UserAddress.objects.get(coin_address=tx_detail['address'])
                        except wallet_models.UserAddress.DoesNotExist:
                            continue

                        create_obj = wallet_models.AppUserRecharge.objects.filter(transaction_id=tx.transaction_id,
                                                                     address=tx_detail['address'],
                                                                     coin_type=coin.coin_type,
                                                                     amount = amount_var,
                                                                     user_id = user_address_obj.user_id,
                                                                                  )

                        if create_obj:
                            create_obj.update(
                                request_status=request_status,
                                confirmations=user_address_obj.app_id.id


                            )
                        else:
                            wallet_models.AppUserRecharge.objects.create(
                                order=self.order_id(),
                                amount=amount_var,
                                request_status=request_status,
                                user_id=user_address_obj.user_id,
                                confirmations=confirmations,
                                platform=user_address_obj.app_id.id,
                                transaction_id=tx.transaction_id,
                                address=tx_detail['address'],
                                coin_type=coin.coin_type,

                            )


                        if transaction_info['confirmations'] >= 1 and request_status == "Confirmed":
                            # 交易确认数和交易状态完成，修改用户的可用余额
                            user_balance, balance_created = wallet_models.UserBalance.objects.get_or_create(
                                user_id=user_address_obj.user_id,
                                coin_type=coin.coin_type,
                                defaults={
                                    "user_balance": amount_var
                                }
                            )

                            if not balance_created:
                                user_balance.user_balance = float(user_balance.user_balance) + float(amount_var)
                                user_balance.save()

                            Old_tx_obj = wallet_models.TransactionsID.objects.get(coin_type=coin.coin_type, transaction_id=tx.transaction_id)
                            Old_tx_obj.used =True
                            Old_tx_obj.save()


if __name__ == '__main__':
    start = ForTransaction()
    start.get_transcation_info()
