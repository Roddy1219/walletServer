#!/bin/env python
#coding:utf8


from bitcoinrpc.authproxy import AuthServiceProxy



class RPCBitcoin(object):

    @classmethod
    def rpc_conn(cls,rpc_user,rpc_password,rpc_host,rpc_port):
        rpc_conn_obj = AuthServiceProxy("http://%s:%s@%s:%s"%(rpc_user,
                                                                rpc_password,
                                                                rpc_host,
                                                                rpc_port))
        return rpc_conn_obj



