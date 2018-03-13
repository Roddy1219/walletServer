# coding:utf8
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import renderers

from django.conf import settings

from walletapi import models as wallet_models

# Create your views here.
import hashlib
import json
from comm.bitcoin_conn import RPCBitcoin


def getHashValue(string, sign):
    hash_value = hashlib.md5(string).hexdigest()

    if not hash_value == sign:
        return False
    else:
        return True

class IndexView(APIView):
    renderer_classes = (renderers.JSONRenderer,)
    def get(self,request):
        return Response({'code':1,'message':'Not Found Path, Please get another path'})


class GetUserWalletAddress(APIView):
    """
        if not address then make new wallet address
    """
    renderer_classes = (renderers.JSONRenderer,)

    def get(self, request, format=None):
        user_id = request.GET.get('user_id', None)
        coin_type = request.GET.get('coin_type', None)
        app_id = request.GET.get('app_id', None)
        sign = request.GET.get('sign', None)
        new_address = request.GET.get('new_address', None)

        if not user_id or not coin_type or not app_id or not sign:
            return Response({'code': 1, 'message': 'Parameter Error!'})

        # sign check
        str_data = str(user_id) + str(coin_type) + str(settings.SIGIN_KEY) + str(app_id)

        # input value md5 check
        if not getHashValue(str_data, sign):
            return Response({'code': 1, 'message': 'Authentication Error!'})

        # Connect RPC Server
        try:
            coin_obj = wallet_models.CoinType.objects.get(coin_type=coin_type)
        except wallet_models.CoinType.DoesNotExist:
            return Response({'code': 1, 'message': 'Coin type does not exist!!'})

        try:
            app_obj = wallet_models.ApiCallback.objects.get(id=app_id)
        except wallet_models.ApiCallback.DoesNotExist:
            return Response({'code': 1, 'message': 'App id does not exist!!'})

        # Search address from db server ,if address existed then response it
        try:
            address_obj = wallet_models.UserAddress.objects.get(coin_type=coin_type, user_id=user_id, used=True)
        except wallet_models.UserAddress.DoesNotExist:
            conn_obj = RPCBitcoin.rpc_conn(coin_obj.rpc_user, coin_obj.rpc_password, coin_obj.rpc_host,
                                           coin_obj.rpc_port)
            callbackAddress = conn_obj.getnewaddress(str(user_id))

            wallet_models.UserAddress.objects.create(user_id=user_id, coin_type=coin_type, coin_address=callbackAddress,
                                                     app_id=app_obj)
        else:
            callbackAddress_obj = address_obj.coin_address

            # 创建新地址
            if new_address == 'true' or new_address == 'True':
                conn_obj = RPCBitcoin.rpc_conn(coin_obj.rpc_user, coin_obj.rpc_password, coin_obj.rpc_host,
                                               coin_obj.rpc_port)
                callbackAddress_obj = conn_obj.getnewaddress(str(user_id))

                wallet_models.UserAddress.objects.filter(coin_type=coin_type, user_id=user_id).update(used=False)

                wallet_models.UserAddress.objects.create(user_id=user_id, coin_type=coin_type,
                                                         coin_address=callbackAddress_obj, app_id=app_obj, used=True)
            callbackAddress = callbackAddress_obj

        # return user's  wallet address
        return Response({'code': 0, 'message': 'Create New address Success!!',
                         'data': {'address': callbackAddress, 'coin': coin_type}})


class GetUserBalance(APIView):
    """
        get user's balance interface
    """

    def get(self, request, format=None):
        user_id = request.GET.get('user_id', None)
        coin_type = request.GET.get('coin_type', None)
        sign = request.GET.get('sign', None)

        str_data = str(user_id)  + str(coin_type) + str(settings.SIGIN_KEY)

        # input value md5 check
        if not getHashValue(str_data, sign):
            return Response({'code': 1, 'message': 'Authentication Error!'})

            # return user's balance
        try:
            balance_obj = wallet_models.UserBalance.objects.get(user_id=user_id, coin_type=coin_type)

        except wallet_models.UserBalance.DoesNotExist:
            return Response({'code': 1, 'message': 'user_id does not exist!!'})
        else:
            return Response({'code': 0, 'message': 'get user balance ok', 'data': {'user_id': user_id,
                                                                                   'balance': balance_obj.user_balance}})


class TransactionsGetApi(APIView):
    """
        get user's recharge history,save transaction id to db server
    """

    def get(self, request, format=None):
        coin_type = request.GET.get('coin', None)
        tx_id = request.GET.get('tx_id', None)

        if not coin_type or not tx_id:
            return Response({'code': 1, 'message': 'Parameter Error!'})

        # remote user request ip address ,check  Is it in the IP list
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip_address = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip_address = request.META['REMOTE_ADDR']

        if ip_address not in settings.REMOTE_IP_LIST:
            return Response({'code': 1, 'message': 'IP Access Denied!'})

        if not wallet_models.CoinType.objects.filter(coin_type=coin_type):
            return Response({'code': 1, 'message': 'Coin Type Error!'})

        wallet_models.TransactionsID.objects.get_or_create(coin_type=coin_type, transaction_id=tx_id)

        return Response({'code': 0, 'message': 'request tx id successful!!'})




#def page_not_found(request):
#    return HttpResponse(json.dumps({'code':1,'message':'404 Error!'}))


#def page_error(request):
#    return HttpResponse(json.dumps({'code':1,'message':'500 Error!'}))


#def permission_denied(request):
#    return HttpResponse(json.dumps({'code':1,'message':'403 Error!'}))