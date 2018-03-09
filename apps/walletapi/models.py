# coding:utf8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from datetime import datetime


class ApiCallback(models.Model):
    """
        回调url管理，当充值状态为Confirmed时进行回调
    """

    app_url = models.URLField(verbose_name="回调地址")
    app_name = models.CharField(max_length=50, verbose_name="应用名")

    class Meta:
        verbose_name = u"应用回调"
        verbose_name_plural = verbose_name
        db_table = "app_callback"

    def __unicode__(self):
        return self.app_url


class UserAddress(models.Model):
    """
        用户地址
    """

    coin_address = models.CharField(max_length=255, verbose_name="钱包地址")
    app_id = models.ForeignKey(ApiCallback,verbose_name="应用",null=True,blank=True)
    user_id = models.CharField(max_length=255, verbose_name="用户ID", null=True, blank=True)
    coin_type = models.CharField(max_length=255, default='BTC')
    used = models.BooleanField(default=True, verbose_name="当前使用")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = u"用户地址"
        verbose_name_plural = verbose_name
        db_table = "user_address"

    def __unicode__(self):
        return self.coin_address




class UserBalance(models.Model):
    """
        用户余额
    """

    user_id = models.CharField(max_length=100, verbose_name="用户ID", null=True, blank=True)
    user_balance = models.DecimalField(max_digits=16, decimal_places=8)
    coin_type = models.CharField(max_length=255, default='BTC')

    class Meta:
        verbose_name = "用户余额"
        verbose_name_plural = verbose_name
        db_table = "user_balance"

    def __unicode__(self):
        return '%s:%s' % (self.user_id, self.user_balance)




class AppUserRecharge(models.Model):
    """
        用户充值表
    """
    date = models.DateTimeField(auto_now_add=True)
    order = models.CharField(max_length=255, verbose_name="订单号")
    user_id = models.IntegerField(blank=True, null=True, verbose_name="用户ID")
    amount = models.DecimalField(max_digits=16, decimal_places=8, verbose_name="充值金额")
    platform = models.IntegerField(blank=True, null=True, verbose_name="应用平台")
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="充值地址")
    transaction_id = models.CharField(max_length=255, verbose_name="交易ID", null=True, blank=True)
    confirmations = models.IntegerField(blank=True, null=True, default=0, verbose_name="确认数")
    request_status = models.CharField(max_length=255,
                                      choices=(("Pending", u"未确认"), ("Confirmed", u"已确认")),
                                      default="Pending", verbose_name=u"充值状态")
    is_callback = models.BooleanField(default=False, verbose_name="通知状态")
    coin_type = models.CharField(max_length=255, choices=(("BTC", u"比特币"), ("BCH", u"比特币现金")), default="BCH")
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "充值数据"
        verbose_name_plural = verbose_name

        db_table = "user_recharge"

    def __unicode__(self):
        return self.order





class TransactionsID(models.Model):
    """
        交易ID记录表，用户保存交易ID：币种，ID
    """

    coin_type = models.CharField(max_length=50,verbose_name="币种")
    transaction_id = models.CharField(max_length=255, verbose_name="交易ID")
    used = models.BooleanField(verbose_name="是否处理",default=False)

    class Meta:
        verbose_name = "交易ID"
        verbose_name_plural = verbose_name
        db_table = "transaction_id"


    def __unicode__(self):
        return self.transaction_id



class CoinType(models.Model):
    coin_type = models.CharField(max_length=50, verbose_name="币种")
    rpc_host = models.GenericIPAddressField(verbose_name="主机")
    rpc_user = models.CharField(max_length=50, verbose_name="用户名")
    rpc_password = models.CharField(max_length=50, verbose_name="密码")
    rpc_port = models.IntegerField(verbose_name=u"端口")

    class Meta:
        verbose_name = "支持币种"
        verbose_name_plural = verbose_name
        db_table = "coin_host"

    def __unicode__(self):
        return self.coin_type





