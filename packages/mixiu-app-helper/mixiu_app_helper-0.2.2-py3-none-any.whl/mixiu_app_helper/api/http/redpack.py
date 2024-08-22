# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     redpack.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/08/15
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from enum import Enum
from mixiu_app_helper.api.http.http_client import HttpApiMeta


class RedpackPathAndroidSuffix(Enum):
    is_receive = '/redpack/isReceive'


class RedpackPathIOSSuffix(Enum):
    pass


class RedpackHttpApi(HttpApiMeta):

    def __init__(self, domain: str, protocol: str):
        super().__init__(domain, protocol)

    def is_receive_by_user(self, json: dict) -> dict:
        """判断用户接收的红包"""
        return self.http_client.send_request(method="post", path=RedpackPathAndroidSuffix.is_receive.value, json=json)

