from django.contrib import admin

from walletapi import models as wallet_models


# Register your models here.
class UserBalanceAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_balance', 'coin_type')
    search_fields = ('user_id', 'coin_type')


class CoinTypeAdmin(admin.ModelAdmin):
    list_display = ('coin_type', 'rpc_host', 'rpc_user', 'rpc_port')
    search_fields = ('coin_type', 'rpc_host')


class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('coin_address', 'app_id', 'user_id', 'coin_type', 'used', 'add_time')
    search_fields = ('coin_address', 'user_id')

class TransactionIDAdmin(admin.ModelAdmin):
    list_display = ('coin_type','transaction_id','used')
    search_fields = ('transaction_id',)
    list_filter = ('used','coin_type')


class ApiCallbackAdmin(admin.ModelAdmin):
    list_display = ('app_name','app_url')


admin.site.site_header = u'Wallet Admin Site'
admin.site.register(wallet_models.CoinType, CoinTypeAdmin)
admin.site.register(wallet_models.ApiCallback,ApiCallbackAdmin)
admin.site.register(wallet_models.TransactionsID,TransactionIDAdmin)
admin.site.register(wallet_models.UserAddress,UserAddressAdmin)
admin.site.register(wallet_models.UserBalance, UserBalanceAdmin)
admin.site.register(wallet_models.AppUserRecharge)
