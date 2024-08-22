# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     gift.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/08/15
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from enum import Enum
from mixiu_app_helper.api.http.http_client import HttpApiMeta


class GiftPathAndroidSuffix(Enum):
    gift_wall_list = '/giftWall/list'


class GiftPathIOSSuffix(Enum):
    pass


class GiftHttpApi(HttpApiMeta):

    def __init__(self, domain: str, protocol: str):
        super().__init__(domain, protocol)

    def get_gift_wall_list(self, json: dict) -> dict:
        """获取礼物墙列表"""
        return self.http_client.send_request(method="post", path=GiftPathAndroidSuffix.gift_wall_list.value, json=json)
