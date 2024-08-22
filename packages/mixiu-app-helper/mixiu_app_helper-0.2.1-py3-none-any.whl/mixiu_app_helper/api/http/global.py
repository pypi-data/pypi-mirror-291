# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     g.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/08/15
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from enum import Enum
from mixiu_app_helper.api.http.http_client import HttpApiMeta


class GlobalPathAndroidSuffix(Enum):
    hide_config = '/g/hide/config/get'


class GlobalPathIOSSuffix(Enum):
    pass


class GlobalHttpApi(HttpApiMeta):

    def __init__(self, domain: str, protocol: str):
        super().__init__(domain, protocol)

    def get_g_hide_config(self, json: dict) -> dict:
        """获取全局隐藏配置"""
        return self.http_client.send_request(method="post", path=GlobalPathAndroidSuffix.hide_config.value, json=json)
