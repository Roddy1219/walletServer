from django.conf.urls import url
from walletapi import views as wallet_views

urlpatterns = [
    url(r'^getaddress/', wallet_views.GetUserWalletAddress.as_view(),name='get_address'),
    url(r'^balance/',wallet_views.GetUserBalance.as_view(),name='get_balance'),
]