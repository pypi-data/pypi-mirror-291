# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     square.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/08/15
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from enum import Enum
from mixiu_app_helper.api.http.http_client import HttpApiMeta


class SquarePathAndroidSuffix(Enum):
    moment_list = '/square/moment/listMoment'


class SquarePathIOSSuffix(Enum):
    pass


class SquareHttpApi(HttpApiMeta):

    def __init__(self, domain: str, protocol: str):
        super().__init__(domain, protocol)

    def get_square_moment_list(self, json: dict) -> dict:
        """获取广场重要信息列表"""
        return self.http_client.send_request(method="post", path=SquarePathAndroidSuffix.moment_list.value, json=json)
