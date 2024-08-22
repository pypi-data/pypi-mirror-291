# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     play_with.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/08/12
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from enum import Enum
from mixiu_app_helper.api.http.http_client import HttpApiMeta


class PlayWithPathAndroidSuffix(Enum):
    order_pagination = '/playwith/order/list'


class PlayWithPathIOSSuffix(Enum):
    pass


class PlayWithHttpApi(HttpApiMeta):

    def __init__(self, domain: str, protocol: str):
        super().__init__(domain, protocol)

    def get_order_pagination(self, json: dict) -> dict:
        """获取分页订单"""
        return self.http_client.send_request(
            method="post", path=PlayWithPathAndroidSuffix.order_pagination.value, json=json
        )
